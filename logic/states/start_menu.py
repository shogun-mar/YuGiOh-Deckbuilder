import pygame as pg
from tkinter import filedialog
from logic.state import State

def handle_start_events(game, event):
    if event.type == pg.MOUSEBUTTONDOWN:
        if game.start_new_button_rect.collidepoint(event.pos):
            game.state = State.DECK_EDITOR
        elif game.start_menu_import_rect.collidepoint(event.pos):
            selected_ydk_path = filedialog.askopenfilename(title="Select a .ydk file", filetypes=[("YDK files", "*.ydk")])
            game.read_deck_from_ydk(selected_ydk_path)
            game.bind_rects_to_cards()
            game.state = State.DECK_EDITOR
        elif game.start_menu_clear_cache_rect.collidepoint(event.pos):
            game.clear_cache()

def update_start(game):
    pass

def render_start(game):
    screen = game.screen

    screen.blit(game.start_new_button_sprite, game.start_new_button_rect)
    screen.blit(game.start_menu_import_sprite, game.start_menu_import_rect)
    screen.blit(game.start_menu_clear_cache_sprite, game.start_menu_clear_cache_rect)
    screen.blit(game.start_menu_logo_sprite, game.start_menu_logo_rect)