from __future__ import annotations

import io
import json
import os
import re
import time
import urllib.request
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

import requests
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)
from PIL import Image, ImageFilter
from pygoogle_image import image as pi
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from wiki2vid.ai import AI
from wiki2vid.audio import AudioBuilder
from wiki2vid.config import Config
from wiki2vid.prompts import Prompts
from wiki2vid.script import ScriptBuilder
from wiki2vid.segment import Content, SegmentNode

if TYPE_CHECKING:
    from wiki2vid import Wiki2Vid


class VideoBuilder:
    def __init__(self, wiki2vid: Wiki2Vid):
        self.base_folder = f"{wiki2vid.base_folder}/video"
        self.openai = wiki2vid.audio_builder.openai
        self.script = wiki2vid.script_builder.script
        self.segment_timestamps = wiki2vid.audio_builder.segment_timestamps

    def build_video(self) -> None:
        self._create_search_terms()
        images = self._prepare_images()
        self._build_video(images)

    def _create_search_terms(self) -> None:
        messages = Prompts.images.format_messages(
            segment_timestamps="\n".join(self.segment_timestamps),
        )
        raw_search_terms = AI.infer(messages, f"{self.base_folder}/search_terms.md")
        self.search_terms = []
        for line in raw_search_terms.split("\n"):
            if line:
                timestamp, method, term = line.split(" ", 2)
                timestamp = timestamp.strip("[]")
                method = method.strip("[]")
                self.search_terms.append((float(timestamp), method, term))

    def _prepare_images(self) -> List[Tuple[float, Image.Image]]:
        os.makedirs(f"{self.base_folder}/images", exist_ok=True)
        images = []
        for i, (timestamp, method, term) in enumerate(self.search_terms):
            image: Optional[Image.Image] = None
            if os.path.exists(f"{self.base_folder}/images/{i}.jpg"):
                print(f"Image {i} already exists.")
                image = Image.open(f"{self.base_folder}/images/{i}.jpg")
            if not image and method == "Google":
                image = self._build_images_google(term, i)
            if not image:
                image = self._build_images_dalle(term, i)
            images.append((timestamp, image))
        return images

    def _build_images_google(self, term: str, i: int) -> Optional[Image.Image]:
        image_path = f"{self.base_folder}/images/{i}"
        google_image_scraper = GoogleImageScraper(
            image_path=image_path,
            search_key=term,
            number_of_images=1,
            headless=True,
            min_resolution=(0, 0),
            max_resolution=(1920, 1080),
            max_missed=10,
        )
        image_urls = google_image_scraper.find_image_urls()
        return google_image_scraper.save_images(image_urls, keep_filenames=False)

    def _build_images_dalle(self, term: str, i: int) -> Image.Image:
        response = self.openai.images.generate(
            prompt=term, model="dall-e-3", size="1792x1024"
        )
        image_url = response.data[0].url
        if not image_url:
            raise ValueError("Failed to get image URL.")
        image = Image.open(requests.get(image_url, stream=True).raw)
        image.save(f"{self.base_folder}/images/{i}.jpg")
        return image

    def _build_video(self, images: List[Tuple[float, Image.Image]]):
        target_size = (1920, 1080)  # Example target resolution, adjust as needed
        clips = []
        audio = AudioFileClip(f"{self.base_folder}/output.mp3")

        for i, (timestamp, image) in enumerate(images):
            if not image:
                continue

            # Resize image
            image = self._size_image(image, target_size)

            # Save the resized image
            image_path = f"{self.base_folder}/images/{i}_f.jpg"
            image.save(image_path)

            # Calculate duration for each clip
            duration = (
                images[i + 1][0] - timestamp
                if i + 1 < len(images)
                else audio.duration - timestamp
            )

            # Create and add the clip
            clips.append(ImageClip(image_path).set_duration(duration))

        # Concatenate and add audio
        video = concatenate_videoclips(clips)
        video = video.set_audio(audio)

        # Write the video file
        video.write_videofile(
            f"{self.base_folder}/output.mp4", codec="libx264", audio_codec="aac", fps=24
        )

    def _size_image(self, image: Image.Image, target_size=(1920, 1080)):
        # Ensure image is in RGB
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            alpha = image.convert("RGBA").split()[-1]
            image = image.convert("RGB")
        else:
            alpha = None
        # Resize the image while maintaining aspect ratio
        aspect_ratio = image.width / image.height
        if aspect_ratio > target_size[0] / target_size[1]:
            new_width = target_size[0]
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = target_size[1]
            new_width = int(new_height * aspect_ratio)

        resized_image = image.resize((new_width, new_height))

        # Create a blurred background
        background = image.resize(target_size).filter(ImageFilter.GaussianBlur(15))

        # Overlay the resized image on the blurred background
        offset = ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2)
        # If the original image had an alpha channel, we use it as a mask
        if alpha:
            alpha = alpha.resize(resized_image.size)
            background.paste(resized_image, offset, alpha)
        else:
            background.paste(resized_image, offset)

        return background


