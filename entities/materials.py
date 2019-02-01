from .base import Vector3, Vector4


class Material(object):
    __slots__ = ('diffuse_color', 'albedo', 'specular_exponent', 'refractive_index')

    def __init__(self, albedo=None, color=None, specular_exponent=0, refractive_index=1):
        self.diffuse_color = color or Vector3()
        self.albedo = albedo or Vector4(1, 0, 0, 0)
        self.specular_exponent = specular_exponent
        self.refractive_index = refractive_index

