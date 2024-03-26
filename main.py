from wiki2vid import Wiki2Vid


def main():
    wiki_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    wiki2vid = Wiki2Vid(wiki_url)
    wiki2vid.create_video()


def test():
    wiki2vid = Wiki2Vid()
    script = wiki2vid.get_script()
    print(script.full_script)


if __name__ == "__main__":
    test()
