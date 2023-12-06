from pprint import pprint as pp


def parse_input(path: str) -> [list, dict]:
    seeds = []
    mappings = {}
    names = []
    current_map = None
    with open(path) as f:
        for line in f:
            if line := line.strip():
                if line.startswith("seeds"):
                    _, seeds_string = line.split(":")
                    seeds = [
                        int(seed.strip()) for seed in seeds_string.split(" ") if seed
                    ]
                elif ":" in line:
                    current_map = line.split(" ")[0]
                    names.append(current_map)
                else:
                    mapping = [int(num.strip()) for num in line.split(" ") if num]
                    mapping = create_range(mapping)
                    if mappings.get(current_map):
                        mappings[current_map].append(mapping)
                    else:
                        mappings[current_map] = [mapping]
    return seeds, mappings, names


def create_range(mapping: list):
    destination, source, offset = mapping
    mapping = {
        "source": [source, source + offset - 1],
        "destination": [destination, destination + offset - 1],
    }
    return mapping


def find_in_map(source: int, mapping: dict):
    min_s, max_s = mapping["source"]
    min_d, max_d = mapping["destination"]
    if min_s <= source <= max_s:
        map_offset = source - min_s
        return min_d + map_offset
    else:
        return source


def find_in_map_range(source_range: tuple, mapping: dict):
    min_s, max_s = mapping["source"]
    min_d, max_d = mapping["destination"]
    seed_range_min, seed_range_max = source_range
    destinations = []
    if seed_range_max < min_s:
        pass
    elif seed_range_min > max_s:
        pass
    elif seed_range_min >= min_s and seed_range_max <= max_s:
        min_offset = seed_range_min - min_s
        max_offset = seed_range_max - max_s
        destinations.append((min_d + min_offset, max_d + max_offset))
    elif seed_range_min < min_s and seed_range_max > max_s:
        destinations.append((min_d, max_d))
        destinations.append((seed_range_min, min_s - 1))
        destinations.append((max_s + 1, seed_range_max))
    elif seed_range_min >= min_s:
        min_offset = seed_range_min - min_s
        max_offset = 0
        destinations.append((max_s + 1, seed_range_max))
        destinations.append((min_d + min_offset, max_d + max_offset))
    elif seed_range_max <= max_s:
        min_offset = 0
        max_offset = seed_range_max - max_s
        destinations.append((seed_range_min, min_s - 1))
        destinations.append((min_d + min_offset, max_d + max_offset))
    return destinations


def find_in_maps_range(source, selected_mapping):
    destinations = []
    for mapping in selected_mapping:
        if destination := find_in_map_range(source, mapping):
            destinations += destination
    if not destinations:
        destinations = [source]
    return destinations


def find_in_maps(source, selected_mapping):
    destination = source
    for mapping in selected_mapping:
        destination = find_in_map(source, mapping)
        if destination != source:
            return destination
    return destination


def apply_foo(seed_range, names, mappings, results):
    source = seed_range
    for index, name in enumerate(names):
        destinations = find_in_maps_range(source, mappings[name])
        if results["mapping_results"].get(name):
            results["mapping_results"][name] += destinations
        else:
            results["mapping_results"][name] = destinations
        # print(name)
        # print(destinations)
        # print(names[index + 1:])
        if len(destinations) > 1:
            for destination in set(destinations):
                apply(destination, names[index + 1 :], mappings, results)
        else:
            source = destinations[0]


def apply(seed_range, names, mappings, results):
    if not names:
        return

    source = seed_range
    index, name = 0, names[0]

    destinations = find_in_maps_range(source, mappings[name])
    if results["mapping_results"].get(name):
        results["mapping_results"][name] += destinations
    else:
        results["mapping_results"][name] = destinations

    for destination in set(destinations):
        apply(destination, names[index + 1 :], mappings, results)


def main(path: str):
    results = {"seeds_paths": {}, "mapping_results": {}}
    seeds, mappings, names = parse_input(path)
    for seed in seeds:
        source = seed
        for name in names:
            destination = find_in_maps(source, mappings[name])
            if results["seeds_paths"].get(seed):
                results["seeds_paths"][seed].append(destination)
            else:
                results["seeds_paths"][seed] = [destination]
            if results["mapping_results"].get(name):
                results["mapping_results"][name].append(destination)
            else:
                results["mapping_results"][name] = [destination]
            source = destination

    results = {"seeds_paths": {}, "mapping_results": {}}

    seed_ranges = []
    for index, seed in enumerate(seeds):
        if index % 2 == 0:
            try:
                seed_ranges.append((seed, seed + seeds[index + 1] - 1))
            except IndexError:
                pass
    for seed_range in seed_ranges:
        apply(seed_range, names, mappings, results)

    print(min(set(results["mapping_results"]["humidity-to-location"])))
    # pp(results["mapping_results"]["humidity-to-location"])
    pp(set(sorted(results["mapping_results"]["humidity-to-location"])[0:20]))


main("test_input.txt")
main("input.txt")
