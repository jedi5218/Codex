from property import Property,Mutator,MutatorType
from action import Action
from copy import copy


def turn():
    for entity in Entity.array:
        entity.timer = min(entity.timer+6., 6.)
        for action in entity.actions.values():
            if 'turn' in action.triggers:
                action()


class Entity:
    array = set()

    def __init__(self, name: str,
                 virtual: bool = False,
                 *args):
        self.properties = dict()
        self.mutators = dict()
        self.global_mutators = dict()
        self.context_mutators = dict()
        self.children = dict()
        self.actions = dict()
        self.parent = None
        self.name = name
        self.timer = 0.
        self.virtual = virtual
        for trait in args:
            if isinstance(trait, Property):
                self.add_property(trait)
            if isinstance(trait, Action):
                self.add_action(trait)
            if isinstance(trait, Entity):
                self.add_child(trait)
            if isinstance(trait, Mutator):
                if trait.type == MutatorType.localMutator:
                    self.add_mutator(self.mutators, trait)
                if trait.type == MutatorType.eventMutator:
                    self.add_mutator(self.context_mutators, trait)
                if trait.type == MutatorType.globalMutator:
                    self.add_mutator(self.global_mutators, trait)
        Entity.array.add(self)

    def __del__(self):
        Entity.array.remove(self)

    def __getattr__(self, item):
        if item in vars(self):
            return vars(self)[item]
        elif item in self.properties:
            return self.properties[item]
        elif item in self.children:
            return self.children[item]
        elif item in self.actions:
            return self.actions[item]
        else:
            raise KeyError('`{}` is not in the object\'s traits'.format(item))

    def __delattr__(self, item):
        if item in vars(self):
            raise KeyError('object property cannot be deleted')
        elif item in self.properties:
            del self.properties[item]
        elif item in self.children:
            del self.children[item]
        elif item in self.actions:
            del self.actions[item]
        else:
            raise KeyError('`{}` is not in the object\'s traits'.format(item))

    def modify(self, key, modifier):
        if key not in self.properties:
            raise KeyError('`{}` is not in the object\'s properties'.format(key))
        self.properties[key][0].value = modifier(self.properties[key][0].value)

    def __str__(self):
        description = ''
        description += '##'+self.name+'\n\n---\n'
        for property in self.properties.values():
            if not property.hidden:
                description +=str(property)+'\n\n---\n'

        return description

    def add_property(self, property):
        if property.propertyKey not in self.properties:
            self.properties[property.propertyKey] = property
        else:
            raise KeyError('item is already in the object\'s properties')

    @staticmethod
    def add_mutator(dict, mutator):
        if mutator.property not in dict:
            dict[mutator.property] = list()
        dict[mutator.property].append(mutator)

    def add_action(self, action):
        if action.key not in self.actions:
            self.actions[action.key] = action
            action.actor = self
        else:
            raise KeyError('{} is already in the object\'s actions'.format(action.key))

    def add_child(self, child):
        if child.name not in self.children:
            self.children[child.name] = child
            child.parent = self
        else:
            raise KeyError('{} is already in the object\'s children'.format(child.name))


class EntityView:

    def __init__(self, entity: Entity, key, *context: Entity):
        self.entity = entity
        self.key = key
        self.context = context
        self.base_view = BaseEntityView(self)

    def query_mutators(self, key):
        mutators = copy(self.entity.mutators[key]) if key in self.entity.mutators else []
        for entity in self.context:
            mutators += copy(entity.context_mutators[key]) if key in entity.context_mutators else []
        for entity in Entity.array:
            mutators += copy(entity.global_mutators[key]) if key in entity.global_mutators else []
        return sorted(mutators, key=lambda x: x.priority)

    def __getattr__(self, item):
        if item == 'base':
            return self.base_view
        else:
            var = self.entity.__getattr__(item)
            mutators = self.query_mutators(item)
            for mutator in mutators:
                var = mutator(var, **{'{}_{}'.format(self.key, item): var})
            return var if not isinstance(var, Entity) else EntityView(var, '_'.join((self.key, item)))


class BaseEntityView:

    def __init__(self, view: EntityView):
        vars(self)['view'] = view

    def __getattr__(self, item):
        return self.view.entity.properties[item].base

    def __setattr__(self, key, value):
        self.view.entity.properties[key].base = value
#
# def hit(this):
#     this.base.jooj += 100
#
# if __name__ == '__main__':
#     jooj = Property('jooj', 12.3, 'Jooj')
#     do=Action('hit',0,hit,'','','')
#     bob = Entity('Bob',False,jooj,do)
#     def mutate(*args,fails_jooj,**kwargs):
#         return fails_jooj.base+50
#     magick = Mutator(MutatorType.globalMutator,'jooj',0,mutate)
#     vodoo = Entity('Vodoo doll',True,magick)
#     view = EntityView(bob, 'fails')
#     print(bob.jooj)
#     bob.hit()
#     view.hit()
#     print(view.jooj)
#
#
# def action(this, target):
#     print('badunkadunk!')
#     target.base.guack -= this.guack
#
# if __name__ == '__main__':
#     from property import Property
#     doThaThing = Action('do_the_thing', 1, action, 'step','Do the thing', '')
#     guack = Property('guack', 100)
#     bob = Entity('Bob', False, guack, doThaThing)
#     bib = Entity('Bib', False, guack.make(20), doThaThing)
#     bob.do_the_thing(bib)