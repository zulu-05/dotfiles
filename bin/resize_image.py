#!/usr/bin/env python3
import sys
import argparse
from PIL import Image
from pathlib import Path

def resize_image(image_path, width, quality):
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Error: Cannot open {image_path}. Is it a valid image file?")
        return

    # Calculate new height while maintaining aspect ratio
    aspect_ratio = img.height / img.width
    new_height = int(width * aspect_ratio)

    # Resize the image
    resized_img = img.resize((width, new_height), Image.Resampling.LANCZOS)

    # Create the new filename
    p = Path(image_path)
    new_filename = f"{p.stem}_resized{p.suffix}"

    print(f"Resizing {image_path} to {width}x{new_height} -> {new_filename}")

    # Save the new image
    resized_img.save(new_filename, quality=quality, optimize=True)

def main():
    parser = argparse.ArgumentParser(description="Resize one or more images.")
    parser.add_argument("files", nargs='+', help="The image file(s) to resize.")
    parser.add_argument("--width", type=int, default=1024, help="The target width in pixels.")
    parser.add_argument("--quality", type=int, default=90, help="The quality for JPEG images (1-100).")
    args = parser.parse_args()

    for f in args.files:
        resize_image(f, args.width, args.quality)

if __name__ == "__main__":
    # Check for Pillow dependency
    try:
        from PIL import Image
    except ImportError:
        print("Error: The 'Pillow' library is required. Please install it with 'pip install Pillow'.")
        sys.exit(1)
    main()
