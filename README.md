Tabii, Taha! Şimdi **proje yapısını** ve şu ana kadar yaptıklarınızı **Türkçe** olarak düzenleyeceğim. Ayrıca, **`check_data.py`**, **`clean_classes.py`**, **`dataset_1_to_cube.py`** gibi dosyaların da proje yapısına dahil edildiğinden emin olacağım.

İşte **güncellenmiş `README.md` dosyası**:

---

```markdown
# Küp Algılama ile YOLOv8-OBB Eğitimi

Bu proje, **YOLOv8-OBB** modelini kullanarak görsellerde **küp** tespiti yapmayı amaçlamaktadır. **Roboflow** ve **Kaggle** üzerinden alınan verilerle model eğitilmiş ve **data augmentation** teknikleri kullanılarak doğruluk artırılmaya çalışılmıştır.

## Proje Yapısı

```

box_dedection/
├── data/                       # Veri ve eğitim verileri
│   ├── train/
│   │   ├── images/             # Eğitim resimleri
│   │   └── labels/             # Eğitim etiketleri
│   ├── valid/
│   │   ├── images/             # Geçerli (validation) resimler
│   │   └── labels/             # Geçerli etiketler
│   ├── test/
│   │   ├── images/             # Test resimleri
│   │   └── labels/             # Test etiketleri
│   ├── merged_data.yaml        # Birleştirilmiş veri yapılandırma dosyası
│   └── data.yaml               # Dataset yapılandırma dosyası
├── runs/                       # Eğitim çıktıları
│   └── obb/
├── yolov8n-obb.pt              # Önceden eğitilmiş YOLOv8-OBB modeli
├── README.md                   # Proje açıklamaları
├── check_data.py               # Veri dosyası kontrol scripti
├── clean_classes.py            # Sınıf temizliği scripti
├── dataset_1_to_cube.py        # Dataset temizleme ve sınıf düzenleme scripti
├── dataset_2_to_cube.py        # Dataset temizleme ve sınıf düzenleme scripti
├── dataset_3_to_cube.py        # Dataset temizleme ve sınıf düzenleme scripti
├── dataset_4_to_cube.py        # Dataset temizleme ve sınıf düzenleme scripti
├── delete_missing_labels.py    # Obb hale getirme scripti
└── train.py                    # Eğitim için gerekli olan diğer dosyalar

````

## Projede İzlenen Adımlar

### 1. **Proje Yapısını Kurma**
   - **`box_dedection`** ana klasörü oluşturuldu.
   - **`data`** klasörü altında `train`, `valid` ve `test` alt klasörleri oluşturuldu ve veriler düzenlendi.
   - Gerekli **`data.yaml`** ve **`merged_data.yaml`** dosyaları oluşturuldu.

### 2. **Anaconda Ortamı Oluşturma**
   - **`boxD`** adında bir Anaconda ortamı oluşturuldu.
   - Gerekli kütüphaneler, özellikle **Ultralytics YOLOv8** ve diğer bağımlılıklar kuruldu.

### 3. **Dataseti Projeye Alma**
   - **Roboflow** ve **Kaggle** üzerinden **datasetler** indirildi.
   - Verilerin **`train`, `valid`, `test`** ve **etiketler** dosyalarına uygun şekilde düzenlenmesi sağlandı.
   - **`clean_classes.py`** scripti, gereksiz sınıfları silip yalnızca **küp** sınıfını tutacak şekilde **etiket dosyalarını düzenledi**.

### 4. **Sınıf Temizliği**
   - **`clean_classes.py`** scripti ile yalnızca **küp** sınıfı tutularak diğer sınıflar temizlendi.
   - **`data.yaml`** dosyası, yalnızca **küp** sınıfını içerecek şekilde güncellendi.
   - **Toplam etiket dosyası**: 2601
   - **Kalan etiket dosyası**: 1796
   - **Silinen görseller ve etiketler**: 805

### 5. **Data Augmentation**
   - **Data augmentation** teknikleri kullanıldı:
     - **Yatay/Dikey Yansıma** (fliplr, flipud)
     - **Renk Değiştirme** (hsv_h, hsv_s, hsv_v)
     - **Rastgele Döndürme** (degrees)
     - **Mosaic Augmentation** ile farklı görsellerin birleştirilmesi.
   - Augmentasyonlu eğitimle modelin doğruluğu artırılmaya çalışıldı.

### 6. **YOLOv8-OBB Model Eğitimi**
   - Model, **YOLOv8-OBB** kullanılarak eğitildi.
   - **Augmentasyonsuz Eğitim**:
     ```bash
     yolo task=obb mode=train model=yolov8n-obb.pt data=.\datas\data.yaml epochs=100 imgsz=640 batch=16 device=0 mosaic=0.0 fliplr=0.0 flipud=0.0 degrees=0.0 translate=0.0 scale=0.0 shear=0.0 perspective=0.0 hsv_h=0.0 hsv_s=0.0 hsv_v=0.0 workers=4 name=cube_obb_noaug_100
     ```

   - **Augmentasyonlu Eğitim**:
     ```bash
     yolo task=obb mode=train model=yolov8n-obb.pt data=.\datas\data.yaml epochs=100 imgsz=640 batch=16 device=0 degrees=15 scale=0.2 fliplr=0.5 flipud=0.0 hsv_h=0.015 hsv_s=0.5 hsv_v=0.3 translate=0.1 mosaic=0.2 workers=4 name=cube_obb_aug_100
     ```

### 7. **Model Performans Sonuçları**
   - **Augmentasyonsuz Eğitim Sonuçları**:
     - **Precision**: 0.99985
     - **Recall**: 0.98603
     - **mAP50**: 0.985
     - **mAP50-95**: 0.83321

   - **Augmentasyonlu Eğitim Sonuçları**:
     - **Precision**: 0.99979
     - **Recall**: 0.98603
     - **mAP50**: 0.985
     - **mAP50-95**: 0.84794

### 8. **Modeli Test Etme**
   - Eğitim tamamlandıktan sonra model **test resimleri** üzerinde test edildi ve **en iyi model** ağırlıkları **`best.pt`** olarak kaydedildi.

### 9. **Sonraki Adımlar**
   - **Daha fazla augmentation** uygulayarak modelin doğruluğunu artırabiliriz.
   - **Epoch sayısını artırarak** daha uzun süreli eğitim yapabiliriz.
   - **Gerçek dünya testleri** (kamera üzerinden) yapılabilir.

---

## Proje Dosyaları

- **`check_data.py`**: Veri dosyasının eksik etiketleri kontrol etmesini sağlar.
- **`clean_classes.py`**: Eğitimde yalnızca **küp** sınıfını tutarak diğer sınıfları siler.
- **`dataset_1_to_cube.py`**: Datasetin **küp** sınıfına dönüştürülmesini sağlar.

---

