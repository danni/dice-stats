from pyparsing import CaselessLiteral, Optional, Word

from dice import Dice, Die

NUMBER = Word('0123456789')
NUMBER.setParseAction(lambda tokens: int(tokens[0]))

DIE = CaselessLiteral('d').suppress() + NUMBER('sides')
DIE.setParseAction(lambda tokens: Die(tokens.sides))

DICE = NUMBER('multiplier') + DIE('die')
DICE.setParseAction(lambda tokens: tokens.die * tokens.multiplier)

PARSER = DIE | DICE


def parse(string):
    return PARSER.parseString(string)[0]
