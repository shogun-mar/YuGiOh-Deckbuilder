import requests, time, os
import pygame as pg
from logic.state import State
from logic.card import Card
from settings import *

from logic.states.start_menu import handle_start_events, update_start, render_start
from logic.states.deck_builder import handle_deck_builder_events, update_deck_builder, render_deck_builder

def get_card_info(search_value, search_type='name'):
    """
    Fetch card information based on search type.
    
    Parameters:
    - search_value: The value to search for (e.g., card name or card ID).
    - search_type: The type of search ('name' or 'id'). Default is 'name'.
    
    Returns:
    - JSON response containing card information if successful, None otherwise.
    """

    if search_type not in ['name', 'id']:
        raise ValueError("Invalid search_type. Must be 'name' or 'id'.")

    base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    url = f"{base_url}?{search_type}={search_value}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def cache_image(value, dimensions, image_type, card_id):
    
    if image_type not in ['pygame surface', 'response']:
        raise ValueError("Invalid image_type. Must be 'pygame surface' or 'response'.")
    if dimensions not in ['cropped', 'small', 'normal', 'viewer normal', 'viewer small']:
        raise ValueError("Invalid dimensions. Must be 'cropped', 'small', 'normal', 'viewer normal' or 'viewer small'.")
    
    path = os.path.join("assets/cached cards", dimensions)

    match image_type:
        case 'pygame surface':
            pg.image.save(value, os.path.join(path, f"{card_id}.png"))

        case 'response':
            image_path = os.path.join(path, f"{card_id}.png")
            with open(image_path, 'wb') as file:
                for chunk in value.iter_content(1024):
                    file.write(chunk)

def is_image_already_cached(dimensions, card_id):
    """
    Check if the image of a card is already cached.

    Parameters:
    - dimensions: The dimensions of the image ('extra small', 'small', 'normal', 'cropped').
    - card_id: The ID of the card.

    Returns:
    - True if the image is already cached, False otherwise.
    """

    path = os.path.join("assets/cached cards", dimensions, f"{card_id}.png")
    return os.path.exists(path)

def get_cached_image(dimensions, card_id):
    """
    Load and return the cached image of a card from its ID.

    Parameters:
    - dimensions: The dimensions of the image ('cropped', 'small', 'normal', 'viewer normal', 'viewer small').
    - card_id: The ID of the card.

    Returns:
    - The cached image as a pygame surface.
    """

    path = os.path.join("assets/cached cards", dimensions, f"{card_id}.png")
    return pg.image.load(path).convert_alpha()

def get_small_card_image(card_id):
    """
    Download, cache and return the small image of a card from its ID.

    Parameters:
    - card_id: The ID of the card.

    Returns:
    - The small image of the card as a pygame surface.
    """
    card_info = get_card_info(search_value=card_id, search_type='id') # Get card info json from ID
    if card_info is not None:

        card_image_url = card_info["data"][0]["card_images"][0]["image_url_small"] # Get the URL of the small image
        response = requests.get(card_image_url, stream=True) # Get the image from the URL

        # If the request was successful
        if response.status_code == 200: 

            # Cache the image
            cache_image(response, 'small', 'response', card_id)

            # Load the image from the cache
            image_path = os.path.join("assets/cached cards/small", f"{card_id}.png")
            card_image = pg.image.load(image_path).convert_alpha()
            return card_image
            
        else:
            print(f"Failed to download image: {response.status_code}")
            return None
    else:
        raise ValueError(f"Failed to get card info from ID: {card_id}")
        
def resize_card(surf, new_dim_preset):
    """
    Resizes input pygame surface to new dimensions based on preset and original size.

    Parameters:
    - surf: The pygame surface to resize.
    - new_dim_preset: The new dimensions preset ('cropped', 'small', 'normal', 'viewer normal', 'viewer small').

    Returns:
    - The resized pygame surface.
    """

    if new_dim_preset not in ['cropped', 'small', 'normal', 'viewer normal', 'viewer small']:
        raise ValueError("Invalid dim_preset. Must be 'cropped', 'small', 'normal', 'viewer normal' or 'viewer small'.")

    if new_dim_preset == 'viewer normal':
        new_width = 83
        new_height = 118
    elif new_dim_preset == 'viewer small':
        new_width = 55
        new_height = 78

    resized_surf = pg.transform.smoothscale(surf, (new_width, new_height))
    return resized_surf

