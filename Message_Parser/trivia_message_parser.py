import json
from dataclasses import asdict
from Games.Trivia.Models.trivia_send_to_front_end import PossibleMovesData

class TriviaMessageParser():
    def __init__(self):
        pass
    
    def get_parsed_trivia_questions(self, questions):
        question_list = []
        for q in questions:
            question_list.append({
                "id": q.id,
                "category": q.category,
                "difficulty": q.difficulty,
                "question": q.question,
                "answers": q.answers,
                "correct_index": q.correct_index,
                "tags": q.tags
            })

        message = {
            "type": "trivia",
            "data": {
                "phase": "QUESTION",
                "topic": "show_question",
                "payload": {
                    "questions": question_list,
                    "amount_of_questions": len(questions)
                }
            }
        }

        return json.dumps(message)
    
    def get_possible_moves_message(self, possible_moves_data: PossibleMovesData):
        message = {
            "type": "trivia",
            "data": {
                "phase": "CHOOSE_MOVE",
                "topic": "possible_moves",
                "payload": asdict(possible_moves_data)
            }
        }
        return json.dumps(message)



        