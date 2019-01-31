from .base import Vector3

class Material(object):
    __slots__ = ('diffuse_color', )
    def __init__(self, color=None):
        self.diffuse_color = color or Vector3()
