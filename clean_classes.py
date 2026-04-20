from pathlib import Path
import os

DATASET_ROOT = Path("datas")

# Sadece küpler kalsın
KEEP_CLASSES = {0, 2, 4}

# Hepsi tek sınıfa dönüşecek
NEW_CLASS_ID = 0

SPLITS = ["train", "valid", "test"]

def process_label_file(label_path: Path) -> bool:
    """
    Label dosyasını temizler.
    Geriye en az bir geçerli anotasyon kaldıysa True döner.
    Hiç anotasyon kalmadıysa False döner.
    """
    if not label_path.exists():
        return False

    lines = label_path.read_text(encoding="utf-8").strip().splitlines()
    new_lines = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 9:
            # OBB formatı değilse atla
            continue

        try:
            class_id = int(parts[0])
        except ValueError:
            continue

        if class_id in KEEP_CLASSES:
            parts[0] = str(NEW_CLASS_ID)
            new_lines.append(" ".join(parts))

    if new_lines:
        label_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return True
    else:
        return False

def remove_image_and_label(image_path: Path, label_path: Path):
    if image_path.exists():
        image_path.unlink()
    if label_path.exists():
        label_path.unlink()

def main():
    total_labels = 0
    kept_labels = 0
    removed_files = 0

    for split in SPLITS:
        images_dir = DATASET_ROOT / split / "images"
        labels_dir = DATASET_ROOT / split / "labels"

        for label_path in labels_dir.glob("*.txt"):
            total_labels += 1
            has_valid = process_label_file(label_path)

            stem = label_path.stem
            possible_images = [
                images_dir / f"{stem}.jpg",
                images_dir / f"{stem}.jpeg",
                images_dir / f"{stem}.png",
                images_dir / f"{stem}.bmp",
                images_dir / f"{stem}.webp",
            ]

            image_path = None
            for img in possible_images:
                if img.exists():
                    image_path = img
                    break

            if has_valid:
                kept_labels += 1
            else:
                if image_path is not None:
                    remove_image_and_label(image_path, label_path)
                    removed_files += 1
                else:
                    if label_path.exists():
                        label_path.unlink()

    yaml_path = DATASET_ROOT / "data.yaml"
    yaml_content = """train: train/images
val: valid/images
test: test/images

names:
  0: cube
"""
    yaml_path.write_text(yaml_content, encoding="utf-8")

    print("Temizleme tamamlandı.")
    print(f"Toplam label dosyası: {total_labels}")
    print(f"Kalan label dosyası: {kept_labels}")
    print(f"Silinen görsel+label sayısı: {removed_files}")
    print("data.yaml güncellendi -> sadece 'cube' kaldı.")

if __name__ == "__main__":
    main()