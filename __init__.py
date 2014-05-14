import matplotlib.pyplot as plt


from parser import parse

plt.rcdefaults()


if __name__ == '__main__':
    while True:
        string = input('Roll? ')
        roll = parse(string)

        scores, probabilities = roll.probability()
        for row in zip(scores, probabilities):
            print("%d: %g" % row)

        plt.title(str(roll))
        plt.bar(scores, probabilities,
                align='center')
        plt.show()
