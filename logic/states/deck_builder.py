from settings import *

rect_width = 350

card_inspect_rect = pg.Rect((0, 0), (rect_width, 1000))

def handle_deck_builder_events(game, event):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # Picking up the card
        card_found = False
        for deck_portion in game.deck:
            for card in deck_portion:
                if card.rect.collidepoint(event.pos):
                    card_found = True # This is used to break out of the outer loop
                    game.current_interacted_card = card
                    break
            if card_found: break
    
    elif event.type == pg.MOUSEMOTION: # Dragging the card
        if game.current_interacted_card:
            game.current_interacted_card.rect.move_ip(event.rel) # Move the card with the relative movement of the mouse 

    elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 1 and game.current_interacted_card != None: # Dropping the card
            game.current_interacted_card.rect = game.current_interacted_card.original_rect
            game.current_interacted_card = None


def update_deck_builder(game):
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
    for deck_portion in game.deck:
        for card in deck_portion:
            game.screen.blit(card.sprite, card.rect)