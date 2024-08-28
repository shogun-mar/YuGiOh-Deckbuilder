import requests, time, os
import pygame as pg
from logic.state import State

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
    if dimensions not in ['extra small', 'small', 'normal', 'cropped']:
        raise ValueError("Invalid dimensions. Must be 'extra small', 'small', 'normal' or 'cropped'.")
    
    path = os.path.join("assets/cached cards", dimensions)

    match image_type:
        case 'pygame surface':
            pg.image.save(value, os.path.join(path, f"{card_id}.jpg"))

        case 'response':
            image_path = os.path.join(path, f"{card_id}.jpg")
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

    path = os.path.join("assets/cached cards", dimensions, f"{card_id}.jpg")
    return os.path.exists(path)

def get_cached_image(dimensions, card_id):
    """
    Load and return the cached image of a card from its ID.

    Parameters:
    - dimensions: The dimensions of the image ('extra small', 'small', 'normal', 'cropped').
    - card_id: The ID of the card.

    Returns:
    - The cached image as a pygame surface.
    """

    path = os.path.join("assets/cached cards", dimensions, f"{card_id}.jpg")
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
            image_path = os.path.join("assets/cached cards/small", f"{card_id}.jpg")
            card_image = pg.image.load(image_path).convert_alpha()
            return card_image
        
        else:
            print(f"Failed to download image: {response.status_code}")
            return None
    else:
        raise ValueError(f"Failed to get card info from ID: {card_id}")

def resize_card(surf, new_dim_preset, original_size):
    """
    Resizes input pygame surface to new dimensions based on preset and original size.

    Parameters:
    - surf: The pygame surface to resize.
    - new_dim_preset: The new dimensions preset ('extra small', 'small', 'normal', 'cropped').
    - original_size: The original size of the card image ('small', 'normal', 'cropped', 'extra small').

    Returns:
    - The resized pygame surface.
    """

    if new_dim_preset not in ['extra small', 'small', 'normal', 'cropped']:
        raise ValueError("Invalid dim_preset. Must be 'extra small', 'small', 'normal' or 'cropped'.")
    if original_size not in ['small', 'normal', 'cropped', 'extra small']:
        raise ValueError("Invalid origin_size. Must be 'small', 'normal', 'cropped' or 'extra small'.")
    
    resize_factor = None

    if original_size == 'small':
        if new_dim_preset == 'extra small':
            resize_factor = 0.5

    if resize_factor is None:
        raise NotImplementedError("Non yet implemented combination of original_size and new_dim_preset")

    new_width = int(surf.get_width() * resize_factor)
    new_height = int(surf.get_height() * resize_factor)
    resized_surf = pg.transform.scale(surf, (new_width, new_height))
    return resized_surf

class App:
    def __init__(self):

        #Settings
        self.RES = (1800, 1000)
        self.FLAGS = pg.RESIZABLE

        #Pygame initialization
        pg.init()
        self.final_screen = pg.display.set_mode(self.RES, flags=self.FLAGS)
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
        self.start_new_button_rect = self.start_new_button_sprite.get_rect(center=(self.RES[0]//2, self.RES[1]//2 + 100))

        self.start_menu_import_sprite = self.start_menu_font.render("Import deck", True, 'white')
        self.start_menu_import_rect = self.start_menu_import_sprite.get_rect(center=(self.RES[0]//2, self.RES[1]//2 + 200))

        self.start_menu_clear_cache_sprite = self.start_menu_font.render("Clear cache", True, 'white')
        self.start_menu_clear_cache_rect = self.start_menu_clear_cache_sprite.get_rect(bottomright=(self.RES[0] - 10, self.RES[1] + 10))

        self.start_menu_logo_sprite = pg.image.load("assets/logo.png").convert_alpha()
        self.start_menu_logo_rect = self.start_menu_logo_sprite.get_rect(midtop = (self.RES[0]//2, self.RES[1]//6))

        #Deck Builder
        self.current_cards_in_deck = [[], [], []] #Main, Extra, Side
        self.current_deck_sprites = [[], [], []] #Main, Extra, Side

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
                    start_time = time.time()  # Record the start time of the iteration

                    line = line.strip()

                    if line == "#main": 
                        current_portion = 0
                        continue  # Skip to next iteration
                    elif line == "#extra": 
                        current_portion = 1
                        continue  # Skip to next iteration
                    elif line == "!side": 
                        current_portion = 2
                        continue  # Skip to next iteration

                    if line.isdigit():  # If line only contains digits
                        try:
                            self.current_cards_in_deck[current_portion].append(line) # Add the card ID to the current portion
                            if is_image_already_cached(dimensions='small', card_id=line): # If the image is already cached
                                card_image = get_cached_image(dimensions='small', card_id=line) # Get the cached image
                            else:
                                card_image = get_small_card_image(card_id=line) # Get the small image of the card
                            
                            if is_image_already_cached(dimensions='extra small', card_id=line):
                                card_image = get_cached_image(dimensions='extra small', card_id=line)
                            else:
                                card_image = resize_card(card_image, new_dim_preset='extra small', original_size='small') # Resize the card image because the small images are still too large
                            cache_image(card_image, dimensions='extra small', image_type='pygame surface', card_id=line) # Cache the resized image 
                            self.current_deck_sprites[current_portion].append(card_image)  # Add the card image to the current portion
                        except Exception as e:
                            print(f"Error processing card ID {line}: {e}")
                            raise
                    else:
                        raise ValueError(f"Invalid line in ydk file: {line}")
                    
                    # Calculate the time taken for the iteration
                    elapsed_time = time.time() - start_time
                    # Sleep for the remaining time to ensure the loop runs 20 times per second
                    time_to_sleep = max(0, (1 / 20) - elapsed_time)
                    time.sleep(time_to_sleep)

        except FileNotFoundError:
            print(f"File not found at: {ydk_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

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
            case State.START_MENU: update_start()
            case State.DECK_EDITOR: update_deck_builder()

    def render(self):
        self.screen.fill((0, 0, 0))

        match self.state:
            case State.START_MENU: render_start(self)
            case State.DECK_EDITOR: render_deck_builder(self)

        self.final_screen.blit(pg.transform.scale(self.screen, self.final_screen.get_rect().size), (0, 0))

if __name__ == "__main__":
    app = App()
    app.run()