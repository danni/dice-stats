from copy import copy
from functools import reduce

import numpy as np


class Die(object):
    def __init__(self, sides):
        self.multiplier = 1
        self.sides = sides

    def __repr__(self):
        return 'd%i' % self.sides

    def __mul__(self, other):
        assert isinstance(other, int), "Must multiply dice by integers"

        return Dice(other, self.sides)

    def __add__(self, other):
        if isinstance(other, Die) and self.sides == other.sides:
            return Dice(self.multiplier + other.multiplier, self.sides)
        else:
            return DiceGroup() + self + other

    def probability(self):
        scores = np.array(range(1, self.sides + 1))
        onedice = totaldice = np.ones(self.sides) / self.sides

        return (scores, onedice)


class Dice(Die):
    def __init__(self, multiplier, sides):
        self.multiplier = multiplier
        self.sides = sides

    def __repr__(self):
        return '%id%i' % (self.multiplier, self.sides)

    def probability(self):
        scores = np.array(range(self.multiplier,
                                self.multiplier * self.sides + 1))
        onedice = totaldice = np.ones(self.sides) / self.sides

        for _ in range(self.multiplier - 1):
            totaldice = np.convolve(totaldice, onedice)

        return (scores, totaldice)


class DiceGroup(object):
    def __init__(self):
        self.dice = {}
        self.static = 0

    def __repr__(self):
        string = ' + '.join(map(str, self.dice.values()))

        if self.static > 0:
            string += ' + %d' % self.static
        elif self.static < 0:
            string += ' - %d' % self.static

        return string

    def __add__(self, other):
        self = copy(self)

        if isinstance(other, DiceGroup):
            for dice in other.dice.values():
                self += dice
        elif isinstance(other, Die):
            try:
                self.dice[other.sides] += other
            except KeyError:
                self.dice[other.sides] = other
        elif isinstance(other, int):
            self.static += other
        else:
            raise NotImplementedError("Unknown type to add")

        return self

    def probability(self):

        scores, probabilities = zip(*(dice.probability()
                                    for dice in self.dice.values()))

        lowest_score = sum(score[0] for score in scores)
        highest_score = sum(score[-1] for score in scores)
        scores = np.array(range(lowest_score, highest_score + 1)) + self.static

        probabilities = reduce(np.convolve, probabilities)

        return (scores, probabilities)
