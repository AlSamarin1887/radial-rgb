# Radial RGB

A minimal, headerless raw RGB image format in which pixels are serialized by their distance from a fixed point.

The file contains only pixel data. Its dimensions, channel structure, and pixel ordering are defined externally by the encoder and decoder.

## Format

| Property | Value |
|---|---|
| Resolution | 1080 × 1920 |
| Pixel representation | 8-bit RGB (3 channels) |
| Pixel count | 2,073,600 |
| File size | 6,220,800 bytes |
| Radial origin | (540, 640) |
| Pixel ordering | Ascending squared Euclidean distance |
| Compression | None |
| Header | None |
| Metadata | None |

Coordinates are measured from the top-left corner of the image, with (0, 0) representing the first pixel.

Each pixel is represented by three consecutive bytes: red, green, and blue.

## Encoding

1. Apply EXIF orientation.
2. Convert the image to RGB.
3. Resize proportionally and center-crop to 1080 × 1920 using LANCZOS resampling.
4. Calculate the squared Euclidean distance of each pixel from (540, 640).
5. Sort pixels by increasing distance, preserving row-major order for equal distances.
6. Write the reordered RGB values as a continuous byte sequence.

The output contains no embedded information about dimensions, coordinates, pixel ordering, or its source image.

## Decoding

The decoder reads exactly 6,220,800 bytes and reconstructs the image using the same radial ordering.

The radial permutation is lossless and reversible. The initial image conversion, resizing, and cropping are not necessarily lossless.

## Installation

Requires Python 3, NumPy, and Pillow.

```bash
pip install numpy pillow
```

## Usage

Encode an image:

```bash
python radial_rgb.py encode input.jpg output.rgb
```

View an encoded image:

```bash
python radial_rgb.py view output.rgb
```

## License

MIT License.

Copyright (c) 2026 Aleksei Samarin