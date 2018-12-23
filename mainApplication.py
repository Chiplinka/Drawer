from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, \
    QPen, QPolygon, QBrush
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QAction, QFileDialog, QMessageBox
import sys
from random import randint


class Drawer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("Drawer")
        self.setWindowIcon(QIcon("pic/mainIcon.png"))
        self.setGeometry(200, 200, 1200, 800)
        self.setFixedSize(1200, 800)

        self.brush = "Brush"
        self.brushSize = 1
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.firstPoint = False
        self.curPoint = QPoint()
        self.lastType = 'Brush'
        self.rubber = False

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushes = mainMenu.addMenu("Brushes")
        brushMenu = mainMenu.addMenu("Brush Size")
        shapes = mainMenu.addMenu("Shapes")

        self.brush_size(brushMenu)
        self.file(fileMenu)
        self.brushes(brushes)
        self.image_main()
        self.colors(mainMenu)
        self.shapes(shapes)

    def image_main(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def brushes(self, brushes):
        brushe = QAction(QIcon("pic/Brushe.png"), "Brushe", self)
        brushes.addAction(brushe)
        brushe.triggered.connect(self.brushe)

        airBrushe = QAction(QIcon("pic/airBrushe.png"), "airBrushe", self)
        brushes.addAction(airBrushe)
        airBrushe.triggered.connect(self.air_brushe)

        calligraphyBrush = QAction(QIcon("pic/calligraphyBrush.png"),
                                   "Calligraphy Brush", self)
        brushes.addAction(calligraphyBrush)
        calligraphyBrush.triggered.connect(self.calligraphy_brush)

    def brush_size(self, brushMenu):
        px1Action = QAction(QIcon("pic/1px.png"), "1px", self)
        brushMenu.addAction(px1Action)
        px1Action.triggered.connect(self.px1)

        px3Action = QAction(QIcon("pic/3px.png"), "3px", self)
        brushMenu.addAction(px3Action)
        px3Action.triggered.connect(self.px3)

        px5Action = QAction(QIcon("pic/5px.png"), "5px", self)
        brushMenu.addAction(px5Action)
        px5Action.triggered.connect(self.px5)

        px8Action = QAction(QIcon("pic/8px.png"), "8px", self)
        brushMenu.addAction(px8Action)
        px8Action.triggered.connect(self.px8)

    def colors(self, mainMenu):
        black = mainMenu.addAction('')
        black.triggered.connect(self.black_color)
        black.setIcon(QIcon("pic/black.png"))

        red = mainMenu.addAction('')
        red.triggered.connect(self.red_color)
        red.setIcon(QIcon("pic/red.png"))

        blue = mainMenu.addAction('')
        blue.triggered.connect(self.blue_color)
        blue.setIcon(QIcon("pic/blue.png"))

        green = mainMenu.addAction('')
        green.triggered.connect(self.green_color)
        green.setIcon(QIcon("pic/green.png"))

        yellow = mainMenu.addAction('')
        yellow.triggered.connect(self.yellow_color)
        yellow.setIcon(QIcon("pic/yellow.png"))

        editColor = mainMenu.addAction('')
        editColor.triggered.connect(self.edit_color)
        editColor.setIcon(QIcon("pic/editColor.png"))

    def file(self, fileMenu):
        saveAction = QAction(QIcon("pic/save.png"), "Save As...", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save_main)

        clearAction = QAction(QIcon("pic/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

    def shapes(self, shape):
        rectangle = QAction(QIcon("pic/rect.png"), "Rectangle", self)
        shape.addAction(rectangle)
        rectangle.triggered.connect(self.rectangle)

        ellipse = QAction(QIcon("pic/ellipse.png"), "Ellipse", self)
        shape.addAction(ellipse)
        ellipse.triggered.connect(self.ellipse)

    def mousePressEvent(self, event):
        self.lastPoint = event.pos()
        self.curPoint = event.pos()
        self.firstPoint = True

    def mouseReleaseEvent(self, event):
        self.curPoint = event.pos()

        if self.brush == 'rectangle':

            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, 1,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(QBrush(self.brushColor, Qt.SolidPattern))
            points = QPolygon([
                self.lastPoint,
                QPoint(event.x(), self.lastPoint.y()),
                event.pos(),
                QPoint(self.lastPoint.x(), event.y())
            ]
            )
            painter.drawPolygon(points)
            self.firstPoint = False
        elif self.brush == 'ellipse':

            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, 8,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(QBrush(self.brushColor, Qt.SolidPattern))
            painter.drawEllipse(self.lastPoint.x(), self.lastPoint.y(),
                                event.x() - self.lastPoint.x(),
                                event.y() - self.lastPoint.y())
            self.firstPoint = False
        self.update()

    def mouseMoveEvent(self, event):

        painter = QPainter(self.image)
        if event.buttons() == Qt.LeftButton:

            if self.rubber:
                self.brush = self.lastType
                self.rubber = False

            if event.buttons() == Qt.LeftButton:
                painter.setPen(QPen(self.brushColor, self.brushSize,
                                    Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            if self.brush == "Brush":
                painter.drawLine(self.lastPoint, event.pos())

            elif self.brush == "airBrushe":
                if event.buttons() == Qt.LeftButton:
                    painter.setPen(QPen(self.brushColor, 1,
                                        Qt.SolidLine,
                                        Qt.RoundCap,
                                        Qt.RoundJoin))
                for i in range((5 if self.brushSize == 1 else 15)):
                    x = randint(event.x(), event.x() + self.brushSize * 5)
                    y = randint(event.y(), event.y() + self.brushSize * 5)
                    painter.drawPoint(x, y)

            elif self.brush == "calligraphyBrush":
                if event.buttons() == Qt.LeftButton:
                    painter.setPen(QPen(self.brushColor, 3,
                                        Qt.SolidLine,
                                        Qt.RoundCap,
                                        Qt.RoundJoin))
                    painter.setBrush(QBrush(self.brushColor, Qt.SolidPattern))
                points = QPolygon([
                    self.lastPoint,
                    QPoint(event.x(), event.y()),
                    QPoint(event.x() - 5,
                           event.y() + int(self.brushSize * 1.5)),
                    QPoint(self.lastPoint.x() - 5,
                           self.lastPoint.y() + int(self.brushSize * 1.5))
                ]
                )
                painter.drawPolygon(points)

        else:
            if not self.rubber:
                self.lastType = self.brush
            self.brush = "Brush"
            self.rubber = True
            painter.setPen(QPen(Qt.white, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())

        if self.brush != "rectangle" and self.brush != "ellipse":
            self.lastPoint = event.pos()
        self.curPoint = event.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

        if self.brush == "rectangle" and self.firstPoint:
            pt = QPainter(self)
            pt.setPen(QPen(self.brushColor, 1,
                           Qt.SolidLine, Qt.RoundCap,
                           Qt.RoundJoin))
            pt.setBrush(QBrush(self.brushColor, Qt.SolidPattern))
            points = QPolygon([
                self.lastPoint,
                QPoint(self.curPoint.x(), self.lastPoint.y()),
                self.curPoint,
                QPoint(self.lastPoint.x(), self.curPoint.y())
            ]
            )
            pt.drawPolygon(points)
            self.update()
        elif self.brush == 'ellipse' and self.firstPoint:

            pt = QPainter(self)
            pt.setPen(QPen(self.brushColor, 8,
                           Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            pt.setBrush(QBrush(self.brushColor, Qt.SolidPattern))
            pt.drawEllipse(self.lastPoint.x(), self.lastPoint.y(),
                           self.curPoint.x() - self.lastPoint.x(),
                           self.curPoint.y() - self.lastPoint.y())
            self.update()
        elif self.brush == 'Brush' and self.rubber:
            pt = QPainter(self)
            pt.setPen(QPen(Qt.black, 2,
                           Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            pt.drawEllipse(self.lastPoint.x() - int(self.brushSize / 2),
                           self.lastPoint.y() - int(self.brushSize / 2),
                           self.brushSize,
                           self.brushSize)
            self.update()

    def closeEvent(self, event):
        flag = QMessageBox.question(self, 'Exit',
                                    "Do you want to save changes?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if flag == QMessageBox.Yes:
            self.save_main()

    def save_main(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;"
                                                  " JPEG(*.jpg *.jpeg);;"
                                                  " ALL Files(*.*)")
        if filePath == '':
            return
        else:
            self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def px1(self):
        self.brushSize = 1

    def px3(self):
        self.brushSize = 3

    def px5(self):
        self.brushSize = 5

    def px8(self):
        self.brushSize = 8

    def black_color(self):
        self.brushColor = Qt.black

    def red_color(self):
        self.brushColor = Qt.red

    def green_color(self):
        self.brushColor = Qt.green

    def yellow_color(self):
        self.brushColor = Qt.yellow

    def blue_color(self):
        self.brushColor = Qt.blue

    def edit_color(self):
        self.brushColor = QColorDialog.getColor()

    def brushe(self):
        self.brush = "Brush"
        self.lastType = self.brush

    def air_brushe(self):
        self.brush = "airBrushe"
        self.lastType = self.brush

    def calligraphy_brush(self):
        self.brush = "calligraphyBrush"
        self.lastType = self.brush

    def rectangle(self):
        self.brush = "rectangle"
        self.lastType = self.brush

    def ellipse(self):
        self.brush = "ellipse"
        self.lastType = self.brush


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Drawer()
    exe.show()
    app.exec()
