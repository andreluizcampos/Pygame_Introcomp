from config.inimigos_config import (
    AND_CONFIG, OR_CONFIG, XOR_CONFIG, NOT_CONFIG,
    MULTIPLEXER_CONFIG, DEMULTIPLEXER_CONFIG,
)
from entidades.sprites import carrega_sprite


class INIMIGO:
    def __init__(self, x, y, dano, vida, projetil, buff, p_dano, cadencia, velocidade, drop, sprite_path, sprite_tamanho):
        self.x = x
        self.y = y
        self.dano = dano
        self.hp = vida
        self.buff = buff
        self.projetil = projetil
        self.p_dano = p_dano
        self.cadencia = cadencia
        self.velocidade = velocidade
        self.drop = drop
        self.sprite = carrega_sprite(sprite_path, sprite_tamanho)
        self.vivo = True
        self.iteracoes = 0
    def Movimenta(self, romX):
        if self.x > romX:
            self.x -= self.velocidade

    def desenha(self, screen):
        rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.sprite, rect)

    def CheckVivo(self):

        if self.hp <= 0:
            self.vivo = False
            self.iteracoes+=1

        if self.vivo == False and self.iteracoes == 1:
            return self.drop
        else:
            return 0



class AND(INIMIGO):
    def __init__(self, x, y):
        super().__init__(x, y, **AND_CONFIG)

   
class OR(INIMIGO):
    def __init__(self, x, y):
        super().__init__(x, y, **OR_CONFIG)


class XOR(INIMIGO):
    def __init__(self, x, y):
        super().__init__(x, y, **XOR_CONFIG)


class NOT(INIMIGO):
    def __init__(self, x, y):
        super().__init__(x, y, **NOT_CONFIG)

    def Not_Checker(self):
        if self.vivo == False and self.iteracoes == 1:
            return 100
        else:
            return 0
            
    

class MULTIPLEXER(INIMIGO):
    def __init__(self, x, y):
        super().__init__(x, y, **MULTIPLEXER_CONFIG)


class DEMULTIPLEXER(INIMIGO):
    def __init__(self, x, y):
        super().__init__(x, y, **DEMULTIPLEXER_CONFIG)
