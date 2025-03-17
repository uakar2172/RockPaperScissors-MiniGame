# Taş Kağıt Makas Oyunu

Bu proje, Pygame kullanılarak geliştirilmiş bir "Taş Kağıt Makas" simülasyon oyunudur. İnternette gördüğüm projeyi temel alarak, kendi geliştirmelerimi ekledim. Yapay zeka destekli yöntemlerle benzer projeler oluşturmak oldukça kolay!

## Özellikler

- Başlangıç ekranı ve geri sayım.
- Dinamik oyun döngüsü.
- Hücrelerin çarpışması ve dönüşümü.
- Kazanan animasyonu (shake efekti).
- FPS, skor ve zaman göstergesi.

## Gereksinimler

- Python 3.x
- [Pygame](https://www.pygame.org/) kütüphanesi

## Kurulum

1. **Python ve Pygame Kurulumu:**  
   Python 3.x yüklü değilse [Python'un resmi sitesinden](https://www.python.org/downloads/) indirebilirsiniz.  
   Terminal veya komut satırında şu komutla Pygame'i yükleyin:pip install pygame


2. **Proje Dosyaları:**  
Bu repoda `main.py` ana kod dosyası yer almaktadır.

**Önemli:** Projeyi çalıştırmadan önce, proje dizininde `oyunresim` adlı bir klasör oluşturun ve aşağıdaki dosyaları bu klasöre ekleyin:
- `tas.png` : Taş görseli
- `kagit.png` : Kağıt görseli
- `makas.png` : Makas görseli
- `muzik.mp3` : Arka plan müziği

Eğer bu dosyalar mevcut değilse, telifsiz kaynaklardan benzer görseller ve müzik dosyaları edinebilir veya yer tutucu dosyalar kullanabilirsiniz.

## Çalıştırma

Proje dizinine gidip terminalde aşağıdaki komutu çalıştırın:python main.py
