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

        # if v * dir < 0:
        #     return False, -1

        # lets do all magic in projection on dir axis

        pc_signed_proj = dir * v  # find the coordinates of v in dir vector

        # calculate distance^2 from center of sphere to dir vector
        dist = v * v - pc_signed_proj * pc_signed_proj

        if dist > self.radius ** 2:
            return False, -1

        # calculate distance from projection point to intersect with a ring
        delta = math.sqrt(self.radius ** 2 - dist)

        # first intersection
        intersection = pc_signed_proj - delta

        # if intersection behind the orig - try another
        if intersection < 0:
            intersection = pc_signed_proj + delta

        # if intersection behind the orig - don't register intersection
        if intersection < 0:
            return False, -1

        return True, intersection

    def ray_intersect(self, origin, dir):
        return self._ray_intersect(origin, dir)
