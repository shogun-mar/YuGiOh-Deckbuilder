import requests
import pygame as pg
from logic.state import State

from logic.states.start_menu import handle_start_events, update_start, render_start

def get_card_info(card_name):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card_name}"
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
                    handle_start_events(event)

    def update(self):
        match self.state:
            case State.START_MENU:
                update_start()

    def render(self):
        self.screen.fill((0, 0, 0))

        match self.state:
            case State.START_MENU:
                render_start(self.screen)

        self.final_screen.blit(pg.transform.scale(self.screen, self.final_screen.get_rect().size), (0, 0))

if __name__ == "__main__":
    app = App()
    app.run()