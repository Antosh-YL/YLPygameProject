import pygame
import os

FPS = 60
HEIGHT = 1200
WIDTH = 700
x0 = 300
y0 = 300
COLORS = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
JUMP_SPEED = 20
MOVE_SPEED = 5
# задал скорость передвижения как глобальную переменную для удобства в обработке
ANGLE = 0
ANIM_COUNT = 0

pygame.init()

screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()

sprites = {}
for folder in ['jump', 'run_right', 'static', 'p2static', 'p2run_right', 'p2jump', 'crouch', 'p2crouch']:
    sprites[folder] = []
    for picture in os.listdir(folder):
        sprites[folder].append(pygame.image.load(folder + '/' + picture))

sprites_inverted = {}
for folder in sprites:
    sprites_inverted[folder] = []
    for sprite in sprites[folder]:
        sprites_inverted[folder].append(pygame.transform.flip(sprite, True, False))

background_img = pygame.image.load('background.png')

inverted = False


def select_sprite(plr, folder, index):
    if inverted:
        if plr == 1:
            return sprites_inverted[folder][index]
        else:
            return sprites[folder][index]
    else:
        if plr == 1:
            return sprites[folder][index]
        else:
            return sprites_inverted[folder][index]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = select_sprite(1, "static", 0)
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0
        self.jump_speed = JUMP_SPEED
        self.move_speed = MOVE_SPEED
        self.isJump = False
        self.crouches = False
        self.punches = False  # проверка на удар подобная прыжку и бегу
        self.run = False
        self.angle = ANGLE
        self.scale_x = 300
        self.scale_y = 200
        self.anim_count = ANIM_COUNT

    def update(self):
        self.running()
        self.crouch()
        self.jump()
        self.anim()

    def running(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.crouches = True
            self.run = False
            return
        if keys[pygame.K_d] and self.rect.x < (HEIGHT - 50):
            self.run = True
            self.rect.x += self.move_speed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.run = True
            self.rect.x -= self.move_speed
        if keys[pygame.K_w]:
            self.isJump = True
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.run = False
        if keys[pygame.K_d] and keys[pygame.K_a]:
            self.run = False
        self.crouches = False

    def crouch(self):
        if self.crouches:
            self.move_speed = 0
        else:
            self.move_speed = 5

    def jump(self):
        if self.isJump:
            if self.jump_speed >= -20:
                self.rect.y -= self.jump_speed
                self.jump_speed -= 1
                self.move_speed = 3
            else:
                self.jump_speed = 20
                self.isJump = False
                self.move_speed = 5

    def punch(self):
        pass

    # без комментариев
    def anim(self):
        if self.anim_count >= 60:
            self.anim_count = 0
        if not self.isJump and not self.run:
            self.image = select_sprite(1, "static", self.anim_count // 15)
            self.anim_count += 1
        if self.isJump and self.run:
            self.image = select_sprite(1, "jump", self.anim_count // 15)
            self.anim_count += 1
        elif self.run:
            self.image = select_sprite(1, "run_right", self.anim_count // 15)
            self.anim_count += 2
        elif self.isJump:
            self.run = False
            self.image = select_sprite(1, "jump", self.anim_count // 15)
            self.anim_count += 1
        if self.crouches:
            self.run = False
            self.image = select_sprite(1, 'crouch', self.anim_count // 60)
            self.anim_count += 1


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.image = select_sprite(2, "p2static", 0)
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0
        self.jump_speed = JUMP_SPEED
        self.move_speed = MOVE_SPEED
        self.isJump = False
        self.punches = False
        self.run = False
        self.crouches = False
        self.angle = ANGLE
        self.scale_x = 300
        self.scale_y = 200
        self.anim_count = ANIM_COUNT

    def update(self):
        self.running()
        self.jump()
        self.anim()
        self

    def running(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.crouches = True
            self.run = False
            return
        if keys[pygame.K_RIGHT] and self.rect.x < HEIGHT - 50:
            self.run = True
            self.rect.x += self.move_speed
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.run = True
            self.rect.x -= self.move_speed
        if keys[pygame.K_UP]:
            self.isJump = True
        if keys[pygame.K_KP5]:
            self.punches = True
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.run = False


    def jump(self):
        if self.isJump:
            if self.jump_speed >= -20:
                self.rect.y -= self.jump_speed
                self.jump_speed -= 1
                self.move_speed = 3
            else:
                self.jump_speed = 20
                self.isJump = False
                self.move_speed = 5

    def crouch(self):
        if self.crouches:
            self.move_speed = 0
        else:
            self.move_speed = 5

    def punch(self):
        pass

    def anim(self):
        if self.anim_count >= 60:
            self.anim_count = 0
        if not self.isJump and not self.run:
            self.image = select_sprite(2, "p2static", self.anim_count // 15)
            self.anim_count += 1
        if self.isJump and self.run:
            self.image = select_sprite(2, "p2jump", self.anim_count // 15)
            self.anim_count += 1
        elif self.run:
            self.image = select_sprite(2, "p2run_right", self.anim_count // 15)
            self.anim_count += 2
        elif self.isJump:
            self.run = False
            self.image = select_sprite(2, "p2jump", self.anim_count // 15)
            self.anim_count += 1
        if self.crouches:
            self.run = False
            self.image = select_sprite(1, 'crouch', self.anim_count // 60)
            self.anim_count += 1


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
player2 = Player2()
all_sprites.add(player, player2)


def update():
    global inverted
    screen.blit(background_img, (0, 0))
    all_sprites.update()
    enemies.update()
    all_sprites.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()
    diff = player2.rect.x - player.rect.x
    inverted = diff < 0


run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    update()