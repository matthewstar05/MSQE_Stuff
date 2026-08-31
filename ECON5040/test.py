class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_front(self, data):
        node = Node(data)
        if self.is_empty():
            node.next = node
            node.prev = node
            self.head = node
        else:
            tail = self.head.prev
            node.next = self.head
            node.prev = tail
            tail.next = node
            self.head.prev = node
            self.head = node
        self.size += 1
        print(f"insert_front({data}) -> {self}")

    def insert_back(self, data):
        node = Node(data)
        if self.is_empty():
            node.next = node
            node.prev = node
            self.head = node
        else:
            tail = self.head.prev
            node.next = self.head
            node.prev = tail
            tail.next = node
            self.head.prev = node
        self.size += 1
        print(f"insert_back({data}) -> {self}")

    def insert_after(self, target, data):
        current = self._find(target)
        if current is None:
            print(f"insert_after({target}, {data}) -> {target} not found")
            return False
        node = Node(data)
        nxt = current.next
        node.prev = current
        node.next = nxt
        current.next = node
        nxt.prev = node
        self.size += 1
        print(f"insert_after({target}, {data}) -> {self}")
        return True

    def delete(self, data):
        current = self._find(data)
        if current is None:
            print(f"delete({data}) -> {data} not found")
            return False
        if current.next is current:
            self.head = None
        else:
            current.prev.next = current.next
            current.next.prev = current.prev
            if current is self.head:
                self.head = current.next
        self.size -= 1
        print(f"delete({data}) -> {self}")
        return True

    def search(self, data):
        found = self._find(data) is not None
        print(f"search({data}) -> {found}")
        return found

    def _find(self, data):
        if self.is_empty():
            return None
        current = self.head
        while True:
            if current.data == data:
                return current
            current = current.next
            if current is self.head:
                return None

    def forward(self):
        if self.is_empty():
            print("forward: []")
            return []
        values = []
        current = self.head
        while True:
            values.append(current.data)
            current = current.next
            if current is self.head:
                break
        print(f"forward: {values}")
        return values

    def backward(self):
        if self.is_empty():
            print("backward: []")
            return []
        values = []
        current = self.head.prev
        while True:
            values.append(current.data)
            current = current.prev
            if current is self.head.prev:
                break
        print(f"backward: {values}")
        return values

    def __len__(self):
        return self.size

    def __str__(self):
        if self.is_empty():
            return "empty"
        values = []
        current = self.head
        while True:
            values.append(str(current.data))
            current = current.next
            if current is self.head:
                break
        return " <-> ".join(values) + " <-> (back to head)"


if __name__ == "__main__":
    print("=== Circular Doubly Linked List ===\n")
    cdll = CircularDoublyLinkedList()
    print(f"new list: {cdll}, size={len(cdll)}\n")

    cdll.insert_back(10)
    cdll.insert_back(20)
    cdll.insert_back(30)
    cdll.insert_front(5)
    cdll.insert_after(20, 25)
    print()

    cdll.forward()
    cdll.backward()
    print()

    cdll.search(25)
    cdll.search(99)
    print()

    cdll.delete(5)
    cdll.delete(30)
    cdll.delete(99)
    print()

    print(f"head={cdll.head}, tail={cdll.head.prev if cdll.head else None}")
    print(f"head.prev={cdll.head.prev.data}, tail.next={cdll.head.prev.next.data}")
    print(f"size={len(cdll)}")
