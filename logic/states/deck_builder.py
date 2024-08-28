import pygame as pg


card_inspect_rect = pg.Rect((0, 0), (288, 1000))
card_view_rect = pg.Rect((288, 0), (1062, 1000))
card_search_rect = pg.Rect((1350, 0), (450, 1000))

card_view_offset = card_view_rect.topleft

def handle_deck_builder_events(game, event):
    pass

def update_deck_builder():
    pass

def render_deck_builder(game):
    screen = game.screen

    screen.fill((0, 0, 0))
    draw_deck(game)

def draw_deck(game):

    pg.draw.rect(game.screen, 'red', card_inspect_rect)
    pg.draw.rect(game.screen, 'blue', card_view_rect)
    pg.draw.rect(game.screen, 'green', card_search_rect)

    for i, portion in enumerate(game.current_deck_sprites):
        for j, card_sprite in enumerate(portion):
            game.screen.blit(card_sprite, (j * 50 + card_view_offset[0], i * 50 + card_view_offset[1]))