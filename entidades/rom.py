import pygame as pg

from config.config_geral import SPRITE_ROM_PATH, SPRITE_ROM_TAMANHO, ROM_VIDA


class ROM:

    def __init__(self, x, y, vida=ROM_VIDA):
        self.hp = vida
        self.hp_max = vida
        self.x = x
        self.y = y
        self.hitbox= pg.Rect(x,y,110,600)
        self.sprite = pg.image.load(SPRITE_ROM_PATH).convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, SPRITE_ROM_TAMANHO)

    def desenha(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        prop = max(0, min(self.hp / self.hp_max, 1))
        pg.draw.rect(screen, pg.Color("red"), (670, 645, 50, 6))
        pg.draw.rect(screen, pg.Color("green"), (670, 645, 50 * prop, 6))