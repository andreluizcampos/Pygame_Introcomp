import pygame as pg
import itertools as IT

from config.config_geral import LARGURA_TELA, ALTURA_TELA, TITULO_JANELA, FPS, TAMANHO_MATRIZ, ALTURA_FILEIRA
from entidades.inimigo import AND, XOR, OR, NOT, MULTIPLEXER, DEMULTIPLEXER
from entidades.rom import ROM
from entidades.flipflop import FFTIPOD, FFTIPOT, FFTIPOJK, FFTIPOSR
from  config.fontes import fonte_padrao
from utilities import algoritmo_spawn, spawn_speed


pg.init()

tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pg.display.set_caption(TITULO_JANELA)

saldo = 400
acc = 0
saldo_text = fonte_padrao.render(f"Saldo: {saldo}",False, (255,255,255))
matriz = [[None for coluna in range(TAMANHO_MATRIZ)] for fileira in range(TAMANHO_MATRIZ)]

clock = pg.time.Clock()
executando = True

def linha_y(indice_linha):
    return indice_linha * ALTURA_FILEIRA + ALTURA_FILEIRA // 2


rom = ROM(0, 0)
inimigos = []
flipflops = []
projeteis = []
tipos = ['D','JK','SR','T']
D, JK, T, SR = FFTIPOD(400, 12), FFTIPOJK(487, 12), FFTIPOT(574, 12), FFTIPOSR(661, 12)

tipo_selecionado = FFTIPOD

botoes = {FFTIPOD: pg.Rect(110, 645, 40, 40), FFTIPOT: pg.Rect(240, 645, 40, 40),
          FFTIPOSR: pg.Rect(370, 645, 40, 40), FFTIPOJK: pg.Rect(500, 645, 40, 40)}

pontos_user = 0
Wave_Rate = 1
it = 0
fila_spawn = []
intervalo_spawn = 0
tempo_spawn_acumulado = 0
tempo_wave_acumulado = 0

while executando:

    
    if it  == 0:
        it+=1
        fila_spawn = algoritmo_spawn(Wave_Rate)
        intervalo_spawn = spawn_speed(fila_spawn)
        tempo_spawn_acumulado = 0
        tempo_wave_acumulado = 0


    dt = 0
    dt+= clock.tick(60)

    tempo_wave_acumulado += dt
    if Wave_Rate < 10 and tempo_wave_acumulado >= 35000:
        tempo_wave_acumulado = 0
        Wave_Rate+=1
        fila_spawn = algoritmo_spawn(Wave_Rate)
        intervalo_spawn = spawn_speed(fila_spawn)
        tempo_spawn_acumulado = 0

    tempo_spawn_acumulado += dt
    if fila_spawn and tempo_spawn_acumulado >= intervalo_spawn:
        tempo_spawn_acumulado = 0
        inimigos.append(fila_spawn.pop(0))

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


    flipflops_da_matriz = [ff for linha in matriz for ff in linha if ff is not None]
    for ff in flipflops + flipflops_da_matriz:
        ff.atira(inimigos, projeteis)

    for inim in inimigos:
        
        inim.Movimenta(rom.x,flipflops + flipflops_da_matriz,rom)
      
    for p in projeteis:
        p.Movimenta()
    projeteis = [p for p in projeteis if not p.atingiu]

    tela.fill((30, 30, 40))
    rom.desenha(tela)
    for inim in inimigos:
        saldo += inim.CheckVivo()
        if not inim.vivo and inim.iteracoes == 1:
            pontos_user += inim.pontos
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
    pontos_text = fonte_padrao.render(f"Pontos: {pontos_user}",True, (255,255,255))
    rom_hp_text = fonte_padrao.render("Rom HP:", True,(255,255,255))
    tela.blit(saldo_text,(600,658))
    tela.blit(pontos_text,(600,676))
    tela.blit(rom_hp_text,(600,640))
    D_label = fonte_padrao.render(f"D - {D.custo}", True, (255, 255, 255))
    T_label = fonte_padrao.render(f"T - {T.custo}", True, (255, 255, 255))
    SR_label = fonte_padrao.render(f"SR - {SR.custo}", True, (255, 255, 255))
    JK_label = fonte_padrao.render(f"JK - {JK.custo}", True, (255, 255, 255))
    tela.blit(D_label, (110, 620))
    tela.blit(T_label, (240, 620))
    tela.blit(SR_label, (370, 620))
    tela.blit(JK_label, (500, 620))
    D.desenha_pos(tela,110,645)
    T.desenha_pos(tela,240,645)
    SR.desenha_pos(tela,370,645)
    JK.desenha_pos(tela,500,645)
    pg.display.flip()

    clock.tick(FPS)

pg.quit()
