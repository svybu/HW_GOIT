class Animal:
    def __init__(self, nickname, weight):
        self.nickname = nickname
        self.weight = weight

    def say(self):
        pass

    def change_weight(self, weight):
        self.weight = weight

animal = Animal('nickname', 10)
print(animal.nickname)
animal.change_weight(12)
print(animal.weight)
