from collections import Counter
from copy import deepcopy

CARD_VALUE_MAPPING = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Hand:
    def __init__(self, hand, bid):
        self.hand = hand
        self.cards = list(hand)
        self.bid = bid
        self.type = Hand.evaluate_hand(hand)
        self.mapping = deepcopy(CARD_VALUE_MAPPING)

    def __repr__(self):
        return f"HAND: {self.hand} - TYPE: {self.type}"

    def __eq__(self, other):
        if self.type == other.type and self.cards == other.cards:
            return 1
        else:
            return 0

    def __lt__(self, other):
        if self.type > other.type:
            return 0
        elif self.type == other.type:
            for x in range(len(self.cards)):
                if self.mapping.get(self.cards[x]) == self.mapping.get(other.cards[x]):
                    continue
                elif self.mapping.get(self.cards[x]) > self.mapping.get(other.cards[x]):
                    return 0
                else:
                    return 1
        else:
            return 1

    def __gt__(self, other):
        if self.type < other.type:
            return 0
        elif self.type == other.type:
            for x in range(len(self.cards)):
                if self.mapping.get(self.cards[x]) == self.mapping.get(other.cards[x]):
                    continue
                elif self.mapping.get(self.cards[x]) > self.mapping.get(other.cards[x]):
                    return 1
                else:
                    return 0
        else:
            return 1

    @staticmethod
    def evaluate_hand(hand: str) -> int:
        sorted_cards = sorted(Counter(hand).items(), key=lambda x: x[1], reverse=True)
        if (highest_value := sorted_cards[0][1]) == 5:
            # Five of a kind
            return 7
        elif highest_value == 4:
            # Four of a kind
            return 6
        elif highest_value == 3:
            if len(sorted_cards) == 2:
                # Full house
                return 5
            else:
                # Three of a kind
                return 4
        elif highest_value == 2:
            if len(sorted_cards) == 3:
                # Two pair
                return 3
            else:
                # One pair
                return 2
        else:
            # High card
            return 1


class JokerHand(Hand):
    def __init__(self, hand, bid):
        super().__init__(hand, bid)
        self.mapping["J"] = 1
        self.type = JokerHand.evaluate_hand(hand)

    @staticmethod
    def evaluate_hand(hand: str) -> int:
        if "J" in hand:
            reduced = Counter(hand)
            number_of_j = reduced.get("J")
            sorted_cards = sorted(reduced.items(), key=lambda x: x[1], reverse=True)
            highest_value, card = sorted_cards[0][1], sorted_cards[0][0]
            if highest_value == 5 or highest_value == 4:
                # Five of a kind
                return 7
            elif highest_value == 3:
                if len(sorted_cards) == 2:
                    return 7
                else:
                    return 6
            elif highest_value == 2:
                if len(sorted_cards) == 3:
                    if number_of_j == 2:
                        return 6
                    else:
                        return 5
                else:
                    return 4
            else:
                # One pair
                return 2
        else:
            return Hand.evaluate_hand(hand)


def parse_input(path: str) -> dict:
    hands = {}
    with open(path) as f:
        for line in f:
            hand, bid = [pair for pair in line.strip().split(" ")]
            hands[hand.strip()] = int(bid.strip())
    return hands


def main(input_file: str):
    hands = parse_input(input_file)
    rankings = []
    joker_rankings = []
    for key, value in hands.items():
        rankings.append(Hand(key, value))
        joker_rankings.append(JokerHand(key, value))
    s_rankings = sorted(rankings)
    s_joker_rankings = sorted(joker_rankings)
    _sum = 0
    for rank, hand in enumerate(s_rankings):
        _sum += (rank + 1) * hand.bid
    print(_sum)

    _sum = 0
    for rank, hand in enumerate(s_joker_rankings):
        _sum += (rank + 1) * hand.bid
    print(_sum)


main("test_input.txt")
main("input.txt")
