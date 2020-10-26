from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction, QStatusBar, QCheckBox
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Signals
        # self.windowTitleChanged.connect(self.onWindowTitleChange)
        # self.windowTitleChanged.connect((lambda x: self.my_custom_fn()))
        # self.windowTitleChanged.connect((lambda x: self.my_custom_fn(x)))
        # self.windowTitleChanged.connect((lambda x: self.my_custom_fn(x, 25)))

        self.setWindowTitle("Volunteer Robot")

        label = QLabel("This is a label")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    # # Slot
    # def onWindowTitleChange(self, s):
    #     print(s)
    #
    # # SLOT: This has default parameters and can be called without a value
    # def my_custom_fn(self, a="HELLLO!", b=5):
    #     print(a, b)
    #
    # def contextMenuEvent(self, event):
    #     # overrides right clicking in the window
    #     print("Context menu event!")
    #     super(MainWindow, self).contextMenuEvent(event)     # but still does the thing

app = QApplication([])  # one instance required for every application

window = MainWindow()
window.show()           # qmainwindow is invisible by default

app.exec_()             # runs until the user closes
