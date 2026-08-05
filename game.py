import pygame as pg
import itertools as IT

from config.config_geral import LARGURA_TELA, ALTURA_TELA, TITULO_JANELA, FPS, TAMANHO_MATRIZ
from entidades.inimigo import AND, XOR, OR, NOT, MULTIPLEXER, DEMULTIPLEXER
from entidades.rom import ROM
from entidades.flipflop import FFTIPOD, FFTIPOJK
from  config.fontes import fonte_padrao


pg.init()

tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pg.display.set_caption(TITULO_JANELA)

saldo = 200
acc = 0
saldo_text = fonte_padrao.render(f"Saldo: {saldo}",False, (255,255,255))
matriz = [[None for coluna in range(TAMANHO_MATRIZ)] for fileira in range(TAMANHO_MATRIZ)]

clock = pg.time.Clock()
executando = True

rom = ROM(0, 0)
inimigos = [
    AND(800, 300),
    OR (700, 180),
    XOR(620, 420),
    DEMULTIPLEXER(540, 250),
    OR (460, 360),
    XOR(760, 300),
    MULTIPLEXER(780, 460),
    OR (900, 500),
    NOT(960, 140),
]
flipflops = []
projeteis = []
tipos = ['D','JK','SR','T']

while executando:
    acc+=1
 
    if acc == 15:
        saldo+=2
        acc=0
 
 
    
    for clicks in pg.event.get():
        if clicks.type == pg.QUIT:
            executando = False

        elif clicks.type == pg.MOUSEBUTTONDOWN:
            MX, MY = clicks.pos
            coluna = (MX - 100) // 87
            fileira = MY // 75
            if MX >= 100 and 0 <= coluna < TAMANHO_MATRIZ and 0 <= fileira < TAMANHO_MATRIZ:
                x = 100 + coluna * 87
                y = fileira * 75
                matriz[fileira][coluna] = FFTIPOD(x, y)

    for inim in inimigos:

        inim.Movimenta(rom.x)

    flipflops_da_matriz = [ff for linha in matriz for ff in linha if ff is not None]
    for ff in flipflops + flipflops_da_matriz:
        ff.atira(inimigos, projeteis)

    for p in projeteis:
        p.Movimenta()
    projeteis = [p for p in projeteis if not p.atingiu]

    tela.fill((30, 30, 40))
    rom.desenha(tela)
    for inim in inimigos:
        saldo += inim.CheckVivo()
        if isinstance(inim, NOT):
            rom.vida += inim.Not_Checker()
        inim.desenha(tela)

    inimigos = [inim for inim in inimigos if inim.hp > 0]
    for fileira in range(TAMANHO_MATRIZ):
        for coluna in range(TAMANHO_MATRIZ):
            if matriz[fileira][coluna] is not None:
                matriz[fileira][coluna].desenha(tela)
    for ff in flipflops:
        ff.desenha(tela)
    for p in projeteis:
        p.desenha(tela)


    saldo_text = fonte_padrao.render(f"Resenha Coins: {saldo}",True, (255,255,255))
    rom_hp_text = fonte_padrao.render("Rom HP:", True,(255,255,255))
    tela.blit(saldo_text,(600,658))
    tela.blit(rom_hp_text,(600,640))
    pg.draw.rect(tela,pg.Color("gray"),(0,600,580,4000))
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
