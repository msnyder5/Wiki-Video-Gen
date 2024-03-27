import random

from wiki2vid import Wiki2Vid


def random_wiki_url():
    return random.choice(
        [
            "https://apexlegends.fandom.com/wiki/Fuse",
            "https://apexlegends.fandom.com/wiki/Bloodhound",
        ]
    )


def main():
    wiki_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    wiki2vid = Wiki2Vid(wiki_url)
    wiki2vid.create_video()


def test():
    wiki2vid = Wiki2Vid("https://en.wikipedia.org/wiki/Cottage_cheese_boycott")
    script = wiki2vid.get_script()
    with open("output.md", "w") as f:
        f.write(script.script)


if __name__ == "__main__":
    test()
