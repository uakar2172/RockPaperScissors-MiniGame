import pygame
import sys
import random
import math
import os

# Pencerenin ekranda ortalanmasını sağlar
os.environ['SDL_VIDEO_CENTERED'] = '1'

# -----------------------------
# Fonksiyonlar
# -----------------------------
def show_start_screen(screen, width, height):
    """Başlangıç ekranı: 'Başlamak için tıkla' butonunu gösterir."""
    title_font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 48)

    # Başlık metni
    title_text = title_font.render("Taş Kağıt Makas Oyunu", True, WHITE)

    # Buton metni ve buton dikdörtgeni (daha büyük)
    button_text = button_font.render("Başlamak için tıkla", True, WHITE)
    button_rect = pygame.Rect(0, 0, 400, 100)
    button_rect.center = (width // 2, height // 2 + 100)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Eğer mouse tıklaması buton alanı içindeyse çık
                if button_rect.collidepoint(event.pos):
                    waiting = False

        screen.fill(DARKSLATEGRAY)
        # Başlık metnini ekrana ortalayarak çizelim
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 150))
        # Buton çizimi
        pygame.draw.rect(screen, (70, 70, 70), button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 3)
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                  button_rect.centery - button_text.get_height() // 2))
        pygame.display.flip()
        clock.tick(60)


