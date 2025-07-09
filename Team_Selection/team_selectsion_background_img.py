from Enums.state_enum import State

def get_background_image(game: State)-> str:
    
    #Get the background image path based on the selected game.
    match game:
        case State.TEAM_SELECTION:
            return r"Assets\Images\team_selection_pong.png"
        case _:
            raise ValueError(f"Unsupported game: {game}")