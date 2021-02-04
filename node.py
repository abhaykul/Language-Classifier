"""
Abhay Kulkarni
python v3.9


Node class
"""
from leaf import Leaf


# Node class, has 2 children for storing either a (Node and/or Leaf)
class Node:

    def __init__(self, attribute, attribute_name=None, default_child=None, child=None):
        if child is None:
            child = {}
        self.attribute = attribute
        self.attribute_name = attribute_name
        self.default_child = default_child
        self.child = child

    def add(self, val, subtree):
        self.child[val] = subtree

    # For debugging by printing
    def show_tree(self, indent=0):
        name = self.attribute_name
        print('Test', name)
        for (key, value) in self.child.items():
            print(((' ' * 2 * indent) + " If " + str(name) + ' is ' + str(key) + ' ==> '), end=' ')
            if isinstance(value, Node):
                value.show_tree(indent + 1)
            elif isinstance(value, Leaf):
                print(value.op())

    # To test the model
    def __call__(self, example):
        attribute_value = example[self.attribute]
        if attribute_value in self.child:
            return self.child[attribute_value](example)
        else:
            return self.default_child(example)

    def __repr__(self):
        return "Branch (" + str(self.attribute_name) + " , " + str(self.child) + ")"
