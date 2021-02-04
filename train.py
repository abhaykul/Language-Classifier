"""
Abhay Kulkarni
python v3.9

training file
"""
import math
import pickle
import sys

from dataset import DataSet
from file_parser import parse_this_file
from functions import normalize, zero_update
from leaf import Leaf
from node import Node
from tree_builder import BuildTree


# ####################################################################################
def decision_stump(data, weight):
    """
    Does everything and normalizes the weights
    :param data: data is of Dataset class
    :param weight: weights of corresponding stumps/trees
    :return:
    """
    all_examples = data.examples
    all_attributes = data.inputs
    col_num, weights = choose_best_attribute(all_examples, all_attributes, weight)
    hypothesis = Node(col_num, data.attribute_name[col_num])

    if weights[0] > weights[1]:
        hypothesis.add("True", Leaf("True"))
    else:
        hypothesis.add("True", Leaf("False"))

    if weights[2] > weights[3]:
        hypothesis.add("False", Leaf("True"))
    else:
        hypothesis.add("False", Leaf("False"))

    correct, wrong = [], []
    total_error = 0
    for example_id in range(len(all_examples)):
        this_row = all_examples[example_id]
        if this_row[col_num] != this_row[-1]:
            total_error += weight[example_id]
            wrong.append(example_id)
        else:
            correct.append(example_id)

    importance = (1 / 2) * (math.log(abs((1 - total_error) / total_error)))

    for c in correct:
        weight[c] *= (math.e ** importance)
    for i_c in wrong:
        weight[i_c] *= (math.e ** (-1 * importance))

    weight = normalize(weight)

    return hypothesis, abs(importance), weight


# ####################################################################################
def choose_best_attribute(examples, attributes, w):
    """
    Chooses best attribute based on weight
    :param examples: All rows
    :param attributes: All columns
    :param w: weight of each stump
    :return: best stump
    """
    highest = -1
    max_gain = -1 * float('inf')
    wt = [0] * 4
    for attribute in attributes:
        TT, TF, FT, FF = 0, 0, 0, 0
        # For every row find weights
        for row_number in range(len(examples)):
            current_row = examples[row_number]
            if current_row[attribute] == "True":
                if current_row[-1] == "True":
                    TT += w[row_number]
                else:
                    TF += w[row_number]
            else:
                if current_row[-1] == "True":
                    FT += w[row_number]
                else:
                    FF += w[row_number]

        remainder = 0

        if (TT + TF) != 0:
            remainder = ((TT + TF) * entropy_weight(TT / (TT + TF)))
        if (FT + FF) != 0:
            remainder += ((FT + FF) * entropy_weight(FT / (FT + FF)))

        gain = entropy_weight((TT + TF)) + remainder
        if gain > max_gain:
            max_gain = gain
            highest = attribute
            wt[0], wt[1], wt[2], wt[3] = TT, TF, FT, FF
    return highest, wt


# ####################################################################################
# Return entropy()
def entropy_weight(q):
    first, second = zero_update(q), zero_update(1 - q)
    total = first + second
    return total * -1


# ####################################################################################
# Ada_boost starter function; Main algorithm in L()
def ada_boost(data, K):
    n = len(data.examples)
    w = [1 / n] * n
    hypothesis_array, hypothesis_weight = [], []
    for k in range(K):
        hypothesis, weight, updated_weight = decision_stump(data, w)
        w = updated_weight
        hypothesis_array.append(hypothesis)
        hypothesis_weight.append(weight)
    return hypothesis_array, hypothesis_weight


# ####################################################################################
# Build the data class; name -> file_name
def my_data(name):
    return DataSet(file_name=name, attribute_name='THE HET/DE AND IK EEN EN HE/SHE HIJ/ZE VAN A isENGLISH')


# ####################################################################################
# Training the model using decision trees
def decision_tree_model(training_file, hypothesis_out, validation_file):
    with open(validation_file, encoding="utf8") as f:
        testing = parse_this_file(f.read())
        max_itr, max_ac = 0, 0
        decision_tree_learning = [None] * 10
        for m in range(1, 11):
            current_stump = BuildTree(my_data(training_file), m)
            right, not_right = 0, 0
            for test1 in testing:
                test = test1[:-1]
                if current_stump(test) == test1[-1]:
                    right += 1
                if current_stump(test) != test1[-1]:
                    not_right += 1

            percent_accuracy = (right / (not_right + right))
            if percent_accuracy >= max_ac:
                max_ac = percent_accuracy
                max_itr = m
            decision_tree_learning[m - 1] = current_stump

        print("******** FOR Tree *******")
        print("Ideal Depth:", max_itr, "Best Accuracy:", max_ac * 100)
        pickle_out = open(hypothesis_out, "wb")
        pickle.dump(decision_tree_learning[max_itr - 1], pickle_out)
        pickle_out.close()


# ####################################################################################
# Training the model using Ada-Boost on decision stumps
def ada_boosted_trees(training_file, hypothesis_out, validation_file):
    best = None
    with open(validation_file, encoding="utf8") as f:
        t1 = parse_this_file(f.read())
        max_K, max_accuracy = 0, 0
        for current_depth in range(1, 11):
            H, Z = ada_boost(my_data(training_file), current_depth)
            correct, wrong = 0, 0
            for test1 in t1:
                test = test1[:-1]
                isEnglish = 0
                for h in range(len(H)):
                    r = H[h](test)
                    if r == "True":
                        isEnglish += Z[h]
                    else:
                        isEnglish -= Z[h]
                if isEnglish >= 0:
                    ans = "True"
                else:
                    ans = "False"

                if ans == test1[-1]:
                    correct += 1
                if ans != test1[-1]:
                    wrong += 1
            accuracy = (correct * 100) / (correct + wrong)
            if accuracy >= max_accuracy:
                max_accuracy = accuracy
                max_K = current_depth
                best = (H, Z)

        print("******** FOR ADA *******")
        print("Ideal K:", max_K, "Best Accuracy:", max_accuracy)
        pickle_out = open(hypothesis_out, "wb")
        pickle.dump(best, pickle_out)
        pickle_out.close()


# ####################################################################################
def main():
    training_file = sys.argv[1]
    hypothesis_out = sys.argv[2]
    l_type = sys.argv[3]
    validation_file = sys.argv[4]

    if l_type == "dt":
        decision_tree_model(training_file, hypothesis_out, validation_file)
    elif l_type == "ada":
        ada_boosted_trees(training_file, hypothesis_out, validation_file)
    else:
        print("Learning type must be either (dt) OR (ada)")
        sys.exit(1)


# ####################################################################################
if __name__ == '__main__':
    main()