def do_countdown(screen, width, height):
    """3'ten geri sayım yapar."""
    countdown_font = pygame.font.SysFont(None, 120)
    countdown_time = 3
    while countdown_time > 0:
        screen.fill(DARKSLATEGRAY)
        countdown_text = countdown_font.render(str(countdown_time), True, WHITE)
        screen.blit(countdown_text,
                    (width // 2 - countdown_text.get_width() // 2,
                     height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # 1 saniye bekle
        countdown_time -= 1


def winner_animation(screen, width, height, winner_text, duration=3000):
    """Kazanan metnini shake efektiyle gösterir."""
    font_big = pygame.font.SysFont(None, 48)
    base_text = font_big.render(winner_text, True, WHITE)
    anim_start = pygame.time.get_ticks()

    while pygame.time.get_ticks() - anim_start < duration:
        screen.fill(DARKSLATEGRAY)
        # Shake efekti: metni küçük rastgele offsetlerle çiz
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.blit(base_text,
                    (width // 2 - base_text.get_width() // 2 + offset_x,
                     height // 2 - base_text.get_height() // 2 + offset_y))
        pygame.display.flip()
        clock.tick(60)


# -----------------------------
# Başlangıç Ayarları
# -----------------------------
pygame.init()
pygame.mixer.init()  # Müzik için

# Ekran boyutları (örneğin 1024x768)
WIDTH, HEIGHT = 1024, 768

# Tam ekran modu yerine pencere modu kullanıyoruz
fullscreen = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taş Kağıt Makas Oyunu")

# Renkler
DARKSLATEGRAY = (47, 79, 79)
WHITE = (255, 255, 255)

# Oyun resimlerinin ve müzik dosyasının bulunduğu klasör
oyunresim_path = r"C:\Users\Umut\Desktop\oyunresim"

# PNG resimlerini yükle (alfa kanallı)
try:
    tas_img = pygame.image.load(os.path.join(oyunresim_path, "tas.png")).convert_alpha()
    kagit_img = pygame.image.load(os.path.join(oyunresim_path, "kagit.png")).convert_alpha()
    makas_img = pygame.image.load(os.path.join(oyunresim_path, "makas.png")).convert_alpha()
except Exception as e:
    print(
        f"PNG resimleri yüklenemedi. Lütfen '{oyunresim_path}' klasöründe 'tas.png', 'kagit.png' ve 'makas.png' dosyalarının bulunduğundan emin olun.")
    print("Hata detayı:", e)
    sys.exit()

# Resimleri yeniden boyutlandır (örneğin 20x20 piksel)
img_size = (20, 20)
tas_img = pygame.transform.scale(tas_img, img_size)
kagit_img = pygame.transform.scale(kagit_img, img_size)
makas_img = pygame.transform.scale(makas_img, img_size)

# Sınıf tiplerine göre resim eşleştirmesi
image_map = {
    "taş": tas_img,
    "kağıt": kagit_img,
    "makas": makas_img
}

# Her sınıftan kaç adet hücre olacak
NUM_PER_TYPE = 30
RADIUS = 10  # Çarpışma kontrolünde kullanılacak yarıçap

# Arka plan müziğini yükle, sesi düşür (örneğin 0.3) ve çalmaya başla
try:
    muzik_path = os.path.join(oyunresim_path, "muzik.mp3")
    pygame.mixer.music.load(muzik_path)
    pygame.mixer.music.set_volume(0.3)  # Ses seviyesi 0.0 - 1.0 arası (0.3 düşük ses)
    pygame.mixer.music.play(-1)  # Sonsuz döngüde çal
except Exception as e:
    print(f"Müzik yüklenemedi. Lütfen '{oyunresim_path}' klasöründe 'muzik.mp3' dosyasının bulunduğundan emin olun.")
    print("Hata detayı:", e)

clock = pygame.time.Clock()


# -----------------------------
# Hücre Sınıfı
# -----------------------------
class Cell:
    def __init__(self, cell_type):
        self.type = cell_type  # "taş", "kağıt", "makas"

        # Gruplu konumlandırma:
        if cell_type == "taş":
            self.x = random.uniform(WIDTH * 0.75, WIDTH - RADIUS)
            self.y = random.uniform(RADIUS, HEIGHT * 0.25)
        elif cell_type == "makas":
            self.x = random.uniform(RADIUS, WIDTH * 0.25)
            self.y = random.uniform(RADIUS, HEIGHT * 0.25)
        elif cell_type == "kağıt":
            self.x = random.uniform(WIDTH * 0.5 - 100, WIDTH * 0.5 + 100)
            self.y = random.uniform(HEIGHT * 0.75, HEIGHT - RADIUS)
        else:
            self.x = random.uniform(RADIUS, WIDTH - RADIUS)
            self.y = random.uniform(RADIUS, HEIGHT - RADIUS)

        # Hızı azaltıyoruz: 0.5 ile 1.5 arası
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x <= RADIUS or self.x >= WIDTH - RADIUS:
            self.vx = -self.vx
        if self.y <= RADIUS or self.y >= HEIGHT - RADIUS:
            self.vy = -self.vy

    def draw(self, surface):
        img = image_map[self.type]
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(img, rect)


# Tüm hücreleri oluşturuyoruz
cells = []
for cell_type in ["taş", "kağıt", "makas"]:
    for _ in range(NUM_PER_TYPE):
        cells.append(Cell(cell_type))


# İki hücrenin çarpışma kontrolü
def is_colliding(cell1, cell2):
    dx = cell1.x - cell2.x
    dy = cell1.y - cell2.y
    return math.hypot(dx, dy) < 2 * RADIUS


def get_winner(type1, type2):
    if type1 == type2:
        return type1
    if (type1 == "taş" and type2 == "makas") or \
       (type1 == "makas" and type2 == "kağıt") or \
       (type1 == "kağıt" and type2 == "taş"):
        return type1
    else:
        return type2


# -----------------------------
# Başlangıç Ekranını Göster
# -----------------------------
show_start_screen(screen, WIDTH, HEIGHT)
do_countdown(screen, WIDTH, HEIGHT)

# Oyun başladığında zamanı ölçmeye başlıyoruz
start_ticks = pygame.time.get_ticks()

# -----------------------------
# Oyun Döngüsü
# -----------------------------
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hücrelerin hareket ettirilmesi ve çarpışma kontrolü
    for cell in cells:
        cell.move()
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            if is_colliding(cells[i], cells[j]):
                winner = get_winner(cells[i].type, cells[j].type)
                cells[i].type = winner
                cells[j].type = winner

    # Tüm hücreler tek türe dönüşmüşse oyunu bitir
    current_types = [cell.type for cell in cells]
    if all(t == current_types[0] for t in current_types):
        running = False

    # Arka planı doldur
    screen.fill(DARKSLATEGRAY)

    # Hücreleri çiz
    for cell in cells:
        cell.draw(screen)

    # FPS göstergesi (sağ üstte)
    fps_text = pygame.font.SysFont(None, 24).render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    # Skor tahtası
    count_tas = sum(1 for cell in cells if cell.type == "taş")
    count_kagit = sum(1 for cell in cells if cell.type == "kağıt")
    count_makas = sum(1 for cell in cells if cell.type == "makas")
    score_text = pygame.font.SysFont(None, 24).render(
        f"Taş: {count_tas}   Kağıt: {count_kagit}   Makas: {count_makas}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Zaman sayacı
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    timer_text = pygame.font.SysFont(None, 24).render(f"Zaman: {elapsed_seconds}s", True, WHITE)
    screen.blit(timer_text, (WIDTH - 170, 10))

    pygame.display.flip()

# -----------------------------
# Oyun Bitti: Kazanan Animasyonu
# -----------------------------
winner_type = cells[0].type
winner_message = f"Oyun Bitti! Kazanan: {winner_type}"
winner_animation(screen, WIDTH, HEIGHT, winner_message, duration=3000)

pygame.time.wait(3000)
pygame.quit()
sys.exit()
