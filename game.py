import pygame as pg
import itertools as IT

from config.config_geral import LARGURA_TELA, ALTURA_TELA, TITULO_JANELA, FPS, TAMANHO_MATRIZ, ALTURA_FILEIRA
from entidades.inimigo import AND, XOR, OR, NOT, MULTIPLEXER, DEMULTIPLEXER
from entidades.rom import ROM
from entidades.flipflop import FFTIPOD, FFTIPOT, FFTIPOJK, FFTIPOSR
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

def linha_y(indice_linha):
    return indice_linha * ALTURA_FILEIRA + ALTURA_FILEIRA // 2


rom = ROM(0, 0)
inimigos = [
    AND(800, linha_y(3)),
    OR (700, linha_y(1)),
    XOR(620, linha_y(5)),
    DEMULTIPLEXER(540, linha_y(2)),
    OR (460, linha_y(4)),
    XOR(760, linha_y(5)),
    MULTIPLEXER(780, linha_y(6)),
    OR (900, linha_y(7)),
    NOT(960, linha_y(0)),
]
flipflops = []
projeteis = []
tipos = ['D','JK','SR','T']
D, JK, T, SR = FFTIPOD(400, 12), FFTIPOJK(487, 12), FFTIPOT(574, 12), FFTIPOSR(661, 12)

tipo_selecionado = FFTIPOD

botoes = {FFTIPOD: pg.Rect(20, 630, 40, 40), FFTIPOT: pg.Rect(150, 630, 40, 40),
          FFTIPOSR: pg.Rect(280, 630, 40, 40), FFTIPOJK: pg.Rect(410, 630, 40, 40)}

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
            for classe, rect in botoes.items():
                if rect.collidepoint(MX, MY):
                    tipo_selecionado = classe
                    break
            else:
                coluna = (MX - 100) // 87
                fileira = MY // 75
                if MX >= 100 and 0 <= coluna < TAMANHO_MATRIZ and 0 <= fileira < TAMANHO_MATRIZ :
                    x = 100 + coluna * 87
                    y = fileira * 75
                    s_ff = tipo_selecionado(x, y)

                if saldo >= s_ff.custo:
                    matriz[fileira][coluna] = s_ff
                    saldo -= s_ff.custo

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
            ff = matriz[fileira][coluna]
            if ff is not None:
                ff.ff_decay()
                if ff.hp > 0:
                    ff.desenha(tela)
                else:
                    matriz[fileira][coluna] = None
    for ff in flipflops:
        ff.ff_decay()
        if ff.hp > 0:
          ff.desenha(tela)
    for p in projeteis:
        p.desenha(tela)


    #pg.draw.rect(tela,pg.Color("gray"),(0,600,580,4000))
    saldo_text = fonte_padrao.render(f"Resenha Coins: {saldo}",True, (255,255,255))
    rom_hp_text = fonte_padrao.render("Rom HP:", True,(255,255,255))
    tela.blit(saldo_text,(600,658))
    tela.blit(rom_hp_text,(600,640))
    D_label = fonte_padrao.render(f"D - {D.custo}", True, (255, 255, 255))
    T_label = fonte_padrao.render(f"T - {T.custo}", True, (255, 255, 255))
    SR_label = fonte_padrao.render(f"SR - {SR.custo}", True, (255, 255, 255))
    JK_label = fonte_padrao.render(f"JK - {JK.custo}", True, (255, 255, 255))
    tela.blit(D_label, (20, 605))
    tela.blit(T_label, (150, 605))
    tela.blit(SR_label, (280, 605))
    tela.blit(JK_label, (410, 605))
    D.desenha_pos(tela,20,630)
    T.desenha_pos(tela,150,630)
    SR.desenha_pos(tela,280,630)
    JK.desenha_pos(tela,410,630)
    pg.display.flip()

    clock.tick(FPS)

pg.quit()
