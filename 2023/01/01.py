import re

map_numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def get_values(calibration_line: str) -> int:
    number = []
    for char in calibration_line:
        try:
            int(char)
            number.append(char)
        except ValueError:
            continue
    if len(number) > 2:
        return int(''.join([number[0], number[-1]]))
    else:
        return 0


def get_corrected_values(line: str) -> int:
    positions = {
    }
    for key, value in map_numbers.items():
        occurrences = [m.start() for m in re.finditer(key, line)]
        for occurrence in occurrences:
            positions[occurrence] = str(value)
    for i, char in enumerate(line):
        try:
            int(char)
            positions[i] = char
        except ValueError:
            continue

    s = sorted(positions.items())
    return int(''.join([s[0][1], s[-1][1]]))


def read_input(path: str) -> list:
    with open(path) as f:
        return f.readlines()


def get_calibration_sum(input_path: str):
    calibration_sum = 0
    for line in read_input(input_path):
        calibration_sum += get_values(line)
    print("Calibration sum:", calibration_sum)
    corrected_sum = 0
    for line in read_input(input_path):
        corrected_sum += get_corrected_values(line)
    print("Corrected sum:", corrected_sum)


get_calibration_sum("test_input.txt")
get_calibration_sum("input.txt")
get_calibration_sum("test_input_2.txt")
get_calibration_sum("input.txt")
