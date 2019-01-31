import itertools
import sys
import math
import time


from entities import Vector2, Vector3, Sphere, Material, Light

def _chanel_color(v, chanel):
    return int(255 * max(0, min(1, v[chanel])))


def get_color(v: Vector3):
    r, g, b = _chanel_color(v, 0), _chanel_color(v, 1), _chanel_color(v, 2)
    return r, g, b


def scene_intersct(orig, dir, spheres):
    hit, normal, material = None, None, None
    distance = sys.maxsize

    for sphere in sorted(spheres, key=lambda s: -(s.center.z + s.radius)):
        intersect, sphere_distance = sphere.ray_intersect(orig, dir)
        if intersect and sphere_distance < distance:
            distance = sphere_distance
            hit = orig + dir * sphere_distance
            normal = (hit - sphere.center).normalize()
            material = sphere.material
            break

    return distance < 1000, hit, normal, material



def cast_ray(orig: Vector3, destination: Vector3, spheres: [Sphere]):
    lights = [
        Light(Vector3(-20, 20,  20), 1.5)
    ]

    intersects, *result = scene_intersct(orig, destination, spheres)
    if not intersects:
        return Vector3(0.2, 0.7, 0.8)

    hit, normal, material = result

    light_intensity = 0.0

    for ligth in lights:
        light_dir = (ligth.position - hit).normalize()
        light_intensity += ligth.intensity * max(0, light_dir * normal)    

    return material.diffuse_color * light_intensity


def render(width, height) -> bytes:
    frame_buffer = [None] * (width * height)

    fov_hor = math.pi / 2.
    fov_vert = 2 * math.atan(width / height)

    ivory = Material(Vector3(0.4, 0.4, 0.3))
    red_bubber = Material(Vector3(0.3, 0.1, 0.1))

    spheres = [
        Sphere(Vector3(-3, 0, -16), 2, ivory),
        Sphere(Vector3(-1.0, -1.5, -12), 2, ivory),
        Sphere(Vector3(1.5, -0.5, -18), 3, red_bubber),
        Sphere(Vector3(7, 5, -18), 4, red_bubber),
        
    ]

    for j in range(height):
        y = -(2 * (j + 0.5) / height - 1) * math.tan(fov_hor / 2)
        
        for i in range(width):
            x = (2 * (i + 0.5) / width - 1) * math.tan(fov_vert / 2)
            
            dir = Vector3(x, y, -1).normalize()
            frame_buffer[i + j * width] = cast_ray(Vector3(0, 0, 0), dir, spheres)

    pack_size = width
    result = []

    for i in range(0, width * height, pack_size):
        start, end = i, pack_size + i
        vectors = frame_buffer[start: end]

        for v in vectors:
            result.extend(get_color(v))

    return bytes(result)


def write_ppm(width, height, frame):
    with open('out2.ppm', 'wb') as f:
        f.write('P6\n{} {}\n255\n'.format(width, height).encode())
        f.write(frame)


def main():
    start = time.time()
    width, height = 640, 480
    frame = render(width, height)
    write_ppm(width, height, frame)
    print("Render took: {:.2f} sec.".format(time.time() - start))


if __name__ == "__main__":
    main()