class App:
    def __init__(self):

        #Pygame initialization
        pg.init()
        self.final_screen = pg.display.set_mode(RES, flags=FLAGS)
        pg.display.set_caption("Unofficial Yu-Gi-Oh! Deck Builder Tool")
        pg.display.set_icon(pg.image.load("assets/icon.png").convert_alpha())
        self.screen = self.final_screen.copy()
        self.clock = pg.time.Clock()

        self.state = State.START_MENU

        self.init_assets()

    def init_assets(self):

        #Start Menu
        self.start_menu_font = pg.font.Font("assets/fonts/Yu-Gi-Oh! Matrix Regular Small Caps 1.ttf", 75)

        self.start_new_button_sprite = self.start_menu_font.render("New deck", True, 'white')
        self.start_new_button_rect = self.start_new_button_sprite.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

        self.start_menu_import_sprite = self.start_menu_font.render("Import deck", True, 'white')
        self.start_menu_import_rect = self.start_menu_import_sprite.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 200))

        self.start_menu_clear_cache_sprite = self.start_menu_font.render("Clear cache", True, 'white')
        self.start_menu_clear_cache_rect = self.start_menu_clear_cache_sprite.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT + 10))

        self.start_menu_logo_sprite = pg.image.load("assets/logo.png").convert_alpha()
        self.start_menu_logo_rect = self.start_menu_logo_sprite.get_rect(midtop = (SCREEN_WIDTH//2, SCREEN_HEIGHT//6))

        #Deck editor
        self.deck = [[], [], []] # Main, side, extra
        self.current_interacted_card = None # The card that the user is currently interacting with

        self.card_search_sprite = pg.image.load("assets/card_search.png").convert_alpha()
        self.card_search_rect = self.card_search_sprite.get_rect(topright=(SCREEN_WIDTH, 5))

        self.main_viewer_sprite = pg.image.load("assets/main_viewer.png").convert_alpha()
        main_topright = (self.card_search_rect.topleft[0] - 5, self.card_search_rect.topleft[1] + 5)
        self.main_viewer_rect = self.main_viewer_sprite.get_rect(topright=main_topright)

        self.side_viewer_sprite = pg.image.load("assets/side_viewer.png").convert_alpha()
        side_topright = (self.card_search_rect.topleft[0] - 5, 725 + 15)
        self.side_viewer_rect = self.side_viewer_sprite.get_rect(topright=side_topright)

        self.extra_viewer_sprite = pg.image.load("assets/extra_viewer.png").convert_alpha()
        extra_bottomright = (self.card_search_rect.bottomleft[0] - 5, self.card_search_rect.bottomleft[1] + 5)
        self.extra_viewer_rect = self.extra_viewer_sprite.get_rect(bottomright=extra_bottomright)

    def read_deck_from_ydk(self, ydk_path):
        """
        Read deck from ydk file and store card IDs in current_cards_in_deck list and the loaded images in current_deck_sprites.

        Parameters:
        - ydk_path: The path to the ydk file.

        Returns:
        - None
        """
        current_portion = None

        try:
            with open(ydk_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    has_api_been_called = False # Flag to check if the API has been called
                    start_time = time.time()  # Record the start time of the iteration

                    line = line.strip()
                    print(f"Processing line: {line}")

                    if line == "#main": 
                        current_portion = 0
                        continue  # Skip to next iteration
                    elif line == "!side": 
                        current_portion = 1
                        continue  # Skip to next iteration
                    elif line == "#extra": 
                        current_portion = 2
                        continue  # Skip to next iteration
                    elif line == "": continue  # Skip to next iteration if line is empty

                    if line.isdigit():  # If line only contains digits
                        try:

                            if is_image_already_cached(dimensions='small', card_id=line):
                                card_sprite = get_cached_image(dimensions='small', card_id=line)
                            else:
                                card_sprite = get_small_card_image(card_id=line)
                                cache_image(card_sprite, dimensions='small', image_type='pygame surface', card_id=line)

                            if current_portion == 0:
                                if is_image_already_cached(dimensions='viewer normal', card_id=line):
                                    card_sprite = get_cached_image(dimensions='viewer normal', card_id=line)
                                    has_api_been_called = False # Set the flag to False because the image is already cached
                                else:
                                    card_sprite = resize_card(card_sprite, new_dim_preset='viewer normal')
                                    # The image is already cached in the get_small_card_image function
                                    has_api_been_called = True # Set the flag to True to avoid letting the program sleep if the image is already cached
                            else:
                                if is_image_already_cached(dimensions='viewer small', card_id=line):
                                    card_sprite = get_cached_image(dimensions='viewer small', card_id=line)
                                else:
                                    card_sprite = resize_card(card_sprite, new_dim_preset='viewer small')
                                    cache_image(card_sprite, dimensions='viewer small', image_type='pygame surface', card_id=line)


                            self.deck[current_portion].append(Card(id=line, sprite=card_sprite, rect=None))

                        except Exception as e:
                            raise Exception(f"Unknown card ID: {line} with error: {e}")
                            
                    else:
                        raise ValueError(f"Invalid line in ydk file: {line}")
                    
                    if has_api_been_called:
                        # Calculate the time taken for the iteration
                        elapsed_time = time.time() - start_time
                        # Sleep for the remaining time to ensure the loop runs 20 times per second
                        time_to_sleep = max(0, (1 / 20) - elapsed_time)
                        time.sleep(time_to_sleep)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at: {ydk_path}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")
            
    def clear_cache(self):
        """
        Clear the cache of card images.

        Parameters:
        - None

        Returns:
        - None
        """

        for root, dirs, files in os.walk("assets/cached cards"):
            for file in files:
                os.remove(os.path.join(root, file))

    def bind_rects_to_cards(self):
        """
        Binds rects to cards in the deck.

        Parameters:
        - None

        Returns:
        - None
        """

        #Main deck
        x, y = self.main_viewer_rect.topleft[0] + 58, self.main_viewer_rect.topleft[1] + 2
        for i, card in enumerate(self.deck[0]):
            card.rect = card.sprite.get_rect(topleft=(x, y))
            card.original_rect = card.rect.copy() # Save the original rect for resetting
            x += 83 + 2 # 83 is the width of the card, 2 is the horizontal padding
            if i % 10 == 9:
                x = self.main_viewer_rect.topleft[0] + 58
                y += 118 + 2 # 118 is the height of the card, 3 is the vertical padding

        #Side deck
        x, y = self.side_viewer_rect.topleft[0] + 44, self.side_viewer_rect.topleft[1] + 22
        for card in self.deck[1]:
            card.rect = card.sprite.get_rect(topleft=(x, y))
            card.original_rect = card.rect.copy() # Save the original rect for resetting
            x += 55 + 2

        #Extra deck
        x, y = self.extra_viewer_rect.topleft[0] + 44, self.extra_viewer_rect.topleft[1] + 22
        for card in self.deck[2]:
            card.rect = card.sprite.get_rect(topleft=(x, y))
            card.original_rect = card.rect.copy() # Save the original rect for resetting
            x += 55 + 2 #55 is the width of the card, 2 is the horizontal padding

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
                case State.START_MENU: handle_start_events(self, event)
                case State.DECK_EDITOR: handle_deck_builder_events(self, event)

    def update(self):
        match self.state:
            case State.START_MENU: update_start(self)
            case State.DECK_EDITOR: update_deck_builder(self)

    def render(self):
        self.screen.fill((0, 0, 0))

        match self.state:
            case State.START_MENU: render_start(self)
            case State.DECK_EDITOR: render_deck_builder(self)

        self.final_screen.blit(pg.transform.scale(self.screen, self.final_screen.get_rect().size), (0, 0))

if __name__ == "__main__":
    app = App()
    app.run()