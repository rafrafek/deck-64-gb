from urllib.request import urlopen

# Set this
ntfy_url = "https://ntfy.sh/YOUR_NTFY_URL"

# We need a timeout to prevent script from hanging
timeout = 8


def parse_availability(data: bytes) -> bool:
    parsed = " ".join(f"{c:02X}" for c in data)
    match parsed:
        case "08 01 10 00":
            return True
        case "08 00 10 00":
            return False
        case _:
            raise Exception("Unknown new value")


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
    print(message)
    with urlopen(ntfy_url, data=str.encode(message), timeout=timeout):
        pass


if __name__ == "__main__":
    # Refurbished 64GB in Europe, tested in Poland
    if is_available("COGVNxICUEw="):
        notify("64GB")
