class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @x.setter
    def x(self, x):
        return self.__x

    @property
    def y(self):
        return self.__y





point = Point(5, 10)

print(point.x)  # 5
print(point.y)  # 10








