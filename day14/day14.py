import os
import math


def read_input(filename):
    recipes = dict()  # product -> (ingredients, nproducts)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    with open(filename) as file:
        lines = file.read().splitlines()
        for line in lines:
            ingredients = dict()
            left, right = line.split(" => ")
            for token in left.split(", "):
                count, label = token.split(" ")
                ingredients[label] = int(count)
            count, product = right.split(" ")
            recipes[product] = (int(count), ingredients)
    return recipes


def get_required_ore(recipes, fuel):
    required = {"FUEL": fuel}
    while True:
        missing = {
            chemical: required[chemical]
            for chemical in required
            if chemical != "ORE" and required[chemical] > 0
        }
        if len(missing) == 0:
            break  # we're done if the only requirement left is ORE
        for product in missing:
            product_count, ingredients_dict = recipes[product]
            n = math.ceil(missing[product] / product_count)
            required[product] -= n * product_count
            for ingredient, ingredient_count in ingredients_dict.items():
                required[ingredient] = (
                    required.get(ingredient, 0) + n * ingredient_count
                )
    return required["ORE"]


def part1(filename):
    recipes = read_input(filename)
    return get_required_ore(recipes, 1)


def part2(filename):
    recipes = read_input(filename)
    budget = 10 ** 12
    lb = get_required_ore(recipes, 1)
    # first find lower and upper bound
    a = lb
    b = 2 * lb
    while get_required_ore(recipes, b) < budget:
        a = b
        b *= 2
    # postcondition: a is below budget, b is above budget
    # binary search to find a, b closest to budget
    while b - a > 1:
        half = a + (b - a) // 2
        if get_required_ore(recipes, half) > budget:
            b = half
        else:
            a = half
    return a


if __name__ == "__main__":
    print(part1("input.txt"))  # 873899
    print(part2("input.txt"))  # 1893569
