"""
Abhay Kulkarni
python v3.9

prediction file
"""
import os
import pickle
import sys

from file_parser import parse_this_file
from node import Node


def print_answer(pickle_object, result_matrix):
    # If the object is a tuple; it's for ADABOOST (H,Z) form
    if isinstance(pickle_object, tuple):
        hypothesis_vector = pickle_object[0]
        current_hypothesis_weight = pickle_object[1]
        for row in result_matrix:
            test = row[:-1]
            isEnglish = 0
            for h in range(len(hypothesis_vector)):
                indication_flag = hypothesis_vector[h](test)
                if indication_flag == "True":
                    isEnglish += current_hypothesis_weight[h]
                if indication_flag == "False":
                    isEnglish -= current_hypothesis_weight[h]
            if isEnglish >= 0:
                flag = "en"
            else:
                flag = "nl"
            print(flag)

    # If the object is a Node; it's for DecisionTree (Node) form
    elif isinstance(pickle_object, Node):
        for row in result_matrix:
            flag = pickle_object(row)
            if flag == "True":
                print("en")
            if flag == "False":
                print("nl")

    # If somehow a wrong pickle file is given, print error and exit
    elif not (isinstance(pickle_object, Node) or isinstance(pickle_object, tuple)):
        print("Wrong file given!")
        print("tuple: for ADABOOST")
        print("Node: for Decision Tree")
        sys.exit(1)


def main():
    hypothesis = sys.argv[1]
    file_name = sys.argv[2]

    if not os.path.exists(file_name):
        print("INPUT FILE NOT FOUND")
        sys.exit(2)

    with open(file_name, encoding="utf8") as f:
        result_matrix = parse_this_file(f.read())
        pickle_in = open(hypothesis, "rb")
        pickle_object = pickle.load(pickle_in)
        pickle_in.close()
        print_answer(pickle_object, result_matrix)


if __name__ == '__main__':
    main()
