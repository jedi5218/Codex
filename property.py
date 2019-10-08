from copy import copy
from enum import Enum
class Property:

    def __init__(self, property_key, value=None, name='Property', description='', hidden=False, *mutators):
        self.base = value
        self.propertyKey = property_key
        self.name = name
        self.description = description
        self.hidden = hidden
        self.mutators = dict(map(lambda x:(x.name,x),mutators))

    def add_mutator(self, other):
        self.mutators.append(other)

    def __delitem__(self, key):
        if key not in self.mutators:
            raise KeyError('item is not in the object\'s properties')
        else:
            del self.mutators[key]

    def __getitem__(self, item):
        if item not in self.mutators:
            raise KeyError('item is not in the object\'s properties')
        else:
            return self.mutators[item]

    def __call__(self, **kwargs):
        val = self.base
        mutators = sorted(self.mutators.values(), key=lambda x: x.priority)
        for mutator in mutators:
            val = mutator(val, **kwargs)
        return val

    def __str__(self):
        return '{}: {}'.format(self.name,self.base)

    def make(self, value):
        retval = copy(self)
        retval.base = value
        return retval


class MutatorType(Enum):
    globalMutator = 0
    eventMutator = 1
    localMutator = 2


class Mutator:
    def __init__(self, type: MutatorType, property, priority, predicate, mutator):
        self.type = type
        self.property = property
        self.priority = priority
        self.mutator = mutator
        self.predicate = predicate

    def __call__(self, *args, **kwargs):
        return self.mutator(*args, **kwargs)