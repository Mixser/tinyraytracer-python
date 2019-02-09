import utils

from .objects import SceneObject, SceneIntersectionObject
from .base import Vector3

class Model(SceneObject):
    def __init__(self, filename):
        vertex = []
        faces = []
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    print(line.split(' '))
                    (_, x, y, z, _) = line.split(' ')
                    vertex.append(Vector3(float(x), float(y), float(z)))
                elif line.startswith('f '):
                    print(line.split(' '))
                    (_, x, y, z, _) = line.split(' ')
                    faces.append(Vector3(int(x) - 1, int(y) - 1, int(z) - 1))

        self._vertex = vertex
        self._faces = faces

    @classmethod
    def _cross(cls, v1, v2):
        return utils.cross(v1, v2)


    def vertices_count(self):
        return len(self._vertex)

    def triangles_count(self):
        return len(self._faces)

    def point_at(self, index):
        return self._vertex[index]

    def vertex_at(self, triangle_index, local_index):
        return self._faces[triangle_index][local_index]

    def get_bbox(self):
        min_ = [self._vertex[0][0], self._vertex[0][1], self._vertex[0][2]]
        max_ = min_[:]

        for v in self._vertex:
            for j in range(0, 3):
                min_[j] = min(min_[j], v[j])
                max_[j] = max(max_[j], v[j])

        return Vector3(*min_), Vector3(*max_)
    

    def _ray_intersect(self, origin, direction):
        min_, max_ = self.get_bbox()
        v1 = max_ - origin

        if v1 * direction < 0:
            return None


        for fi in range(self.triangles_count()):
            intersecion = self.ray_triangle_intersect(fi, origin, direction)
            if intersecion:
                return intersecion

        return None

    def ray_triangle_intersect(self, fi, origin, direction):
        edge_1 = self.point_at(self.vertex_at(fi, 1) - self.vertex_at(fi, 0))
        edge_2 = self.point_at(self.vertex_at(fi, 2) - self.vertex_at(fi, 0))

        pvec = self._cross(direction, edge_2)

        determinant = edge_1 * pvec

        if determinant < 1e-5:
            return None

        tvec = origin - self.point_at(self.vertex_at(fi, 0))

        u = tvec * tvec
        if u < 0 or u > determinant:
            return None


        qvec = self._cross(tvec, edge_1)
        v = dir * qvec

        if v < 0 or u + v > determinant:
            return None

        tnear = edge_2 * qvec * (1.0/determinant)

        normal = pvec.normalize()
        return tnear, pvec, normal

    
