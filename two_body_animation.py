import two_body_simulation as tbs

import sys
import pygame as pg
from pygame.math import Vector2


class Planet(pg.sprite.Sprite):

    def __init__(self, pos, start, color, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        pg.draw.circle(self.image, pg.Color(color), (20, 20), 10)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.angle = 0
        # self.positions = arr
        self.offset = Vector2(start[0], start[1])

    def update(self):

        self.rect.center = self.pos + self.offset.rotate(self.angle)


def main():
    pg.init()
    file = open("coordinates.txt", "r")
    read = file.readlines()
    first = []
    second = []

    count = 0
    for line in read:
        coors = line.split(",")
        coor1x = -float(coors[0]) * 100
        coor1y = -float(coors[1]) * 100
        coor2x = -float(coors[2]) * 100
        coor2y = -float(coors[3]) * 100
        first.append((coor1x, coor1y))
        second.append((coor2x, coor2y))

    pg.init()
    screen = pg.display.set_mode((900, 800))
    screen_rect = screen.get_rect()
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    planet1 = Planet(screen_rect.center, first[0], "blue", all_sprites)
    planet2 = Planet(screen_rect.center, second[0], "red", all_sprites)

    # yellow = pg.Color('yellow')


    sayı = 0
    pause = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    pause = True
                if event.key == pg.K_e:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_r:
                    sayı = 0

        while pause:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        pause = False
                    if event.key == pg.K_e:
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_r:
                        sayı = 0
                        planet1.offset = Vector2(first[sayı][0], first[sayı][1])
                        planet2.offset = Vector2(second[sayı][0], second[sayı][1])
                        sayı += 1

                        all_sprites.update()
                        screen.fill((0, 0, 0))  # background color
                        all_sprites.draw(screen)

                        pg.display.flip()
                        clock.tick(60)


        if sayı == len(first):
            sayı = 0

        planet1.offset = Vector2(first[sayı][0], first[sayı][1])
        planet2.offset = Vector2(second[sayı][0], second[sayı][1])
        sayı += 1

        all_sprites.update()
        screen.fill((0, 0, 0)) # background color
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    tbs.app.run()
    main()
    pg.quit()