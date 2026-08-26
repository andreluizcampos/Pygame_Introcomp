import pygame as pg



class PROJETIL:
    def __init__(self, x, y, dano, alvo, velocidade, cor=pg.Color("yellow")):
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
        pg.draw.circle(screen, self.cor, ((self.x , self.y)), 8 )
