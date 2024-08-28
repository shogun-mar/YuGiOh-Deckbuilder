from settings import *

rect_width = 350

card_inspect_rect = pg.Rect((0, 0), (rect_width, 1000))
card_search_rect = pg.Rect((SCREEN_WIDTH - rect_width, 0), (rect_width, 1000))

rect_width = SCREEN_WIDTH - (rect_width * 2)


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
    pg.draw.rect(game.screen, 'yellow', card_search_rect)

    #Draw background
    game.screen.blit(game.main_viewer_sprite, game.main_viewer_rect)
    game.screen.blit(game.side_viewer_sprite, game.side_viewer_rect)
    game.screen.blit(game.extra_viewer_sprite, game.extra_viewer_rect)

    # Draw the main deck
    for i, card in enumerate(game.current_deck_sprites[0]): #dimensions of extra small card = (76, 116) 27% of the small card
        x = game.main_view_rect.x + 5 + ((i % 10) * 76)
        y = game.main_view_rect.y + 5 + ((i // 10) * 116)
        game.screen.blit(card, (x, y))

    # Draw the side deck
    for i, card in enumerate(game.current_deck_sprites[2]): #dimensions of extra small card = (76, 116) 27% of the small card
        x = game.side_view_rect.x + 5 + (i  * 76)
        y = game.side_view_rect.y + 5
        #y = side_deck_view_rect.y + 5 + ((i // 10) * 116)
        game.screen.blit(card, (x, y))
            