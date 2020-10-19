from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Volunteer Robot")
        label = QLabel("This is a label")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)


app = QApplication([])  # one instance required for pyqt

window = MainWindow()
window.show()

app.exec_()             # runs until the user closes
