from home_automation import switcher
import time


def test():
    switcher.turn_on("rlamp")
    time.sleep(2)
    switcher.turn_off("rlamp")

    time.sleep(2)
    switcher.turn_on("fan")
    time.sleep(2)
    switcher.turn_off("fan")


if __name__ == "__main__":
    test()
