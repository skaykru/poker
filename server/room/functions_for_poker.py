def check_poker_hand(hand):
    ranks = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    suits = {
        'C': 'Clubs', 'D': 'Diamonds', 'H': 'Hearts', 'S': 'Spades'
    }

    cards = [(card[:-1], card[-1]) for card in hand]

    # Перевірка на наявність покерних комбінацій

    # Функція для перевірки наявності флеш-роялю
    def has_royal_flush(cards):
        suits_count = {}
        for card in cards:
            suit = card[1]
            if suit in suits_count:
                suits_count[suit] += 1
            else:
                suits_count[suit] = 1
        return 'AAAAAK' in ''.join(sorted(card[0] for card in cards)) and 5 in suits_count.values()

    # Функція для перевірки наявності стріт-флешу
    def has_straight_flush(cards):
        suits_count = {}
        for card in cards:
            suit = card[1]
            if suit in suits_count:
                suits_count[suit] += 1
            else:
                suits_count[suit] = 1
        for suit, count in suits_count.items():
            if count >= 5:
                suited_cards = [card for card in cards if card[1] == suit]
                sorted_cards = sorted(suited_cards, key=lambda x: ranks[x[0]])
                for i in range(len(sorted_cards) - 4):
                    if all(ranks[sorted_cards[i + j][0]] == ranks[sorted_cards[i + j + 1][0]] - 1 for j in range(4)):
                        return True
        return False

    # Функція для перевірки наявності каре
    def has_four_of_a_kind(cards):
        ranks_count = {}
        for card in cards:
            rank = card[0]
            if rank in ranks_count:
                ranks_count[rank] += 1
            else:
                ranks_count[rank] = 1
        return 4 in ranks_count.values()

    # Функція для перевірки наявності фул-хаусу
    def has_full_house(cards):
        ranks_count = {}
        for card in cards:
            rank = card[0]
            if rank in ranks_count:
                ranks_count[rank] += 1
            else:
                ranks_count[rank] = 1
        return 3 in ranks_count.values() and 2 in ranks_count.values()

    # Функція для перевірки наявності флешу
    def has_flush(cards):
        suits_count = {}
        for card in cards:
            suit = card[1]
            if suit in suits_count:
                suits_count[suit] += 1
            else:
                suits_count[suit] = 1
        return 5 in suits_count.values()

    # Функція для перевірки наявності стріта
    def has_straight(cards):
        sorted_cards = sorted(cards, key=lambda x: ranks[x[0]])
        for i in range(len(sorted_cards) - 4):
            if all(ranks[sorted_cards[i + j][0]] == ranks[sorted_cards[i + j + 1][0]] - 1 for j in range(4)):
                return True
        # Перевірка спеціального випадку з тузом
        if 'A' in [card[0] for card in sorted_cards] and '2' in [card[0] for card in sorted_cards] and \
                '3' in [card[0] for card in sorted_cards] and '4' in [card[0] for card in sorted_cards] and \
                '5' in [card[0] for card in sorted_cards]:
            return True
        return False

    # Функція для перевірки наявності трійки
    def has_three_of_a_kind(cards):
        ranks_count = {}
        for card in cards:
            rank = card[0]
            if rank in ranks_count:
                ranks_count[rank] += 1
            else:
                ranks_count[rank] = 1
        return 3 in ranks_count.values()

    # Функція для перевірки наявності двох пар
    def has_two_pairs(cards):
        ranks_count = {}
        for card in cards:
            rank = card[0]
            if rank in ranks_count:
                ranks_count[rank] += 1
            else:
                ranks_count[rank] = 1
        return list(ranks_count.values()).count(2) == 2

    # Функція для перевірки наявності однієї пари
    def has_one_pair(cards):
        ranks_count = {}
        for card in cards:
            rank = card[0]
            if rank in ranks_count:
                ranks_count[rank] += 1
            else:
                ranks_count[rank] = 1
        return 2 in ranks_count.values()

    # Перевірка комбінацій по порядку, від найбільшої до найменшої
    if has_royal_flush(cards):
        return 10
    elif has_straight_flush(cards):
        return 9
    elif has_four_of_a_kind(cards):
        return 8
    elif has_full_house(cards):
        return 7
    elif has_flush(cards):
        return 6
    elif has_straight(cards):
        return 5
    elif has_three_of_a_kind(cards):
        return 4
    elif has_two_pairs(cards):
        return 3
    elif has_one_pair(cards):
        return 2
    else:
        return 1