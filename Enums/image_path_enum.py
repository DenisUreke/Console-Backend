from enum import Enum
from Enums.state_enum import State
from Enums.game_enum import Game

class ImagePath(Enum):
    LOBBY = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\background_image.png"
    PONG = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\team_selection_pong.png"
    TRIVIA = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\team_selection_trivia.png"
    RACER = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\team_selection_racer.png"
    TETRIS = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\team_selection_tetris.png"
    SPACE_INVADERS = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\team_selection_space_invaders.png"

    @staticmethod
    def get_image_path(game: State | Game) -> str:
        return {
            State.LOBBY: ImagePath.LOBBY.value,
            Game.TRIVIA: ImagePath.TRIVIA.value,
            Game.PONG: ImagePath.PONG.value,
            Game.TETRIS: ImagePath.TETRIS.value,
            Game.SPACE_INVADERS: ImagePath.SPACE_INVADERS.value,
            Game.RACER: ImagePath.RACER.value
        }.get(game, None)  # returns None if the state is not found
        

        