from settings import *

rect_width = 350

card_inspect_rect = pg.Rect((0, 0), (rect_width, 1000))

rect_width = SCREEN_WIDTH - (rect_width * 2)


def handle_deck_builder_events(game, event):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        card_found = False
        for deck_rects in game.current_deck_rects:
            for rect in deck_rects:
                if rect.collidepoint(event.pos):
                    print("Card clicked")
                    card_found = True
                    break
                if card_found: break


def update_deck_builder():
    pass

def render_deck_builder(game):
    screen = game.screen

    screen.fill((0, 0, 0))
    draw_deck(game)

def draw_deck(game):

    pg.draw.rect(game.screen, 'red', card_inspect_rect)

    #Draw background
    game.screen.blit(game.main_viewer_sprite, game.main_viewer_rect)
    game.screen.blit(game.side_viewer_sprite, game.side_viewer_rect)
    game.screen.blit(game.extra_viewer_sprite, game.extra_viewer_rect)
    game.screen.blit(game.card_search_sprite, game.card_search_rect)

    # Draw the deck
    for sprites, rects in zip(game.current_deck_sprites, game.current_deck_rects):
        for sprite, rect in zip(sprites, rects):
            game.screen.blit(sprite, rect)