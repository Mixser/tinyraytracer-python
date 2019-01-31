import itertools
import sys
import math

from geometry import Vector3, Sphere


def _chanel_color(v, chanel):
    return int(255 * max(0, min(1, v[chanel])))


def get_color(v: Vector3):
    r, g, b = _chanel_color(v, 0), _chanel_color(v, 1), _chanel_color(v, 2)
    return r, g, b


def cast_ray(orig: Vector3, destination: Vector3, sphere: Sphere):
    sphere_dist = sys.maxsize

    if not sphere.ray_intersect(orig, destination):
        return Vector3(0.2, 0.7, 0.8)

    return Vector3(0.4, 0.4, 0.4)


def render(width, height) -> bytes:
    frame_buffer = [None] * (width * height)

    fov = math.pi / 2.

    sphere = Sphere(Vector3(-3, 0, -16), 2)

    for j in range(height):
        for i in range(width):

            x = (2 * (i + 0.5) / width - 1) * math.tan(fov / 2.) * width / height
            y = -(2 * (j + 0.5) / height - 1) * math.tan(fov / 2.)

            dir = Vector3(x, y, -1).normalize()

            frame_buffer[i + j * width] = cast_ray(Vector3(0, 0, 0), dir, sphere)

    pack_size = width
    result = []

    for i in range(0, width * height, pack_size):
        start, end = i, pack_size + i
        vectors = frame_buffer[start: end]

        for v in vectors:
            result.extend(get_color(v))

    return bytes(result)


def write_ppm(width, height, frame):
    with open('out.ppm', 'wb') as f:
        f.write('P6\n{} {}\n255\n'.format(width, height).encode())
        f.write(frame)


def main():
    width, height = 1024, 768
    frame = render(width, height)
    write_ppm(width, height, frame)




if __name__ == "__main__":
    main()