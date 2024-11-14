import random
import string

from flask import Flask, request

from deck import Deck

alphanumeric = string.ascii_letters + string.digits
decks: dict[str, Deck] = dict()

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to cards api"

@app.route("/shuffled-deck", methods=["GET"])
def shuffled_deck():
    try:
        tryCount = 0
        deckId = None
        while True:
            deckId = "".join(random.choices(alphanumeric, k=10))
            if deckId not in decks:
                break
            tryCount += 1
            if tryCount >= 20:
                return {"error": "No more deck ids available"}, 500
        decks[deckId] = Deck()
        return {"deck_id": deckId}
    except Exception as e:
        return {"error": "Exception "+str(e)}, 400

@app.route("/draw-cards/<deckId>/<int:numberOfCards>", methods=["GET"])
def draw_cards(deckId, numberOfCards: int):
    if deckId not in decks:
        return {"error": "Invalid deckId"}, 400
    try:
        res = decks[deckId].draw(numberOfCards)
        return {"Result": [card.toJson() for card in res]}
    except Exception as e:
        return {"error": "Exception "+str(e)}, 400

@app.route("/reshuffle-deck/<deckId>", methods=["GET"])
def reshuffle_deck(deckId):
    if deckId not in decks:
        return {"error": "Invalid deckId"}, 400
    try:
        decks[deckId].reshuffle()
        return {"Result": True}
    except Exception as e:
        return {"error": "Exception "+str(e)}, 400

@app.route("/insert-cards/<deckId>", methods=["POST"])
def insert_cards(deckId):
    if deckId not in decks:
        return {"error": "Invalid deckId"}, 404
    try:
        data = request.get_json()
        cards = data["cards"]
        invalid_cards = []
        for card in cards:
            try:
                decks[deckId].insert(card["value"], card["suit"])
            except Exception as e:
                invalid_cards.append(card)
        if not invalid_cards:
            return {"Result": "added all cards"}
        return {"Invalid cards": invalid_cards}
    except Exception as e:
        return {"error": "Exception "+str(e)}

@app.route("/players/<deckId>/<int:numberOfPlayers>", methods=["GET","POST"])
def create_players(deckId, numberOfPlayers: int):
    if deckId not in decks:
        return {"error": "Invalid deckId"}, 400
    try:
        players = decks[deckId].createPlayers(numberOfPlayers)
        return {"Result": players}
    except Exception as e:
        return {"error": "Exception "+str(e)}, 400

@app.route("/insert-cards/<deckId>/players/<playerId>", methods=["POST"])
def insert_cards_player(deckId, playerId):
    if deckId not in decks or not decks[deckId].hasPlayer(playerId):
        return {"error": "Invalid deckId or playerId"}, 400
    try:
        data = request.get_json()
        cards = data["cards"]
        invalid_cards = []
        for card in cards:
            try:
                decks[deckId].insert(card["value"], card["suit"],playerId)
            except Exception as e:
                invalid_cards.append(card)
        if not invalid_cards:
            return {"Result": "added all cards"}
        return {"Invalid cards": invalid_cards}
    except Exception as e:
        return {"error": "Exception "+str(e)}

@app.route("/cards/<deckId>", methods = ["GET"])
def get_cards_deck(deckId):
    if deckId not in decks:
        return {"error": "Invalid deckId"}, 400
    try:
        res = decks[deckId].getCards()
        return {"Result": [card.toJson() for card in res]}
    except Exception as e:
        return {"error": "Exception "+str(e)}, 400

@app.route("/cards/<deckId>/players/<playerId>", methods = ["POST"])
def get_cards_players(deckId, playerId):
    if deckId not in decks or not decks[deckId].hasPlayer(playerId):
        return {"error": "Invalid deckId or playerId"}, 400
    try:
        res = decks[deckId].getCards(playerId)
        return {"Result": [card.toJson() for card in res]}
    except Exception as e:
        return {"error": "Exception "+str(e)}, 400
    






