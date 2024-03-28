from dotenv import load_dotenv

load_dotenv()

from wiki2vid import Wiki2Vid


def main():
    wiki2vid = Wiki2Vid("https://en.wikipedia.org/wiki/Train_surfing")
    wiki2vid.build_script()


if __name__ == "__main__":
    main()
