import matplotlib.pyplot as plt


from parser import parse

plt.rcdefaults()


if __name__ == '__main__':
    while True:
        string = input('Roll? ')
        roll = parse(string)

        print(roll)
        print(roll.probability())
