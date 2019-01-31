import math
import operator


class Vector(object):
    __slots__ = ('dimension', '_coordinates')

    def __init__(self, coordinates):
        self._coordinates = coordinates
        self.dimension = len(coordinates)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.coordinates)

    def __getitem__(self, index):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    @property
    def coordinates(self):
        return self._coordinates

    def norm(self):
        return math.sqrt(sum(p ** 2 for p in self.coordinates))

    def normalize(self):
        norm = self.norm()

        for i in range(self.dimension):
            self[i] = self[i] / norm

        return self

    def __process_number_operation__(self, other, operation):
        points = [operation(p, other) for p in self.coordinates]
        return self.__class__(*points)

    def __process_vector_operation__(self, other, operation):
        if self.dimension != other.dimension:
            raise ValueError("Invalid dimension")

        points = [operation(p1, p2) for p1, p2 in zip(self.coordinates, other.coordinates)]

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
    __slots__ = Vector.__slots__

    def __init__(self, x=0, y=0):
        super(Vector2, self).__init__([x, y])

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    def __getitem__(self, index):
        assert index < self.dimension
        return self._coordinates[index]

    def __setitem__(self, index, value):
        assert index < self.dimension
        self._coordinates[index] = value


class Vector3(Vector):
    __slots__ = Vector.__slots__

    def __init__(self, x=0, y=0, z=0):
        super(Vector3, self).__init__([x, y, z])

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    @property
    def z(self):
        return self._coordinates[2]

    def __getitem__(self, index):
        assert index < self.dimension
        return self._coordinates[index]

    def __setitem__(self, index, value):
        assert index < self.dimension
        self._coordinates[index] = value


