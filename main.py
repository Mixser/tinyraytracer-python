from PIL import Image

from scene import Scene
from renderer import Renderer

from entities import Vector3, Vector4, Sphere, Light, Material, Panel

def write_ppm(filename, frame):
    with open(filename, 'wb') as f:
        f.write('P6\n{} {}\n255\n'.format(frame.width, frame.height).encode())
        for line_bytes in frame.bytes:
            f.write(line_bytes)

def add_lights(scene):
    lights = [
        Light(Vector3(-20, 20,  20), 1.5),
        Light(Vector3(30, 50, -25), 1.8),
        Light(Vector3(30, 20, 30), 1.7),
    ]

    for light in lights:
        scene.add_light(light)

    return scene

def add_objects(scene):
    ivory = Material(Vector4(0.6, 0.3, 0.1, 0), Vector3(0.4, 0.4, 0.3), 50.0, 1.0)
    red_rubber = Material(Vector4(0.9, 0.1, 0, 0), Vector3(0.3, 0.1, 0.1), 10.0, 1.0)

    glass = Material(Vector4(0.0, 0.5, 0.1, 0.8), Vector3(0.4, 0.4, 0.3), 125.0, 1.5)
    mirror = Material(Vector4(0.0, 10.0, 0.8, 0), Vector3(1.0, 1.0, 1.0), 1425.0, 1.0)
    
    objects = [
        Panel(Vector3(0, -4, -20), 20, 20),
        Sphere(Vector3(-3, 0, -16), 2, ivory),
        Sphere(Vector3(-1, -1.5, -12), 2, glass),
        Sphere(Vector3(1.5, -0.5, -18), 3, red_rubber),
        Sphere(Vector3(7, 5, -18), 4, mirror),
    ]

    for obj in objects:
        scene.add_object(obj)

    return scene


def main():
    options = {
        'reflect': True, 
        'refract': False, 
        'max_depth': 3,
        'shadow': True,
        'light': True,
        'specular_light': False,
        'envmap': False,
    }
    renderer = Renderer(1024, 768, options)

    envmap = Image.open("envmap.jpg")
    scene = Scene(envmap)

    add_lights(scene)
    add_objects(scene)

    frame = renderer.render(scene)

    write_ppm('out_new.ppm', frame)


if __name__ == "__main__":
    main()