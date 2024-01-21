import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from projectionObject import ProjectionObject

class ProjectionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.cube = ProjectionObject()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('3D Projection Visualization')
        self.setGeometry(100, 100, 600, 800)

        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111, projection='3d')
        self.ax.set_xlim([0, 8])
        self.ax.set_ylim([0, 8])
        self.ax.set_zlim([0, 8])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.coordinate_label = QLabel('Coordinate:')
        self.coordinate_edit = QLineEdit(self)
        self.coordinate_edit.setText('0, 0, 1')

        self.size_label = QLabel('Size:')
        self.size_edit = QLineEdit(self)
        self.size_edit.setText('1')
        
        self.light_label = QLabel('Light Source Coordinate:')
        self.light_edit = QLineEdit(self)
        self.light_edit.setText('0, 0, 8')
        
        self.translation_label = QLabel('Translation Vector:')
        self.translation_edit = QLineEdit(self)
        self.translation_edit.setText('0, 0, 0')
        
        self.scale_label = QLabel('Scale Factor:')
        self.scale_edit = QLineEdit(self)
        self.scale_edit.setText('1')

        self.projection_choice_label = QLabel('Projection Type:')
        self.projection_choice_combo = QComboBox()
        self.projection_choice_combo.addItem('Orthographic')
        self.projection_choice_combo.addItem('Oblique')
        self.projection_choice_combo.addItem('Perspective')

        self.plot_button = QPushButton('Plot', self)
        self.plot_button.clicked.connect(self.plot_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.coordinate_label)
        layout.addWidget(self.coordinate_edit)
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_edit)
        layout.addWidget(self.light_label)
        layout.addWidget(self.light_edit)
        layout.addWidget(self.projection_choice_label)
        layout.addWidget(self.projection_choice_combo)
        layout.addWidget(self.translation_label)
        layout.addWidget(self.translation_edit)
        layout.addWidget(self.scale_label)
        layout.addWidget(self.scale_edit)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot_clicked(self):
        self.cube = ProjectionObject(coordinate=[float(x) for x in self.coordinate_edit.text().split(',')], size=float(self.size_edit.text()))
        self.update_canvas()

    def update_canvas(self):
        self.ax.clear()
        self.cube.plot_object(self.ax)
        projection_choice=self.projection_choice_combo.currentText().lower()
        light=[float(x) for x in self.light_edit.text().split(',')]
        self.cube.plot_projection(self.ax, self.cube.get_projection_vertices(light=[float(x) for x in self.light_edit.text().split(',')], projection_choice=projection_choice, translation_vector=[float(x) for x in self.translation_edit.text().split(',')], scale_factor=float(self.scale_edit.text())))
        if projection_choice != 'orthographic':
            self.cube.plot_light_source(self.ax, light=light)
        self.ax.set_xlim([0, 8])
        self.ax.set_ylim([0, 8])
        self.ax.set_zlim([0, 8])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.legend()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProjectionApp()
    window.show()
    sys.exit(app.exec_())