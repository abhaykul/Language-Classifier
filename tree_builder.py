from node import Node
from leaf import Leaf
from functions import remove_all, argmax, normalize
import numpy as np


# Decision tree algorithm with all the necessary functions
def BuildTree(data, MAX_DEPTH):
    def decision_tree(examples, attributes, parent_examples=(), depth=0):
        """
        Same algorithm as AI:AMA Text-book
        :param depth:
        :param examples: Data - rows
        :param attributes: Attributes
        :param parent_examples: Root node examples
        :return: tree
        """
        # Depth check
        if depth == MAX_DEPTH:
            return plurality_value(examples)

        # If examples empty
        if len(examples) == 0:
            return plurality_value(parent_examples)

        # If all have same class
        if is_same_classification(examples):
            return Leaf(examples[0][-1])

        # If attributes are empty
        if len(attributes) == 0:
            return plurality_value(examples)

        # "A" <- argmax_ Importance(a, examples)
        A = best_attribute(attributes, examples)
        depth += 1
        # tree <- tree with root "a"
        tree = Node(A, data.attribute_name[A], plurality_value(examples))
        for (vk, vk_values) in split(A, examples):
            subtree = decision_tree(vk_values, remove_all(A, attributes), examples, depth)
            tree.add(vk, subtree)
        return tree

    # Most common value from examples > with tie break
    def plurality_value(examples):
        summation = lambda v: sum(e[-1] == v for e in examples)
        popular = argmax(data.values[-1], key=summation)
        return Leaf(popular)

    # Checks if all examples have the same result
    def is_same_classification(examples):
        classifier = examples[0][-1]
        return all(e[-1] == classifier for e in examples)

    # Highest information gain; if tie > break randomly
    def best_attribute(attribute, examples):
        counter = lambda a: information_gain(a, examples)
        return argmax(attribute, key=counter)

    # Information Gain
    def information_gain(attribute, examples):
        n = len(examples)
        remainder = 0
        # Summation part
        for (v, v_example) in split(attribute, examples):
            remainder += ((len(v_example) / n) * entropy(v_example))
        gain = entropy(examples) - remainder
        return gain

    # Calculates the B() value
    def entropy(input_examples):
        value_list = []
        for value in data.values[-1]:
            count = 0
            for e in input_examples:
                if e[-1] == value:
                    count += 1
            value_list.append(count)

        probabilities = normalize(remove_all(0, value_list))
        summation = 0
        for probability in probabilities:
            summation += (-probability * np.log2(probability))
        return summation

    # List of pairs which split the examples by attributes
    # return Format: [("True",[..examples..]),("False",[..examples..])]
    def split(attribute, examples):
        final_list = []
        for val in data.values[attribute]:
            value_list = []
            for example in examples:
                if example[attribute] == val:
                    value_list.append(example)
            final_list.append((val, value_list))

        return final_list

    return decision_tree(data.examples, data.inputs)
