import requests
import pygame as pg
from logic.state import State

from logic.states.start_menu import handle_start_events, update_start, render_start
from logic.states.deck_builder import handle_deck_builder_events, update_deck_builder, render_deck_builder

def get_card_info_from_name(card_name):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_card_image_from_id(card_id):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

class App:
    def __init__(self):

        #Settings
        self.RES = (1600, 900)
        self.FLAGS = pg.RESIZABLE

        #Pygame initialization
        pg.init()
        self.final_screen = pg.display.set_mode(self.RES, flags=self.FLAGS)
        pg.display.set_caption("Yu-Gi-Oh! Deck Builder Tool")
        pg.display.set_icon(pg.image.load("assets/icon.png"))
        self.screen = self.final_screen.copy()
        self.clock = pg.time.Clock()

        self.state = State.START_MENU

        self.init_assets()

    def init_assets(self):

        #Start Menu
        self.start_menu_font = pg.font.Font("assets/fonts/Yu-Gi-Oh! Matrix Regular Small Caps 1.ttf", 75)

        self.start_new_button_sprite = self.start_menu_font.render("New deck", True, 'white')
        self.start_new_button_rect = self.start_new_button_sprite.get_rect(center=(self.RES[0]//2, self.RES[1]//2))

        self.start_menu_import_sprite = self.start_menu_font.render("Import deck", True, 'white')
        self.start_menu_import_rect = self.start_menu_import_sprite.get_rect(center=(self.RES[0]//2, self.RES[1]//2 + 100))

        #Deck Builder
        self.current_cards_in_deck = [[], [], []] #Main, Extra, Side

    def read_deck_from_ydk(self, ydk_path):
        current_portion = None

        try:
            with open(ydk_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()

                    if line == "#main":
                        current_portion = self.current_cards_in_deck[0]
                    elif line == "#extra":
                        current_portion = self.current_cards_in_deck[1]
                    elif line == "!side":
                        current_portion = self.current_cards_in_deck[2]

                    if line.isnumeric():
                        self.current_cards_in_deck[current_portion].append(line)
                    else:
                        raise ValueError(f"Invalid line in ydk file: {line}")
                    
        except FileNotFoundError:
            print(f"File not found at: {ydk_path}")

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

            pg.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            match self.state:
                case State.START_MENU:
                    handle_start_events(self, event)

    def update(self):
        match self.state:
            case State.START_MENU:
                update_start()

    def render(self):
        self.screen.fill((0, 0, 0))

        match self.state:
            case State.START_MENU:
                render_start(self)

        self.final_screen.blit(pg.transform.scale(self.screen, self.final_screen.get_rect().size), (0, 0))

if __name__ == "__main__":
    app = App()
    app.run()