import math
import pygame as pg
import random as rd

from config.config_geral import HUD_ALTURA, ALTURA_CELULA
from entidades.inimigo import XOR,AND,OR,NOT,MULTIPLEXER,DEMULTIPLEXER

def in_range(ff, inimigo, fileira, range):

    na_fileira = (inimigo.y - HUD_ALTURA) // ALTURA_CELULA == fileira

    frente = inimigo.x > ff.x and (inimigo.x - ff.x) < range

    return frente and na_fileira


def conta_moedas(saldo, tempo):


    if(tempo <=15):
        return saldo +2

    else :
        return saldo

def algoritmo_spawn(Nivel):
    qtd = Nivel * 3 + 10
    vel_spawn = Nivel
    tipos =[XOR, OR, AND, DEMULTIPLEXER, MULTIPLEXER, NOT]

    bandidos =[]

    for _ in range(qtd):

        classe = rd.choice(tipos)   
        fileira = rd.randint(0,7)
        bandido = classe(700, fileira)
        bandidos.append(bandido)

    return bandidos



                

           
