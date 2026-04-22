import os
from pathlib import Path

# Dataset klasör yolu
data_root = Path("data")

# Klasörler
image_dirs = ["train", "valid", "test"]
image_ext = ['.jpg', '.png', '.jpeg']  # Resim uzantıları

# Her klasörde resim ve etiketlerin eşleşip eşleşmediğini kontrol et
def check_data():
    for split in image_dirs:
        image_dir = data_root / split / "images"
        label_dir = data_root / split / "labels"
        
        if not image_dir.exists():
            print(f"Error: '{split}/images' directory not found!")
            continue
        if not label_dir.exists():
            print(f"Error: '{split}/labels' directory not found!")
            continue
        
        print(f"Checking {split} data...")

        # Resim ve etiket dosyalarını eşleştir
        image_files = set([f.stem for f in image_dir.glob("*") if f.suffix in image_ext])
        label_files = set([f.stem for f in label_dir.glob("*")])

        # Eşleşmeyen dosyaları kontrol et
        missing_labels = image_files - label_files
        missing_images = label_files - image_files

        if missing_labels:
            print(f"Missing labels for images: {missing_labels}")
        if missing_images:
            print(f"Missing images for labels: {missing_images}")

        # Eğer her şey uyuyorsa, veri düzgün
        if not missing_labels and not missing_images:
            print(f"{split} data is valid.")

if __name__ == "__main__":
    check_data()