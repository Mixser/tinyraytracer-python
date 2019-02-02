import math

from .base import Vector3, Vector4
from .materials import Material

class SceneObject(object):
    def _ray_intersect(self, origin, direction):
        raise NotImplementedError

    def ray_intersect(self, origin, direction):
        return self._ray_intersect(origin, direction)

    def get_normal_at(self, point):
        raise NotImplementedError


class SceneIntersectionObject(object):
    __slots__ = ('point', 'normal', 'material', 'distance')

    def __init__(self, distance, point, normal, material):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.material = material


class Panel(SceneObject):
    def __init__(self, center, width, height, material=None):
        self.center = center
        self.width = width
        self.height = height
        self.material = material
        color_1 = Vector3(1, 1, 1) * 0.3
        color_2 = Vector3(1, .7, .3) * 0.3
        self._first_material = Material(Vector4(1, 0, 0, 0), color=color_1)
        self._second_material = Material(Vector4(1, 0, 0, 0), color=color_2)

    def _ray_intersect(self, origin, direction):
        
        if abs(direction.y) <=  1e-3:
            return None

        d = -(origin.y - self.center.y) / direction.y
        pt = origin + direction * d

        if d < 0:
            return None

        if self.center.x - self.width / 2 > pt.x:
            return None

        if self.center.x + self.width / 2 < pt.x:
            return None

        if self.center.z - self.height / 2 > pt.z:
            return None

        if self.center.z + self.height / 2 < pt.z:
            return None

        normal = self.get_normal_at(pt)

        if (int(.5 * pt.x + 1000) + int(.5 * pt.z)) & 1:
            material = self._first_material
        else:
            material = self._second_material

        return SceneIntersectionObject(d, pt, normal, material)

    def get_normal_at(self, pt):
        return Vector3(0, 1, 0)
        

class Sphere(SceneObject):
    __slots__ = ('center', 'radius', 'material')

    def __init__(self, center, radius, material=None):
        self.center = center
        self.radius = radius
        self.material = material or Material()

    def get_normal_at(self, point):
        return (point - self.center).normalize()

    def _ray_intersect(self, origin, dir):
        # vector from origin to sphere center
        v = self.center - origin

        # lets do all magic in projection on dir axis

        pc_signed_proj = dir * v  # find the coordinates of v in dir vector

        # calculate distance^2 from center of sphere to dir vector
        dist = v * v - pc_signed_proj * pc_signed_proj

        if dist > self.radius ** 2:
            return None

        # calculate distance from projection point to intersect with a ring
        delta = math.sqrt(self.radius ** 2 - dist)

        # first intersection
        intersection = pc_signed_proj - delta

        # if intersection behind the orig - try another
        if intersection < 0:
            intersection = pc_signed_proj + delta

        # if intersection behind the orig - don't register intersection
        if intersection < 0:
            return None

        point = origin + dir * intersection
        normal = self.get_normal_at(point)

        return SceneIntersectionObject(intersection, point, normal, self.material)