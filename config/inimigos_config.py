AND_CONFIG = dict(
    dano=60, vida=700, buff=False, velocidade=0.5, drop=45, pontos=80,
    sprite_path="sprites/AND.png", sprite_tamanho=(80, 35),
)

OR_CONFIG = dict(
    dano=40, vida=550, buff=False, velocidade=1.0, drop=40, pontos=35,
    sprite_path="sprites/OR.png", sprite_tamanho=(80, 35),
)

XOR_CONFIG = dict(
    dano=70, vida=580, buff=False, velocidade=0.8, drop=50, pontos=45,
    sprite_path="sprites/XOR.png", sprite_tamanho=(80, 35),
)

NOT_CONFIG = dict(
    dano=0, vida=200, buff=True, velocidade=0.7, drop=45, pontos=15,
    sprite_path="sprites/NOT.png", sprite_tamanho=(80, 35),
)

MULTIPLEXER_CONFIG = dict(
    dano=160, vida=1100, buff=False, velocidade=0.7, drop=70, pontos=160,
    sprite_path="sprites/MUX.png", sprite_tamanho=(80, 36),
)

DEMULTIPLEXER_CONFIG = dict(
    dano=250, vida=800, buff=True, velocidade=0.40, drop=55, pontos=85,
    sprite_path="sprites/DEMUX.png", sprite_tamanho=(80, 36),
)
