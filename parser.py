import operator
from functools import reduce

from pyparsing import CaselessLiteral, Optional, Word, ZeroOrMore, Literal

from dice import Die

NUMBER = Word('0123456789')
NUMBER.setParseAction(lambda tokens: int(tokens[0]))

DIE = CaselessLiteral('d').suppress() + NUMBER('sides')
DIE.setParseAction(lambda tokens: Die(tokens.sides))

DICE = NUMBER('multiplier') + DIE('die')
DICE.setParseAction(lambda tokens: tokens.die * tokens.multiplier)


DICE_GROUP = \
    (DIE | DICE | NUMBER) + \
    ZeroOrMore(Literal('+').suppress() + (DIE | DICE | NUMBER))
DICE_GROUP.setParseAction(lambda tokens: reduce(operator.add, tokens))


def parse(string):
    return DICE_GROUP.parseString(string)[0]
