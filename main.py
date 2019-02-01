import sys
import math
import time


from entities import Vector4, Vector3, Sphere, Material, Light


def _chanel_color(v, chanel):
    return int(255 * max(0, min(1, v[chanel])))


def get_color(v: Vector3):
    r, g, b = _chanel_color(v, 0), _chanel_color(v, 1), _chanel_color(v, 2)
    return r, g, b


def scene_intersct(orig, dir, spheres):
    hit, normal, material = None, None, Material()
    distance = sys.maxsize

    for sphere in sorted(spheres, key=lambda s: -(s.center.z + s.radius)):
        intersect, sphere_distance = sphere.ray_intersect(orig, dir)
        if intersect and sphere_distance < distance:
            distance = sphere_distance
            hit = orig + dir * sphere_distance
            normal = (hit - sphere.center).normalize()
            material = sphere.material

    board_distance = sys.maxsize

    if abs(dir.y) > 1e-3:
        d = -(orig.y + 4) / dir.y
        pt = orig + dir * d

        if d > 0 and abs(pt.x) < 10 and pt.z < -10 and pt.z > -30 and d < distance:
            board_distance = d
            hit = pt
            normal = Vector3(0, 1, 0)

            if (int(.5 * hit.x + 1000) + int(.5 * hit.z)) & 1:
                color = Vector3(1, 1, 1)
            else:
                color = Vector3(1, .7, .3)
            material.diffuse_color = color * 0.3

    return min(board_distance, distance) < 1000, hit, normal, material


def reflect(v, normal):
    return v - normal * 2.0 * (v * normal)


def refract(v, normal, refractive_index):
    cos_v = - max(-1.0, min(1.0, v * normal))
    etav, etat = 1, refractive_index

    if cos_v < 0:
        cos_v = -cos_v
        etav, etat = etat, etav
        normal = -1 * normal

    eta = etav / etat
    k = 1 - eta * eta * (1 - cos_v ** 2)

    if k < 0:
        res_vector = Vector3(1, 0, 0)
    else:
        res_vector = v * eta + normal * (eta * cos_v - math.sqrt(k))

    return res_vector


def cast_ray(orig: Vector3, dir: Vector3, spheres: [Sphere], depth=0):
    lights = [
        Light(Vector3(-20, 20,  20), 1.5),
        Light(Vector3(30, 50, -25), 1.8),
        Light(Vector3(30, 20, 30), 1.7),
    ]

    intersects, *result = scene_intersct(orig, dir, spheres)
    if depth >= 4 or not intersects:
        return Vector3(0.2, 0.7, 0.8)

    hit, normal, material = result

    reflect_dir = reflect(dir, normal).normalize()
    refract_dir = refract(dir, normal, material.refractive_index).normalize()

    reflect_origin = hit - normal * 1e-3 if reflect_dir * normal < 0 else hit + normal * 1e-3
    refract_origin = hit - normal * 1e-3 if refract_dir * normal < 0 else hit + normal * 1e-3

    reflect_color = cast_ray(reflect_origin, reflect_dir, spheres, depth + 1)
    refract_color = cast_ray(refract_origin, refract_dir, spheres, depth + 1)

    light_intensity = 0.0
    specular_light_intensity = 0.0

    for light in lights:
        light_dir = (light.position - hit).normalize()
        light_distance = (light.position - hit).norm()

        shadow_orig = hit - normal * 1e-3 if light_dir * normal < 0 else hit + normal * 1e-3

        intersection, *result = scene_intersct(shadow_orig, light_dir, spheres)
        if intersection:
            shadow_hit, shadow_normal, _ = result

            if (shadow_hit - shadow_orig).norm() < light_distance:
                continue

        light_intensity += light.intensity * max(0, light_dir * normal)

        specular_reflect_scalar = max(0, ((-1) * reflect((-1)*light_dir, normal) * dir))
        specular_light_intensity += math.pow(specular_reflect_scalar, material.specular_exponent) * light.intensity

    result = material.diffuse_color * light_intensity * material.albedo[0] \
             + Vector3(1, 1, 1) * specular_light_intensity * material.albedo[1] \
             + reflect_color * material.albedo[2] \
             + refract_color * material.albedo[3]

    return result


def render(width, height) -> bytes:
    frame_buffer = [None] * (width * height)

    fov_hor = math.pi / 2.
    fov_vert = 2 * math.atan(width / height)

    ivory = Material(Vector4(0.6, 0.3, 0.1, 0), Vector3(0.4, 0.4, 0.3), 50.0, 1.0)
    glass = Material(Vector4(0.0, 0.5, 0.1, 0.8), Vector3(0.4, 0.4, 0.3), 50.0, 1.5)

    red_rubber = Material(Vector4(0.9, 0.1, 0, 0), Vector3(0.3, 0.1, 0.1), 10.0, 1)
    mirror = Material(Vector4(0.0, 10.0, 0.8, 0), Vector3(1.0, 1.0, 1.0), 1425., 1)

    spheres = [
        Sphere(Vector3(-3, 0, -16), 2, ivory),
        Sphere(Vector3(-1.0, -1.5, -12), 2, glass),
        Sphere(Vector3(1.5, -0.5, -18), 3, red_rubber),
        Sphere(Vector3(7, 5, -18), 4, mirror),
        
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
    with open('out.ppm', 'wb') as f:
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