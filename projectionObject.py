import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class ProjectionObject:
    def __init__(self, coordinate=[0, 0, 0], size=1):
        self.vertices = np.array([[0, 0, 0],
                                  [1, 0, 0],
                                  [1, 1, 0],
                                  [0, 1, 0],
                                  [0, 0, 1],
                                  [1, 0, 1],
                                  [1, 1, 1],
                                  [0, 1, 1]]) * size + np.array(coordinate)
        self.faces = [[0, 1, 2, 3],
                      [4, 5, 6, 7],
                      [0, 1, 5, 4],
                      [2, 3, 7, 6],
                      [1, 2, 6, 5],
                      [0, 3, 7, 4]]

    def get_center(self):
        min_coords = np.min(self.vertices, axis=0)
        max_coords = np.max(self.vertices, axis=0)
        center = (min_coords + max_coords) / 2
        return center

    def translate_object(self, translation_vector):
        self.vertices += translation_vector

    def scale_object(self, scale_factor):
        center = self.get_center()
        self.vertices = center + scale_factor * (self.vertices - center)

    def get_projection_vertices_with_vector(self, direction_vectors_normalized:np.ndarray):
        # Find the intersection points of direction vectors and the XY plane
        vector_scale_value = -self.vertices[:, 2] / direction_vectors_normalized[:, 2]
        projection_vertices = self.vertices + vector_scale_value[:, np.newaxis] * direction_vectors_normalized
        return projection_vertices

    def plot_object(self, ax):
        cube = Poly3DCollection([self.vertices[face] for face in self.faces], alpha=0.25, edgecolor='black', label='Original object')
        ax.add_collection3d(cube)
        ax.scatter3D(*self.vertices.T, color='red')

    def plot_projection(self, ax, projection_vertices):
        polygon = Poly3DCollection([projection_vertices[face] for face in self.faces], alpha=0.5, edgecolor='black', label='Projection')
        ax.add_collection3d(polygon)

    def plot_light_source(self, ax, light):
        ax.scatter(*light, color='g', label='Light source')

    def get_projection_vertices(self, light=[0, 0, 8], projection_choice='parallel', translation_vector=None, scale_factor=None):
        self.light = np.array(light)
        if scale_factor is not None:
            self.scale_object(scale_factor)

        if translation_vector is not None:
            self.translate_object(translation_vector)

        projection_vertices = None

        if projection_choice == 'orthographic':
            projection_vertices = self.vertices.copy()
            projection_vertices[:,2] = 0
        elif projection_choice == 'oblique':
            direction_vectors = self.get_center() - self.light
            direction_vectors_normalized = direction_vectors / np.linalg.norm(direction_vectors, keepdims=True)
            direction_vectors_normalized = np.tile(direction_vectors_normalized, (self.vertices.shape[0], 1))
            projection_vertices = self.get_projection_vertices_with_vector(direction_vectors_normalized)
        elif projection_choice == 'perspective':
            direction_vectors = self.vertices - self.light
            direction_vectors_normalized = direction_vectors / np.linalg.norm(direction_vectors, axis=1, keepdims=True)
            projection_vertices = self.get_projection_vertices_with_vector(direction_vectors_normalized)

        return projection_vertices

if __name__ == "__main__":
    cube = ProjectionObject(coordinate=[1, 1, 1], size=2)
    projection_vertices = cube.get_projection_vertices(projection_choice='orthographic')