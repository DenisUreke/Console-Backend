# Api_Handler/trivia_models.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Sequence
from enum import Enum


class TriviaDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class TriviaType(str, Enum):
    text_choice = "text_choice"   # keep it simple for now


class TriviaCategory(str, Enum):
    arts_and_literature   = "arts_and_literature"
    film_and_tv           = "film_and_tv"
    food_and_drink        = "food_and_drink"
    general_knowledge     = "general_knowledge"
    geography             = "geography"
    history               = "history"
    music                 = "music"
    science               = "science"
    society_and_culture   = "society_and_culture"
    sport_and_leisure     = "sport_and_leisure"
    
CATEGORY_LABELS = {
    TriviaCategory.arts_and_literature: "Arts & Literature",
    TriviaCategory.film_and_tv: "Film & TV",
    TriviaCategory.food_and_drink: "Food & Drink",
    TriviaCategory.general_knowledge: "General Knowledge",
    TriviaCategory.geography: "Geography",
    TriviaCategory.history: "History",
    TriviaCategory.music: "Music",
    TriviaCategory.science: "Science",
    TriviaCategory.society_and_culture: "Society & Culture",
    TriviaCategory.sport_and_leisure: "Sport & Leisure",
}

@dataclass(frozen=True)
class TriviaRequest:
    limit: int = 10
    categories: Optional[Sequence[TriviaCategory]] = None
    difficulties: Optional[Sequence[TriviaDifficulty]] = None
    region: Optional[str] = None          # ISO-3166 alpha2 like "SE"
    tags: Optional[Sequence[str]] = None
    qtype: TriviaType = TriviaType.text_choice


@dataclass(frozen=True)
class TriviaQuestion:
    id: str
    category: str
    difficulty: str
    question: str
    answers: List[str]
    correct_index: int
    tags: List[str]
