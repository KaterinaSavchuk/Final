from pygame import *
from random import randint
import time as pytime

# Ініціалізація
mixer.init()
font.init()

# Завантаження звуків
path_music = "assets\\sounds\\music.ogg"
shoot_sound = "assets\\sounds\\shot.ogg"
mixer.music.load(path_music)
mixer.music.play(-1)  # Зациклення музики
fire_sound = mixer.Sound(shoot_sound)

# Шрифти
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

# Тексти
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

# Завантаження зображень
img_back = "assets\\pictures\\sky.png"
img_hero = "assets\\pictures\\plane.png"
img_bullet = "assets\\pictures\\bullet.png"
img_enemy = "assets\\pictures\\ufo.png"

# Налаштування вікна
win_width = 700
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
clock = time.Clock()
FPS = 60
score = 0
goal = 50
lost = 0
max_lost = 3
life = 3
bullet_count = 10
reload_start_time = None

# Клас спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        global bullet_count
        if bullet_count > 0:
            bullet_count -= 1
            fire_sound.play()
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost += 1

# Створення об'єктів
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

finish = False
run = True
# Рівні гри
level = input ("Оберіть рівень (від 1 до 3)")
if level == 1:

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if bullet_count > 0 and reload_start_time is None:
                ship.fire()
            elif bullet_count == 0 and reload_start_time is None:
                reload_start_time = pytime.time()

    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        
        # Відображення рахунку
        window.blit(font2.render(f"Рахунок: {score}", 1, (255, 255, 255)), (10, 20))
        window.blit(font2.render(f"Пропущено: {lost}", 1, (255, 255, 255)), (10, 50))
        window.blit(font1.render(str(life), 1, (255, 0, 0)), (650, 10))

        # Перевірка перезарядки
        if reload_start_time and pytime.time() - reload_start_time > 3:
            bullet_count = 10
            reload_start_time = None
        
        # Перевірка зіткнень
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for _ in collides:
            score += 1
            monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3)))
        
        if sprite.spritecollide(ship, monsters, True):
            life -= 1
            monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3)))
        
        # Умови завершення гри
        if life == 0 or lost >= max_lost:
            finish = True
            mixer.music.stop()
            window.blit(lose, (200, 200))
        elif score >= goal:
            finish = True
            mixer.music.stop()
            window.blit(win, (200, 200))
    
    display.update()
    clock.tick(FPS)
