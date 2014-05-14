import numpy as np


class Die(object):
    def __init__(self, sides):
        self.sides = sides

    def __repr__(self):
        return 'd%i' % self.sides

    def __mul__(self, other):
        assert isinstance(other, int), "Must multiply dice by integers"

        return Dice(other, self.sides)

    def probability(self):
        scores = np.array(range(1, self.sides + 1))
        onedice = totaldice = np.ones(self.sides) / self.sides

        return (scores, onedice)


class Dice(object):
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
