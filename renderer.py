import math
import time
import itertools

from entities import Vector3
from ray import RayTracer

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

        ray_tracer = RayTracer(scene, self._options)

        print('RENDERING: [', end='', flush=True)
        for j in range(self._height):
            y = - (2 * (j + 0.5) / self._height - 1) * math.tan(self._fov_hor / 2)

            for i in range(self._width):
                x = (2 * (i + 0.5) / self._width - 1) * math.tan(self._fov_vert / 2)

                origin = Vector3(0, 0, 0)
                direction = Vector3(x, y, -1).normalize()

                vector = ray_tracer.trace(origin, direction)

                frame[i + j * self._width] = self._cast_vector_to_rgb_tuple(vector)
                proceesed_count += 1
            
            if ((proceesed_count / total_count) * 100) // 10 > percent:
                percent += 1
                print('#', end='', flush=True)

        print(']')
            
        print('[RENDER FINISHED options=%s] took: %.2f sec.' % (self._options, time.time() - start))
        return Frame(self._width, self._height, frame)
