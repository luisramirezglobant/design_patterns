from abc import ABC, abstractmethod

# Implementor
class DrawingAPI(ABC):
    @abstractmethod
    def draw_circle(self, x, y, radius):
        pass

    @abstractmethod
    def draw_square(self, x, y, side):
        pass

# Concrete Implementor 1
class WindowsAPI(DrawingAPI):
    def draw_circle(self, x, y, radius):
        print(f"WindowsAPI: Drawing circle at ({x}, {y}) with radius {radius}")

    def draw_square(self, x, y, side):
        print(f"WindowsAPI: Drawing square at ({x}, {y}) with side {side}")

# Concrete Implementor 2
class LinuxAPI(DrawingAPI):
    def draw_circle(self, x, y, radius):
        print(f"LinuxAPI: Drawing circle at ({x}, {y}) with radius {radius}")

    def draw_square(self, x, y, side):
        print(f"LinuxAPI: Drawing square at ({x}, {y}) with side {side}")

# Abstraction
class Shape(ABC):
    def __init__(self, drawing_api):
        self._drawing_api = drawing_api

    @abstractmethod
    def draw(self):
        pass

# Refined Abstraction 1
class Circle(Shape):
    def __init__(self, x, y, radius, drawing_api):
        super().__init__(drawing_api)
        self._x = x
        self._y = y
        self._radius = radius

    def draw(self):
        self._drawing_api.draw_circle(self._x, self._y, self._radius)

# Refined Abstraction 2
class Square(Shape):
    def __init__(self, x, y, side, drawing_api):
        super().__init__(drawing_api)
        self._x = x
        self._y = y
        self._side = side

    def draw(self):
        self._drawing_api.draw_square(self._x, self._y, self._side)

# Client Code
def main():
    circle = Circle(1, 2, 3, WindowsAPI())
    circle.draw()

    square = Square(4, 5, 6, LinuxAPI())
    square.draw()

if __name__ == "__main__":
    main()