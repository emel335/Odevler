import pygame
import random
from abc import ABC, abstractmethod

# ==========================================
# 1. ABSTRACTION (SOYUTLAMA)
# ==========================================
class GameObject(ABC):
    """
    Tüm oyun nesnelerinin (Gemi, Mermi, Güçlendirici) temelini oluşturur.
    Doğrudan bu sınıftan nesne üretilemez (Abstract).
    """
    def __init__(self, x, y):
        # ENCAPSULATION: Değişkenleri '_' ile korumalı hale getiriyoruz.
        self._x = x
        self._y = y

    @abstractmethod
    def draw(self, screen):
        """Her alt sınıf bu metodu override etmek zorundadır."""
        pass

# ==========================================
# 2. COMPOSITION (BİLEŞİM)
# ==========================================
class Laser:
    """
    Bağımsız bir sınıftır. Ship sınıfı içinde liste olarak tutularak 
    'Composition' (Bileşim) prensibini temsil eder.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -10

    def draw(self, screen):
        # Sarı mermi çizimi
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, 5, 15))

    def move(self):
        self.y += self.speed

# ==========================================
# 3. INHERITANCE (KALITIM)
# ==========================================
class Ship(GameObject):
    """GameObject'ten türetilmiştir."""
    def __init__(self, x, y, health=100):
        super().__init__(x, y) # Üst sınıfın başlangıç değerlerini al
        self.health = health
        self.lasers = []

    def shoot(self):
        """Mermi oluşturur (Composition kullanımı)."""
        new_laser = Laser(self._x + 22, self._y)
        self.lasers.append(new_laser)

# ==========================================
# 4. POLYMORPHISM (ÇOK BİÇİMLİLİK)
# ==========================================
class Player(Ship):
    """Ship sınıfının tüm özelliklerini taşır ancak hareket ve çizimi farklıdır."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 100

    def move(self, keys, width, height):
        if keys[pygame.K_LEFT] and self._x > 0:
            self._x -= 7
        if keys[pygame.K_RIGHT] and self._x < width - 50:
            self._x += 7

    def draw(self, screen):
        # Oyuncu Mavi Kare
        pygame.draw.rect(screen, (0, 100, 255), (self._x, self._y, 50, 50))
        # Dinamik Can Barı (Kapsüllenmiş verinin görsel sunumu)
        pygame.draw.rect(screen, (255, 0, 0), (self._x, self._y + 60, 50, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self._x, self._y + 60, 50 * (self.health/100), 5))

class Enemy(Ship):
    """Ship sınıfından türer ama otomatik hareket eder."""
    def move(self):
        self._y += 3

    def draw(self, screen):
        # Düşman Kırmızı Kare
        pygame.draw.rect(screen, (255, 0, 0), (self._x, self._y, 50, 50))

# ==========================================
# 5. İLERİ SEVİYE HİYERARŞİ (GÜÇLENDİRİCİLER)
# ==========================================
class PowerUp(GameObject):
    """Tüm güçlendiriciler için temel sınıf (Inheritance)."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 2

    def move(self):
        self._y += self.speed

    @abstractmethod
    def draw(self, screen):
        pass

class HealthPack(PowerUp):
    """Güçlendiricinin özel bir türü (Polymorphism)."""
    def draw(self, screen):
        # Yeşil Can Paketi
        pygame.draw.rect(screen, (0, 255, 0), (self._x, self._y, 20, 20))

    def apply(self, player):
        """Kapsüllenmiş player.health değerini günceller."""
        player.health = min(100, player.health + 20)