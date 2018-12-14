from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPolygon, QBrush
from PyQt5.QtCore import Qt, QPoint
import sys
from random import randint


class Project(QMainWindow):
    def __init__(self):
        super().__init__()

        self.Top = 200
        self.Left = 200
        self.Width = 1200
        self.Height = 800

        self.setup()

    def setup(self):
        self.setWindowTitle("Paint.V.2.0")
        self.setWindowIcon(QIcon("pic/mainIcon.png"))
        self.setGeometry(self.Top, self.Left, self.Width, self.Height)
        self.setFixedSize(self.Width, self.Height)

        self.brush = "Brush"
        self.brushSize = 1
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushes = mainMenu.addMenu("Brushes")
        brushMenu = mainMenu.addMenu("Brush Size")

        self.BrushSize(brushMenu)
        self.File(fileMenu)
        self.Brushes(brushes)
        self.Image()
        self.Colors(mainMenu)

    def Image(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def Brushes(self, brushes):
        brushe = QAction(QIcon("pic/Brushe.png"), "Brushe", self)
        brushes.addAction(brushe)
        brushe.triggered.connect(self.Brushe)

        airBrushe = QAction(QIcon("pic/airBrushe.png"), "airBrushe", self)
        brushes.addAction(airBrushe)
        airBrushe.triggered.connect(self.AirBrushe)

        calligraphyBrush = QAction(QIcon("pic/calligraphyBrush.png"), "Calligraphy Brush", self)
        brushes.addAction(calligraphyBrush)
        calligraphyBrush.triggered.connect(self.CalligraphyBrush)

    def BrushSize(self, brushMenu):
        px1Action = QAction(QIcon("pic/1px.png"), "1px", self)
        brushMenu.addAction(px1Action)
        px1Action.triggered.connect(self.Px1)

        px3Action = QAction(QIcon("pic/3px.png"), "3px", self)
        brushMenu.addAction(px3Action)
        px3Action.triggered.connect(self.Px3)

        px5Action = QAction(QIcon("pic/5px.png"), "5px", self)
        brushMenu.addAction(px5Action)
        px5Action.triggered.connect(self.Px5)

        px8Action = QAction(QIcon("pic/8px.png"), "8px", self)
        brushMenu.addAction(px8Action)
        px8Action.triggered.connect(self.Px8)

    def Colors(self, mainMenu):
        black = mainMenu.addAction('')
        black.triggered.connect(self.BlackColor)
        black.setIcon(QIcon("pic/black.png"))

        red = mainMenu.addAction('')
        red.triggered.connect(self.RedColor)
        red.setIcon(QIcon("pic/red.png"))

        blue = mainMenu.addAction('')
        blue.triggered.connect(self.BlueColor)
        blue.setIcon(QIcon("pic/blue.png"))

        green = mainMenu.addAction('')
        green.triggered.connect(self.GreenColor)
        green.setIcon(QIcon("pic/green.png"))

        yellow = mainMenu.addAction('')
        yellow.triggered.connect(self.YellowColor)
        yellow.setIcon(QIcon("pic/yellow.png"))

        editColor = mainMenu.addAction('')
        editColor.triggered.connect(self.EditColor)
        editColor.setIcon(QIcon("pic/editColor.png"))

    def File(self, fileMenu):
        saveAction = QAction(QIcon("pic/save.png"), "Save As...", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.Save)

        clearAction = QAction(QIcon("pic/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.Clear)

    def mousePressEvent(self, event):
        self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):

        painter = QPainter(self.image)

        if event.buttons() == Qt.LeftButton:
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            painter.setPen(QPen(Qt.white, self.brushSize, Qt.SolidLine,
                                Qt.RoundCap, Qt.RoundJoin))

        if self.brush == "Brush":
            painter.drawLine(self.lastPoint, event.pos())

        elif self.brush == "airBrushe":
            if event.buttons() == Qt.LeftButton:
                painter.setPen(QPen(self.brushColor, 1,
                                    Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                painter.setPen(QPen(Qt.white, 1, Qt.SolidLine,
                                    Qt.RoundCap, Qt.RoundJoin))
            for i in range((5 if self.brushSize == 1 else 15)):
                x = randint(event.x(), event.x() + self.brushSize * 5)
                y = randint(event.y(), event.y() + self.brushSize * 5)
                painter.drawPoint(x, y)

        elif self.brush == "calligraphyBrush":
            painter.setPen(QPen(self.brushColor, 3,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(QBrush(self.brushColor, Qt.SolidPattern))

            points = QPolygon([
                self.lastPoint,
                QPoint(event.x(), event.y()),
                QPoint(event.x() - 5, event.y() + int(self.brushSize * 1.5)),
                QPoint(self.lastPoint.x() - 5, self.lastPoint.y() + int(self.brushSize * 1.5))
            ]
            )
            painter.drawPolygon(points)

        self.lastPoint = event.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def Save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;"
                                                  " JPEG(*.jpg *.jpeg);;"
                                                  " ALL Files(*.*)")
        if filePath == '':
            return
        else:
            self.image.save(filePath)

    def Clear(self):
        self.image.fill(Qt.white)
        self.update()

    def Px1(self):
        self.brushSize = 1

    def Px3(self):
        self.brushSize = 3

    def Px5(self):
        self.brushSize = 5

    def Px8(self):
        self.brushSize = 8

    def BlackColor(self):
        self.brushColor = Qt.black

    def RedColor(self):
        self.brushColor = Qt.red

    def GreenColor(self):
        self.brushColor = Qt.green

    def YellowColor(self):
        self.brushColor = Qt.yellow

    def BlueColor(self):
        self.brushColor = Qt.blue

    def EditColor(self):
        self.brushColor = QColorDialog.getColor()

    def Brushe(self):
        self.brush = "Brush"

    def AirBrushe(self):
        self.brush = "airBrushe"

    def CalligraphyBrush(self):
        self.brush = "calligraphyBrush"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Project()
    exe.show()
    app.exec()