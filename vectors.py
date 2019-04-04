
class PropertyVector:

    def _apply_to_all(self, other: object, function) -> object:
        if not isinstance(other,self.__class__):
            raise ValueError("Invalid vector operation on {0} and {1}".format(str(self.__class__), str(other.__class__)))
        result = self.__class__()
        rdict = vars(result)
        for key in rdict.keys():
            rdict[key] = function(vars(self)[key], vars(other)[key])
        return result

    def _apply_to_all_unary(self, function) -> object:
        result = self.__class__()
        rdict = vars(result)
        for key in rdict.keys():
            rdict[key] = function(vars(self)[key])
        return result

    def __add__(self, other):
        return self._apply_to_all(other, lambda x, y: x + y)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self._apply_to_all_unary(lambda x: x - other)
        elif isinstance(other, self.__class__):
            return self._apply_to_all(other, lambda x, y: x - y)

    def __mul__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            return self._apply_to_all_unary(lambda x:x*other)
        elif isinstance(other,self.__class__):
            return self._apply_to_all(other, lambda x, y: x * y)

    def oneminus(self):
        return self._apply_to_all_unary(lambda x: 1-x)

    def __str__(self):
        return self.__class__.__name__+': '+' '.join(map(lambda x: '{0}: {1}'.format(x[0], x[1]), vars(self).items()))


class ElementalVector(PropertyVector):

    def __init__(self, fire=0, water=0, air=0, earth=0, metal=0, life=0, aether=0):
        self.fire = fire
        self.water = water
        self.air = air
        self.earth = earth
        self.metal = metal
        self.life = life
        self.aether = aether


class StructuralVector(PropertyVector):

    def __init__(self, blunt=0, slashing=0, piercing=0):
        self.blunt = blunt
        self.slashing = slashing
        self.piercing = piercing

    def damage(self):
        retval = max(vars(self).values())
        return retval if retval > 0 else 0


if __name__ == '__main__':
    resistance = StructuralVector(0.4, 0.5, 1)
    attack = StructuralVector(10, 20, 30)
    print('object recieved:')
    print(vars(attack*resistance.oneminus()))
    print('passed the object:')
    print(vars(attack*resistance))
