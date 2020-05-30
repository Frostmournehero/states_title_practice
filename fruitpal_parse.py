""" 
This module houses the code for parsing the JSON data and
the class object used to store to the JSON data. A list of
these objects is then sent to the fruitpal cli.

Classes:
    Fruit

Functions:
    parse_json()

"""
import json
import os
import sys
import time
import re

class Fruit():
    """
    Class to represent a single data entry from the the parsed
    JSON data in ./Data/fruit_data.txt

    Attributes:
        commodity: The type of fruit
        country: The country where the fruit is from
        fixed_overhead: The ectra cost per transaction regardless of 
            trade volume
        variable_overhead: The extra cost per fruit. Depends on the
            trade volume.

    Methods:
        None
    """
    def __init__(self, commodity: str, country: str, fixed_overhead: float, 
                 variable_overhead: float) -> None:
        """
        Initializes the fruit class object

         Args:
            commodity: The type of fruit
            country: The country where the fruit is from
            fixed_overhead: The ectra cost per transaction regardless of 
                trade volume
            variable_overhead: The extra cost per fruit. Depends on the
                trade volume.
            
        Returns:
            None

        Raises:
            None
        """
        self.commodity = commodity
        self.country = country
        self.fixed_overhead = fixed_overhead
        self.variable_overhead = variable_overhead

    def __repr__(self):
        out_string = (
            f"Fruit: [commodity: {self.commodity}, "
            f"country: {self.country}, "
            f"fixed_overhead: {self.fixed_overhead}, "
            f"variable_overhead: {self.variable_overhead}]"
        )
        return out_string


def parse_json(file_path: str = None) -> list:
    """
    Parses the JSON in ./Data/fruit_data.txt.

    Args:
        file_path: Usually defaults to ./Data/fruit_data.txt.

    Returns:
        List: List of Fruit objects

    Raises
        JSONDecodeError: If there is an issue decoding the JSON
        FileNotFoundError: If the file path cannot be found
        KeyError: If Json object is missing data for a required fruit 
            object attribute
    """
    object_list = []

    if file_path is None:
        cwd = os.getcwd()
        file_path = f"{cwd}/Data/fruit_data.txt"
        
    try:
        with open(file_path) as fruit_data:
            data = json.load(fruit_data)
            # For each entry create a new Fruit object and store the
            # JSON data in its attributes.
            for entry in data:
                country = entry["COUNTRY"]
                commodity = entry["COMMODITY"]
                fixed_overhead = entry["FIXED_OVERHEAD"]
                variable_overhead = entry["VARIABLE_OVERHEAD"]
                fruit = Fruit(commodity, country, float(fixed_overhead),
                              float(variable_overhead))
                object_list.append(fruit)
    # Catch exception if JSON file fails to load.
    except json.JSONDecodeError as error:
        error_string= (
            f"Error: Failed to parse the JSON file {error.doc}."
            f"{error.msg} on line {error.lineno}"
        )
        print(error_string)
        sys.exit(1)
    except FileNotFoundError as error:
        print(f"Error: Cannot find file name {error.filename}")
        sys.exit(1)
    # Catch exception if JSON file is missing a field but formatted 
    # correctly.
    except KeyError as error:
        error_string= (
            f"Error: Failed to parse the file. "
            f"JSON file is missing expected field {error}"
        )
        print(error_string)
        sys.exit(1)
    return object_list

def parse_flat_file(file_path: str = None) -> list:
    """
    Parses the data in ./Data/flat_file.txt.

    Args:
        file_path: Usually defaults to ./Data/flat_file.txt.

    Returns:
        List: List of Fruit objects

    Raises
        FileNotFoundError: If the file path cannot be found
    """
    object_list = []

    if file_path is None:
        cwd = os.getcwd()
        file_path = f"{cwd}/Data/flat_file.txt"

    try:
        with open(file_path) as fruit_data:
            # Parse each line into an entry using regex
            # Create a fruit object for each entry
            # MANGO MX 31 1.24
            # MANGO BR 20 1.42
            regex_pattern = r"""
                ^               # match beginning of the string
                    ([A-Za-z]+) # MANGO ManGO or mango
                    \s+         # allow for arbitrary space
                    ([A-Za-z]{2}) # Two chars only MX Mx or mx
                    \s+         
                    (\d*\.\d+|\d+) # 31 or 31.0
                    \s+
                    (\d*\.\d+|\d+) # 1 or 1.24
                $               # match end of the string
            """                 
            pattern = re.compile(regex_pattern, re.VERBOSE)
            for line in fruit_data:
                entry = pattern.match(line)
                if entry is None:
                    raise "Error"
                (commodity, country, fixed_overhead, 
                 variable_overhead) = entry.groups()
                
                fruit = Fruit(commodity, country, float(fixed_overhead),
                              float(variable_overhead))
                object_list.append(fruit)
    except FileNotFoundError as error:
        print(f"Error: Cannot find file name {error.filename}")
        sys.exit(1)
    # Catch exception if JSON file is missing a field but formatted 
    # correctly.
    except KeyError as error:
        error_string= (
            f"Error: Failed to parse the file. "
            f"JSON file is missing expected field {error}"
        )
        print(error_string)
        sys.exit(1)
    return object_list
