import math
import pygame as pg
import random as rd

from config.config_geral import ALTURA_FILEIRA, TAMANHO_MATRIZ
from entidades.inimigo import XOR,AND,OR,NOT,MULTIPLEXER,DEMULTIPLEXER

def conta_moedas(saldo, tempo):


    if(tempo <=15):
        return saldo +2

    else :
        return saldo

def algoritmo_spawn(Nivel):
    qtd = (Nivel+3) * 4 + 10
    vel_spawn = Nivel
    tipos =[XOR, OR, AND, DEMULTIPLEXER, MULTIPLEXER, NOT]

    bandidos =[]

    for _ in range(qtd):

        classe = rd.choice(tipos)
        fileira = rd.randint(0, TAMANHO_MATRIZ - 1)
        y = fileira * ALTURA_FILEIRA + ALTURA_FILEIRA // 2
        bandido = classe(700, y)
        bandidos.append(bandido)

    return bandidos

def spawn_speed(inimgos):

    return 35000//len(inimgos)



                

           
