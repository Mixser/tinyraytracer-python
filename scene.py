import sys
import math

from entities import Material, Vector3
from entities.objects import SceneIntersectionObject

class Scene(object):
    def __init__(self, envmap):
        self._envmap = envmap
        self._objects = []
        self._lights = []

    @property
    def lights(self):
        return self._lights

    @property
    def objects(self):
        return self._objects

    def add_object(self, obj):
        self._objects.append(obj)

    def add_light(self, light_obj):
        self._lights.append(light_obj)

    def intersect(self, origin, direction):
        result = None
        distance = 1000 # sys.maxsize

        for obj in self._objects:
            intersection = obj.ray_intersect(origin, direction)

            if not intersection or intersection.distance >= distance:
                continue

            distance = intersection.distance
            result = intersection

        return result


    def envmap(self, origin, direction):
        width, height = self._envmap.width, self._envmap.height

        direction = direction.normalize()

        x = int((math.atan2(direction.z, direction.x) / (2 * math.pi) + 0.5) * width)
        y = int(math.acos(direction.y) / math.pi * height)

        r, g, b = self._envmap.getpixel((x, y))
        return Vector3(r / 255, g / 255, b / 255)
