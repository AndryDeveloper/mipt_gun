import math
from random import randint, random

import pygame

FPS = 60

N_TARGETS = 2
N_BOMBS = 5
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA]

WIDTH = 800
HEIGHT = 600


class Ball(pygame.sprite.Sprite):
    def __init__(self, position, speed, color, size=50):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, color, (self.size // 2, self.size // 2), self.size // 2)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])
        self.speed = speed
        self.k = -0.6
        self.a = 0.1
        self.live = 1000

    def update(self):
        self.live -= 1
        if self.live <= 0:
            self.kill()

        self.speed[1] += self.a

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.speed[0] *= self.k
            self.speed[1] *= abs(self.k)
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed[0] *= self.k
            self.speed[1] *= abs(self.k)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed[0] *= abs(self.k)
            self.speed[1] *= self.k
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed[0] *= abs(self.k)
            self.speed[1] *= self.k


class Gun1(pygame.sprite.Sprite):
    def __init__(self, size=70):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.angle = math.pi / 2
        self.image = pygame.Surface((self.size, self.size))
        self.draw_gun()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - self.size // 2, HEIGHT - self.size // 2)
        self.speed = 0
        self.ax = 5
        self.min_force = 1
        self.max_force = 50
        self.force_speed = 1
        self.on_pressed = False
        self.angle_force = math.pi / 100
        self.force = self.min_force

    def draw_gun(self):
        self.image.fill(BLACK)
        pygame.draw.line(self.image, MAGENTA,
                         (self.size // 2, self.size - self.size // 4),
                         (self.size / 2 * (1 - math.cos(self.angle)),
                          3*self.size/4 - self.size / 2 * math.sin(self.angle)),
                         self.size // 4)
        pygame.draw.circle(self.image, CYAN, (self.size - self.size // 4, self.size - self.size // 4), self.size // 4)
        pygame.draw.circle(self.image, CYAN, (self.size // 4, self.size - self.size // 4), self.size // 4)

        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.speed = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed = -self.ax
        if key_state[pygame.K_RIGHT]:
            self.speed = self.ax
        if key_state[pygame.K_RCTRL]:
            self.on_pressed = True
            self.force = min(self.max_force, self.force + self.force_speed)
        else:
            if self.on_pressed:
                self.on_pressed = False
                size = (randint(0, 1) / 2 + 0.5) * 50
                ball_speed = [-math.cos(self.angle) * self.force / size * 50,
                              -math.sin(self.angle) * self.force / size * 50]
                ball_center = [self.rect.x, self.rect.y]
                ball_center[0] += self.size / 2 * (1 - math.cos(self.angle))
                ball_center[1] += 3*self.size/4 - self.size / 2 * math.sin(self.angle)
                balls_sprites_1.add(Ball(ball_center, ball_speed, YELLOW, size=size))
                self.force = self.min_force
        if key_state[pygame.K_UP]:
            self.angle = min(math.pi, (self.angle + self.angle_force) % (2 * math.pi))
            self.draw_gun()
        if key_state[pygame.K_DOWN]:
            if math.pi < (self.angle - self.angle_force) % (2 * math.pi):
                self.angle = 0
            else:
                self.angle = (self.angle - self.angle_force) % (2 * math.pi)
            self.draw_gun()

        self.rect.x += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Gun2(pygame.sprite.Sprite):
    def __init__(self, size=70):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.angle = math.pi / 2
        self.image = pygame.Surface((self.size, self.size))
        self.draw_gun()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.size // 2, HEIGHT - self.size // 2)
        self.speed = 0
        self.ax = 5
        self.min_force = 1
        self.max_force = 50
        self.force_speed = 1
        self.on_pressed = False
        self.angle_force = math.pi / 100
        self.force = self.min_force

    def draw_gun(self):
        self.image.fill(BLACK)
        pygame.draw.line(self.image, CYAN,
                         (self.size // 2, self.size - self.size // 4),
                         (self.size / 2 * (1 - math.cos(self.angle)),
                          3*self.size/4 - self.size / 2 * math.sin(self.angle)),
                         self.size // 4)
        pygame.draw.circle(self.image, MAGENTA, (self.size - self.size // 4, self.size - self.size // 4), self.size // 4)
        pygame.draw.circle(self.image, MAGENTA, (self.size // 4, self.size - self.size // 4), self.size // 4)

        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.speed = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.speed = -self.ax
        if key_state[pygame.K_d]:
            self.speed = self.ax
        if key_state[pygame.K_SPACE]:
            self.on_pressed = True
            self.force = min(self.max_force, self.force + self.force_speed)
        else:
            if self.on_pressed:
                self.on_pressed = False
                size = (randint(0, 1) / 2 + 0.5) * 50
                ball_speed = [-math.cos(self.angle) * self.force / size * 50,
                              -math.sin(self.angle) * self.force / size * 50]
                ball_center = [self.rect.x, self.rect.y]
                ball_center[0] += self.size / 2 * (1 - math.cos(self.angle))
                ball_center[1] += 3*self.size/4 - self.size / 2 * math.sin(self.angle)
                balls_sprites_2.add(Ball(ball_center, ball_speed, GREY, size=size))
                self.force = self.min_force
        if key_state[pygame.K_w]:
            self.angle = min(math.pi, (self.angle + self.angle_force) % (2 * math.pi))
            self.draw_gun()
        if key_state[pygame.K_s]:
            if math.pi < (self.angle - self.angle_force) % (2 * math.pi):
                self.angle = 0
            else:
                self.angle = (self.angle - self.angle_force) % (2 * math.pi)
            self.draw_gun()

        self.rect.x += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Bomb(pygame.sprite.Sprite):
    def __init__(self, minsize=10, maxsize=80, speed=1):
        pygame.sprite.Sprite.__init__(self)
        self.size = randint(minsize, maxsize)
        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, RED, (self.size // 2, self.size // 2), self.size // 2)
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(self.size, WIDTH - self.size), -self.size // 2)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.kill()


class Target(pygame.sprite.Sprite):
    def __init__(self, minsize=10, maxsize=80):
        pygame.sprite.Sprite.__init__(self)
        self.size = randint(minsize, maxsize)
        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, BLUE, (self.size // 2, self.size // 2), self.size // 2)
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(self.size, WIDTH - self.size), randint(self.size, HEIGHT - self.size))
        self.speed = [0, 0]
        self.force = 50 / self.size
        self.k = -0.6

    def update(self):
        self.speed[0] += (random() - 0.5) * self.force
        self.speed[1] += (random() - 0.5) * self.force

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.speed[0] *= self.k
            self.speed[1] *= abs(self.k)
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed[0] *= self.k
            self.speed[1] *= abs(self.k)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed[0] *= abs(self.k)
            self.speed[1] *= self.k
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed[0] *= abs(self.k)
            self.speed[1] *= self.k


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gun")
clock = pygame.time.Clock()

guns_sprites = pygame.sprite.Group()
balls_sprites_1 = pygame.sprite.Group()
balls_sprites_2 = pygame.sprite.Group()
targets_sprites = pygame.sprite.Group()
boms_sprites = pygame.sprite.Group()
for _ in range(N_TARGETS):
    targets_sprites.add(Target())

for _ in range(N_BOMBS):
    boms_sprites.add(Bomb(speed=(random() + 0.5) * 3))

gun1 = Gun1()
gun2 = Gun2()
guns_sprites.add(gun1)
guns_sprites.add(gun2)

running = True
while running:
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    balls_sprites_1.update()
    balls_sprites_2.update()
    guns_sprites.update()
    targets_sprites.update()
    boms_sprites.update()
    if pygame.sprite.spritecollideany(gun1, boms_sprites, collided=pygame.sprite.collide_mask):
        gun1.kill()
        gun1 = Gun1()
        guns_sprites.add(gun1)
    if pygame.sprite.spritecollideany(gun2, boms_sprites, collided=pygame.sprite.collide_mask):
        gun2.kill()
        gun2 = Gun2()
        guns_sprites.add(gun2)
    if pygame.sprite.spritecollide(gun1, balls_sprites_2, True, collided=pygame.sprite.collide_mask):
        gun1.kill()
        gun1 = Gun1()
        guns_sprites.add(gun1)
    if pygame.sprite.spritecollide(gun2, balls_sprites_1, True, collided=pygame.sprite.collide_mask):
        gun2.kill()
        gun2 = Gun2()
        guns_sprites.add(gun2)
    pygame.sprite.groupcollide(targets_sprites, balls_sprites_1, True, True, collided=pygame.sprite.collide_mask)
    pygame.sprite.groupcollide(targets_sprites, balls_sprites_2, True, True, collided=pygame.sprite.collide_mask)

    while len(targets_sprites) < N_TARGETS:
        targets_sprites.add(Target())

    while len(boms_sprites) < N_BOMBS:
        boms_sprites.add(Bomb(speed=(random() + 0.5) * 3))

    # Рендеринг
    screen.fill(WHITE)
    balls_sprites_1.draw(screen)
    balls_sprites_2.draw(screen)
    targets_sprites.draw(screen)
    boms_sprites.draw(screen)
    guns_sprites.draw(screen)

    pygame.display.flip()
