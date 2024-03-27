from dotenv import load_dotenv

load_dotenv()

from wiki2vid import Wiki2Vid


def main():
    wiki2vid = Wiki2Vid("https://en.wikipedia.org/wiki/Cottage_cheese_boycott")
    wiki2vid.run()


if __name__ == "__main__":
    main()
