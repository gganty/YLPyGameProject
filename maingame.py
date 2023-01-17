import os
import sys
import math
import random
import pygame
import time
import pytmx
import socket

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
mode = int(input("CHOOSE MODE (1 - Host; 2 - Connect): "))
if mode == 1:
    server_socket = socket.socket()
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    conn, address = server_socket.accept()
else:
    host, port = 'localhost', 5000
    conn = socket.socket()
    conn.connect((host, port))
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
SHOOT_TIME = 1.0
glag = 1
# exec(open('classes.py').read())
SETTINGS = False


def rast(tup1, tup2):
    return math.sqrt((tup1[0] - tup2[0]) ** 2 + (tup1[1] - tup2[1]) ** 2)


def HealthBar(center, hp):
    n = 70
    yy = 7
    x, y = center[0] - 100, center[1] - n // 5
    x1 = n * hp // 100
    pygame.draw.rect(screen, (255, 0, 0), (x, y, n, yy))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, x1, yy))


def moncol(col):
    global glag
    # qqqqqqqqq
    running = True
    st = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glag = 1
                    return
        if col == 1:
            screen.fill((255, 0, 0))
        elif col == 2:
            screen.fill((0, 0, 255))
        else:
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        if time.time() - st > 1:
            glag = 1
            return
        pygame.display.flip()


def AI(tank):
    # scr1 = pygame.surface.Surface(100, 100)
    newang = math.degrees(math.atan2(0 - tank.y, 0 - tank.x)) % 360
    # self.angle += 0.5
    # return 0, 0, False
    newang = 270 - newang
    # rot = 0
    # ang = tank.angle
    # if (newang - ang) % 360 > 180:
    #     rot = -1
    # elif (newang - ang) % 360 < 180:
    #     rot = 1
    return 0, 0, True


def main_game():
    global glag, SHOOT_TIME, tanks, group, maps
    tanks = []
    group = pygame.sprite.Group()
    tanks.append(Tank(group, (900, 600), 'blue', True))
    tanks.append(Tank(group, (100, 100), 'red', False))
    tanks.append(Tank(group, (900, 100), 'green', False))
    tanks.append(Tank(group, (100, 600), 'yellow', False))
    maps = Map()
    clock = pygame.time.Clock()
    running = True
    is_shoot = False
    move = 0
    rot = 0
    rot1 = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
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
                if event.key == pygame.K_F1:
                    SHOOT_TIME -= 1
                    SHOOT_TIME = abs(SHOOT_TIME)
                if event.key == pygame.K_ESCAPE:
                    glag = 1
                    return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move = 0
                if event.key == pygame.K_a:
                    rot = 0
                if event.key == pygame.K_s:
                    move = 0
                if event.key == pygame.K_d:
                    rot = 0

        yy = clock.tick()
        screen.fill((0, 0, 0))
        maps.group.draw(screen)
        group.draw(screen)
        for tank1 in tanks:
            if is_shoot and tank1.player:
                tank1.shoot()

            if tank1.player:
                tank1.move(yy, move)
                tank1.rotate(yy, rot)
            tank1.update(screen, yy, move)

            if not tank1.player:
                mov1, ro1, is_shoot1 = AI(tank1)
                tank1.move(yy, mov1)
                tank1.rotate(yy, rot1)
                if is_shoot1:
                    tank1.shoot()
            if tank1.player:
                pass
        sd = []
        for i in tanks:
            if i.hp <= 0:
                group.remove(i.body)
                group.remove(i.tower)
            else:
                sd.append(i)
        tanks = sd
        pygame.display.flip()


