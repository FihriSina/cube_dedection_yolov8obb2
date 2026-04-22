import os
from pathlib import Path

# Dataset klasör yolu
DATASET_ROOT = Path("dataset_2")  # dataset_2 için yol

# Küp sınıfını tek bir sınıfa indiriyoruz (Blue, Green, Red → cube)
KEEP_CLASSES = {0: 'cube', 1: 'cube', 2: 'cube'}  # Hepsini cube yapıyoruz

# Etiketleri düzenle
def process_label_file(label_path, image_dir):
    print(f"Processing label file: {label_path}")
    try:
        with open(label_path, "r") as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading {label_path}: {e}")
        return []

    new_lines = []

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])

        # Hepsi `cube` sınıfına dönüştürülecek
        class_id = 0  # Her sınıfı `cube` olarak işaretle

        # Yeni satır oluştur
        new_lines.append(f"{class_id} {' '.join(parts[1:])}")

    # Yeni etiket dosyasını yaz
    if new_lines:
        with open(label_path, "w") as file:
            file.write("\n".join(new_lines) + "\n")
    else:
        # Eğer hiç geçerli sınıf yoksa, etiket dosyasını ve resmi sil
        image_file = image_dir / f"{label_path.stem}.jpg"  # Etiket dosyasının uzantısına göre resmi bul
        if image_file.exists():
            os.remove(image_file)  # Resmi sil
        os.remove(label_path)  # Etiket dosyasını sil
        print(f"Deleted empty label file and image: {label_path}")


# Dataset üzerinde işlem yap
def process_dataset():
    image_dirs = ["train", "valid", "test"]  # Alt klasörler

    for folder in image_dirs:
        image_dir = DATASET_ROOT / folder / "images"
        label_dir = DATASET_ROOT / folder / "labels"

        if not image_dir.exists():
            print(f"Error: 'images' directory not found in {folder}")
            continue
        if not label_dir.exists():
            print(f"Error: 'labels' directory not found in {folder}")
            continue

        print(f"Processing {folder} dataset...")

        for label_file in label_dir.glob("*.txt"):
            # Etiket dosyasını işle
            process_label_file(label_file, image_dir)

if __name__ == "__main__":
    process_dataset()