import os
import sys
import math
import random
import pygame
import time

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        print(1)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def blitRotate(surf, image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)


class Tank:
    def __init__(self, pos, color, player=False):
        self.main_group = pygame.sprite.Group()
        self.body = Body(self.main_group, pos=[pos[0] - 1, pos[1] - 11], col=color)
        self.tower = Tower(self.main_group, pos=pos, col=color, player=player)
        self.main_group.add(self.body)
        self.main_group.add(self.body)
        self.shells = pygame.sprite.Group()
        self.player = player
        self.angle = 0
        self.x = pos[0]
        self.y = pos[1]

    def update(self, screen, time, move):
        #self.main_group.update(screen, time)
        self.tower.rect.x = self.x - math.cos(math.radians(270 - self.angle)) * 12 + math.cos(math.radians(270 - self.angle))
        self.tower.rect.y = self.y - math.sin(math.radians(270 - self.angle)) * 12 + math.sin(math.radians(270 - self.angle))
        self.body.angle = self.angle
        self.body.rect.x = self.x
        self.body.rect.y = self.y
        self.body.update(screen, time, move)
        self.tower.update(screen, time)

        self.shells.update(screen, time)

    def shoot(self):
        self.tower.shoot(self.shells)

    def move(self, time, pos):  # pos: 1
        x = 100 * time / 1000 * math.cos(math.radians(270 - self.angle)) * pos
        y = 100 * time / 1000 * math.sin(math.radians(270 - self.angle)) * pos
        self.x += x
        self.y += y

    def rotate(self, time, angle):
        angle = angle * time * 90 / 1000
        newang = self.angle + angle
        self.angle = newang
        #self.tower.rect.x = self.x - math.cos(math.radians(270 - self.angle)) * 12 + math.sin(math.radians(self.angle))
        #self.tower.rect.y = self.y - math.sin(math.radians(270 - self.angle)) * 12 + math.cos(math.radians(self.angle))


class Body(pygame.sprite.Sprite):
    def __init__(self, *group, pos, col):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        if col == 'blue':
            self.image = load_image("body0.png", colorkey=(255, 255, 255))
            self.images = [load_image("body0.png", colorkey=(255, 255, 255)),
                      load_image("body1.png", colorkey=(255, 255, 255)),
                      load_image("body2.png", colorkey=(255, 255, 255)),
                      load_image("body3.png", colorkey=(255, 255, 255))]
            self.w, self.h = self.image.get_size()
        elif col == 'green':
            self.image = load_image("body10.png", colorkey=(255, 255, 255))
            self.images = [load_image("body10.png", colorkey=(255, 255, 255)),
                      load_image("body11.png", colorkey=(255, 255, 255)),
                      load_image("body12.png", colorkey=(255, 255, 255)),
                      load_image("body13.png", colorkey=(255, 255, 255))]
            self.w, self.h = self.image.get_size()
        #self.image = Body.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.x = -600
        self.y = 0
        self.rect.y = pos[1]
        self.mod = 0
        self.angle = 0
        self.st = time.time()
        self.rast = pos
        self.ind = 0

    def update(self, screen, time, move):
        newrast = math.sqrt((self.rast[0] - self.rect.x) ** 2 + (self.rast[1] - self.rect.y) ** 2)
        blitRotate(screen, self.image, (self.rect.x, self.rect.y), (self.w / 2, self.h / 2), self.angle)
        if newrast >= 2:
            self.rast = (self.rect.x, self.rect.y)
            self.ind += move
            self.ind %= 4
            self.image = self.images[self.ind]



class Tower(pygame.sprite.Sprite):
    def __init__(self, *group, pos, col, player):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        if col == 'blue':
            self.image = load_image("Tower.png", colorkey=(255, 255, 255))
            self.w, self.h = self.image.get_size()
        elif col == 'green':
            self.image = load_image("Tower1.png", colorkey=(255, 255, 255))
            self.w, self.h = self.image.get_size()
        self.player = player
        #self.image = Tower.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.x = -600
        self.y = 0
        self.rect.y = pos[1]
        self.mod = 0
        self.angle = 0
        self.st = time.time()

    def update(self, screen, time):
        x1, y1 = pygame.mouse.get_pos()
        if self.player:
            newang = math.degrees(math.atan2(y1 - self.rect.y, x1 - self.rect.x)) % 360
        else:
            newang = 270
        #self.angle += 0.5
        newang = 270 - newang
        if (newang - self.angle) % 360 > 180:
            self.angle -= min(135 * time / 1000, (newang - self.angle) % 360)
        elif (newang - self.angle) % 360 < 180:
            self.angle += min(135 * time / 1000, (newang - self.angle) % 360)
        pos = (self.rect.x, self.rect.y)
        originPos = (49, 12)
        blitRotate(screen, self.image, (self.rect.x, self.rect.y), (self.w / 2, self.h - 12), self.angle)
        #pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y , 100, 100))


        #pygame.draw.rect(self.image, (255, 255, 255), (512, 549, 1, 1))
        #pygame.display.flip()
    def shoot(self, group):
        if time.time() - self.st < 1.0:
            return
        self.st = time.time()
        #pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - self.w / 2, self.rect.y - self.h + 12, 100, 100))
        pos = (self.rect.x + 49 * math.cos(math.radians(270 - self.angle)), self.rect.y + 49 * math.sin(math.radians(270 - self.angle)))
        group.add(Shell(group, angle=self.angle, pos=pos))

class Shell(pygame.sprite.Sprite):
    image = load_image("shell.png", colorkey=(255, 255, 255))
    w, h = image.get_size()
    def __init__(self, *group, angle, pos):
        super().__init__(*group)
        #self.image1 = Shell.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]

        self.rect.y = pos[1]
        self.x = self.rect.x
        self.y = self.rect.y
        self.mod = 0
        self.angle = angle
        #self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self, screen, time):
        #print(time)
        blitRotate(screen, self.image, (self.rect.x, self.rect.y), (self.w / 2, self.h), self.angle)
        self.x += math.cos(math.radians(270 - self.angle)) * 600 * time / 1000
        self.y += math.sin(math.radians(270 - self.angle)) * 600 * time / 1000
        self.rect.x = self.x
        self.rect.y = self.y


tank1 = Tank((500, 500), 'green', True)

#tank2 = Tank((100, 100))
clock = pygame.time.Clock()
running = True
is_shoot = False
move = 0
rot = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                is_shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                is_shoot = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = 1
            if event.key == pygame.K_a:
                rot = 1
            if event.key == pygame.K_s:
                move = -1
            if event.key == pygame.K_d:
                rot = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move = 0
            if event.key == pygame.K_a:
                rot = 0
            if event.key == pygame.K_s:
                move = 0
            if event.key == pygame.K_d:
                rot = 0

    if is_shoot and tank1.player:
        tank1.shoot()
    screen.fill((0, 0, 0))
    yy = clock.tick()
    if tank1.player:
        tank1.move(yy, move)
        tank1.rotate(yy, rot)
    tank1.update(screen, yy, move)
    #tank2.update(screen, yy, move)
    #shells.draw(screen)
    pygame.display.flip()
