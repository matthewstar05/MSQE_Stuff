class MyClass:
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return f"MyClass: {self.x}"

    def __repr__(self):
        return f"MyClass: {self.x}"

    def __eq__(self, other):
        return self.x == other.x

def test_classes():
    obj1 = MyClass(1)
    obj2 = MyClass(1)
    obj3 = MyClass(2)
    assert obj1 == obj2
    assert obj1 != obj3
    assert obj2 != obj3
    assert obj1 != "1"
    assert obj1 != 1
    assert obj1 != [1]

def main():
    test_classes()

if __name__ == "__main__":
    main()