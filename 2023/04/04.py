def parse_input(path: str):
    winning_num = []
    numbers = []
    with open(path) as f:
        for line in f:
            _, card_values = line.strip().split(":")
            w_n, n = card_values.strip().split("|")
            winning_num.append(
                [int(num.strip()) for num in w_n.strip().split(" ") if num]
            )
            numbers.append([int(num.strip()) for num in n.strip().split(" ") if num])
    return winning_num, numbers


def get_card_worth(winning_num, numbers):
    points = 0
    for number in numbers:
        if number in winning_num:
            if points == 0:
                points = 1
            else:
                points *= 2
    return points


def get_number_of_copies(winning_num, numbers):
    copies_dict = {}
    for card_number, card in enumerate(numbers):
        copies = 0
        for number in card:
            if number in winning_num[card_number]:
                copies += 1
        copies_dict[card_number + 1] = copies
    cards_dict = {}
    for card, copies in copies_dict.items():
        if cards_dict.get(card):
            cards_dict[card] += 1
        else:
            cards_dict[card] = 1
        for copy in range(1, copies + 1):
            if cards_dict.get(copy + card):
                cards_dict[copy + card] += 1
            else:
                cards_dict[copy + card] = 1
        copies_of_card = cards_dict[card]
        if copies_of_card > 1:
            for copy_of_card in range(1, copies_of_card):
                for copy in range(1, copies + 1):
                    if cards_dict.get(copy + card):
                        cards_dict[copy + card] += 1
                    else:
                        cards_dict[copy + card] = 1
    print(copies_dict)
    print(cards_dict)
    print(sum(cards_dict.values()))


def main(path):
    winning_num, numbers = parse_input(path)
    sum_points = 0
    for card_number, card in enumerate(numbers):
        sum_points += get_card_worth(winning_num[card_number], card)
    copies = get_number_of_copies(winning_num, numbers)
    print("POINTS:", sum_points)


main("test_input.txt")
main("input.txt")
