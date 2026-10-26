"""Create 32x32 copies of Training and Test images, preserving folders and filenames.

Install Pillow: python -m pip install Pillow
Run: python resize_training.py
Output: Dataset_32x32/<Training or Test>/<class folder>/<original filename>
"""

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCES = (ROOT / "Training", ROOT / "Test")
DESTINATION = ROOT / "Dataset_32x32"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def main():
    for source in SOURCES:
        if not source.is_dir():
            raise SystemExit(f"Dataset folder not found: {source}")

    converted = 0
    failed = 0
    paths = (path for source in SOURCES for path in source.rglob("*"))
    for source_path in paths:
        destination_path = DESTINATION / source_path.relative_to(ROOT)
        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue
        if source_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        try:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source_path) as image:
                resized = ImageOps.exif_transpose(image).resize(
                    (32, 32), Image.Resampling.LANCZOS
                )
                if source_path.suffix.lower() in {".jpg", ".jpeg"}:
                    resized = resized.convert("RGB")
                    resized.save(destination_path, quality=95)
                else:
                    resized.save(destination_path)
            converted += 1
            if converted % 1000 == 0:
                print(f"Resized {converted:,} images...", flush=True)
        except (OSError, ValueError) as error:
            failed += 1
            print(f"Failed: {source_path}: {error}")

    print(f"Resized {converted:,} images to 32x32 in {DESTINATION}")
    if failed:
        raise SystemExit(f"Could not resize {failed:,} images; see errors above.")


if __name__ == "__main__":
    main()
