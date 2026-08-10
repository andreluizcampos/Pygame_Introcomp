AND_CONFIG = dict(
    dano=45, vida=700, projetil=False, buff=False, p_dano=0, cadencia=2, velocidade=1.2, drop=45, pontos=80,
    sprite_path="sprites/AND.png", sprite_tamanho=(80, 35),
)

OR_CONFIG = dict(
    dano=40, vida=550, projetil=True, buff=False, p_dano=50, cadencia=3, velocidade=2.2, drop=40, pontos=35,
    sprite_path="sprites/OR.png", sprite_tamanho=(80, 35),
)

XOR_CONFIG = dict(
    dano=55, vida=580, projetil=True, buff=False, p_dano=50, cadencia=5, velocidade=1.3, drop=50, pontos=45,
    sprite_path="sprites/XOR.png", sprite_tamanho=(80, 35),
)

NOT_CONFIG = dict(
    dano=0, vida=200, projetil=False, buff=True, p_dano=0, cadencia=0, velocidade=1.0, drop=45, pontos=15,
    sprite_path="sprites/NOT.png", sprite_tamanho=(80, 35),
)

MULTIPLEXER_CONFIG = dict(
    dano=90, vida=1100, projetil=False, buff=False, p_dano=0, cadencia=1, velocidade=0.85, drop=70, pontos=160,
    sprite_path="sprites/MUX.png", sprite_tamanho=(80, 36),
)

DEMULTIPLEXER_CONFIG = dict(
    dano=60, vida=975, projetil=True, buff=False, p_dano=70, cadencia=2.5, velocidade=1.0, drop=55, pontos=85,
    sprite_path="sprites/DEMUX.png", sprite_tamanho=(80, 36),
)
