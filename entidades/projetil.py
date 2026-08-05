import pygame as pg

VELOCIDADE_PADRAO = 5


class PROJETIL:
    def __init__(self, x, y, dano, alvo, cor=(255, 255, 0), velocidade=VELOCIDADE_PADRAO):
        self.x = x
        self.y = y
        self.dano = dano
        self.alvo = alvo
        self.cor = cor
        self.velocidade = velocidade
        self.atingiu = False

    def Movimenta(self):
        if self.alvo.hp <= 0:
            self.atingiu = True
            return

        distancia = self.alvo.x - self.x
        if abs(distancia) <= self.velocidade:
            self.alvo.hp -= self.dano
            self.atingiu = True
        else:
            self.x += self.velocidade if distancia > 0 else -self.velocidade

    def desenha(self, screen):
        pg.draw.circle(screen, self.cor, (int(self.x), int(self.y)), 5)
