"""
Abhay Kulkarni
python v3.9

Dataset Class
"""

from functions import distinct_val
from file_parser import parse_this_file

# Data class for initializing the data file into values, attributes, results
class DataSet:

    def __init__(self, file_name, attribute_name):
        """
        All names only for printing; Separates the values from the a blob of data
        to attributes, result, etc.
        :param file_name: Name of the data file
        :param attribute_name: Name of all the attributes
        """
        self.file_name = file_name
        self.examples = parse_this_file(open(file_name, encoding="utf8").read())  # All the rows of the dataSet
        self.attribute_name = attribute_name.split()  # Name of columns of dataSet
        n = len(self.examples[0])  # No. of columns
        self.inputs = list(range(n - 1))  # All input(data) columns
        self.values = list(map(distinct_val, zip(*self.examples)))  # Unique values
