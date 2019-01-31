import operator
import math

class Vector(object):
    __slots__ = ('dimension', )

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.coodinates)

    def __getitem__(self, index):
        raise NotImplementedError

    def __setitem(self, index, value):
        raise NotImplementedError

    @property
    def coodinates(self):
        return [self[i] for i in range(self.dimension)]

    def norm(self):
        return math.sqrt(sum(p ** 2 for p in self.coodinates))

    def normalize(self):
        norm = self.norm()

        for i in range(self.dimension):
            self[i] = self[i] / norm

        return self

    def __process_number_operation__(self, other, operation):
        points = [operation(p, other) for p in self.coodinates]
        return self.__class__(*points)

    def __process_vector_operation__(self, other, operation):
        if self.dimension != other.dimension:
            raise ValueError("Invalid dimension")

        points = [operation(p1, p2) for p1, p2 in zip(self.coodinates, other.coodinates)]

        return self.__class__(*points)

    def __process_scalar_operation__(self, other, operation):
        if self.dimension != other.dimension:
            raise ValueError("Invalid dimensions")

        result = 0

        for i in range(self.dimension):
            result += operation(self[i], other[i])

        return result

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__process_number_operation__(other, operator.add)
        return self.__process_vector_operation__(other, operator.add)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__process_number_operation__(other, operator.sub)
        return self.__process_vector_operation__(other, operator.sub)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__process_number_operation__(other, operator.mul)
        return self.__process_scalar_operation__(other, operator.mul)

    def __rmul__(self, other):
        return self.__mul__(other)



class Vector2(Vector):
    __slots__ = Vector.__slots__ + ('x', 'y')
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.dimension = 2

    def __getitem__(self, index):
        assert index < self.dimension
        return self.x if index <= 0 else self.y

    def __setitem__(self, index, value):
        assert index < self.dimension
        if index <= 0:
            self.x = value
        else:
            self.y = value



class Vector3(Vector):
    __slots__ = Vector.__slots__ + ('x' , 'y', 'z')

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.dimension = 3


    def __getitem__(self, index):
        assert index < self.dimension
        if index <= 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            return self.z

    def __setitem__(self, index, value):
        assert index < self.dimension
        if index <= 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            self.z = value


if __name__ == "__main__":
    v1 = Vector2(1, 0)
    v2 = Vector2(2, 0)

    print(v1 + v2)
    print(v1 * v2)
    print(v1 * 2, 2 * v1 + 1)

    v1 = Vector3(1, 0, 1)
    v2 = Vector3(0, 1, 0)

    print(v1 * v2)
    print(v1 + v2)
    print(v1 + 1)


    v1 = Vector2(3, 4)
    print(v1.normalize())




