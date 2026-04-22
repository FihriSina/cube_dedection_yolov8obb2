import os
from pathlib import Path

# Dataset klasör yolu
DATASET_ROOT = Path("dataset_3")  # dataset_3 için yol

# Yalnızca küp sınıfını tutacağız (sadece 2: cube olacak)
KEEP_CLASSES = {2: 'cube'}  # Küp sınıfı (2)

# `notcube` sınıfı, diğer tüm nesneler için kullanılacak
NOTCUBE_CLASS_ID = 0  # notcube id'si (şimdi 0 olacak, cube için)

# Etiketleri düzenle
def process_label_file(label_path):
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

        if class_id == 2:  # Eğer sınıf `cube` ise, bu satırı tut
            class_id = 0  # Küpleri `cube` olarak 0 numara ile kaydet

        else:  # Diğer sınıfları `notcube` yapacağız
            class_id = 1  # notcube id'si

        # Yeni satır oluştur
        new_lines.append(f"{class_id} {' '.join(parts[1:])}")

    return new_lines

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
            new_lines = process_label_file(label_file)

            # Yeni etiket dosyasını yaz
            if new_lines:
                with open(label_file, "w") as file:
                    file.write("\n".join(new_lines) + "\n")
            else:
                # Eğer hiç geçerli sınıf yoksa, etiket dosyasını ve resmi sil
                os.remove(label_file)
                os.remove(image_file)  # Resmi de siliyoruz
                print(f"Deleted empty label file and image: {label_file}")

if __name__ == "__main__":
    process_dataset()