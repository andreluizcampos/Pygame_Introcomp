from config.config_geral import FPS, ALTURA_FILEIRA
from config.flipflops_config import (
    FFTIPOD_CONFIG, FFTIPOSR_CONFIG, FFTIPOJK_CONFIG, FFTIPOT_CONFIG,
)
from entidades.sprites import carrega_sprite
from entidades.projetil import PROJETIL


class FLIPFLOPS:
    def __init__(self, x, y, hp_drop, hp, custo, dano, cadencia, cor, alcance, sprite_path, sprite_tamanho):
        self.x = x
        self.y = y
        self.hp = hp
        self.hp_drop = hp_drop
        self.custo = custo
        self.dano = dano
        self.cadencia = cadencia
        self.cor = cor
        self.alcance = alcance
        self.sprite = carrega_sprite(sprite_path, sprite_tamanho)
        self.cooldown = 0

    def procura_alvo(self, inimigos):
        alvo = None
        menor_distancia = self.alcance + 1
        for inimigo in inimigos:
            distancia = inimigo.x - self.x
            mesma_fileira = abs(inimigo.y - self.y) < ALTURA_FILEIRA
            if 0 < distancia <= self.alcance and mesma_fileira and distancia < menor_distancia:
                alvo = inimigo
                menor_distancia = distancia
        return alvo

    def atira(self, inimigos, projeteis):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        alvo = self.procura_alvo(inimigos)
        if alvo is None:
            return

        origem_x = self.x + self.sprite.get_width()
        origem_y = self.y + self.sprite.get_height() / 2
        projeteis.append(PROJETIL(origem_x, origem_y, self.dano, alvo, self.cor))
        self.cooldown = self.cadencia * FPS

    def desenha(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def desenha_pos(self, screen, x,y):
         screen.blit(self.sprite, (x,y))

    def ff_decay(self):
        self.hp-=self.hp_drop

class FFTIPOD(FLIPFLOPS):
    def __init__(self, x, y):
        super().__init__(x, y, **FFTIPOD_CONFIG)


class FFTIPOSR(FLIPFLOPS):
    def __init__(self, x, y):
        super().__init__(x, y, **FFTIPOSR_CONFIG)


class FFTIPOJK(FLIPFLOPS):
    def __init__(self, x, y):
        super().__init__(x, y, **FFTIPOJK_CONFIG)


class FFTIPOT(FLIPFLOPS):
    def __init__(self, x, y):
        super().__init__(x, y, **FFTIPOT_CONFIG)
