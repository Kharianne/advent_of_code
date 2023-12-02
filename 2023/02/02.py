def parse_input(path: str) -> dict:
    with open(path) as f:
        games = {}
        for line in f:
            game, result = line.strip().split(":")
            _, number = game.split(" ")
            grabs = result.split(";")
            games[number] = {}
            for grab in grabs:
                color_tuples = [(pair.strip().split(" ")[1],
                                 int(pair.strip().split(" ")[0])) for pair in
                                grab.strip().split(",")]
                if not games[number]:
                    games[number].update(dict(color_tuples))
                else:
                    for color, value in dict(color_tuples).items():
                        if current_value := games[number].get(color):
                            if current_value < value:
                                games[number][color] = value
                        else:
                            games[number][color] = value
        return games


def compare(rules: dict, path: str) -> int:
    games = parse_input(path)
    print(games)
    game_sum = 0
    for game, cubes in games.items():
        count_game = True
        for color, count in rules.items():
            if max_count := cubes.get(color):
                if max_count > count:
                    count_game = False
                    break
            else:
                count_game = False
                break

        if count_game:
            game_sum += int(game)
    print("Game sum", game_sum)
    greater_sum = 0
    for _, values in games.items():
        greater_sum += values.values()
    print("Greater sum", greater_sum)
    return game_sum

rules = {
    "red": 12,
    "green": 13,
    "blue": 14
}
compare(rules, "test_input.txt")
compare(rules, "input.txt")