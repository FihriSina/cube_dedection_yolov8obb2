https://universe.roboflow.com/2024robotcube/cube-udoei
https://universe.roboflow.com/autonomous-object-picking-robot/colored-blocks/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true
https://universe.roboflow.com/roboticarm/cube-pr1ld/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true
https://universe.roboflow.com/yolov8-hhmit/cube-detection-project/browse?queryText=class%3Acube&pageSize=200&startingIndex=0&browseQuery=true
https://www.kaggle.com/datasets/saikatpanda/cubes-craters-and-cylinder/

### Kısa Roadmap

1. **Proje yapısını kuracağız**

   * `box_dedection` ana klasörü
   * `datas` dataset klasörü
   * Anaconda ortamı: `boxD`

2. **Anaconda sanal ortamını oluşturacağız**

   * Python sürümünü belirleyip
   * `boxD` ortamını açacağız
   * Gerekli paketleri kuracağız

3. **Dataseti projeye alacağız**

   * Roboflow datasetini indireceğiz
   * Klasör yapısını kontrol edeceğiz
   * `train / valid / test` ve etiket dosyalarını doğrulayacağız

4. **Class temizliği yapacağız**

   * Sadece küp ile ilgili class kalacak
   * Fazlalık classları sileceğiz
   * Label dosyalarını buna göre düzenleyeceğiz
   * `data.yaml` dosyasını güncelleyeceğiz

5. **Data augmentation uygulayacağız**

   * Uygun dönüşümleri belirleyeceğiz
   * OBB yapısını bozmayacak augmentasyonlar seçeceğiz
   * Gerekirse eğitim sırasında augmentation parametreleriyle ilerleyeceğiz

6. **YOLOv8-OBB kurulumunu yapacağız**

   * Ultralytics kuracağız
   * OBB destekli veri yapısını doğrulayacağız
   * Ön kontrol amaçlı birkaç örnek label görselleştireceğiz

7. **Model eğitimi yapacağız**

   * Uygun pretrained OBB modelini seçeceğiz
   * Eğitim parametrelerini belirleyeceğiz
   * Eğitimi başlatacağız

8. **Sonuçları inceleyeceğiz**

   * `best.pt` ve `last.pt` çıktıları
   * loss, mAP ve confusion benzeri metrikler
   * örnek tahmin görselleri

9. **Test ve gerçek kullanım aşaması**

   * Görseller üzerinde test
   * Kamerada test
   * İnternetten bulduğun yeni görsellerde deneme

10. **İyileştirme aşaması**

* Veri artırma
* epoch / image size / batch ayarı
* düşük performanslı örnekleri analiz etme


---

- train: 1820 image / 1820 label
- valid: 521 / 521
- test: 260 / 260

- clean_classes.py sadece tek sınıf yaptı ve pillar etiketlerini ve resimlerini sildi.

python .\clean_classes.py
Temizleme tamamlandı.
Toplam label dosyası: 2601
Kalan label dosyası: 1796
Silinen görsel+label sayısı: 805
data.yaml güncellendi -> sadece 'cube' kaldı.

--- 

**Sade Eğitim:**
yolo task=obb mode=train model=yolov8n-obb.pt data=.\datas\data.yaml epochs=100 imgsz=640 batch=16 device=0 mosaic=0.0 fliplr=0.0 flipud=0.0 degrees=0.0 translate=0.0 scale=0.0 shear=0.0 perspective=0.0 hsv_h=0.0 hsv_s=0.0 hsv_v=0.0 workers=4 name=cube_obb_noaug_100

**Augmentation Eğitim**
yolo task=obb mode=train model=yolov8n-obb.pt data=.\datas\data.yaml epochs=100 imgsz=640 batch=16 device=0 degrees=15 scale=0.2 fliplr=0.5 flipud=0.0 hsv_h=0.015 hsv_s=0.5 hsv_v=0.3 translate=0.1 mosaic=0.2 workers=4 name=cube_obb_aug_100

**Augmentationsız final**
precision: 0.99985
recall: 0.98603
mAP50: 0.985
mAP50-95: 0.83321

**Augmentation’lı final**
precision: 0.99979
recall: 0.98603
mAP50: 0.985
mAP50-95: 0.84794

# Proje Yapısı

box_dedection