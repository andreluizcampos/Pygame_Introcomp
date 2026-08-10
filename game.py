import pygame as pg

from config.config_geral import LARGURA_TELA, ALTURA_TELA, TITULO_JANELA, FPS, TAMANHO_MATRIZ, ALTURA_FILEIRA, MUSICA_FUNDO_PATH, MUSICA_VOLUME, TEMPO_JOGO_SEGUNDOS
from entidades.inimigo import AND, XOR, OR, NOT, MULTIPLEXER, DEMULTIPLEXER
from entidades.rom import ROM
from entidades.flipflop import FFTIPOD, FFTIPOT, FFTIPOJK, FFTIPOSR
from  config.fontes import fonte_padrao, fonte_grande
from utilities import algoritmo_spawn, spawn_speed


pg.init()

tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pg.display.set_caption(TITULO_JANELA)

pg.mixer.init()
pg.mixer.music.load(MUSICA_FUNDO_PATH)
pg.mixer.music.set_volume(MUSICA_VOLUME)
pg.mixer.music.play(loops=-1)

saldo = 800
acc = 0
saldo_text = fonte_padrao.render(f"Saldo: {saldo}",False, (255,255,255))
matriz = [[None for coluna in range(TAMANHO_MATRIZ)] for fileira in range(TAMANHO_MATRIZ)]

clock = pg.time.Clock()
executando = True

def linha_y(indice_linha):
    return indice_linha * ALTURA_FILEIRA + ALTURA_FILEIRA // 2


def carrega_botao_sprite(caminho, largura_alvo):
    img = pg.image.load(caminho).convert_alpha()
    escala = largura_alvo / img.get_width()
    altura_alvo = round(img.get_height() * escala)
    return pg.transform.smoothscale(img, (largura_alvo, altura_alvo))


sprite_btn_iniciar = carrega_botao_sprite("botoes/começar_game.png", 320)
sprite_btn_vitoria = carrega_botao_sprite("botoes/jogar_novamente_win.png", 320)
sprite_btn_derrota = carrega_botao_sprite("botoes/jogar_novamente_defeat.png", 320)


def desenha_botao(tela, rect, imagem):
    tela.blit(imagem, rect)


def formata_tempo(ms):
    total_seg = max(0, ms) // 1000
    return f"{total_seg // 60}:{total_seg % 60:02d}"


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
Wave_Rate = 0
it = 0
fila_spawn = []
intervalo_spawn = 0
tempo_spawn_acumulado = 0
tempo_wave_acumulado = 0
acc_2 = 0
tempo_restante_ms = TEMPO_JOGO_SEGUNDOS * 1000

dificuldades = ["Fácil", "Normal", "Difícil"]
DIFICULDADE_CONFIG = {
    "Fácil":   {"saldo": 1000, "mult_hp": 0.8, "mult_dano": 0.8},
    "Normal":  {"saldo": 800,  "mult_hp": 1.0, "mult_dano": 1.0},
    "Difícil": {"saldo": 600,  "mult_hp": 1.3, "mult_dano": 1.3},
}
dificuldade_atual = "Normal"


def aplica_dificuldade(lista_inimigos):
    config = DIFICULDADE_CONFIG[dificuldade_atual]
    for inim in lista_inimigos:
        inim.hp = round(inim.hp * config["mult_hp"])
        inim.hp_max = inim.hp
        inim.dano = round(inim.dano * config["mult_dano"])


estado = "start"




