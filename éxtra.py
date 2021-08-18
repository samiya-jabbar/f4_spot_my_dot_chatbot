import json

result = {
    "message": "Error logging in for user sana123@gmail.com",
    "status": 'Error: [Errno 400 Client Error: Bad Request for url: https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=xxxx] {\n  "error": {\n    "code": 400,\n    "message": "EMAIL_NOT_FOUND",\n    "errors": [\n      {\n      "message": "EMAIL_NOT_FOUND",\n        "domain": "global",\n        "reason": "invalid"\n      }\n    ]\n  }\n}\n',
}

data = json.loads("{" + result["status"].split("] {", maxsplit=1)[-1])
for error in data["error"]["errors"]:
    print(error["message"])
    print(error["reason"])