def start_double():
    global glag, SHOOT_TIME, tanks, group, maps, SETTINGS
    running = True
    tanks = []
    clock = pygame.time.Clock()
    group = pygame.sprite.Group()
    if mode == 1:
        tanks.append(Tank(group, (900, 600), 'blue', True, is_rotate=False, controlled=True))
        tanks.append(Tank(group, (100, 100), 'red', True, is_rotate=False, controlled=False))
    else:
        tanks.append(Tank(group, (900, 600), 'blue', True, is_rotate=False, controlled=False))
        tanks.append(Tank(group, (100, 100), 'red', True, is_rotate=False, controlled=True))
    moves = []
    move = 0
    rot = 0
    move1 = 0
    rot1 = 0
    is_shoot = False
    is_shoot1 = False
    while running:
        a = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == pygame.BUTTON_LEFT:
            #         is_shoot = True
            # if event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == pygame.BUTTON_LEFT:
            #         is_shoot = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and mode == 1:
                    move = 1
                    a.append("K_w|d")
                if event.key == pygame.K_a and mode == 1:
                    rot = 1
                    a.append("K_a|d")
                if event.key == pygame.K_s and mode == 1:
                    move = -1
                    a.append("K_s|d")
                if event.key == pygame.K_d and mode == 1:
                    rot = -1
                    a.append("K_d|d")
                if event.key == pygame.K_UP and mode == 2:
                    move1 = 1
                    a.append("K_UP|d")
                if event.key == pygame.K_LEFT and mode == 2:
                    rot1 = 1
                    a.append("K_LEFT|d")
                if event.key == pygame.K_DOWN and mode == 2:
                    move1 = -1
                    a.append("K_DOWN|d")
                if event.key == pygame.K_RIGHT and mode == 2:
                    rot1 = -1
                    a.append("K_RIGHT|d")
                if event.key == pygame.K_q and mode == 1:
                    is_shoot = True
                    a.append("K_q|d")
                if event.key == pygame.K_m and mode == 2:
                    is_shoot1 = True
                    a.append("K_m|d")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w and mode == 1:
                    move = 0
                    a.append("K_w|u")
                if event.key == pygame.K_a and mode == 1:
                    rot = 0
                    a.append("K_a|u")
                if event.key == pygame.K_s and mode == 1:
                    move = 0
                    a.append("K_s|u")
                if event.key == pygame.K_d and mode == 1:
                    rot = 0
                    a.append("K_d|u")
                if event.key == pygame.K_UP and mode == 2:
                    move1 = 0
                    a.append("K_UP|u")
                if event.key == pygame.K_LEFT and mode == 2:
                    rot1 = 0
                    a.append("K_LEFT|u")
                if event.key == pygame.K_DOWN and mode == 2:
                    move1 = 0
                    a.append("K_DOWN|u")
                if event.key == pygame.K_RIGHT and mode == 2:
                    rot1 = 0
                    a.append("K_RIGHT|u")
                if event.key == pygame.K_q and mode == 1:
                    is_shoot = False
                    a.append("K_q|u")
                if event.key == pygame.K_m and mode == 2:
                    is_shoot1 = False
                    a.append("K_m|u")
        a = ';;'.join(a + list(map(str, list(pygame.mouse.get_pos()))))
        print(a)
        conn.send(a.encode())
        data = conn.recv(1024).decode().split(';;')
        coordinates = tuple(data[-2:])
        data = data[:-2]
        if mode == 1:
            c1, c2 = pygame.mouse.get_pos(), tuple(coordinates)
        else:
            c2, c1 = pygame.mouse.get_pos(), tuple(coordinates)
        for event in data:
            if event == 'K_w|d' and mode == 2:
                move = 1
            if event == 'K_a|d' and mode == 2:
                rot = 1
            if event == 'K_s|d' and mode == 2:
                move = -1
            if event == 'K_d|d' and mode == 2:
                rot = -1
            if event == 'K_q|d' and mode == 2:
                is_shoot = True
            if event == 'K_UP|d' and mode == 1:
                move1 = 1
            if event == 'K_LEFT|d' and mode == 1:
                rot1 = 1
            if event == 'K_DOWN|d' and mode == 1:
                move1 = -1
            if event == 'K_RIGHT|d' and mode == 1:
                rot1 = -1
            if event == 'K_m|d' and mode == 1:
                is_shoot1 = True
            if event == 'K_w|u' and mode == 2:
                move = 0
            if event == 'K_a|u' and mode == 2:
                rot = 0
            if event == 'K_s|u' and mode == 2:
                move = 0
            if event == 'K_d|u' and mode == 2:
                rot = 0
            if event == 'K_q|u' and mode == 2:
                is_shoot = False
            if event == 'K_UP|u' and mode == 1:
                move1 = 0
            if event == 'K_LEFT|u' and mode == 1:
                rot1 = 0
            if event == 'K_DOWN|u' and mode == 1:
                move1 = 0
            if event == 'K_RIGHT|u' and mode == 1:
                rot1 = 0
            if event == 'K_m|u' and mode == 1:
                is_shoot1 = False
        yy = clock.tick()
        moves = [(move, rot, is_shoot, c1), (move1, rot1, is_shoot1, c2)]
        screen.fill((0, 0, 0))
        maps.group.draw(screen)
        group.draw(screen)
        for tank1 in tanks:
            move2, rot2, is_shoot2, m_coords = moves.pop(0)
            if is_shoot2 and tank1.player or not tank1.player:
                tank1.shoot()

            if tank1.player:
                tank1.move(yy, move2)
                tank1.rotate(yy, rot2)
            tank1.update(screen, yy, move2, coords=m_coords)
            if tank1.player:
                pass
        if tanks[0].hp <= 0 and tanks[1].hp <= 0:
            SETTINGS = 0
            glag = 3
            return
        elif tanks[0].hp <= 0:
            SETTINGS = 1
            glag = 3
            return
        elif tanks[1].hp <= 0:
            SETTINGS = 2
            glag = 3
            return
        pygame.display.set_caption(f'{SETTINGS}')
        pygame.display.flip()


