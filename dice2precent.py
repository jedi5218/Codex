
def dice2percent(sides, *rolls: int):
    max = sides**(len(rolls))-1
    sum = 0
    for die, i in zip(rolls, range(len(rolls))):
        sum += (die-1) * sides ** i
    return sum/max

if __name__ == '__main__':
    print(dice2percent(8,*[1]*6))


