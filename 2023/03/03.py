from pprint import pprint as pp


def validation(parts, coords):
    try:
        print("COORDS:", coords)
        value = parts[coords[0]][coords[1]]
        parts[coords[0]][coords[1]] = 0
        if isinstance(value, int):
            print("TO SUM: ", value)
            return value
        else:
            return 0
    except IndexError:
        return 0


def parse_input(path: str) -> list:
    with open(path) as f:
        part_list = []
        special_coords = []
        for line_num, line in enumerate(f):
            print(line.strip())
            line_parsed = []
            for char_num, char in enumerate(line.strip()):
                if char == ".":
                    line_parsed.append(".")
                else:
                    try:
                        int(char)
                        line_parsed.append(char)
                    except ValueError:
                        line_parsed.append(char)
                        special_coords.append((line_num, char_num))

            line_merged = []
            curr, previous = None, None
            for char_num, char in enumerate(line_parsed):
                counter = 0
                num_string = ""
                try:
                    int(char)
                    num_string += char
                    is_number = True
                    curr = True
                except ValueError:
                    curr = False
                    is_number = False
                if not previous and is_number:
                    while is_number:
                        counter += 1
                        try:
                            int(line_parsed[char_num + counter])
                            num_string += line_parsed[char_num + counter]
                        except ValueError:
                            is_number = False
                        except IndexError:
                            break

                    for i in range(counter):
                        line_merged.append(int(num_string))
                else:
                    if not curr:
                        line_merged.append(char)
                previous = curr
            part_list.append(line_merged)
    pp(part_list)
    _sum = 0
    gear_sum = 0
    for x, y in special_coords:
        print("X:", x)
        print("Y", y)
        print("CHAR:", part_list[x][y])
        add_to_sum = []
        add_to_sum.append(validation(part_list, [x - 1, y - 1]))
        add_to_sum.append(validation(part_list, [x - 1, y + 1]))
        add_to_sum.append(validation(part_list, [x - 1, y]))
        add_to_sum.append(validation(part_list, [x, y - 1]))
        add_to_sum.append(validation(part_list, [x, y + 1]))
        add_to_sum.append(validation(part_list, [x + 1, y - 1]))
        add_to_sum.append(validation(part_list, [x + 1, y + 1]))
        add_to_sum.append(validation(part_list, [x + 1, y]))

        gear_add_to_sum = list(set(add_to_sum))
        gear_add_to_sum.remove(0)
        if len(gear_add_to_sum) == 2 and part_list[x][y] == "*":
            gear_sum += gear_add_to_sum[0] * gear_add_to_sum[1]
        _sum += sum(list(set(add_to_sum)))

        print("+++++++++++++++++")

    print("SUM:", _sum)
    print("GEAR SUM", gear_sum)


# coords
# line above: (i-1, j-1), (i-1, j+1), (i-1, j)
# current line: (i, j-1), (i, j+1)
# line bellow: (i+1, j-1), (i+1, j+1), (i+1, j)

# parse_input("test_input.txt")
parse_input("input.txt")