class GoogleImageScraper:
    def __init__(
        self,
        image_path,
        search_key,
        number_of_images=1,
        headless=True,
        min_resolution=(0, 0),
        max_resolution=(1920, 1080),
        max_missed=10,
    ):

        for _ in range(1):
            options = webdriver.ChromeOptions()
            options.binary_location = (
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            )
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(options)
            driver.set_window_size(1400, 1050)
            driver.get("https://www.google.com")
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "W0wltc"))
                ).click()
            except Exception as e:
                continue
        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.image_path = image_path
        self.url = (
            "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"
            % (search_key)
        )
        self.headless = headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed

    def find_image_urls(self):
        """
        This function search and return a list of image urls based on the search key.
        Example:
            google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
            image_urls = google_image_scraper.find_image_urls()

        """
        print("[INFO] Gathering image links")
        self.driver.get(self.url)
        image_urls = []
        count = 0
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        time.sleep(3)
        while self.number_of_images > count and missed_count < self.max_missed:
            if indx_2 > 0:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1, indx_2 + 1)
                    )
                    imgurl.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH, search_string % (indx_1 + 1, 1)
                        )
                        imgurl.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except:
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            else:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1 + 1)
                    )
                    imgurl.click()
                    missed_count = 0
                    indx_1 = indx_1 + 1
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH,
                            '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                            % (indx_1, indx_2 + 1),
                        )
                        imgurl.click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                        search_string = (
                            '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                        )
                    except Exception:
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1

            try:
                # select image from the popup
                time.sleep(1)
                class_names = ["n3VNCb", "iPVvYb", "r48jcc", "pT0Scc"]
                images = [
                    self.driver.find_elements(By.CLASS_NAME, class_name)
                    for class_name in class_names
                    if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0
                ][0]
                for image in images:
                    # only download images that starts with http
                    src_link = image.get_attribute("src")
                    if (
                        src_link
                        and ("http" in src_link)
                        and (not "encrypted" in src_link)
                    ):
                        print(f"[INFO] {self.search_key} \t #{count} \t {src_link}")
                        image_urls.append(src_link)
                        count += 1
                        break
            except Exception:
                print("[INFO] Unable to get link")

            try:
                # scroll page to load next image
                if count % 3 == 0:
                    self.driver.execute_script(
                        "window.scrollTo(0, " + str(indx_1 * 60) + ");"
                    )
                element = self.driver.find_element(By.CLASS_NAME, "mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)

        self.driver.quit()
        print("[INFO] Google search ended")
        return image_urls

    def save_images(self, image_urls, keep_filenames) -> Optional[Image.Image]:
        print(keep_filenames)
        # save images into file directory
        """
            This function takes in an array of image urls and save it into the given image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)

        """
        print("[INFO] Saving image, please wait...")
        for indx, image_url in enumerate(image_urls):
            try:
                print("[INFO] Image url:%s" % (image_url))
                search_string = "".join(e for e in self.search_key if e.isalnum())
                image = requests.get(image_url, timeout=5)
                if image.status_code == 200:
                    with Image.open(io.BytesIO(image.content)) as image_from_web:
                        try:
                            extension = image_url.split(".")[-1]
                            image_path = f"{self.image_path}.{extension}"
                            print(
                                f"[INFO] {self.search_key} \t {indx} \t Image saved at: {image_path}"
                            )
                            image_from_web.save(image_path)
                            return image_from_web
                        except OSError:
                            rgb_im = image_from_web.convert("RGB")
                            rgb_im.save(image_path)
                        image_resolution = image_from_web.size
                        if image_resolution != None:
                            if (
                                image_resolution[0] < self.min_resolution[0]
                                or image_resolution[1] < self.min_resolution[1]
                                or image_resolution[0] > self.max_resolution[0]
                                or image_resolution[1] > self.max_resolution[1]
                            ):
                                image_from_web.close()
                                os.remove(image_path)

                        image_from_web.close()
            except Exception as e:
                print("[ERROR] Download failed: ", e)
                pass
        print("--------------------------------------------------")
        print(
            "[INFO] Downloads completed. Please note that some photos were not downloaded as they were not in the correct format (e.g. jpg, jpeg, png)"
        )

        # pi.download(keywords=term, limit=1, directory=f"{self.folder}/images")
        # print("Downloaded image for", term)
        # time.sleep(10)
        # options = webdriver.ChromeOptions()
        # options.binary_location = (
        #     "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        # )
        # driver = webdriver.Chrome(
        #     options=options,
        # )
        # driver.implicitly_wait(5)
        # for i, (_, term) in enumerate(self.search_terms):
        #     driver.get(
        #         f"https://www.google.com/search?q={term}&udm=2&tbs=isz:l&biw=1872&bih=924"
        #     )
        #     # Find the first img element with a rect of area greater than 500 square pixels
        #     # This is to filter out small images like icons
        #     images = driver.find_elements(By.TAG_NAME, "img")
        #     for image in images:
        #         if image.rect["width"] * image.rect["height"] > 4_000:
        #             image.click()
        #             break
        #     else:
        #         print(f"Failed to find image for search term {i}.")
        #         continue
        #     sidebar = driver.find_element(By.ID, "islrg").find_element(By.ID, "islrg")
        #     sidebar_images = sidebar.find_elements(By.TAG_NAME, "img")
        #     for image in sidebar_images:
        #         src = image.get_attribute("src")
        #         if not src or "http" not in src:
        #             continue
        #         if image.rect["width"] * image.rect["height"] > 4_000:
        #             break
        #     else:
        #         print(f"Failed to find image for search term {i}.")
        #         continue
        #     src = image.get_attribute("src")
        #     if not src:
        #         print(f"Failed to get src for image {i}.")
        #         continue
        #     response = requests.get(src)
        #     if response.status_code != 200:
        #         print(f"Failed to download image for image {i}.")
        #         continue
        #     image_path = f"{self.folder}/images/{i}.jpg"
        #     with open(image_path, "wb") as f:
        #         f.write(response.content)
        #     self.images.append(image_path)
        # driver.quit()
        # # Select the div with id "search"
        # search_div = driver.find_element(By.ID, "islrg")
        # print(f"{search_div = }")
        # # Select the first image
        # image = search_div.find_element(By.TAG_NAME, "img")
        # print(f"{image = }")
        # # Select the encapsulating anchor tag of the image multiple levels up
        # # <a><div><div><div><g-img><img></g-img></div></div></div></a>
        # anchor = image
        # while anchor.tag_name != "a":
        #     anchor = anchor.find_element(By.XPATH, "..")
        #     print(f"{anchor.tag_name = }")
        # # Get the href attribute of the anchor tag
        # href = anchor.get_attribute("href")
        # print(f"{href = }")
        # time.sleep(600)
        # if not href:
        #     print(f"Failed to get href for image {i}.")
        #     continue
        # # Visit the image page
        # driver.get(href)
        # # Get the first a tag's href attribute
        # image_url = driver.find_element(By.TAG_NAME, "a").get_attribute("href")
        # print(f"{image_url = }")
        # if not image_url:
        #     print(f"Failed to get image URL for image {i}.")
        #     continue
        # # Download the image
        # response = requests.get(image_url)
        # if response.status_code != 200:
        #     continue
        # image_path = f"{self.folder}/images/{i}.jpg"
        # with open(image_path, "wb") as f:
        #     f.write(response.content)
        # self.images.append(image_path)
