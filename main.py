import ctypes
import itertools

from geometry import Vector3


def _chanel_color(v, chanel):
    return int(255 * max(0, min(1, v[chanel])))


def get_color(v: Vector3):
    r, g ,b = _chanel_color(v, 0), _chanel_color(v, 1), _chanel_color(v, 2)
    return r, g, b


def render(width, height):
    farame_buffer = [None] * (width * height)

    for j in range(height):
        for i in range(width):
            farame_buffer[i + j * width] = Vector3(j / height, i / width, 0)

    with open('out.ppm', 'wb') as f:
        f.write('P6\n{} {}\n255\n'.format(width, height).encode())
        for i in range(0, height * width, width):
            start, end = i, width + i
            vectors = farame_buffer[start: end]

            pixels = itertools.chain.from_iterable((get_color(v) for v in vectors))

            f.write(bytes(p for p in pixels))


def main():
    render(1024, 768)


if __name__ == "__main__":
    main()