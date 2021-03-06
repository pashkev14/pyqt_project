import sys

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPolygon, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QFileDialog, QColorDialog, QSizePolicy, \
    QLabel
from PyQt5.QtCore import Qt, QPoint, QRect

# фантазия дошла только до размеров и их текстовых ключей
MAINSIZE_KEYS = {'Маленькая': 2,
                 'Средняя': 3,
                 'Большая': 5,
                 'Очень большая': 8}


class Canvas(QWidget):  # виновник торжества
    def __init__(self):
        super(Canvas, self).__init__()
        # сколько параметров, на любой вкус
        # стандартный инструмент, цвет(прописано как для кисти, так и для заливки), толщина, курсор, заливать или нет
        # также здесь определены точка и отображаемые цвета; окно бы попросту не поделилось такой инфой с холстом
        self.objects = []
        self.instrument = 'brush'
        self.default_color = 'color_1'
        self.pen_color = QColor(0, 0, 0)
        self.brush_color = QColor(255, 255, 255)
        self.lineSize = 3
        self.setCursor(Qt.CrossCursor)
        self.currentPoint = QPoint()
        self.fill = False
        self.saved = False
        self.color_pix1 = QLabel()
        self.color_pix2 = QLabel()
        self.color_pix1.setStyleSheet('background-color: rgb(0, 0, 0)')
        self.color_pix2.setStyleSheet('background-color: rgb(255, 255, 255)')

    def paintEvent(self, event):  # непосредственно процесс отрисовки объектов на холст
        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            obj.draw(painter)
        painter.end()

    def mousePressEvent(self, event):  # обработка клика по мыши; о хитросплетениях параметров в описании классов
        if self.instrument == 'brush':
            if self.default_color == 'color_1':
                self.objects.append(Brush(event.pos(), event.pos(), self.lineSize, self.pen_color))
            else:
                self.objects.append(Brush(event.pos(), event.pos(), self.lineSize, self.brush_color))
            self.currentPoint = event.pos()
            self.update()
        elif self.instrument == 'pencil':
            if self.default_color == 'color_1':
                self.objects.append(Pencil(event.pos(), event.pos(), self.pen_color))
            else:
                self.objects.append(Pencil(event.pos(), event.pos(), self.brush_color))
            self.currentPoint = event.pos()
            self.update()
        elif self.instrument == 'eraser':
            self.objects.append(Eraser(event.pos(), event.pos(), self.lineSize))
            self.currentPoint = event.pos()
            self.update()
        elif self.instrument == 'fill':
            if self.default_color == 'color_1':
                self.objects.append(Fill(self.width(), self.height(), self.pen_color))
            else:
                self.objects.append(Fill(self.width(), self.height(), self.brush_color))
            self.update()
        elif self.instrument == 'line':
            if self.default_color == 'color_1':
                self.objects.append(Line(event.x(), event.y(), event.x(), event.y(), self.lineSize, self.pen_color))
            else:
                self.objects.append(Line(event.x(), event.y(), event.x(), event.y(), self.lineSize, self.brush_color))
            self.update()
        elif self.instrument == 'circle':
            if self.default_color == 'color_1':
                self.objects.append(
                    Circle(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.pen_color,
                           self.brush_color))
            else:
                self.objects.append(
                    Circle(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.brush_color,
                           self.pen_color))
            self.update()
        elif self.instrument == 'rectangle':
            if self.default_color == 'color_1':
                self.objects.append(
                    Rectangle(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.pen_color,
                              self.brush_color))
            else:
                self.objects.append(
                    Rectangle(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.brush_color,
                              self.pen_color))
            self.update()
        elif self.instrument == 'triangle':
            if self.default_color == 'color_1':
                self.objects.append(
                    Triangle(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.pen_color,
                             self.brush_color))
            else:
                self.objects.append(
                    Triangle(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.brush_color,
                             self.pen_color))
            self.update()
        elif self.instrument == '5gon':
            if self.default_color == 'color_1':
                self.objects.append(
                    Pentagon(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.pen_color,
                             self.brush_color))
            else:
                self.objects.append(
                    Pentagon(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.brush_color,
                             self.pen_color))
            self.update()
        elif self.instrument == '6gon':
            if self.default_color == 'color_1':
                self.objects.append(
                    Hexagon(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.pen_color,
                            self.brush_color))
            else:
                self.objects.append(
                    Hexagon(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.brush_color,
                            self.pen_color))
            self.update()
        elif self.instrument == '8gon':
            if self.default_color == 'color_1':
                self.objects.append(
                    Octagon(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.pen_color,
                            self.brush_color))
            else:
                self.objects.append(
                    Octagon(event.x(), event.y(), event.x(), event.y(), self.fill, self.lineSize, self.brush_color,
                            self.pen_color))
            self.update()

    def mouseMoveEvent(self, event):  # обработка движения мыши; о хитросплетениях параметров в описании классов
        if self.instrument == 'brush':
            if self.default_color == 'color_1':
                self.objects.append(Brush(self.currentPoint, event.pos(), self.lineSize, self.pen_color))
            else:
                self.objects.append(Brush(self.currentPoint, event.pos(), self.lineSize, self.brush_color))
            self.currentPoint = event.pos()
            self.update()
        elif self.instrument == 'pencil':
            if self.default_color == 'color_1':
                self.objects.append(Pencil(self.currentPoint, event.pos(), self.pen_color))
            else:
                self.objects.append(Pencil(self.currentPoint, event.pos(), self.brush_color))
            self.currentPoint = event.pos()
            self.update()
        elif self.instrument == 'eraser':
            self.objects.append(Eraser(self.currentPoint, event.pos(), self.lineSize))
            self.currentPoint = event.pos()
            self.update()
        elif self.instrument == 'line':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'circle':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == 'rectangle':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == 'triangle':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == '5gon':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == '6gon':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == '8gon':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()

    def setDefaultColor(self):  # установка ведущего цвета
        if self.sender().text() == 'Цвет 1':
            self.default_color = 'color_1'
        else:
            self.default_color = 'color_2'

    def setCustomColor(self):  # дадим пользователю расширить палитру
        custom = QColorDialog()
        custom.exec()
        if self.default_color == 'color_1':
            self.pen_color = custom.selectedColor()
            self.updateColor(self.pen_color)
        else:
            self.brush_color = custom.selectedColor()
            self.updateColor(self.brush_color)

    def updateColor(self, color):  # обновление отображаемых цветов
        fill_color = color.name()
        if self.default_color == 'color_1':
            self.color_pix1.setStyleSheet(f'background-color: {fill_color}')
        else:
            self.color_pix2.setStyleSheet(f'background-color: {fill_color}')

    # спасибо Яндексу за предоставленную инфу
    def setRed(self):  # поставить красный
        if self.default_color == 'color_1':
            self.pen_color = QColor(255, 0, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(255, 0, 0)
            self.updateColor(self.brush_color)

    def setOrange(self):  # поставить оранжевый
        if self.default_color == 'color_1':
            self.pen_color = QColor(255, 165, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(255, 165, 0)
            self.updateColor(self.brush_color)

    def setYellow(self):  # поставить желтый
        if self.default_color == 'color_1':
            self.pen_color = QColor(255, 255, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(255, 255, 0)
            self.updateColor(self.brush_color)

    def setGreen(self):  # поставить зеленый
        if self.default_color == 'color_1':
            self.pen_color = QColor(0, 128, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(0, 128, 0)
            self.updateColor(self.brush_color)

    def setLightBlue(self):  # поставить голубой
        if self.default_color == 'color_1':
            self.pen_color = QColor(66, 170, 255)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(66, 170, 255)
            self.updateColor(self.brush_color)

    def setBlue(self):  # поставить синий
        if self.default_color == 'color_1':
            self.pen_color = QColor(0, 0, 255)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(0, 0, 255)
            self.updateColor(self.brush_color)

    def setPurple(self):  # поставить фиолетовый
        if self.default_color == 'color_1':
            self.pen_color = QColor(139, 0, 255)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(139, 0, 255)
            self.updateColor(self.brush_color)

    def setBlack(self):  # поставить черный
        if self.default_color == 'color_1':
            self.pen_color = QColor(0, 0, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(0, 0, 0)
            self.updateColor(self.brush_color)

    def setWhite(self):  # поставить белый
        if self.default_color == 'color_1':
            self.pen_color = QColor(255, 255, 255)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(255, 255, 255)
            self.updateColor(self.brush_color)

    def setLightGrey(self):  # поставить светло-серый
        if self.default_color == 'color_1':
            self.pen_color = QColor(187, 187, 187)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(187, 187, 187)
            self.updateColor(self.brush_color)

    def setDarkGrey(self):  # поставить темно-серый
        if self.default_color == 'color_1':
            self.pen_color = QColor(73, 66, 61)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(73, 66, 61)
            self.updateColor(self.brush_color)

    def setBrown(self):  # поставить коричневый
        if self.default_color == 'color_1':
            self.pen_color = QColor(150, 75, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(150, 75, 0)
            self.updateColor(self.brush_color)

    def setDarkRed(self):  # поставить темно-красный(а не бордовый)
        if self.default_color == 'color_1':
            self.pen_color = QColor(139, 0, 0)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(139, 0, 0)
            self.updateColor(self.brush_color)

    def setPink(self):  # поставить розовый
        if self.default_color == 'color_1':
            self.pen_color = QColor(255, 192, 203)
            self.updateColor(self.pen_color)
        else:
            self.brush_color = QColor(255, 192, 203)
            self.updateColor(self.brush_color)

    def setFigureFill(self):  # разрешить заливать площадь фигуры
        if self.sender().isChecked():
            self.fill = True
        else:
            self.fill = False

    def setSize(self):  # установить текущую толщину кисти на основе переданного значения
        self.lineSize = MAINSIZE_KEYS[self.sender().currentText()]

    def setBrush(self):  # установить кисть
        self.instrument = 'brush'

    def setPencil(self):  # установить карандаш
        self.instrument = 'pencil'

    def setEraser(self):  # установить ластик
        self.instrument = 'eraser'

    def setFill(self):  # установить заливку
        self.instrument = 'fill'

    def setLine(self):  # установить линию
        self.instrument = 'line'

    def setCircle(self):  # установить эллипс
        self.instrument = 'circle'

    def setTriangle(self):  # установить треугольник
        self.instrument = 'triangle'

    def setRectangle(self):  # установить прямоугольник
        self.instrument = 'rectangle'

    def setPentagon(self):  # установить пятиугольник
        self.instrument = '5gon'

    def setHexagon(self):  # установить шестиугольник
        self.instrument = '6gon'

    def setOctagon(self):  # установить восьмиугольник
        self.instrument = '8gon'


class Brush(Canvas):  # класс кисти, принимает начальную и конечную точки, толщину и цвет кисти
    def __init__(self, sp, ep, size, color):
        super(Brush, self).__init__()
        self.sp = sp
        self.ep = ep
        self.size = size
        self.color = color

    def draw(self, painter):  # отрисовка построена на рисовании линии с постоянным обновлением обеих точек
        painter.setPen(QPen(self.color, self.size, Qt.SolidLine, Qt.RoundCap, Qt.BevelJoin))
        painter.drawLine(self.sp, self.ep)


class Pencil(Brush):  # класс карандаш, для удобства наследован от кисти, только толщина всегда 1 пикс
    def __init__(self, sp, ep, color):
        super(Brush, self).__init__()
        self.sp = sp
        self.ep = ep
        self.color = color

    def draw(self, painter):  # отрисовка карандаша схожа с кистью
        painter.setPen(QPen(self.color, 1))
        painter.drawLine(self.sp, self.ep)


class Eraser(Brush):  # класс ластика, также наследован от кисти, только цвет всегда белый и толщина на 2 пикс больше
    # заданной
    def __init__(self, sp, ep, size):
        super(Brush, self).__init__()
        self.sp = sp
        self.ep = ep
        self.size = size

    def draw(self, painter):  # отрисовка ластика схожа с кистью
        painter.setPen(QPen(Qt.white, self.size + 2))
        painter.drawLine(self.sp, self.ep)


class Line(Canvas):  # класс линии, принимает координаты начальной и конечной точек, толщину и цвет кисти
    def __init__(self, sx, sy, ex, ey, size, color):
        super(Line, self).__init__()
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.size = size
        self.color = color

    def draw(self, painter):  # отличие от кисти в том, что линия обновляет только конечную точку
        painter.setPen(QPen(self.color, self.size))
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)


# пошли многоугольники в бой
# их отрисовка подвязана на прямоугольнике с определенными точками внутри него
class Circle(Canvas):  # класс эллипса, принимает координаты начальной и конечной точек, разрешение на заливку,
    # толщину и цвет контура, а также цвет заливки
    def __init__(self, sx, sy, x, y, fill, size, color, color_2):
        super(Circle, self).__init__()
        self.sx = sx
        self.sy = sy
        self.x = x
        self.y = y
        self.to_fill = fill
        self.size = size
        self.color = color
        self.color_2 = color_2

    def draw(self, painter):  # для отрисовки уже есть метод drawEllipse, реализованный здесь через прямоугольник
        painter.setPen(QPen(self.color, self.size))
        if self.to_fill:
            painter.setBrush(QBrush(self.color_2))
        else:
            painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(self.sx, self.sy, self.x - self.sx, self.y - self.sy)


class Triangle(Canvas):  # класс треугольника, принимает координаты начальной и конечной точек, разрешение на заливку,
    # толщину и цвет контура, а также цвет заливки
    def __init__(self, sx, sy, x, y, fill, size, color, color_2):
        super(Triangle, self).__init__()
        self.sx = sx
        self.sy = sy
        self.x = x
        self.y = y
        self.to_fill = fill
        self.size = size
        self.color = color
        self.color_2 = color_2

    def draw(self, painter):  # отрисовка построена на рисовании многоугольника внутри прямоугольника по правилу
        painter.setPen(QPen(self.color, self.size))
        if self.to_fill:
            painter.setBrush(QBrush(self.color_2))
        else:
            painter.setBrush(QBrush(Qt.NoBrush))
        dist = (self.x - self.sx) // 2  # само правило
        triangle = QPolygon()
        triangle.append(QPoint(self.sx, self.sy))
        triangle.append(QPoint(self.sx + dist, self.y))
        triangle.append(QPoint(self.x, self.sy))
        painter.drawPolygon(triangle)


class Rectangle(Canvas):  # класс прямоугольника, принимает координаты начальной и конечной точек, разрешение на
    # заливку, толщину и цвет контура, а также цвет заливки
    def __init__(self, sx, sy, x, y, fill, size, color, color_2):
        super(Rectangle, self).__init__()
        self.sx = sx
        self.sy = sy
        self.x = x
        self.y = y
        self.to_fill = fill
        self.size = size
        self.color = color
        self.color_2 = color_2

    def draw(self, painter):  # метод drawRect никто не забывал
        painter.setPen(QPen(self.color, self.size))
        if self.to_fill:
            painter.setBrush(QBrush(self.color_2))
        else:
            painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(self.sx, self.sy, self.x - self.sx, self.y - self.sy)


class Pentagon(Canvas):  # класс пятиугольника, принимает координаты начальной и конечной точек, разрешение на заливку,
    # толщину и цвет контура, а также цвет заливки
    def __init__(self, sx, sy, x, y, fill, size, color, color_2):
        super(Pentagon, self).__init__()
        self.sx = sx
        self.sy = sy
        self.x = x
        self.y = y
        self.to_fill = fill
        self.size = size
        self.color = color
        self.color_2 = color_2

    def draw(self, painter):  # отрисовка построена на рисовании многоугольника внутри прямоугольника по правилу
        painter.setPen(QPen(self.color, self.size))
        if self.to_fill:
            painter.setBrush(QBrush(self.color_2))
        else:
            painter.setBrush(QBrush(Qt.NoBrush))
        pentagon = QPolygon()
        dist_x = self.x - self.sx
        dist_y = self.y - self.sy
        # для такого шаманства обратился к нарисованному в MS Paint пятиугольнику
        # и самостоятельно просчитывал координаты
        pentagon.append(QPoint(self.sx + int(dist_x * 0.19), self.sy))
        pentagon.append(QPoint(self.sx, self.sy + int(dist_y * 0.61)))
        pentagon.append(QPoint(self.sx + dist_x // 2, self.y))
        pentagon.append(QPoint(self.x, self.sy + int(dist_y * 0.61)))
        pentagon.append(QPoint(self.sx + int(dist_x * 0.81), self.sy))
        painter.drawPolygon(pentagon)


class Hexagon(Canvas):  # класс шестиугольника, принимает координаты начальной и конечной точек, разрешение на заливку,
    # толщину и цвет контура, а также цвет заливки
    def __init__(self, sx, sy, x, y, fill, size, color, color_2):
        super(Hexagon, self).__init__()
        self.sx = sx
        self.sy = sy
        self.x = x
        self.y = y
        self.to_fill = fill
        self.size = size
        self.color = color
        self.color_2 = color_2

    def draw(self, painter):  # отрисовка построена на рисовании многоугольника внутри прямоугольника по правилу
        painter.setPen(QPen(self.color, self.size))
        if self.to_fill:
            painter.setBrush(QBrush(self.color_2))
        else:
            painter.setBrush(QBrush(Qt.NoBrush))
        hexagon = QPolygon()
        dist_x = self.x - self.sx
        dist_y = self.y - self.sy
        # для такого шаманства обратился к нарисованному в MS Paint шестиугольнику
        # и самостоятельно просчитывал координаты
        hexagon.append(QPoint(self.sx + dist_x // 2, self.sy))
        hexagon.append(QPoint(self.sx, self.sy + int(dist_y * 0.25)))
        hexagon.append(QPoint(self.sx, self.sy + int(dist_y * 0.75)))
        hexagon.append(QPoint(self.sx + dist_x // 2, self.y))
        hexagon.append(QPoint(self.x, self.sy + int(dist_y * 0.75)))
        hexagon.append(QPoint(self.x, self.sy + int(dist_y * 0.25)))
        painter.drawPolygon(hexagon)


class Octagon(Canvas):  # класс восьмиугольника, принимает координаты начальной и конечной точек, разрешение на заливку,
    # толщину и цвет контура, а также цвет заливки
    def __init__(self, sx, sy, x, y, fill, size, color, color_2):
        super(Octagon, self).__init__()
        self.sx = sx
        self.sy = sy
        self.x = x
        self.y = y
        self.to_fill = fill
        self.size = size
        self.color = color
        self.color_2 = color_2

    def draw(self, painter):  # отрисовка построена на рисовании многоугольника внутри прямоугольника по правилу
        painter.setPen(QPen(self.color, self.size))
        if self.to_fill:
            painter.setBrush(QBrush(self.color_2))
        else:
            painter.setBrush(QBrush(Qt.NoBrush))
        octagon = QPolygon()
        dist_x = self.x - self.sx
        dist_y = self.y - self.sy
        octagon.append(QPoint(self.sx + int(dist_x * 0.25), self.sy))
        octagon.append(QPoint(self.sx, self.sy + int(dist_y * 0.25)))
        octagon.append(QPoint(self.sx, self.sy + int(dist_y * 0.75)))
        octagon.append(QPoint(self.sx + int(dist_x * 0.25), self.y))
        octagon.append(QPoint(self.sx + int(dist_x * 0.75), self.y))
        octagon.append(QPoint(self.x, self.sy + int(dist_y * 0.75)))
        octagon.append(QPoint(self.x, self.sy + int(dist_y * 0.25)))
        octagon.append(QPoint(self.sx + int(dist_x * 0.75), self.sy))
        painter.drawPolygon(octagon)


class Fill(Canvas):  # класс заливки
    def __init__(self, w, h, color):
        super(Fill, self).__init__()
        self.w = w
        self.h = h
        self.color = color

    def draw(self, painter):  # заливка построена на прямоугольнике во весь холст заданного цвета
        painter.setPen(QPen(self.color))
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0, 0, self.w, self.h)


class Image(Canvas):  # класс картинки
    def __init__(self, w, h, file):
        super(Image, self).__init__()
        self.rect = QRect(0, 0, w, h)
        self.file = file

    def draw(self, painter):  # создаем картинку, загружаем файл и ставим ее на весь холст
        image = QImage()
        image.load(self.file)
        painter.drawImage(self.rect, image)


class Save(QWidget):  # класс сохранения, создает картинку для сохранения
    def __init__(self, size):
        super(Save, self).__init__()
        self.image = QImage(size, QImage.Format_RGB16)
        self.image.fill(Qt.white)

    def save(self, objects):  # нарисуем все объекты холста на картинке и сохраним эту картинку
        painter = QPainter(self.image)
        for obj in objects:
            obj.draw(painter)
        painter.end()
        file = QFileDialog.getSaveFileName(self, 'Сохранитесь', 'C:/', '(*.bmp);;(*.jpg);;(*.png)')[0]
        self.image.save(file)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())


class Window(QMainWindow):  # класс окна
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('window.ui', self)

        self.main_widget.setEnabled(False)
        self.setMouseTracking(True)
        self.menubar.setEnabled(False)
        # это чтобы юзер мог получать по шапке вовремя, но для начала выведем стартовое сообщение
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Question)
        self.message.setWindowTitle('Запускаем')
        self.message.setText('- Для начала работы создайте новый файл или откройте '
                             'существующий.')
        self.message.addButton('- Хорошо.', QMessageBox.YesRole)
        self.message.exec()
        self.menubar.setEnabled(True)
        # создаем и настраиваем холст
        self.canvas = Canvas()
        self.canvas_layout.addWidget(self.canvas)
        self.color_layout.addWidget(self.canvas.color_pix1, 0, 0)
        self.color_layout.addWidget(self.canvas.color_pix2, 0, 1)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # настраиваем список толщин
        self.size_box.addItems(MAINSIZE_KEYS.keys())
        self.size_box.activated.connect(self.canvas.setSize)
        self.size_box.setCurrentIndex(1)
        # подключение кнопок к инструментам
        self.brush_button.setDefaultAction(self.action_brush)
        self.pencil_button.setDefaultAction(self.action_pencil)
        self.fill_button.setDefaultAction(self.action_fill)
        self.eraser_button.setDefaultAction(self.action_eraser)
        self.line_button.setDefaultAction(self.action_line)
        self.circle_button.setDefaultAction(self.action_circle)
        self.triangle_button.setDefaultAction(self.action_triangle)
        self.rectangle_button.setDefaultAction(self.action_rectangle)
        self.pentagon_button.setDefaultAction(self.action_pentagon)
        self.hexagon_button.setDefaultAction(self.action_hexagon)
        self.octagon_button.setDefaultAction(self.action_octagon)
        # подключение инструментов
        self.action_brush.triggered.connect(self.canvas.setBrush)
        self.action_pencil.triggered.connect(self.canvas.setPencil)
        self.action_fill.triggered.connect(self.canvas.setFill)
        self.action_eraser.triggered.connect(self.canvas.setEraser)
        self.action_line.triggered.connect(self.canvas.setLine)
        self.action_circle.triggered.connect(self.canvas.setCircle)
        self.action_triangle.triggered.connect(self.canvas.setTriangle)
        self.action_rectangle.triggered.connect(self.canvas.setRectangle)
        self.action_pentagon.triggered.connect(self.canvas.setPentagon)
        self.action_hexagon.triggered.connect(self.canvas.setHexagon)
        self.action_octagon.triggered.connect(self.canvas.setOctagon)
        # подключение переключателей
        self.fill_check.toggled.connect(self.canvas.setFigureFill)
        self.maincolor_button.toggled.connect(self.canvas.setDefaultColor)
        self.secondcolor_button.toggled.connect(self.canvas.setDefaultColor)
        self.maincolor_button.setChecked(True)
        # настройки файла
        self.action_open.triggered.connect(self.openFile)
        self.action_save.triggered.connect(self.saveFile)
        self.action_create.triggered.connect(self.newCanvas)
        self.action_clear.triggered.connect(self.clearCanvas)
        # подключение кнопок цветов к действиям
        self.red_button.setDefaultAction(self.action_red)
        self.orange_button.setDefaultAction(self.action_orange)
        self.yellow_button.setDefaultAction(self.action_yellow)
        self.green_button.setDefaultAction(self.action_green)
        self.lightblue_button.setDefaultAction(self.action_lightblue)
        self.blue_button.setDefaultAction(self.action_blue)
        self.purple_button.setDefaultAction(self.action_purple)
        self.black_button.setDefaultAction(self.action_black)
        self.white_button.setDefaultAction(self.action_white)
        self.lightgrey_button.setDefaultAction(self.action_lightgrey)
        self.darkgrey_button.setDefaultAction(self.action_darkgrey)
        self.brown_button.setDefaultAction(self.action_brown)
        self.darkred_button.setDefaultAction(self.action_darkred)
        self.pink_button.setDefaultAction(self.action_pink)
        self.customcolor_button.clicked.connect(self.canvas.setCustomColor)
        # подключение стандартных цветов
        self.action_red.triggered.connect(self.canvas.setRed)
        self.action_orange.triggered.connect(self.canvas.setOrange)
        self.action_yellow.triggered.connect(self.canvas.setYellow)
        self.action_green.triggered.connect(self.canvas.setGreen)
        self.action_lightblue.triggered.connect(self.canvas.setLightBlue)
        self.action_blue.triggered.connect(self.canvas.setBlue)
        self.action_purple.triggered.connect(self.canvas.setPurple)
        self.action_black.triggered.connect(self.canvas.setBlack)
        self.action_white.triggered.connect(self.canvas.setWhite)
        self.action_lightgrey.triggered.connect(self.canvas.setLightGrey)
        self.action_darkgrey.triggered.connect(self.canvas.setDarkGrey)
        self.action_brown.triggered.connect(self.canvas.setBrown)
        self.action_darkred.triggered.connect(self.canvas.setDarkRed)
        self.action_pink.triggered.connect(self.canvas.setPink)
        # особые кнопочки
        self.action_aboutme.triggered.connect(self.aboutProgram)
        self.action_help.triggered.connect(self.helpMe)

    def openFile(self):  # открываем файл
        file = QFileDialog.getOpenFileName(self, 'Выберите картинку', 'C:/', '(*.bmp);;(*.jpg);;(*.png)')[0]
        self.canvas.objects.append(Image(self.canvas.width(), self.canvas.height(), file))  # просто рисуем объект
        # класса картинка
        self.main_widget.setEnabled(True)

    def saveFile(self):  # сохраняем файл, то есть, выполняем метод сохранения из класса сохранения
        saver = Save(self.canvas.size())
        saver.save(self.canvas.objects)
        self.canvas.saved = True

    def newCanvas(self):  # создаем файл
        if not self.main_widget.isEnabled():  # при запуске окно отключено, чтобы юзер не намутил лишнего
            self.main_widget.setEnabled(True)
            self.clearCanvas()
        else:
            if not self.canvas.saved:
                self.message = QMessageBox()  # создание файла предлагает сохранение в отличии от очистки холста
                self.message.setIcon(QMessageBox.Warning)
                self.message.setWindowTitle('Помощь забывчивым')
                self.message.setText('- Погоди. Ты сейчас хочешь избавиться от рисунка, '
                                     'и даже не предусмотрел сохранение!\n'
                                     'Следующий ход ведет к точке невозврата, хорошо подумай!\n')
                self.message.addButton('- Лучше сохраниться.', QMessageBox.YesRole)
                self.message.addButton('- Не, не буду.', QMessageBox.NoRole)
                self.message.exec()
                if self.message.buttonRole(self.message.clickedButton()) == 5:  # именно тест принтом вывел такое
                    # значение
                    self.saveFile()
                else:
                    self.clearCanvas()
            else:
                self.clearCanvas()

    def clearCanvas(self):  # рисует объект класса заливки белого цвета
        self.canvas.objects.append(Fill(self.canvas.width(), self.canvas.height(), Qt.white))
        self.update()

    def aboutProgram(self):  # не бейте за такое кощунство, но лучше уж написать инфо, пока не поздно
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)
        self.message.setWindowTitle('Для совсем скучающих или любопытных')
        self.message.setText('Made by Пабло Сабля, 2020. ver. 1.1\n\n\n\n\n'
                             'Апдейт-лист:\n'
                             '1.1 - исправлено сохранение в более удобную сторону.\n\n\n\n\n'
                             '    - добавлены координаты под холст'
                             'Привет! Тебя уже стоит отблагодарить, что зашел!\n'
                             'Здесь творятся чудеса графики, стоит лишь взять под контроль мышь.\n\n\n\n\n'
                             'За использование программы в коммерческих целях а-та-та.\n'
                             'ТЫ ПОНЯЛ!?')
        self.message.addButton('Очень полезная информация, спасибо автору!', QMessageBox.YesRole)
        self.message.exec()

    def helpMe(self):  # самый крутой и важный метод
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)
        self.message.setWindowTitle('Подмога')
        self.message.setText('Общее:\n\n'
                             'Привет! Если попал сюда, а окно не работает, то создай или открой файл.\n'
                             'Невзрачные или громоздкие курсоры? Это Qt выпендривается, '
                             'тебе могу предложить лишь поменять стандартный курсор в панели управления.\n'
                             'Тебе будут предлагать сохраниться. Лучше сохраняться, '
                             'специально для тебя будет диалоговое окно.\n'
                             'За очистку холста и баны за непотребные художества '
                             'НИКТО не ответственен, держи в курсе!\n\n\n\n'
                             'Рисование:\n\n'
                             'Стандартный инструмент - кисть черного цвета средней толщины, '
                             'можешь сразу начать рисовать.\n'
                             'Принцип знаешь? Если нет, то тебе нужна мышь с левой кнопкой или устройства, '
                             'имитирующие ЛКМ.\n'
                             'Все стандартные действия прописаны сверху, '
                             'но самые необходимые продублированы в удобном виде на панели инструментов.\n'
                             'Кнопки "Цвет 1" и "Цвет 2" меняют текущий цвет. Не влияет на ластик.\n'
                             'Флажок заливки позволяет залить площадь фигуры вторым цветом, '
                             'потому он расположен в разделе "Фигуры".\n'
                             'Предупреждение: под вторым цветом имеется ввиду неактивный цвет, '
                             'то есть, если выбранный цвет "Цвет 1" - контур будет рисоваться цветом 1 , '
                             'а заливка - цветом 2.\n'
                             'Нужны собственные цвета? Кнопка "Создать цвет" , '
                             'и диалоговое окно с цветами в твоем распоряжении.\n'
                             'Список толщин позволяет настроить толщину кисти. Не влияет на карандаш.\n\n\n\n'
                             'Работа с файлами:\n\n'
                             'Открыв картинку, она отобразится поверх всего холста.\n'
                             'Кнопка "Очистить" не ответственна за потери!\n\n'
                             'Надеюсь, что ты разобрался с этой маленькой брошюркой!')
        self.message.addButton('Тоже хочу надеяться', QMessageBox.YesRole)
        self.message.exec()

    def closeEvent(self, event):  # перед закрытием ОБЯЗАТЕЛЬНО предупредить о сохранениях
        if self.main_widget.isEnabled():
            if not self.canvas.saved:
                self.message = QMessageBox()
                self.message.setIcon(QMessageBox.Warning)
                self.message.setWindowTitle('Полиция сохраненок')
                self.message.setText('- Стоять! Это полиция!\n'
                                     'Вы нарушили приказ 66 "О сохранениях"!\n')
                self.message.addButton('- Ладно, сохранюсь.', QMessageBox.YesRole)
                self.message.addButton('- Нет, я против системы!', QMessageBox.NoRole)
                self.message.exec()
                if self.message.buttonRole(self.message.clickedButton()) == 5:
                    self.saveFile()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.showMaximized()
    sys.exit(app.exec())
