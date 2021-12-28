import math

import pygame

FPS = 60
HEIGHT = 1920
WIDTH = 1080
x0 = 500
y0 = 800
x1 = 1500
y1 = 800
COLORS = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
JUMP_SPEED = 20
ANGLE = 0

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface((70, 140))
        self.image.fill(COLORS[3])
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0
        self.jump_speed = JUMP_SPEED
        self.isJump = False
        self.angle = ANGLE
        self.scale_x = 300
        self.scale_x2 = 500
        self.scale_y = 200

    def update(self):
        self.run()
        self.jump()
        self.attack()
        self.death()
        self.crouch()

    def run(self):
        keys = pygame.key.get_pressed()
        self.movespeed = 10
        if keys[pygame.K_d] and self.rect.x < HEIGHT - 50:
            self.rect.x += self.movespeed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.movespeed
        if keys[pygame.K_SPACE]:
            self.isJump = True

    def jump(self):
        if self.isJump:
            if self.jump_speed >= -20:
                self.rect.y -= self.jump_speed
                self.jump_speed -= 1
            else:
                self.jump_speed = 20
                self.isJump = False

    def attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            pygame.draw.line(screen, COLORS[2], (self.rect.x + 50, self.rect.y + 50),
                             (self.rect.x - 300 * math.cos(self.angle),
                              self.rect.y + 300 * math.sin(self.angle)), 5)
            self.angle -= 0.3
        if not keys[pygame.K_f]:
            self.angle = 0

    def crouch(self):
        crouchkey = pygame.key.get_pressed()
        if crouchkey[pygame.K_g]:
            self.movespeed - 5
        if not crouchkey[pygame.K_g]:
            pass

    def death(self):
        global run
        pygame.draw.line(screen, COLORS[2], (self.scale_x, self.scale_y), (self.scale_x2, self.scale_y), 20)
        if self.rect.x < enemy.rect.x + 300 * math.cos(enemy.angle) \
                and self.rect.y < enemy.rect.y + 300 * math.sin(enemy.angle) and not enemy.dead:
            self.scale_x2 -= 1
            if self.scale_x2 <= self.scale_x:
                run = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.Surface((70, 140))
        self.image.fill(COLORS[-1])
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.angle = ANGLE
        self.scale_x = 1500
        self.scale_y = 200
        self.scale_x2 = 1700
        self.angle = ANGLE
        self.dead = False

    def update(self):
        self.death()
        self.run()
        self.attack()

    def death(self):
        pygame.draw.line(screen, COLORS[2], (self.scale_x, self.scale_y), (self.scale_x2, self.scale_y), 20)
        if self.rect.x < player.rect.x + 300 * math.cos(player.angle) and \
                self.rect.y < player.rect.y + 300 * math.sin(player.angle):
            self.scale_x2 -= 2
            if self.scale_x2 <= self.scale_x:
                self.kill()
                self.dead = True

    def run(self):
        if player.rect.x < self.rect.x:
            self.rect.x -= 5
        if player.rect.x > self.rect.x:
            self.rect.x += 5

    def attack(self):
        if not player.isJump:
            if self.rect.x < player.rect.x + 300 and not self.rect.x < player.rect.x:
                pygame.draw.line(screen, COLORS[2], (self.rect.x, self.rect.y),
                                 (self.rect.x + 300 * math.cos(self.angle),
                                  self.rect.y + 300 * math.sin(self.angle)), 5)
                self.angle -= 0.3
            if self.rect.x > player.rect.x - 300 and not self.rect.x > player.rect.x:
                pygame.draw.line(screen, COLORS[2], (self.rect.x, self.rect.y),
                                 (self.rect.x + 300 * math.cos(self.angle),
                                  self.rect.y + 300 * math.sin(self.angle)), 5)
                self.angle += 0.3


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
enemy = Enemy()
all_sprites.add(player)
enemies.add(enemy)


def update():
    screen.fill(COLORS[0])
    all_sprites.update()
    enemies.update()
    all_sprites.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()


run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    update()