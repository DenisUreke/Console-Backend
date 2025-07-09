from enum import Enum
from Enums.state_enum import State

class ImagePath(Enum):
    LOBBY = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\background_image.png"
    TEAM_SELECTION = r"C:\Users\ureke\Documents\GitHub\Console-Backend\Assets\Images\team_selection_pong.png"

    @staticmethod
    def get_image_path(game: State) -> str:
        return {
            State.TEAM_SELECTION: ImagePath.TEAM_SELECTION.value,
            State.LOBBY: ImagePath.LOBBY.value
        }.get(game, None)  # returns None if the state is not found

        