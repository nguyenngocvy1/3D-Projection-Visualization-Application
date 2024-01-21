import numpy as np
import matplotlib.pyplot as plt
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

    def get_projection_vertices(self, direction_vectors_normalized):
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

    def plot_object_and_projection(self, light=[0, 0, 8], projection_choice='orthographic', translation_vector=None, scale_factor=None):
        self.light = np.array(light)
        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal', adjustable='box')
        
        # Scale and translate
        if scale_factor is not None:
            self.scale_object(scale_factor)

        if translation_vector is not None:
            self.translate_object(translation_vector)

        # Calculate projection
        match projection_choice:
            case 'orthographic':
                projection_vertices = self.vertices.copy()
                projection_vertices[:,2] = 0
            case 'oblique':
                direction_vectors = self.get_center() - self.light
                direction_vectors_normalized = direction_vectors / np.linalg.norm(direction_vectors, keepdims=True)
                direction_vectors_normalized = np.tile(direction_vectors_normalized, (self.vertices.shape[0], 1))
                projection_vertices = self.get_projection_vertices(direction_vectors_normalized)
                self.plot_light_source(ax, self.light)
            case 'perspective':
                direction_vectors = self.vertices - self.light
                direction_vectors_normalized = direction_vectors / np.linalg.norm(direction_vectors, axis=1, keepdims=True)
                projection_vertices = self.get_projection_vertices(direction_vectors_normalized)
                self.plot_light_source(ax, self.light)

        #plot object and projection
        self.plot_object(ax)
        self.plot_projection(ax, projection_vertices)

        # Set plot limits for better visualization
        ax.set_xlim([0, 8])
        ax.set_ylim([0, 8])
        ax.set_zlim([0, 8])

        # Add labels and legend
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()

def main():
    cube = ProjectionObject(coordinate=[1, 1, 1], size=2)
    cube.plot_object_and_projection(projection_choice = 'orthographic')
    
    # Plot the parallel projection
    light = [0, 0, 8]
    cube.plot_object_and_projection(light=light, projection_choice = 'oblique')
    
    # Plot perspective projection
    cube.plot_object_and_projection(projection_choice = 'perspective')

    # Move the cube by applying a translation
    translation_vector = np.array([1, 1, 1])
    cube.plot_object_and_projection(translation_vector=translation_vector)

    # Scale the cube by applying a scaling factor
    scale_factor = 2
    cube.plot_object_and_projection(light=[0, 4, 8], scale_factor=scale_factor)
    
if __name__ == '__main__':
    main()