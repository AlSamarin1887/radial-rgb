from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
import argparse

WIDTH = 1080
HEIGHT = 1920
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 3
EXPECTED_BYTES = WIDTH * HEIGHT * 3


def get_order():
    y, x = np.indices((HEIGHT, WIDTH))

    distance = (
            (x - CENTER_X) ** 2 +
            (y - CENTER_Y) ** 2
    )

    return np.argsort(
        distance.ravel(),
        kind="stable"
    )


ORDER = get_order()


def encode(input_path: str, output_path: str) -> None:
    with Image.open(input_path) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")

        image = ImageOps.fit(
            image,
            (WIDTH, HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

        pixels = np.asarray(
            image,
            dtype=np.uint8
        ).reshape(-1, 3).copy()

    radial_pixels = pixels[ORDER]
    data = radial_pixels.tobytes()

    if len(data) != EXPECTED_BYTES:
        raise RuntimeError(
            f"Unexpected data size: {len(data)} bytes"
        )

    Path(output_path).write_bytes(data)

    print(f"Output:     {output_path}")
    print(f"Resolution: {WIDTH} × {HEIGHT}")
    print(f"Center:     {CENTER_X}, {CENTER_Y}")
    print(f"Pixels:     {WIDTH * HEIGHT:,}")
    print(f"Bytes:      {len(data):,}")


def view(input_path: str) -> None:
    data = Path(input_path).read_bytes()

    if len(data) != EXPECTED_BYTES:
        raise ValueError(
            f"Invalid file size: {len(data)} bytes, "
            f"expected {EXPECTED_BYTES}"
        )

    radial_pixels = np.frombuffer(
        data,
        dtype=np.uint8
    ).reshape(-1, 3)

    pixels = np.empty(
        (WIDTH * HEIGHT, 3),
        dtype=np.uint8
    )

    pixels[ORDER] = radial_pixels

    image = Image.fromarray(
        pixels.reshape(HEIGHT, WIDTH, 3)
    )

    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    encode_parser = subparsers.add_parser("encode")
    encode_parser.add_argument("input")
    encode_parser.add_argument("output")

    view_parser = subparsers.add_parser("view")
    view_parser.add_argument("input")

    args = parser.parse_args()

    if args.command == "encode":
        encode(args.input, args.output)

    elif args.command == "view":
        view(args.input)
