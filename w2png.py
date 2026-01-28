import sys
import os
import glob
from PIL import Image

def convert_to_webp(folder, recursive=False):
    folder = os.path.abspath(folder)

    patterns = ["**/*.webp", "**/*.jpg", "**/*.jpeg"] if recursive else ["*.webp", "*.jpg", "*.jpeg"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(folder, pattern), recursive=recursive))

    if not files:
        print(f"⚠️ No PNG or JPG files found in '{folder}'")
        return

    print(f"🌀 Converting {len(files)} image files in '{folder}' → WebP ...")

    for file in files:
        try:
            webp_path = file.rsplit(".", 1)[0] + ".png"
            if os.path.exists(webp_path):
                print(f"⏭️  Skipping (already exists): {webp_path}")
                continue

            image = Image.open(file)
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

            image.save(webp_path, "png", quality=100, method=6)
            print(f"✅ {os.path.basename(file)} → {os.path.basename(webp_path)}")
        except Exception as e:
            print(f"❌ Error converting {file}: {e}")

    print("🎉 Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python png2w.py [--recursive] <folder>")
        sys.exit(1)

    recursive = "--recursive" in sys.argv
    # pick the first argument that is not '--recursive' as folder
    folder = next(arg for arg in sys.argv[1:] if arg != "--recursive")

    convert_to_webp(folder, recursive)