while executando:

    b_start = sprite_btn_iniciar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 60))
    b_restart = sprite_btn_derrota.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50))
    b_restart_win = sprite_btn_vitoria.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    b_dificuldades = {
        nome: pg.Rect(0, 0, 300, 80).move_to(
            center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 80 + indice * 120)
        )
        for indice, nome in enumerate(dificuldades)
    }
    for clicks in pg.event.get():

        if clicks.type == pg.QUIT:
            executando = False

        elif clicks.type == pg.MOUSEBUTTONDOWN:

            if estado == "start":

                if b_start.collidepoint(clicks.pos):
                    estado = "dificuldade"

            elif estado == "dificuldade":

                for nome, rect in b_dificuldades.items():
                    if rect.collidepoint(clicks.pos):
                        dificuldade_atual = nome
                        saldo = DIFICULDADE_CONFIG[nome]["saldo"]
                        matriz = [[None for coluna in range(TAMANHO_MATRIZ)] for fileira in range(TAMANHO_MATRIZ)]
                        rom = ROM(0, 0)
                        inimigos = []
                        flipflops = []
                        projeteis = []
                        pontos_user = 0
                        Wave_Rate = 1
                        it = 0
                        fila_spawn = []
                        intervalo_spawn = 0
                        tempo_spawn_acumulado = 0
                        tempo_wave_acumulado = 0
                        tempo_restante_ms = TEMPO_JOGO_SEGUNDOS * 1000
                        estado = "jogando"
                        break
            elif estado in ("perdeu_playboy", "win"):
                rect_clicavel = b_restart_win if estado == "win" else b_restart
                if rect_clicavel.collidepoint(clicks.pos):
                    matriz = [[None for coluna in range(TAMANHO_MATRIZ)] for fileira in range(TAMANHO_MATRIZ)]
                    rom = ROM(0, 0)
                    inimigos = []
                    flipflops = []
                    projeteis = []
                    pontos_user = 0
                    Wave_Rate = 1
                    it = 0
                    fila_spawn = []
                    intervalo_spawn = 0
                    tempo_spawn_acumulado = 0
                    tempo_wave_acumulado = 0
                    tempo_restante_ms = TEMPO_JOGO_SEGUNDOS * 1000
                    estado = "jogando"
            else:
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
                        y = linha_y(fileira)
                        s_ff = tipo_selecionado(x, y)

                        if saldo >= s_ff.custo:
                            matriz[fileira][coluna] = s_ff
                            saldo -= s_ff.custo


    if estado == "start":

        fundo = pg.image.load("fundos/começo.png")
        fundo = pg.transform.scale(fundo,(LARGURA_TELA, ALTURA_TELA))
        tela.blit(fundo,(0,0))
        desenha_botao(tela, b_start, sprite_btn_iniciar)
        pg.display.flip()
        continue

    if estado == "dificuldade":

        tela.fill((0, 0, 0))
        titulo_text = fonte_grande.render("Escolha a dificuldade", True, (255, 255, 255))
        tela.blit(titulo_text, titulo_text.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 200)))
        for nome, rect in b_dificuldades.items():
            pg.draw.rect(tela, pg.Color("gray20"), rect)
            pg.draw.rect(tela, pg.Color("white"), rect, 2)
            nome_text = fonte_padrao.render(nome, True, (255, 255, 255))
            tela.blit(nome_text, nome_text.get_rect(center=rect.center))
        pg.display.flip()
        continue

    if it == 0:
        it+=1
        fila_spawn = algoritmo_spawn(Wave_Rate)
        aplica_dificuldade(fila_spawn)
        intervalo_spawn = spawn_speed(fila_spawn)
        tempo_spawn_acumulado = 0
        tempo_wave_acumulado = 0

    dt = 0
    dt+= clock.tick(60)

    tempo_wave_acumulado += dt

    if tempo_wave_acumulado >= 25000:
        tempo_wave_acumulado = 0
        Wave_Rate+=1
        fila_spawn = algoritmo_spawn(Wave_Rate)
        aplica_dificuldade(fila_spawn)
        intervalo_spawn = spawn_speed(fila_spawn)
        tempo_spawn_acumulado = 0

    tempo_restante_ms -= dt
    if tempo_restante_ms <= 0:
        tempo_restante_ms = 0
        estado = "win"


    if estado == "win":

                        fundo = pg.image.load("fundos/vitoria.png")
                        fundo = pg.transform.scale(fundo,(LARGURA_TELA, ALTURA_TELA))
                        tela.blit(fundo,(0,0))
                        desenha_botao(tela, b_restart_win, sprite_btn_vitoria)
                        pg.display.flip()
                        continue

    tempo_spawn_acumulado += dt
    if fila_spawn and tempo_spawn_acumulado >= intervalo_spawn:
        tempo_spawn_acumulado = 0
        inimigos.append(fila_spawn.pop(0))

    acc+=1
    acc_2 +=1

    if acc_2 == 30:

        saldo+=Wave_Rate*2
        acc_2 = 0

    if acc == 15:
        saldo+=3
        saldo += (Wave_Rate//2)
        acc=0
 
    if rom.vida <= 0:
        estado = "perdeu_playboy"

    if estado == "perdeu_playboy":
       
        fundo = pg.image.load("fundos/derrota.png")
        fundo = pg.transform.scale(fundo,(LARGURA_TELA, ALTURA_TELA))
        tela.blit(fundo,(0,0))
        desenha_botao(tela, b_restart, sprite_btn_derrota)
        pg.display.flip()
        continue

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
            if rom.vida <= rom.vida_max:
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
    wave_text = fonte_padrao.render(f"Wave: {Wave_Rate}", True, (255,255,255))
    cronometro_text = fonte_padrao.render(f"Tempo: {formata_tempo(tempo_restante_ms)}", True, (255,255,255))
    tela.blit(cronometro_text,(600,604))
    tela.blit(wave_text,(600,622))
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
