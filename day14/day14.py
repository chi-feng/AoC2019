import os
import sys
import math
import numpy as np


class Reaction:
    def __init__(self, reagents, products):
        self.reagents = reagents
        self.products = products

    def __repr__(self):
        return f"{self.reagents} => {self.products}"


def read_input(filename):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    reactions = []
    with open(filename) as file:
        lines = file.read().splitlines()
        for line in lines:
            reagents = dict()
            products = dict()
            left, right = line.split(" => ")
            reagent_tokens = left.split(", ")
            for token in reagent_tokens:
                count, label = token.split(" ")
                reagents[label] = int(count)
            product_tokens = right.split(", ")
            for token in product_tokens:
                count, label = token.split(" ")
                products[label] = int(count)
            reaction = Reaction(reagents, products)
            reactions.append(reaction)
    return reactions


def find_rx(reactions, product):
    for i, rx in enumerate(reactions):
        if product in rx.products:
            return i, rx


def part1(filename):
    reactions = read_input(filename)

    missing = {"FUEL": 1}
    intermediates = dict()

    def run_rx(rx_id, rx, n):
        nonlocal missing
        nonlocal intermediates
        # print(f'Running {n:4d} x {rx}')
        for chem, count in rx.products.items():
            intermediates[chem] = intermediates.get(chem, 0) + n * count
        for chem, count in rx.reagents.items():
            missing[chem] = missing.get(chem, 0) + n * count
        # now do some accounting
        for chem, count in missing.items():
            if count == 0:
                continue
            if chem == "ORE":
                continue
            # check if it's present in intermediate products
            if intermediates.get(chem, 0) > 0:
                missing[chem] -= min(intermediates[chem], count)
                intermediates[chem] -= min(intermediates[chem], count)

    while True:
        chems = [key for key in missing.keys() if missing[key] > 0]
        if len(chems) == 1 and chems[0] == "ORE":
            break
        for chem in chems:
            if chem == "ORE":
                continue
            count = missing[chem]
            # find reaction that produces missing chemical
            rx_id, rx = find_rx(reactions, chem)
            # how many times we need to run the reaction
            n = math.ceil(count / rx.products[chem])
            # run the reaction
            run_rx(rx_id, rx, n)

    print("missing", [(k, v) for (k, v) in missing.items() if v > 0])
    print("intermediates", [(k, v) for (k, v) in intermediates.items() if v > 0])

    simple_cost = missing["ORE"]
    budget = 1000000000000
    missing = {"FUEL": int(1.654 * budget // simple_cost)}
    fuel_created = missing["FUEL"]
    intermediates = dict()

    while True:
        chems = [key for key in missing.keys() if missing[key] > 0]
        if len(chems) == 1 and chems[0] == "ORE":
            print(budget - missing["ORE"])
            if missing["ORE"] > budget:
                break
            fuel_created += 1
            missing["FUEL"] = 1
        for chem in chems:
            if chem == "ORE":
                continue
            count = missing[chem]
            # find reaction that produces missing chemical
            rx_id, rx = find_rx(reactions, chem)
            # how many times we need to run the reaction
            n = math.ceil(count / rx.products[chem])
            # run the reaction
            run_rx(rx_id, rx, n)
    print(fuel_created - 1)


if __name__ == "__main__":
    part1("input.txt")
