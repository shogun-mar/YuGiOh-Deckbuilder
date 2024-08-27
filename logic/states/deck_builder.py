def handle_deck_builder_events(game, event):
    print("Handling deck builder events")

def update_deck_builder():
    print("Updating deck builder")

def render_deck_builder(game):
    screen = game.screen

    screen.fill((0, 0, 0))

    # for i, portion in enumerate(game.current_deck_sprites):
    #     for j, card_sprite in enumerate(portion):
    #         screen.blit(card_sprite, (j * 50, i * 50))