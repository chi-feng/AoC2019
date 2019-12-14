import os
import math
from collections import defaultdict


def read_input(filename):
    # INPUT: "1 A, 2 B => 3 C"
    # OUTPUT: recipes["C"] = (3, {"A": 1, "B": 2})
    recipes = dict()
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, filename)) as file:
        for line in file.read().splitlines():
            left, right = line.split(" => ")
            ingredients = {
                token.split(" ")[1]: int(token.split(" ")[0])
                for token in left.split(", ")
            }
            count, product = right.split(" ")
            recipes[product] = (int(count), ingredients)
    return recipes


def get_required_ore(recipes, fuel):
    # satisfy each requirement and treat products as negative requirements
    # terminate when all requirements are satisfied
    required = defaultdict(int, {"FUEL": fuel})
    while True:
        missing = {
            chemical: required[chemical]
            for chemical in required
            if chemical != "ORE" and required[chemical] > 0
        }
        if len(missing) == 0:
            break
        for product in missing:
            product_count, ingredients_dict = recipes[product]
            n = math.ceil(missing[product] / product_count)
            required[product] -= n * product_count
            for ingredient, ingredient_count in ingredients_dict.items():
                required[ingredient] += n * ingredient_count
    return required["ORE"]


def part1(filename):
    recipes = read_input(filename)
    return get_required_ore(recipes, 1)


def part2(filename):
    recipes = read_input(filename)
    budget = 10 ** 12
    fuel = budget // get_required_ore(recipes, 1)
    while True:
        cost = get_required_ore(recipes, fuel)
        avg_cost = cost // fuel
        increment = (budget - cost) // avg_cost
        if increment == 0:
            break
        fuel += increment
    return fuel


if __name__ == "__main__":
    print(part1("input.txt"))  # 873899
    print(part2("input.txt"))  # 1893569
