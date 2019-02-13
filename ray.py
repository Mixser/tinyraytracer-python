import math

from entities import Vector3

import utils

class RayIntersector(object):
    def __init__(self, scene):
        self._scene = scene

    def intersection(self, origin, direction):
        return self._scene.intersect(origin, direction)


class RayReflector(object):
    def __init__(self, tracer, scene, options):
        self._tracer = tracer
        self._scene = scene
        self._options = options

    @classmethod
    def _reflect(cls, v, normal):
        return utils.reflect(v, normal)

    def calculate_reflection(self, origin, direction, intersection, depth):
        if not self._options['reflect']:
            return Vector3()

        reflect_dir = self._reflect(direction, intersection.normal).normalize()
        reflect_origin = utils.build_origin(intersection.point, reflect_dir, intersection.normal)

        return self._tracer.trace(reflect_origin, reflect_dir, depth + 1)


class RayRefractor(object):
    def __init__(self, tracer, scene, options):
        self._tracer = tracer
        self._scene = scene
        self._options = options

    @classmethod
    def _refract(self, v, normal, refractive_index):
        return utils.refract(v, normal, refractive_index)

    def calculate_refraction(self, origin, direction, intersection, depth):
        if not self._options['refract']:
            return Vector3()

        refract_dir = self._refract(direction, 
                                    intersection.normal, 
                                    intersection.material.refractive_index)

        refract_dir = refract_dir.normalize()
        refract_origin = utils.build_origin(intersection.point, refract_dir, intersection.normal)

        return self._tracer.trace(refract_origin, refract_dir, depth + 1)


class LightIntensityCalculator(object):
    def __init__(self, scene, options):
        self._options = options
        self._scene = scene

    def calculate_intensity(self, origin, direction, intersection, dept):
        light_intensity = 0
        specular_light_intensity = 0

        if not self._options['light']:
            return 1, 0

        for light in self._scene.lights:
            light_dir = (light.position - intersection.point).normalize()
            light_distance = (light.position - intersection.point).norm()
            
            if self._options['shadow']:
                shadow_origin = utils.build_origin(intersection.point, light_dir, intersection.normal)
                shadow_intersection = self._scene.intersect(shadow_origin, light_dir)

                if shadow_intersection:
                    if (shadow_intersection.point - shadow_origin).norm() < light_distance:
                        continue
            
            light_intensity += light.intensity * max(0, light_dir * intersection.normal)

            if self._options['specular_light']:
                reflect_scalar = -utils.reflect(-light_dir, intersection.normal) * direction
                reflect_scalar = max(0, reflect_scalar)

                specular_light_intensity += math.pow(reflect_scalar, intersection.material.specular_exponent) * light_intensity
            else:
                specular_light_intensity = 0

        return light_intensity, specular_light_intensity


class RayTracer(object):
    def __init__(self, scene, options):
        self._scene = scene
        self._options = options

        self._intersector = RayIntersector(scene)

        self._ray_reflector = RayReflector(self, scene, options)
        self._ray_refractor = RayRefractor(self, scene, options)

        self._light_tracer = LightIntensityCalculator(scene, options)

    def trace(self, origin, direction, depth=0):
        intersection = self._intersector.intersection(origin, direction)

        if depth >= self._options['max_depth'] or not intersection:
            # no intersection detected or we have reached max recursive depth for relfection or refraction
            if self._options['envmap']:
                return self._scene.envmap(origin, direction) 
            return Vector3(0.2, 0.7, 0.8)

        refraction = self._ray_refractor.calculate_refraction(origin, direction, intersection, depth)
        reflection = self._ray_reflector.calculate_reflection(origin, direction, intersection, depth)

        light_intensity, specular_light_intensity = self._light_tracer.calculate_intensity(origin, direction, intersection, depth)

        # resut vecotr - it's a material color
        result_vector = intersection.material.diffuse_color

        # apply light
        result_vector = result_vector * light_intensity * intersection.material.albedo[0]

        # add specular intensity
        result_vector += Vector3(1, 1, 1) * specular_light_intensity * intersection.material.albedo[1]
        
        # add reflection
        result_vector += reflection * intersection.material.albedo[2]

        # add refraction
        result_vector += refraction * intersection.material.albedo[3]

        return result_vector