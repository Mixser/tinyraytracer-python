import math
import time
import itertools

from entities import Vector3

class Frame(object):
    __slots__ = ('width', 'height', 'buffer')
    def __init__(self, width, height, buffer):
        self.width = width
        self.height = height
        self.buffer = buffer

    @property
    def bytes(self):
        for index in range(0, self.width * self.height, self.width):
            line = self.buffer[index: index + self.width]
            yield bytes(p for p in itertools.chain.from_iterable(line))

class Renderer(object):
    def __init__(self, width, height, options=None):
        self._width = width
        self._height = height

        self._fov_hor = 2 * math.atan(height / width)
        self._fov_vert = math.pi / 2 

        self._options = self._prepare_options(options)

    def _prepare_options(self, user_options):
        options = {
            'reflect': True,
            'refract': True,
            'light': True,
            'shadow': True,
            'specular_light': True,
            'envmap': True,
            'max_depth': 4
        }
        user_options = user_options or {}
        options.update(user_options)

        return options

    def _create_frame(self):
        frame = [None] * (self._width * self._height)
        return frame

    @classmethod
    def _reflect(cls, v, normal):
        return v - normal * 2.0 * (v * normal)

    @classmethod
    def _refract(cls, v, normal, refractive_index):
        if refractive_index == 0:
            return Vector3(1, 0, 0)

        cos_v = - max(-1.0, min(1.0, v * normal))
        etav, etat = 1, refractive_index

        if cos_v < 0:
            cos_v = - cos_v
            etav, etat = etat, etav
            normal = -normal
        
        eta = etav / etat
        k = 1 - eta * eta * (1 - cos_v ** 2)

        if k < 0:
            res_vector = Vector3(1, 0, 0)
        else:
            res_vector = v * eta + normal * (eta * cos_v - math.sqrt(k))
        
        return res_vector


    def _calculate_reflect_color(self, scene, direction, info, depth):
        if not self._options['reflect']:
            return Vector3()

        reflect_dir = self._reflect(direction, info.normal).normalize()

        if reflect_dir * info.normal < 0:
            reflect_origin = info.point - info.normal * 1e-3
        else:
            reflect_origin = info.point + info.normal * 1e-3

        return self._cast_ray(reflect_origin, reflect_dir, scene, depth + 1)


    def _calculate_refract_color(self, scene, direction, intersection, depth):
        if not self._options['refract']:
            return Vector3()

        refract_dir = self._refract(direction, 
                                    intersection.normal, 
                                    intersection.material.refractive_index)

        refract_dir = refract_dir.normalize()

        if refract_dir * intersection.normal < 0:
            refract_origin = intersection.point - intersection.normal * 1e-3
        else:
            refract_origin = intersection.point + intersection.normal * 1e-3

        return self._cast_ray(refract_origin, refract_dir, scene, depth + 1)

    def _calculate_ligth_intensity(self, scene, origin, direction, intersection):
        light_intensity = 0
        specular_ligth_intensity = 0

        if not self._options['light']:
            return 1, 0

        for light in scene.lights:
            light_dir = (light.position - intersection.point).normalize()
            light_distance = (light.position - intersection.point).norm()
            
            if self._options['shadow']:
                if light_dir * intersection.normal < 0:
                    shadow_origin = intersection.point - intersection.normal * 1e-3
                else:
                    shadow_origin = intersection.point + intersection.normal * 1e-3

                shadow_intersection = scene.intersect(shadow_origin, light_dir)

                if shadow_intersection:
                    if (shadow_intersection.point - shadow_origin).norm() < light_distance:
                        continue
            
            light_intensity += light.intensity * max(0, light_dir * intersection.normal)

            if self._options['specular_light']:
                reflect_scalar =  -self._reflect(-light_dir, intersection.normal) * direction
                reflect_scalar = max(0, reflect_scalar)

                specular_ligth_intensity += math.pow(reflect_scalar, intersection.material.specular_exponent) * light_intensity
            else:
                specular_ligth_intensity = 0

        return light_intensity, specular_ligth_intensity
            

    def _cast_ray(self, origin, direction, scene, depth=0):
        
        intersection = scene.intersect(origin, direction)
        if depth >= self._options['max_depth'] or not intersection:
            # no intersectio find of we have reached max depth
            if self._options['envmap']:
                return scene.envmap(origin, direction)
            return Vector3(0.2, 0.7, 0.8)

        # calculate reflection
        reflect_color = self._calculate_reflect_color(scene, direction, intersection, depth)
        # calculate refraction
        refract_color = self._calculate_refract_color(scene, direction, intersection, depth)

        # calculate ligh intensity and specular light intensity
        light_intensity, specular_light_intensity = self._calculate_ligth_intensity(scene, origin, direction, intersection)

        # calcualte result color
        result_color = intersection.material.diffuse_color * light_intensity * intersection.material.albedo[0]
        
        # add specular intensity
        if self._options['specular_light']:
            result_color += Vector3(1, 1, 1) * specular_light_intensity * intersection.material.albedo[1]

        # add reflect 
        if self._options['reflect']:
            result_color += reflect_color * intersection.material.albedo[2]

        # add refract
        if self._options['refract']:
            result_color += refract_color * intersection.material.albedo[3]

        return result_color

    @classmethod
    def _cast_vector_to_rgb_tuple(cls, v):
        r = int(255 * max(0, min(1, v[0])))
        g = int(255 * max(0, min(1, v[1])))
        b = int(255 * max(0, min(1, v[2])))

        return r, g, b

    def render(self, scene):
        start = time.time()
        frame = self._create_frame()
        total_count = self._width * self._height
        proceesed_count = 0
        percent = 0

        print('RENDERING: [', end='', flush=True)
        for j in range(self._height):
            y = - (2 * (j + 0.5) / self._height - 1) * math.tan(self._fov_hor / 2)

            for i in range(self._width):
                x = (2 * (i + 0.5) / self._width - 1) * math.tan(self._fov_vert / 2)

                origin = Vector3(0, 0, 0)
                direction = Vector3(x, y, -1).normalize()

                vector = self._cast_ray(origin, direction, scene)

                frame[i + j * self._width] = self._cast_vector_to_rgb_tuple(vector)
                proceesed_count += 1
            
            if ((proceesed_count / total_count) * 100) // 10 > percent:
                percent += 1
                print('#', end='', flush=True)

        print(']')
            
        print('[RENDER FINISHED options=%s] took: %.2f sec.' % (self._options, time.time() - start))
        return Frame(self._width, self._height, frame)
