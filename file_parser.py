"""
Abhay Kulkarni
python v3.9

File parser function
"""


# Parses the file with given name to desired format
def parse_this_file(ip, delimiter=' '):
    """

    :param ip: valid data file
    :param delimiter: word splitter
    :return: List of flag arrays
    """
    return_this_matrix = []
    # Split lines if not blank
    lines = [line for line in ip.splitlines() if line.strip()]

    for line in lines:
        flag_array = [""] * 11
        current_line_array = line.strip().split(delimiter)
        result = None
        if current_line_array[0].startswith("nl|"):
            current_line_array[0] = current_line_array[0].replace("nl|", "")
            result = "False"

        if current_line_array[0].startswith("en|"):
            current_line_array[0] = current_line_array[0].replace("en|", "")
            result = "True"

        flag_array[-1] = result

        # Selected words for classification
        string_check = [["the"],
                        ["het", "de"],
                        ["and"],
                        ["ik"],
                        ["een"],
                        ["en"],
                        ["he", "she"],
                        ["hij", "ze", "zij"],
                        ["van"],
                        ["a"]]

        for i in range(10):
            flag_array[i] = "False"
            for word in string_check[i]:
                checker = any(current_string.lower() == word for current_string in current_line_array)
                if checker:
                    flag_array[i] = "True"
                    break

        return_this_matrix.append(flag_array)
    return return_this_matrix
