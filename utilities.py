import math
import pygame as pg

from config.config_geral import HUD_ALTURA, ALTURA_CELULA


def in_range(ff, inimigo, fileira, range):

    na_fileira = (inimigo.y - HUD_ALTURA) // ALTURA_CELULA == fileira

    frente = inimigo.x > ff.x and (inimigo.x - ff.x) < range

    return frente and na_fileira


def conta_moedas(saldo, tempo):


    if(tempo <=15):
        return saldo +2

    else :
        return saldo
    
    
