AND_CONFIG = dict(
    dano=50, vida=300, projetil=False, buff=False, p_dano=0, cadencia=2, velocidade=0.1, drop=1000,
    sprite_path="sprites/AND.png", sprite_tamanho=(80, 35),
)

OR_CONFIG = dict(
    dano=0, vida=300, projetil=True, buff=False, p_dano=50, cadencia=3, velocidade=0.15, drop=35,
    sprite_path="sprites/OR.png", sprite_tamanho=(80, 35),
)

XOR_CONFIG = dict(
    dano=0, vida=300, projetil=True, buff=False, p_dano=50, cadencia=5, velocidade=0.1, drop=35,
    sprite_path="sprites/XOR.png", sprite_tamanho=(80, 35),
)

NOT_CONFIG = dict(
    dano=0, vida=1, projetil=False, buff=True, p_dano=0, cadencia=0, velocidade=0.5, drop=40,
    sprite_path="sprites/NOT.png", sprite_tamanho=(80, 35),
)

MULTIPLEXER_CONFIG = dict(
    dano=80, vida=600, projetil=False, buff=False, p_dano=0, cadencia=1, velocidade=0.3, drop=60,
    sprite_path="sprites/MUX.png", sprite_tamanho=(80, 36),
)

DEMULTIPLEXER_CONFIG = dict(
    dano=0, vida=450, projetil=True, buff=False, p_dano=70, cadencia=2.5, velocidade=0.4, drop=50,
    sprite_path="sprites/DEMUX.png", sprite_tamanho=(80, 36),
)
