import json

suits = ["HEARTS", "CLUBS", "DIAMONDS", "SPADES"]
suits_num = {"HEARTS": 0, "CLUBS": 1, "DIAMONDS": 2, "SPADES": 3}
str_cards = {1: "ACE", 11: "JACK", 12: "QUEEN", 13: "KING"}
cards_str = {"ACE": 1, "JACK": 11, "QUEEN": 12, "KING": 13}

class Card:
    def __init__(self,value,suit):
        if type(suit) is str:
            if suit not in suits:
                raise Exception("Invalid suit")
        elif type(suit) is int:
            if suit<0 or suit>3:
                raise Exception("Invalid suit")
            suit = suits[suit]
        else:
            raise Exception("Invalid suit")
        if type(value) is str:
            if value.isnumeric():
                value = int(value)
            elif value in cards_str:
                value = cards_str[value]
            else:
                raise Exception("Invalid suit")
        if type(value) is int:
            if value < 1 or value > 13:
                raise Exception("Invalid value")
            if value in str_cards:
                value = str_cards[value]
            else:
                value = str(value)
        else:
            raise Exception("Invalid value")
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return f"Card: {self.value} of {self.suit}"
    
    def __repr__(self):
        return f"({self.value}, {self.suit})"
    
    def __hash__(self):
        value = self.value
        if value.isnumeric():
            value = int(value)
        else:
            value = cards_str[value]
        suit = suits_num[self.suit]
        return (suit*13)+value
    
    def toJson(self):
        return {
            "value": self.value,
            "suit": self.suit
        }