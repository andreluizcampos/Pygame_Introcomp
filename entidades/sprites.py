import pygame as pg

_cache_sprites = {}


def carrega_sprite(caminho, tamanho):
    chave = (caminho, tamanho)
    if chave not in _cache_sprites:
        imagem = pg.image.load(caminho).convert_alpha()
        imagem = pg.transform.scale(imagem, tamanho)
        _cache_sprites[chave] = imagem
    return _cache_sprites[chave]
