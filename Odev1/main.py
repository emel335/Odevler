import pygame
import random
import sys
from installer_logic import check_and_set_install_flag
from sprites import Player, Enemy

# --- KURULUM KONTROLÜ ---
# check_and_set_install_flag() # Testlerin için kapalı tutabilirsin

# --- BAŞLATMA ---
pygame.init()
pygame.font.init()

# --- AYARLAR ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emel - OOP Tekil Kurulum Oyunu")

# --- DURUM SABİTLERİ ---
MENU = 0
PLAYING = 1
# state değişkenini fonksiyon içinde yöneteceğiz

# --- SKOR YÖNETİCİSİ ---
class ScoreManager:
    @staticmethod
    def save_high_score(score):
        with open("data.dat", "w") as f:
            f.write(str(score))

    @staticmethod
    def load_high_score():
        try:
            with open("data.dat", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

# --- YARDIMCI FONKSİYONLAR ---
def draw_score(screen, score):
    font = pygame.font.SysFont("Arial", 32)
    score_text = font.render(f"Puan: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def show_game_over(screen):
    font = pygame.font.SysFont("Arial", 64)
    text = font.render("OYUN BİTTİ", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)

# --- ANA OYUN FONKSİYONU ---
def main():
    # Oyun Nesneleri ve Değişkenleri
    player = Player(375, 500)
    enemies = []
    clock = pygame.time.Clock()
    score = 0
    running = True
    state = MENU # Oyun menü ile başlar

    while running:
        clock.tick(60)

        # 1. OLAY KONTROLLERİ (Events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Menüdeyken Enter'a basınca oyunu başlat
                if state == MENU:
                    if event.key == pygame.K_RETURN:
                        state = PLAYING
                # Oyun içindeyken Boşluk ile ateş et
                elif state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

        # 2. EKRAN ÇİZİMİ VE OYUN MANTIĞI
        if state == MENU:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 48)
            title_text = font.render("UZAY SAVAŞI", True, (255, 255, 255))
            start_text = pygame.font.SysFont("Arial", 24).render("Başlamak için ENTER'a basın", True, (0, 255, 0))
            screen.blit(title_text, (WIDTH//2 - 140, HEIGHT//2 - 50))
            screen.blit(start_text, (WIDTH//2 - 130, HEIGHT//2 + 20))

        elif state == PLAYING:
            screen.fill((0, 0, 20)) # Koyu lacivert uzay teması

            # Oyuncu Hareketleri
            keys = pygame.key.get_pressed()
            player.move(keys, WIDTH, HEIGHT)

            # Mermileri Hareket Ettir ve Çiz
            for laser in player.lasers[:]:
                laser.move()
                laser.draw(screen)
                if laser.y < 0:
                    player.lasers.remove(laser)

            # Dinamik Zorluk (Düşman Hızlanması)
            enemy_speed = 3 + (score // 100) 

            # Düşman Oluşturma
            if len(enemies) < 5:
                enemies.append(Enemy(random.randrange(0, WIDTH-50), random.randrange(-500, -50)))

            # Düşman Hareketleri ve Çarpışma Kontrolü
            for enemy in enemies[:]:
                # Düşmanı hareket ettir (hız faktörünü ekleyerek)
                enemy._y += enemy_speed 
                enemy.draw(screen)

                # Düşman ekranın altına ulaşırsa
                if enemy._y > HEIGHT: 
                    enemies.remove(enemy)
                    player.health -= 20

                # Düşman oyuncuya çarparsa
                player_rect = pygame.Rect(player._x, player._y, 50, 50)
                enemy_rect = pygame.Rect(enemy._x, enemy._y, 50, 50)
                if player_rect.colliderect(enemy_rect):
                    if enemy in enemies: enemies.remove(enemy)
                    player.health -= 40

                # Mermi düşmana çarparsa (Çarpışma Kontrolü)
                for laser in player.lasers[:]:
                    laser_rect = pygame.Rect(laser.x, laser.y, 5, 15)
                    if laser_rect.colliderect(enemy_rect):
                        if laser in player.lasers: player.lasers.remove(laser)
                        if enemy in enemies: enemies.remove(enemy)
                        score += 10
                        break

            # Nesneleri Çiz
            player.draw(screen)
            draw_score(screen, score)

            # Oyun Bitti Kontrolü
            if player.health <= 0:
                ScoreManager.save_high_score(score) # Skoru kaydet
                show_game_over(screen)
                running = False

        # Ekranı Güncelle
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()