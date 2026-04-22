import os
from pathlib import Path

# Dataset klasör yolu
data_root = Path("data")

# Klasörler
image_dirs = ["train", "valid", "test"]

# Resim ve etiket dosyalarının eşleşip eşleşmediğini kontrol et
def delete_missing_labels():
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

        # Resim dosyalarını kontrol et
        image_files = set([f.stem for f in image_dir.glob("*") if f.suffix in ['.jpg', '.png', '.jpeg']])
        label_files = set([f.stem for f in label_dir.glob("*")])

        # Etiketsiz resimleri sil
        missing_labels = image_files - label_files
        if missing_labels:
            for missing_image in missing_labels:
                image_to_delete = image_dir / f"{missing_image}.jpg"  # veya .png, .jpeg
                if image_to_delete.exists():
                    os.remove(image_to_delete)
                    print(f"Deleted missing image: {image_to_delete}")

        print(f"{split} data is cleaned.")

if __name__ == "__main__":
    delete_missing_labels()