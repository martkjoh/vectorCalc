from abc import ABC, abstractmethod
from numbers import Number
import numpy as np
from matplotlib import pyplot as plt

'''
Abstract classes

The base calsses for fields
'''

# The Field is the patriach of all classes. Everything is a type of Field
class Field(ABC):

    __shape__ = ()

    @abstractmethod
    def __init__(self, f, L = 1):
        self.f = f
        # the domain of the Field is [-L, L]^D in D dim.
        self.L = L


    @classmethod
    def nill(cls):
        return cls(lambda x: 0)

# the difference between vector/Scalar fields is the output produced
class FieldScalar(Field):
    pass

# The dimensionality of the fields is given by its input

# A 0D Field is a Scalar/vector
class Field0D(Field):
    pass

# A 1D Field is just a funcion
class Field1D(Field):

    @abstractmethod
    def plot(self, ax, n):
        x = np.linspace(-self.L, self.L, n)
        y = self.f(x)
        return ax.plot(x, y)

class Field2D(Field):
    pass


'''
Errors

Errors related to fields
'''

# A field must recive the right Function when instantiated
class InstantionExeption(Exception):

    def __init__(slef, field, f):
        raise Exception("{} can't be instatiated with {}. Is the returntype right?".format(type(field), type(f)))

'''
Instantiable Classes

The implementation of different kinds of fields
'''

class Scalar(FieldScalar, Field0D):

    # Private Methods
    def __init__(self, f):
        print(f())
        if not isinstance(f(), Number):
            raise InstantionExeption(self, f)

        super().__init__(f)

    def __add__(self, other):
        return Scalar(lambda : self.f() + other.f())


    # Public methods
    def plot(self, ax, n = 100, L = 1):
        x = np.linspace(-self.L, self.L, n)
        y = np.ones_like(x) * self.f()
        return ax.plot(x, y)


class Function(FieldScalar, Field1D):
    
    __shape__ = (1,)

    # Private Methods
    def __init__(self, f, L = 1):
        if not f(np.array([np.nan])).shape == self.__shape__:
            raise InstantionExeption(self, f)

        super().__init__(f, L)

    def __add__(self, other):
        if isinstance(other, Function):
            L = min(self.L, other.L)
            return Function(lambda x: self.f(x) + other.f(x), L)

        elif isinstance(other, Scalar):
            return Function(lambda x: self.f(x) + other.f(), self.L)


    # Public methods
    def plot(self, ax, n = 100):
        return super().plot(ax, n)
