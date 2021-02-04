"""
Abhay Kulkarni
python v3.9

Leaf class; For terminal "Nodes"
"""


# Leaf class for holding the final outcome
class Leaf:
    def __init__(self, result):
        self.result = result

    def __call__(self, example):
        return self.result

    def op(self):
        return "Final Outcome [" + str(self.result) + "]"

    def __repr__(self):
        return repr(self.result)