def start_screen():
    global glag
    start = load_image("start.png")
    running = True
    tank = load_image('tank0.png', colorkey=(255, 255, 255))
    s = [(310, 360), (310, 465), (310, 570)]
    ind = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    ind -= 1
                if event.key == pygame.K_s:
                    ind += 1
                if event.key == pygame.K_RETURN:
                    if ind == 0:
                        print(1)
                        glag = 0
                        return
                    if ind == 1:
                        glag = 2
                        return
        ind %= 3
        screen.blit(start, (0, 0))
        screen.blit(tank, s[ind])
        pygame.display.flip()


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
    # surf.blit(rotated_image, rotated_image_rect)
    # rotated_image.rect = rotated_image_rect
    # pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)
    return rotated_image, rotated_image_center


class Tile(pygame.sprite.Sprite):
    def __init__(self, *group, image, id, x, y, size):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * size
        self.rect.y = y * size
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.id = id
        self.size = size


class Map:
    def __init__(self):
        self.map = pytmx.load_pygame('tmx/simple_map.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.group = pygame.sprite.Group()
        for i in range(self.width):
            for j in range(self.height):
                image = self.map.get_tile_image(i, j, 0)
                self.group.add(
                    Tile(self.group, image=image, id=self.map.get_tile_gid(i, j, 0), x=i, y=j, size=self.tile_size))


class Tank:
    def __init__(self, group, pos, color, player=False, is_rotate=True, controlled=True):
        self.main_group = group
        self.body = Body(self.main_group, tank=self, pos=[pos[0] - 1, pos[1] - 11], col=color)
        self.tower = Tower(self.main_group, tank=self, pos=pos, col=color, player=player, is_rotate=is_rotate,
                           controlled=controlled)
        self.main_group.add(self.body)
        self.main_group.add(self.tower)
        self.shells = pygame.sprite.Group()
        self.hp = 100
        self.player = player
        self.angle = 0
        self.x = pos[0]
        self.color = color
        self.y = pos[1]

    def update(self, screen, time, move, coords=None):
        if self.hp <= 0:
            return
        self.tower.rect.x = self.x - math.cos(math.radians(270 - self.angle)) * 12
        self.tower.rect.y = self.y - math.sin(math.radians(270 - self.angle)) * 12
        self.body.angle = self.angle
        self.body.rect.x = self.x
        self.body.rect.y = self.y
        self.body.update(screen, time, move)
        self.tower.update(screen, time, coords=coords)
        self.last = 0

        self.shells.update(screen, time)
        self.shells.draw(screen)
        # HealthBar((self.x, self.y), self.hp)

    def shoot(self):
        self.tower.shoot(self.shells)

    def move(self, time, pos):  # pos: 1
        # tanks.remove(self)
        x = 100 * time / 1000 * math.cos(math.radians(270 - self.angle)) * pos
        y = 100 * time / 1000 * math.sin(math.radians(270 - self.angle)) * pos
        s = pygame.sprite.spritecollide(self.body, self.main_group, False)
        ifx = True
        ify = True
        s1 = []
        for i in s:
            if i.tank != self:
                offset = (-(self.body.rect.x - i.rect.x), -(self.body.rect.y - i.rect.y))

                # pygame.draw.rect(screen, (255, 255, 0), i.rect, 2)
                offsetx = (offset[0] - x, offset[1])
                offsety = (offset[0], offset[1] - y)

                dx = self.body.mask.overlap_area(i.mask, offset=offset)
                dx1 = self.body.mask.overlap_area(i.mask, offset=offsetx)
                dx2 = self.body.mask.overlap_area(i.mask, offset=offsety)
                if dx < dx1:
                    ifx = False
                if dx < dx2:
                    ify = False
                s1.append(dx)

        s = pygame.sprite.spritecollide(self.body, maps.group, False)
        for i in s:
            if i.id == 2:
                offset = (-(self.body.rect.x - i.rect.x), -(self.body.rect.y - i.rect.y))

                # pygame.draw.rect(screen, (255, 255, 0), i.rect, 2)
                offsetx = (offset[0] - x, offset[1])
                offsety = (offset[0], offset[1] - y)

                dx = self.body.mask.overlap_area(i.mask, offset=offset)
                dx1 = self.body.mask.overlap_area(i.mask, offset=offsetx)
                dx2 = self.body.mask.overlap_area(i.mask, offset=offsety)
                if dx < dx1:
                    ifx = False
                if dx < dx2:
                    ify = False
                s1.append(dx)
        s = pygame.sprite.spritecollide(self.tower, maps.group, False)
        for i in s:
            if i.id == 2:
                offset = (-(self.tower.rect.x - i.rect.x), -(self.tower.rect.y - i.rect.y))

                # pygame.draw.rect(screen, (255, 255, 0), i.rect, 2)
                offsetx = (offset[0] - x, offset[1])
                offsety = (offset[0], offset[1] - y)

                dx = self.tower.mask.overlap_area(i.mask, offset=offset)
                dx1 = self.tower.mask.overlap_area(i.mask, offset=offsetx)
                dx2 = self.tower.mask.overlap_area(i.mask, offset=offsety)
                if dx < dx1:
                    ifx = False
                if dx < dx2:
                    ify = False
                s1.append(dx)

        if (self.body.rect.x + x < 0 and self.body.rect.x > self.body.rect.x + x) or (
                self.body.rect.bottomright[0] + x > 1000 and self.body.rect.x < self.body.rect.x + x):
            ifx = False

        if (self.body.rect.y + y < 0 and self.body.rect.y > self.body.rect.y + y) or (
                self.body.rect.bottomright[1] + y > 1000 and self.body.rect.y < self.body.rect.y + y):
            ify = False
        if ifx:
            self.x += x
        if ify:
            self.y += y

    def rotate(self, time, angle):
        angle = angle * time * 90 / 1000
        newang = self.angle + angle
        pipa = blitRotate(screen, self.body.original_image, (self.body.rect.x, self.body.rect.y),
                          (self.body.w / 2, self.body.h / 2), self.angle)
        newimage = pipa[0]
        newrect = newimage.get_rect(center=(self.x, self.y))
        newmask = pygame.mask.from_surface(newimage)
        oldrect = self.body.rect
        # self.angle = newang
        # self.body.update(screen, 0, 0)
        s = pygame.sprite.spritecollide(self.body, self.main_group, False)

        glag = True
        s1 = []
        for i in s:
            if i.tank != self:
                offsetnew = ((-(newrect.x - i.rect.x), -(newrect.y - i.rect.y)))
                offset = (-(self.body.rect.x - i.rect.x), -(self.body.rect.y - i.rect.y))
                dx = newmask.overlap_area(i.mask, offset=offsetnew)
                # pygame.display.set_caption(f'{dx}, {self.body.mask.overlap_area(i.mask, offset=offset)}')
                if self.body.mask.overlap_area(i.mask, offset=offset) != 0:
                    # pygame.display.set_caption(f'{self.body.mask.overlap_area(i.mask, offset=offset)}, {oldmask.overlap_area(oldmask, offset=offsetold)}')
                    glag = False
                    break

        s = pygame.sprite.spritecollide(self.body, maps.group, False)

        s1 = []
        for i in s:
            if i.id == 2:
                offsetnew = (-(newrect.x - i.rect.x), -(newrect.y - i.rect.y))
                offset = (-(self.body.rect.x - i.rect.x), -(self.body.rect.y - i.rect.y))
                dx = newmask.overlap_area(i.mask, offset=offsetnew)
                # pygame.display.set_caption(f'{dx}, {self.body.mask.overlap_area(i.mask, offset=offset)}')
                # pygame.draw.polygon(screen, (0, 255, 0),
                #                     list(map(lambda x: (x[0] + 100, x[1] + 100), newmask.outline(every=1))))
                # pygame.draw.polygon(screen, (0, 255, 0),
                #                     list(map(lambda x: (x[0] + 100 + offsetnew[0], x[1] + 100 + offsetnew[1]),
                #                              i.mask.outline(every=1))))
                # pygame.draw.rect(screen, (255, 0, 0), newrect, 2)
                if self.body.mask.overlap_area(i.mask, offset=offset) != 0:
                    # pygame.display.set_caption(f'{self.body.mask.overlap_area(i.mask, offset=offset)}, {oldmask.overlap_area(oldmask, offset=offsetold)}')
                    glag = False
                    break
        if glag:
            self.angle = newang
        self.body.update(screen, 0, 0)


class Body(pygame.sprite.Sprite):
    def __init__(self, *group, tank, pos, col):
        super().__init__(*group)
        self.tank = tank
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
        elif col == 'red':
            self.image = load_image("body20.png", colorkey=(255, 255, 255))
            self.images = [load_image("body20.png", colorkey=(255, 255, 255)),
                           load_image("body21.png", colorkey=(255, 255, 255)),
                           load_image("body22.png", colorkey=(255, 255, 255)),
                           load_image("body23.png", colorkey=(255, 255, 255))]
            self.w, self.h = self.image.get_size()
        elif col == 'yellow':
            self.image = load_image("body30.png", colorkey=(255, 255, 255))
            self.images = [load_image("body30.png", colorkey=(255, 255, 255)),
                           load_image("body31.png", colorkey=(255, 255, 255)),
                           load_image("body32.png", colorkey=(255, 255, 255)),
                           load_image("body33.png", colorkey=(255, 255, 255))]
            self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.original_image = self.image
        self.x = -600
        self.y = 0
        self.rect.y = pos[1]
        self.mod = 0
        self.angle = 0
        self.st = time.time()
        self.rast = pos
        self.ind = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, screen, time, move):
        newrast = math.sqrt((self.rast[0] - self.rect.x) ** 2 + (self.rast[1] - self.rect.y) ** 2)
        pipa = blitRotate(screen, self.original_image, (self.rect.x, self.rect.y), (self.w / 2, self.h / 2), self.angle)
        self.image = pipa[0]
        self.rect = self.image.get_rect(center=pipa[1])
        if pygame.sprite.spritecollideany(self, maps.group):
            s = pygame.sprite.spritecollide(self, maps.group, False)
            for i in s:
                if i.id == 2:
                    pass
        self.mask = pygame.mask.from_surface(self.image)
        if newrast >= 2 and self.tank.player:
            self.rast = (self.rect.x, self.rect.y)
            self.ind += move
            self.ind %= 4
            self.original_image = self.images[self.ind]
        self.mask = pygame.mask.from_surface(self.image)


