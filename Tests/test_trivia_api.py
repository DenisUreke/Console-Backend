import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Api_Handler.api_caller import ApiCaller, ApiOk

api = ApiCaller(
    base_url="https://the-trivia-api.com",
    timeout_seconds=6.0,
)

res = api.get_json(
    path="/v2/questions",
    params={
        "limit": 5,
        "categories": "sport_and_leisure",
        "difficulties": "medium",
        "region": "SE",
        "types": "text_choice",
    },
)

if isinstance(res, ApiOk):
    print("OK", res.status_code, res.elapsed_ms, "ms")
    print(res.data[:1])
else:
    print("ERR", res.error_type, res.status_code, res.message)
