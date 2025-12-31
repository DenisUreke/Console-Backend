# Api_Handler/trivia_gateway.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
import random

from Api_Handler.api_caller import ApiCaller, ApiOk, ApiErr
from Games.Trivia.Models.trivia_models import TriviaRequest, TriviaQuestion, TriviaCategory, TriviaDifficulty


class TriviaGatewayError(Exception):
    pass


class TriviaGateway:
    def __init__(self, api: ApiCaller, rng: Optional[random.Random] = None) -> None:
        self.api = api
        self.rng = rng or random.Random()

    def get_questions(self, req: TriviaRequest) -> List[TriviaQuestion]:
        params = self._build_params(req)

        res = self.api.get_json(path="/v2/questions", params=params)
        if isinstance(res, ApiErr):
            raise TriviaGatewayError(f"Trivia API error: {res.error_type} {res.status_code} {res.message}")

        if not isinstance(res.data, list):
            raise TriviaGatewayError("Trivia API returned unexpected JSON shape (expected list).")

        return [self._parse_question(q) for q in res.data]

    def _build_params(self, req: TriviaRequest) -> Dict[str, Any]:
        # Validate basics
        limit = int(req.limit)
        if limit < 1:
            limit = 1
        if limit > 50:  # keep sane; API supports higher, but this is a good guard
            limit = 50

        params: Dict[str, Any] = {
            "limit": limit,
            "types": req.qtype.value,
        }

        if req.categories:
            params["categories"] = [c.value for c in req.categories]

        if req.difficulties:
            params["difficulties"] = [d.value for d in req.difficulties]

        if req.region:
            params["region"] = req.region.upper()

        if req.tags:
            # API expects comma-separated; ApiCaller will join lists with commas
            params["tags"] = [t.strip() for t in req.tags if t and t.strip()]

        return params

    def _parse_question(self, q: Dict[str, Any]) -> TriviaQuestion:
        qid = str(q.get("id", ""))
        category = str(q.get("category", ""))
        difficulty = str(q.get("difficulty", ""))

        question_text = ""
        question_obj = q.get("question")
        if isinstance(question_obj, dict):
            question_text = str(question_obj.get("text", ""))
        else:
            question_text = str(q.get("question", ""))

        correct = str(q.get("correctAnswer", ""))
        incorrect = q.get("incorrectAnswers", [])
        if not isinstance(incorrect, list):
            incorrect = []

        answers = [correct] + [str(x) for x in incorrect]
        # Shuffle answers so correct isn't always index 0
        self.rng.shuffle(answers)

        try:
            correct_index = answers.index(correct)
        except ValueError:
            # Shouldn't happen, but keep safe
            correct_index = 0

        tags = q.get("tags", [])
        if not isinstance(tags, list):
            tags = []
        tags = [str(t) for t in tags]

        return TriviaQuestion(
            id=qid,
            category=category,
            difficulty=difficulty,
            question=question_text,
            answers=answers,
            correct_index=correct_index,
            tags=tags,
        )

    '''from Games.Trivia.Gateway.trivia_gateway import TriviaGateway
        from Api_Handler.trivia_gateway import TriviaGateway
        from Api_Handler.trivia_models import TriviaRequest, TriviaCategory, TriviaDifficulty

        api = ApiCaller(base_url="https://the-trivia-api.com", timeout_seconds=6.0)
        gateway = TriviaGateway(api)

        req = TriviaRequest(
            limit=10,
            categories=[TriviaCategory.sport_and_leisure],
            difficulties=[TriviaDifficulty.medium],
            region="SE",
            tags=["football"],
        )

        questions = gateway.get_questions(req)

        # game loop uses:
        # questions[i].question
        # questions[i].answers
        # questions[i].correct_index
    '''