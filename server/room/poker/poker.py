import random

def gen():  # Генерирует колоду карт
    ranks = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    suits = {
        'C': 'Clubs', 'D': 'Diamonds', 'H': 'Hearts', 'S': 'Spades'
    }
    deck=[]
    for i in suits:
        for j in ranks:
            deck.append(str(j + i))
    random.shuffle(deck)
    return deck



