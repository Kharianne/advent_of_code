from math import sqrt, ceil, floor


def parse_input(path: str) -> [list, list]:
    with open(path) as f:
        data = []
        long_race_data = []
        for line in f:
            _, races = line.strip().split(":")
            data.append([int(num.strip()) for num in races.strip().split(" ") if num])
            long_race_data.append(
                int(
                    "".join(
                        [str(num.strip()) for num in races.strip().split(" ") if num]
                    )
                )
            )

        return list(zip(data[0], data[1])), long_race_data


def main(path: str):
    races, long_race_data = parse_input(path)
    diffs = []
    for length, distance in races:
        x = ceil((length + sqrt(length**2 - 4 * distance)) / 2)
        x_2 = floor((length - sqrt(length**2 - 4 * distance)) / 2)
        diffs.append(x - x_2 - 1)
    _sum = 1
    for diff in diffs:
        _sum *= diff
    print(_sum)

    lr_length, lr_distance = long_race_data
    x = ceil((lr_length + sqrt(lr_length**2 - 4 * lr_distance)) / 2)
    x_2 = floor((lr_length - sqrt(lr_length**2 - 4 * lr_distance)) / 2)
    print(x - x_2 - 1)


main("test_input.txt")
main("input.txt")
