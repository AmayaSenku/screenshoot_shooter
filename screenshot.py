"""Take a screenshot of the whole screen every N seconds until Ctrl+C.

Usage:
    python screenshot.py                  # asks for the interval
    python screenshot.py -i 7             # every 7 seconds
    python screenshot.py -i 5 -o shots    # custom output folder
"""
import argparse
import os
import time
from datetime import datetime

from PIL import ImageGrab


def ask_interval():
    while True:
        raw = input("Interval in seconds (e.g. 5-10): ").strip()
        try:
            value = float(raw)
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a number greater than 0.")


def main():
    parser = argparse.ArgumentParser(description="Periodic full-screen screenshots")
    parser.add_argument("-i", "--interval", type=float, help="seconds between screenshots")
    parser.add_argument("-o", "--output", default="screenshots", help="output folder")
    args = parser.parse_args()

    interval = args.interval if args.interval and args.interval > 0 else ask_interval()
    os.makedirs(args.output, exist_ok=True)

    print(f"Saving a screenshot every {interval}s to '{args.output}'. Press Ctrl+C to stop.")
    count = 0
    try:
        while True:
            started = time.monotonic()
            name = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
            path = os.path.join(args.output, name)
            ImageGrab.grab(all_screens=True).save(path)
            count += 1
            print(f"[{count}] {path}")
            # subtract capture time so the interval stays accurate
            time.sleep(max(0, interval - (time.monotonic() - started)))
    except KeyboardInterrupt:
        print(f"\nStopped. {count} screenshots saved.")


if __name__ == "__main__":
    main()
