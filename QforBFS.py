class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.right = None
        self.left = None

class QforBFS:
    def __init__(self) -> None:
        self.len = 0
        self.head = None
        self.tail = None

    def enqueue(self, value):
        new_node = Node(value)
        if not self.head:
            self.tail = new_node
            self.head = self.tail
        else:
            self.tail.right = new_node
            new_node.left = self.tail
            self.tail = new_node
        self.len += 1
        return self
    
    def dequeue(self):
        if not self.head: return self
        self.head = self.head.right
        self.len -= 1
        if self.len == 0: self.tail = None
        return self
    
    def as_list(self):
        node = self.head
        outp = []
        while node:
            outp.append(node.value)
            node = node.right
        return outp
    
