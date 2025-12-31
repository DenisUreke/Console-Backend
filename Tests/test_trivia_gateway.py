from Api_Handler.api_caller import ApiCaller
from Games.Trivia.Gateway.trivia_gateway import TriviaGateway
from Games.Trivia.Models.trivia_models import (
    TriviaRequest,
    TriviaCategory,
    TriviaDifficulty,
)

def main():
    api = ApiCaller(
        base_url="https://the-trivia-api.com",
        timeout_seconds=6.0,
    )
    gateway = TriviaGateway(api)

    req = TriviaRequest(
        limit=5,
        categories=[TriviaCategory.sport_and_leisure],
        difficulties=[TriviaDifficulty.medium],
        region="SE",
        tags=["football"],
    )

    questions = gateway.get_questions(req)

    print(f"Got {len(questions)} questions\n")
    for i, q in enumerate(questions, start=1):
        print(f"{i}) [{q.category} | {q.difficulty}] {q.question}")
        for idx, ans in enumerate(q.answers):
            marker = " ✅" if idx == q.correct_index else ""
            print(f"   {idx}: {ans}{marker}")
        print()

if __name__ == "__main__":
    main()
