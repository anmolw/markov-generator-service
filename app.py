import config
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json, text
from typing import Union
import asyncio
from json import dumps, loads
from markovhandler import InitializationError, MarkovHandler

app = Sanic(name="MarkovService")
markov = MarkovHandler()

LISTEN_PORT = 8000


# @app.on_response
# def check_api_token(request: Request, response: HTTPResponse) -> Union[HTTPResponse, None]:
#     test_msg = "Authorization failed"
#     auth_key = request.headers.get("Authorization")
#     if auth_key is None or auth_key != config.auth_key:
#         return json(status=401, body=test_msg, dumps=dumps)


@app.route("/generate")
async def generate(request) -> HTTPResponse:
    try:
        result = await markov.generate()
        if result is not None:
            response = {"result": result}
            return json(response, dumps=dumps)
        else:
            response = {"error": "Failed to generate a sentence"}
            return json(response, status=500, dumps=dumps)

    except InitializationError:
        response = {
            "error": "Model not initialized",
        }
        return json(response, status=500, dumps=dumps)


@app.route("/add", methods=("POST",))
async def add_to_corpus(request: Request) -> HTTPResponse:
    print(request.json)
    if "text" not in request.json or not isinstance(request.json["text"], str):
        response = {"error": "No text provided"}
        return json(response, status=500, dumps=dumps)
    try:
        await markov.add(request.json["text"])
        response = {"status": "Success"}
        return json(response, status=200, dumps=dumps)
    except Exception as e:
        print(e)


@app.route("/info")
async def info(request) -> HTTPResponse:
    return


@app.route("/clear")
async def clear(request) -> HTTPResponse:
    return


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=LISTEN_PORT)
