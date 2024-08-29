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
    main_deck_origin_x, main_deck_origin_y = game.main_viewer_rect.topleft[0] + 59, game.main_viewer_rect.topleft[1] + 2
    x, y = main_deck_origin_x, main_deck_origin_y

    for i, card in enumerate(game.current_deck_sprites[0]):  # dimensions of viewer normal card = (83, 118)
        x = main_deck_origin_x + (i % 10) * (83 + 3)
        y = main_deck_origin_y + (i // 10) * (118 + 2)

        game.screen.blit(card, (x, y))


    # Draw the side deck
    side_deck_origin_x, side_deck_origin_y = game.side_viewer_rect.topleft[0] + 43, game.side_viewer_rect.topleft[1] + 21

    for i, card in enumerate(game.current_deck_sprites[2]): #dimensions of extra small card = (80, 117)
        x = side_deck_origin_x + 3 + (i  * 80)
        y = side_deck_origin_y

        game.screen.blit(card, (x, y))