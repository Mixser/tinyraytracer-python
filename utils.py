import math

from entities import Vector3

def build_origin(point, direction, normal):
    if direction * normal < 0:
        origin = point - normal * 1e-3
    else:
        origin = point + normal * 1e-3

    return origin


def reflect(v, normal):
    return v - normal * 2 * (v * normal)

def refract(v, normal, refractive_index):
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