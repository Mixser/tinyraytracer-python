import operator
import math


class Vector(object):
    __slots__ = ('dimension', '_coordinates')

    def __init__(self, *args):
        self._coordinates = list(args)

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
        super(Vector2, self).__init__(x, y)
        self.dimension = 2

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
        super(Vector3, self).__init__(x, y, z)
        self.dimension = 3

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


class Sphere(object):
    __slots__ = ('center', 'radius')

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius


    def _habr_ray_intersect(self, origin, dir):
        L = self.center - origin
        tca = L * dir
        d2 = L * L - tca * tca
        if d2 > self.radius ** 2:
            return False

        thc = math.sqrt(self.radius**2 - d2)
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return False

        return True

    def _ray_intersect(self, origin, dir):
        # vector from origin to sphere center
        v = self.center - origin

        pc = (dir * v) * dir

        dist = abs(pc * pc - v * v)

        if dist > self.radius ** 2:
            return False

        di1 = math.sqrt(self.radius ** 2 - dist)




        return True

    def ray_intersect(self, origin, dir):
        # habr = self._habr_ray_intersect(origin, dir)
        my = self._ray_intersect(origin, dir)

        # if habr != my:
        #     print("DIFF: ", origin, dir, habr, my)

        return my

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





