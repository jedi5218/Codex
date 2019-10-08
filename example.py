from entity import *
from property import Property
from vectors import *
from collections import deque
from dice2precent import dice2percent
from copy import copy
import random


def attack(this, target, damage):
    attack, target_stack = assemble_target_stack(target)

    #at this point full stack of objects is established, and attack execution starts

    while len(target_stack):
        current_target = target_stack.pop()
        if current_target.virtual:
            continue
        if attack > current_target.cover() and len(target_stack) >= 1:
            attack = (attack - current_target.cover()) / \
                     (1-current_target.cover())
            print('attack has penetrated '+current_target.name)
        else:
            damage -= current_target.armor()
            current_target.suffer_damage(damage=damage)
            damage = damage * current_target.protection().oneminus()


def suffer_damage(this, damage):
    structural_damage = (damage * this.protection()).damage()
    print('attack dealt ' + str(structural_damage) + ' damage to ' + this.name)
    this.structure.base -= structural_damage
    if this.structure() <= 0:
        print(this.name + " is destroyed")


def assemble_target_stack(target):
    base_target = target
    target_stack = deque()
    while True:  # attack backpropagation
        target_stack.append(base_target)
        base_target = base_target.parent
        if base_target is None:
            break
    final_target = target
    rolls = list(map(int, input('roll the d20 dice: ').split()))
    #rolls = [20, 20, 20]
    attack = dice2percent(20, *rolls)
    random.seed(int(1000 * attack))
    while len(final_target.children):  # attack forward propagation
        target = random.random() * sum(map(lambda x: x.size))
        for child in sorted(final_target.children, key=lambda x: x.size, reverse=True):
            if target > child.size:
                target -= child.size
            else:
                final_target = child
                target_stack.appendleft(final_target)
                break
    return attack, target_stack

if __name__ == '__main__':
    structure = Property(
        'structure',
        50,
        'Structure',
        'The parameter describing how far the object is from falling apart'
    )
    armor = Property(
        'armor',
        StructuralVector(10, 10, 10),
        'Armor',
        'The parameter describing the amount by which the damage is reduced'
    )
    protection = Property(
        'protection',
        StructuralVector(1, 1, 1),
        'Protection',
        'The parameter describing how much damage this object gets vs how much damage is passed to children'
    )
    penetration_minimum = Property(
        'protection',
        StructuralVector(1, 1, 1),
        'Protection',
        'The parameter describing how much damage this object gets vs how much damage is passed to children'
    )
    cover = Property(
        'cover',
        0.67,
        'Cover',
        'The percentage of the object that this layer hides'
    )
    size = Property(
        'size',
        100,
        'Size',
        'size of an entity'
    )
    # enchantment = Mutator(
    #     lambda x: x+StructuralVector(5, 5, 5),
    #     Properties.armor,
    #     1,
    #     'Armor enchantment +5',
    #     'Increases armor in all categories by 5')
    #
    # enchantment2 = copy(enchantment)
    # enchantment2.mutator = lambda x: x*StructuralVector(1.2, 1.2, 1.2)
    # enchantment2.priority = 2
    # enchantment2.description = 'Multiplies armor in all categories by 1.2'

    hit = Action('hit', 3, attack, [''], 'attack', 'Do the attack')
    damage = Action('suffer_damage', 0, suffer_damage, '', 'suffer damage', '')

    dummy = Entity('dummy', False,
                   structure,
                   armor,
                   protection,
                   cover,
                   hit,
                   copy(damage))

    gambezon = Entity('gambezon', False,
                      dummy,
                      structure.make(15),
                      armor.make(StructuralVector(5, 2, 0)),
                      protection.make(StructuralVector(0, 0.5, 0.2)),
                      cover.make(0.9),
                      damage)

    print(gambezon.children)
    print(dummy.parent)
    dmg = StructuralVector(30, 30, 0)

    print('damage is '+str(dmg))
    print('before attack dummy`s structure at: ' + str(dummy.structure()) + 'sp')
    # turn()
    dummy.hit(target=dummy, damage=dmg)
    # print(dummy.timer)
    print(dummy.structure)
    print('after attack dummy`s structure: ' + str(dummy.structure()) + 'sp')

    # print(dummy)