class Tower(pygame.sprite.Sprite):
    def __init__(self, *group, tank, pos, col, player, is_rotate=True, controlled=True):
        super().__init__(*group)
        self.tank = tank
        if col == 'blue':
            self.image = load_image("Tower.png", colorkey=(255, 255, 255))
            self.w, self.h = self.image.get_size()
        elif col == 'green':
            self.image = load_image("Tower1.png", colorkey=(255, 255, 255))
            self.w, self.h = self.image.get_size()
        elif col == 'red':
            self.image = load_image("Tower2.png", colorkey=(255, 255, 255))
            self.w, self.h = self.image.get_size()
        elif col == 'yellow':
            self.image = load_image("Tower3.png", colorkey=(255, 255, 255))
            self.w, self.h = self.image.get_size()
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.original_image = self.image
        self.x = -600
        self.y = 0
        self.is_rotate = is_rotate
        self.rect.y = pos[1]
        self.center = (0, 0)
        self.mod = 0
        self.angle = 0
        self.controlled = controlled
        self.st = time.time()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, screen, time, coords):
        if self.controlled:
            x1, y1 = pygame.mouse.get_pos()
        else:
            x1, y1 = map(int, coords)

        if self.player:
            newang = math.degrees(math.atan2(y1 - self.rect.y, x1 - self.rect.x)) % 360
        else:
            newang = -90
            # newang = math.degrees(math.atan2(tanks[0].y - self.rect.y, tanks[0].x - self.rect.x)) % 360
        # self.angle += 0.5
        newang = 270 - newang
        if not self.is_rotate:
            newang = self.tank.angle
        ang = self.angle
        if (newang - self.angle) % 360 > 180:
            ang -= min(135 * time / 1000, (newang - self.angle) % 360)
        elif (newang - self.angle) % 360 < 180:
            ang += min(135 * time / 1000, (newang - self.angle) % 360)
        pos = (self.rect.x, self.rect.y)
        originPos = (49, 12)
        pipa = blitRotate(screen, self.original_image, (self.rect.x, self.rect.y), (self.w / 2, self.h - 12), ang)
        self.mask = pygame.mask.from_surface(self.image)
        s = []
        for i in tanks:
            s.append(i.body)
            s.append(i.tower)
        glag = True
        image = pipa[0]
        mask = pygame.mask.from_surface(image)
        rect = image.get_rect(center=pipa[1])
        # self.center = (0, 0)
        oldrect = self.image.get_rect(center=self.center)
        for i in s:
            if i.tank != self.tank:
                offsetold = (-(oldrect.x - i.rect.x), -(oldrect.y - i.rect.y))
                offsetnew = (-(rect.x - i.rect.x), -(rect.y - i.rect.y))
                i.mask = pygame.mask.from_surface(i.image)
                if self.mask.overlap_area(i.mask, offset=offsetold) < mask.overlap_area(i.mask, offset=offsetnew):
                    glag = False

        s = []
        for i in maps.group:
            s.append(i)
        glag = True
        image = pipa[0]
        mask = pygame.mask.from_surface(image)
        rect = image.get_rect(center=pipa[1])
        # self.center = (0, 0)
        oldrect = self.image.get_rect(center=self.center)
        for i in s:
            if i.id == 2:
                offsetold = (-(oldrect.x - i.rect.x), -(oldrect.y - i.rect.y))
                offsetnew = (-(rect.x - i.rect.x), -(rect.y - i.rect.y))
                i.mask = pygame.mask.from_surface(i.image)
                if self.mask.overlap_area(i.mask, offset=offsetold) < mask.overlap_area(i.mask, offset=offsetnew):
                    glag = False
        HealthBar((self.rect.x + 65, self.rect.y - 50), self.tank.hp)
        if glag:
            self.angle = ang
            self.image = pipa[0]
            self.rect = pipa[0].get_rect(center=pipa[1])
            self.center = pipa[1]

        else:
            self.rect = self.image.get_rect(center=pipa[1])

    def shoot(self, group):
        if time.time() - self.st < SHOOT_TIME:
            return
        self.st = time.time()
        pos = (self.center[0] + 33 * math.cos(math.radians(270 - self.angle)),
               self.center[1] + 33 * math.sin(math.radians(270 - self.angle)))
        # pygame.display.set_caption(f'{pos}')
        group.add(Shell(group, tank=self.tank, angle=self.angle, pos=pos))


