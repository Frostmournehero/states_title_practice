""" 
This module houses the code for fruit pal CLI. It receives the
parsed JSON data from the fruitpal json parser in the form of
an object list. It uses that list to display the total cost
and list the countries and commodities

Functions:
    fruit_pal()
    cost()
    show()
"""

import click
import sys

from fruitpal_parse import parse_json

@click.group(no_args_is_help=True)
def fruit_pal() -> None:
    """
    A CLI tool for determining the price of fruit trades based on the 
    country.
    """
    pass


@fruit_pal.command(no_args_is_help=True)
@click.option("--file_path", type=click.STRING,
              help="Fully qualified path for the JSON data file")
@click.argument("commodity", required=True, type=click.STRING)
@click.argument("price_per_ton", required=True, type=click.FLOAT)
@click.argument("trade_volume", required=True, type=click.FLOAT)
def cost(file_path: str, commodity: str, price_per_ton: float, 
         trade_volume: float) -> None:
    """
    Prints to stdout the total cost for a trade with each country for a 
    specific commodity.

    Prints to standard out the format:

    COUNTRY | (PRICE_PER_TON + VARIABLE_OVERHEAD) 
    * TRADE_VOLUME + FIXED_OVERHEAD

    Args:
    
        commodity <string> : the type of fruit being traded
    
        price_per_ton <float> : the cost per ton of the fruit
    
        trade_volume <float> : the total volume of fruit in tons
    
    Returns:
    
        None
    
    Raises
    
        None
    """

    output = []

    #check to make sure the values of price_per_ton and trade_volume
    # are greater than or equal to 0
    if price_per_ton < 0 or trade_volume < 0:
        error_string = (
            "Error: trade_volume and price_per_ton arguments must "
            "be greater than or equal to zero."
        )
        print(error_string)
        sys.exit(1)

    # Parse the JSON file and get back a list of objects
    commodity = commodity.lower()
    fruit_list = parse_json(file_path)

    # Iterate through the list of objects and create a list of dicts
    # with the object as a key and the total price as the value.
    for fruit in fruit_list:
        if commodity == fruit.commodity:
            cost_dict = {}
            cost_dict["OBJECT"] = fruit
            total_cost = (trade_volume 
                          * (price_per_ton + fruit.variable_overhead)
                          + fruit.fixed_overhead)
            cost_dict["TOTAL_COST"] = total_cost
            output.append(cost_dict)

    # Check if the output list is empty. If so return that the fruit
    # does not exist.
    if not output:
        error_string = (
            f"Commodity {commodity} was not found. "
            "Please run fruitpal_cli.py list commodity for valid values"
        )
        print(error_string)
        sys.exit(1)
    # Sort the list by the cost. Greatest to least.
    output.sort(key = lambda x: x["TOTAL_COST"], reverse=True)
    
    # Iterate through the output list and print the correctly formatted 
    # output
    # COUNTRY | (PRICE_PER_TON + VARIABLE_OVERHEAD) 
    # * TRADE_VOLUME + FIXED_OVERHEAD
    for object_cost_dict in output:
        fruit = object_cost_dict["OBJECT"]
        total_cost = object_cost_dict["TOTAL_COST"]

        out_string = (
            f"{fruit.country:3} {total_cost:9.2f} | "
            f"(({price_per_ton:5.2f} + {fruit.variable_overhead:5.2f})"
            f" * {trade_volume:5.2f}) + {fruit.fixed_overhead:5.2f}"
        )
        print(out_string)       
    return

@fruit_pal.command(no_args_is_help=True)
@click.option("--file_path", type=str,
              help="Fully qualified path for the JSON data file")
@click.argument("key", required=True, type=str)
def show(file_path: str, key: str) -> None:
    """
    Prints to stdout a list of all the commodities or countries in the 
    JSON data.

    Args:

        key <string> : commodity or country

    Returns:
    
        None

    Raises:
    
        None
    """
    # Check to make sure the key is valid
    valid_keys = ["commodity","country"]
    key = key.lower()
    if key not in valid_keys:
        error_string = (
            f"Error: List of the value {key} is not available.\n"
            "Please choose from these options:"
        )
        print(error_string)
        print(*valid_keys, sep="\n")
        sys.exit(1)
    
    # Parse the JSON file and get back a list of objects.
    output = set()
    fruit_list = parse_json(file_path)

    # Iterate through the list of objects and create a list of
    # commodities or countries.
    for fruit in fruit_list:
        output.add(getattr(fruit,key))

    # Print the possible key values in alphabetical order
    print(key.upper() + ":")
    print(*sorted(output), sep="\n")
    return

if __name__ == '__main__':
    fruit_pal()

