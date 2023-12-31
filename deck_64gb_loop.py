from time import sleep
from typing import NoReturn
from urllib.request import urlopen

# Set this
ntfy_url = "https://ntfy.sh/YOUR_NTFY_URL"

# Default value should be OK
checking_frequency_in_seconds = 20

# We need a timeout to prevent script from hanging
timeout = 8


def parse_availability(data: bytes) -> bool:
    parsed = " ".join(f"{c:02X}" for c in data)
    if parsed.startswith("08 01 10 "):
        return True
    elif parsed.startswith("08 00 10 "):
        return False
    else:
        raise Exception("Unknown response value")


def is_available(id: str) -> bool:
    url = (
        "https://api.steampowered.com/IPhysicalGoodsService/"
        "CheckInventoryAvailableByPackage/v1?origin="
        f"https://store.steampowered.com&input_protobuf_encoded={id}"
    )
    with urlopen(url, timeout=timeout) as response:
        data = response.read()
    return parse_availability(data)


def notify(name: str) -> None:
    message = f"Version {name} is now available!"
    print()
    print(message)
    with urlopen(ntfy_url, data=str.encode(message), timeout=timeout):
        pass


def flush_print(text: str) -> None:
    print(text, end=" ", flush=True)


def main_loop() -> NoReturn:
    n = 0
    sleep_time = checking_frequency_in_seconds
    flush_print("Press CTRL-C to stop. Checks passed:")
    while True:
        n += 1
        flush_print(str(n))
        try:
            if is_available("COGVNxICUEw="):
                notify("64GB")
                sleep_time = checking_frequency_in_seconds * 10
            else:
                sleep_time = checking_frequency_in_seconds
        except Exception as e:
            print()
            print(e)

        sleep(sleep_time)


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print()
