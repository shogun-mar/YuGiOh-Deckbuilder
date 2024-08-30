from settings import *

rect_width = 350

card_inspect_rect = pg.Rect((0, 0), (rect_width, 1000))

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

    #Draw background
    game.screen.blit(game.main_viewer_sprite, game.main_viewer_rect)
    game.screen.blit(game.side_viewer_sprite, game.side_viewer_rect)
    game.screen.blit(game.extra_viewer_sprite, game.extra_viewer_rect)
    game.screen.blit(game.card_search_sprite, game.card_search_rect)

    # Draw the main deck
    x, y = game.main_viewer_rect.topleft[0] + 58, game.main_viewer_rect.topleft[1] + 2

    for i, card in enumerate(game.current_deck_sprites[0]):  # dimensions of viewer normal card = (82, 117)

        game.screen.blit(card, (x, y))

        x += 83 + 2 # 83 is the width of the card, 2 is the horizontal padding
        if i % 10 == 9:
            x = game.main_viewer_rect.topleft[0] + 58
            y += 118 + 2 # 118 is the height of the card, 3 is the vertical padding

    # Draw the side deck
    x, y = game.side_viewer_rect.topleft[0] + 44, game.side_viewer_rect.topleft[1] + 22

    for i, card in enumerate(game.current_deck_sprites[2]): #dimensions of extra small card = (54, 78)
        game.screen.blit(card, (x, y))
        
        x += 54 + 2 # 54 is the width of the card, 2 is the horizontal padding

        