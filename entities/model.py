import utils

from .objects import SceneObject, SceneIntersectionObject
from .base import Vector3

class Model(object):
    def __init__(self, filename):
        vertex = []
        faces = []
        triangles = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                items = line.split()

                x, y, z = items[1:4]
                if items[0] == 'v':                    
                    vertex.append(Vector3(float(x), float(y), float(z)))
                elif items[0] == 'f':
                    faces.append(Vector3(int(x) - 1, int(y) - 1, int(z) - 1))
                    triangles.append(
                        (vertex[int(x) - 1], vertex[int(y) - 1], vertex[int(z) - 1])
                    )

        self._vertex = vertex
        self._faces = faces
        self._triangles = triangles

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

    def ray_intersect(self, origin, direction):
        for fi, triangle in enumerate(self._triangles):
            intersection = self.ray_triangle_intersect(fi, triangle, origin, direction)

            if intersection:
                return intersection
            
        return None

    def ray_triangle_intersect(self, fi, tri, origin, direction):
        edge_1 = tri[1] - tri[0]
        edge_2 = tri[2] - tri[0]

        pvec = self._cross(direction, edge_2)

        determinant = edge_1 * pvec

        if determinant < 1e-5:
            return None

        tvec = origin - tri[0]

        u = tvec * pvec
        if u < 0 or u > determinant:
            return None

        qvec = self._cross(tvec, edge_1)
        v = direction * qvec

        if v < 0 or u + v > determinant:
            return None

        tnear = edge_2 * qvec * (1.0/determinant)

        if tnear < 1e-5:
            return None

        normal = self._cross(edge_1, edge_2).normalize()
        return tnear, origin + tnear * direction, normal

    
