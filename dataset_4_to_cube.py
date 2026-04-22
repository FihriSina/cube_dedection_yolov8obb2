import os
from pathlib import Path

# Dataset klasör yolu
DATASET_ROOT = Path("dataset_4")  # Kaggle datasetini buraya koy

# Sadece küp sınıflarını tutmak
KEEP_CLASSES = {0, 2}  # Küp id'leri (green cube, yellow cube)

# OBB formatına dönüştürmek için
def convert_to_obb_format(x1, y1, x2, y2, x3, y3, x4, y4, image_width, image_height):
    # Koordinatları normalize et
    x1, x2, x3, x4 = x1 * image_width, x2 * image_width, x3 * image_width, x4 * image_width
    y1, y2, y3, y4 = y1 * image_height, y2 * image_height, y3 * image_height, y4 * image_height

    return f"{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}"

# Etiketleri işle
def process_label_file(label_path, image_width, image_height):
    print(f"Processing label file: {label_path}")  # Hangi dosya işlendiği
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

        if class_id == 0 or class_id == 3:  # Eğer sınıf green cube veya yellow cube ise
            class_id = 0  # Hepsini cube sınıfına kaydet

        elif class_id not in KEEP_CLASSES:  # Diğer sınıflar "notcube" olacak
            class_id = 4  # "notcube" id'si

        # 8 koordinatı al (OBB)
        x1, y1, x2, y2, x3, y3, x4, y4 = map(float, parts[1:])
        
        # OBB formatına dönüştür
        new_line = convert_to_obb_format(x1, y1, x2, y2, x3, y3, x4, y4, image_width, image_height)
        new_lines.append(f"{class_id} {new_line}")
    
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
            image_file = image_dir / f"{label_file.stem}.jpg"  # veya .png, .jpeg - resim formatını kontrol et
            if image_file.exists():
                try:
                    image_width, image_height = get_image_dimensions(image_file)  # Resmin boyutlarını al
                    print(f"Processing image: {image_file} - Dimensions: {image_width}x{image_height}")
                except Exception as e:
                    print(f"Error getting image dimensions for {image_file}: {e}")
                    continue

                new_lines = process_label_file(label_file, image_width, image_height)

                # Yeni etiket dosyasını yaz
                if new_lines:
                    with open(label_file, "w") as file:
                        file.write("\n".join(new_lines) + "\n")
                else:
                    # Eğer hiç geçerli sınıf yoksa, etiket dosyasını sil
                    os.remove(label_file)
                    os.remove(image_file)  # Resmi de siliyoruz
                    print(f"Deleted empty label file and image: {label_file}")

def get_image_dimensions(image_path):
    from PIL import Image
    with Image.open(image_path) as img:
        return img.size  # (width, height)

if __name__ == "__main__":
    process_dataset()