class Shell(pygame.sprite.Sprite):
    image = load_image("shell.png", colorkey=(255, 255, 255))
    images = [load_image(f"explode{i}.png", colorkey=(255, 255, 255)) for i in range(8)]
    w, h = image.get_size()

    def __init__(self, *group, tank, angle, pos):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x = self.rect.x
        self.y = self.rect.y
        self.original_image = self.image
        self.mod = 0
        self.angle = angle
        self.tank = tank
        self.ind = 1
        self.st = time.time()

    def update(self, screen, time):
        # print(time)
        if self.mod == 1:
            self.explode()
            return
        pipa = blitRotate(screen, self.original_image, (self.x, self.y), (self.w / 2, self.h), self.angle)
        self.image = pipa[0]

        for i in tanks:
            if i != self.tank:
                if pygame.sprite.collide_mask(self, i.tower):
                    self.mod = 1
                    self.image = self.images[0]
                    i.hp -= 20
                    self.rect.x -= math.cos(math.radians(self.angle)) * (self.h / 2)
                    self.rect.y -= math.sin(math.radians(self.angle)) * (self.h / 2)
                    # self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
                    return
                elif pygame.sprite.collide_mask(self, i.body):
                    i.hp -= 20
                    self.mod = 1
                    self.image = self.images[0]
                    self.rect.x -= math.cos(math.radians(self.angle)) * (self.h / 2)
                    self.rect.y -= math.sin(math.radians(self.angle)) * (self.h / 2)
                    # self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
                    return
                if i.hp <= 0:
                    pass
                    # анимация взрыва
        if pygame.sprite.spritecollideany(self, maps.group):
            s = pygame.sprite.spritecollide(self, maps.group, False)
            for i in s:
                if i.id == 2:
                    self.mod = 1
                    self.image = self.images[0]
                    self.rect.x -= math.cos(math.radians(self.angle)) * (self.h / 2)
                    self.rect.y -= math.sin(math.radians(self.angle)) * (self.h / 2)
                    self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
                    return

        for i in tanks:
            if pygame.sprite.spritecollideany(self, i.shells) and i != self.tank:
                # s = pygame.sprite.spritecollide(self, i.shells, False)
                if True:
                    self.mod = 1
                    self.image = self.images[0]
                    self.rect.x -= math.cos(math.radians(self.angle)) * (self.h / 2)
                    self.rect.y -= math.sin(math.radians(self.angle)) * (self.h / 2)
                    self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))

                    return

        self.x += math.cos(math.radians(270 - self.angle)) * 600 * time / 1000
        self.y += math.sin(math.radians(270 - self.angle)) * 600 * time / 1000
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect = self.image.get_rect(center=(pipa[1]))
        if self.rect.x < 0 or self.rect.x > 1000:
            self.mod = 1
            self.image = self.images[0]
            if self.rect.x > 1000:
                self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
                self.rect.x -= 10
            else:
                self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
            return

        if self.rect.y < 0 or self.rect.y > 1000:
            self.mod = 1
            self.image = self.images[0]
            if self.rect.y > 1000:
                self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
                self.rect.y -= 10
            else:
                self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
            return

    def explode(self):
        if time.time() - self.st > 0.1:
            self.st = time.time()
            self.ind += 1
            if self.ind == 8:
                self.groups()[0].remove(self)
                return
            self.image = self.images[self.ind]
            w, h = self.image.get_size()
            self.rect = self.image.get_rect(center=(self.rect.x + w / 2, self.rect.y + h / 2))


tanks = []
group = pygame.sprite.Group()
tanks.append(Tank(group, (900, 600), 'blue', True))
tanks.append(Tank(group, (100, 100), 'red', False))
tanks.append(Tank(group, (900, 100), 'green', False))
tanks.append(Tank(group, (100, 600), 'yellow', False))
maps = Map()
while True:
    if False:
        pass
    elif glag == 1:
        start_screen()
    elif glag == 0:
        main_game()
    elif glag == 2:
        start_double()
    elif glag == 3:
        moncol(SETTINGS)
