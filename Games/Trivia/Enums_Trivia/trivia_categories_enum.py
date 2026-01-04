from enum import Enum
from Games.Trivia.Models.trivia_models import TriviaCategory

class TPWedgeCategory(str, Enum):
    GEOGRAPHY = "geography"
    HISTORY = "history"
    SCIENCE = "science"
    ARTS = "arts"
    ENTERTAINMENT = "entertainment"
    SPORTS_AND_LEISURE = "sports_and_leisure"
    
TP_WEDGE_LABELS = {
    TPWedgeCategory.GEOGRAPHY: "Geography",
    TPWedgeCategory.HISTORY: "History",
    TPWedgeCategory.SCIENCE: "Science",
    TPWedgeCategory.ARTS: "Arts",
    TPWedgeCategory.ENTERTAINMENT: "Entertainment",
    TPWedgeCategory.SPORTS_AND_LEISURE: "Sports & Leisure",
}

API_TO_WEDGE = {
    TriviaCategory.arts_and_literature: TPWedgeCategory.ARTS,
    TriviaCategory.society_and_culture: TPWedgeCategory.ARTS,

    TriviaCategory.film_and_tv: TPWedgeCategory.ENTERTAINMENT,
    TriviaCategory.music: TPWedgeCategory.ENTERTAINMENT,
    TriviaCategory.food_and_drink: TPWedgeCategory.ENTERTAINMENT,
    TriviaCategory.general_knowledge: TPWedgeCategory.ENTERTAINMENT,

    TriviaCategory.geography: TPWedgeCategory.GEOGRAPHY,
    TriviaCategory.history: TPWedgeCategory.HISTORY,
    TriviaCategory.science: TPWedgeCategory.SCIENCE,
    TriviaCategory.sport_and_leisure: TPWedgeCategory.SPORTS_AND_LEISURE,
}

WEDGE_TO_API = {
    TPWedgeCategory.ARTS: [
        TriviaCategory.arts_and_literature,
        TriviaCategory.society_and_culture,
    ],
    TPWedgeCategory.ENTERTAINMENT: [
        TriviaCategory.film_and_tv,
        TriviaCategory.music,
        TriviaCategory.food_and_drink,
        TriviaCategory.general_knowledge,
    ],
    TPWedgeCategory.GEOGRAPHY: [TriviaCategory.geography],
    TPWedgeCategory.HISTORY: [TriviaCategory.history],
    TPWedgeCategory.SCIENCE: [TriviaCategory.science],
    TPWedgeCategory.SPORTS_AND_LEISURE: [TriviaCategory.sport_and_leisure],
}

class WedgeColor(str, Enum):
    YELLOW = "yellow"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    PINK = "pink"
    ORANGE = "orange"
    
WEDGE_CATEGORY_TO_COLOR = {
    TPWedgeCategory.HISTORY: WedgeColor.YELLOW,
    TPWedgeCategory.GEOGRAPHY: WedgeColor.BLUE,
    TPWedgeCategory.SCIENCE: WedgeColor.GREEN,
    TPWedgeCategory.ARTS: WedgeColor.PURPLE,
    TPWedgeCategory.ENTERTAINMENT: WedgeColor.PINK,
    TPWedgeCategory.SPORTS_AND_LEISURE: WedgeColor.ORANGE,
}

COLOR_TO_WEDGE_CATEGORY = {
    WedgeColor.YELLOW: TPWedgeCategory.HISTORY,
    WedgeColor.BLUE: TPWedgeCategory.GEOGRAPHY,
    WedgeColor.GREEN: TPWedgeCategory.SCIENCE,
    WedgeColor.PURPLE: TPWedgeCategory.ARTS,
    WedgeColor.PINK: TPWedgeCategory.ENTERTAINMENT,
    WedgeColor.ORANGE: TPWedgeCategory.SPORTS_AND_LEISURE,
}



