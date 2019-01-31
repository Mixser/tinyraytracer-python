import math
from .materials import Material

class Sphere(object):
    __slots__ = ('center', 'radius', 'material')

    def __init__(self, center, radius, material=None):
        self.center = center
        self.radius = radius
        self.material = material or Material()

    def _ray_intersect(self, origin, dir):
        # vector from origin to sphere center
        v = self.center - origin

        pc = (dir * v) * dir

        dist = abs(pc * pc - v * v)

        if dist > self.radius ** 2:
            return False, -1

        c = math.sqrt(self.radius ** 2 - dist)
        first_intersection = origin + dir * ((pc - origin).norm() - c)

        # TODO: check if the cam in the sphere (or sphere behined the cam)
        return True, first_intersection.norm()

    def ray_intersect(self, origin, dir):
        return self._ray_intersect(origin, dir)