import pygame as pg

from config.config_geral import SPRITE_ROM_PATH, SPRITE_ROM_TAMANHO, ROM_VIDA


class ROM:
    _sprite = None

    def __init__(self, x, y, vida=ROM_VIDA):
        self.vida = vida
        self.vida_max = vida
        self.x = x
        self.y = y
        self.hitbox= pg.Rect(x,y,110,600)
        if ROM._sprite is None:
            ROM._sprite = pg.image.load(SPRITE_ROM_PATH).convert_alpha()
            ROM._sprite = pg.transform.scale(ROM._sprite, SPRITE_ROM_TAMANHO)

    def desenha(self, screen):
        screen.blit(ROM._sprite, (self.x, self.y))
        prop = max(0, min(self.vida / self.vida_max, 1))
        pg.draw.rect(screen, pg.Color("red"), (670, 645, 50, 6))
        pg.draw.rect(screen, pg.Color("green"), (670, 645, 50 * prop, 6))