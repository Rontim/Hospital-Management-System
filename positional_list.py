class _Node:
    def __init__(self, element, prev=None, next=None):
        self._element = element
        self._prev = prev
        self._next = next


class PositionalList:
    class Position:
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            return not (self == other)

        def __str__(self):
            return str(self.element())

    def __init__(self):
        self._header = _Node(None)
        self._trailer = _Node(None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("Position is not valid.")
        if p._container is not self:
            raise ValueError("Position does not belong to this list.")
        if p._node._next is None:
            raise ValueError("Position is no longer valid.")
        return p._node

    def _make_position(self, node):
        if node is self._header or node is self._trailer:
            return None
        else:
            return self.Position(self, node)

    def first(self):
        return self._make_position(self._header._next)

    def last(self):
        return self._make_position(self._trailer._prev)

    def before(self, p):
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        node = self._validate(p)
        return self._make_position(node._next)

    def _insert_between(self, element, predecessor, successor):
        new_node = _Node(element, predecessor, successor)
        predecessor._next = new_node
        successor._prev = new_node
        self._size += 1
        return self._make_position(new_node)

    def add_first(self, element):
        return self._insert_between(element, self._header, self._header._next)

    def add_last(self, element):
        return self._insert_between(element, self._trailer._prev, self._trailer)

    def add_before(self, p, element):
        node = self._validate(p)
        return self._insert_between(element, node._prev, node)

    def add_after(self, p, element):
        node = self._validate(p)
        return self._insert_between(element, node, node._next)

    def delete(self, p):
        node = self._validate(p)
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        element = node._element
        node._prev = node._next = node._element = None
        self._size -= 1
        return element

    def replace(self, p, element):
        node = self._validate(p)
        old_element = node._element
        node._element = element
        return old_element

    def __iter__(self):
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def __str__(self):
        elements = [str(position.element()) for position in self]
        return "PositionalList: " + ", ".join(elements)
