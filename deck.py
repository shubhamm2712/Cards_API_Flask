import random
import string

from card import Card

alphanumeric = string.ascii_letters + string.digits

class Deck:
    def __init__(self):
        self.cards = []
        for i in range(1,14):
            for j in range(4):
                self.cards.append(Card(i,j))
        self.cardsLeft = 52
        self.players = dict()
        self.drawnOrder = []
        self.drawnSet = set()
        self.openSet = set()
        self.reshuffle()
    
    def reshuffle(self):
        random.shuffle(self.cards)
    
    def draw(self, numberOfCards):
        if numberOfCards == 0:
            return []
        if numberOfCards > self.cardsLeft:
            raise Exception("Not enough cards in deck")
        res = []
        for _ in range(numberOfCards):
            card = self.cards.pop()
            res.append(card)
            self.drawnOrder.append(card)
            self.drawnSet.add(card)
            self.openSet.add(card)
            self.cardsLeft -= 1
        return res

    def insert(self, cardValue, cardSuit, playerId = None):
        card = Card(cardValue, cardSuit)
        if card in self.openSet:
            if playerId is None:
                self.openSet.remove(card)
                self.drawnSet.remove(card)
                self.cards.append(card)
                self.cardsLeft += 1
            elif playerId not in self.players:
                raise Exception("Invalid player id")
            else:
                self.openSet.remove(card)
                self.players[playerId].append(card)
        else:
            raise Exception("Card already in deck")
    
    def createPlayers(self, numberOfPlayers):
        playerIds = set()
        for _ in range(numberOfPlayers):
            playerId = None
            retryCount = 0
            while playerId is None and playerId not in self.players and playerId not in playerIds:
                playerId = "".join(random.choices(alphanumeric, k=6))
                retryCount += 1
                if retryCount == 20:
                    raise Exception("Max players created")
            playerIds.add(playerId)
        for playerId in playerIds:
            self.players[playerId] = []
        print(playerIds)
        return list(playerIds)
    
    def getCards(self, playerId = None):
        if playerId is None:
            return self.drawnOrder
        elif playerId not in self.players:
            raise Exception("Invalid player id")
        else:
            return self.players[playerId]
    
    def hasPlayer(self, playerId):
        if playerId not in self.players:
            return False
        return True
    




        
        
    
    



