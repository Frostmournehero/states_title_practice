""" 
This module houses the code for testing the fruitpal cli and JSON
parsing. This code is run separately from the cli.

Classes:
    TestFruitpal

"""
import sys
import os
import unittest
from click.testing import CliRunner

from fruitpal_cli import fruit_pal
from fruitpal_parse import parse_json, Fruit


class TestFruitpal(unittest.TestCase):
    """
    Custom test class that takes from the unittest.TestCase.
    The methods below are each separate tests that are run by unittest
    when this file is run.

    Attributes:
        None

    Methods:
        test_cli_cost_negative_input
        test_cli_cost_missing_fruit
        test_parse_bad_entry
        test_parse_missing_field
        test_parse_good_entry
        test_given_example
        test_extended_example
        test_cli_show_commodity
        test_cli_show_country
        test_cli_show_bad_key

    """

    # Bad CLI Input
    def test_cli_cost_negative_input(self) -> None:
        """
        Test negative price_per_ton and trade volume values in 
        fruitpal cli.
        """
        # Run the cli script in isolation and capture the output
        # Test negative price_per_ton
        runner = CliRunner()
        command = "cost"
        # Special char is needed for negative input. It indicates
        # everything after it is a command rather than option
        special_char = "--"
        commodity = "mango"
        price_per_ton = "-5.0"
        trade_volume = "50.0"
        result = runner.invoke(fruit_pal, 
                               [command, special_char, commodity, 
                                price_per_ton, trade_volume])
        error_string = (
            "Error: trade_volume and price_per_ton arguments must be "
            "greater than or equal to zero."
        )
        self.assertIn(error_string,result.output)
        self.assertEqual(result.exit_code,1)

        # Test the negative trade_volume
        price_per_ton = "5.0"
        trade_volume = "-50.0"
        result = runner.invoke(fruit_pal, 
                               [command, special_char, commodity, 
                                price_per_ton, trade_volume])

        self.assertIn(error_string,result.output)
        self.assertEqual(result.exit_code,1)

    def test_cli_cost_missing_fruit(self) -> None:
        """
        Test the cli when the chosen fruit is not in the JSON file.
        """
        # Run the cli script in isolation and capture the output
        runner = CliRunner()
        command = "cost"
        commodity = "apple"
        price_per_ton = "5.0"
        trade_volume = "50.0"
        result = runner.invoke(fruit_pal, 
                               [command, commodity, 
                                price_per_ton, trade_volume])

        error_string = (
            f"Commodity apple was not found. "
            "Please run fruitpal_cli.py list commodity for valid values"
        )
        self.assertIn(error_string,result.output)
        self.assertEqual(result.exit_code,1)

    # Bad JSON
    def test_parse_bad_entry(self) -> None:
        """Test a bad JSON file"""
        cwd = os.getcwd()
        path = f"{cwd}/Data/test_bad_format.txt"
        with self.assertRaises(SystemExit) as catch:
            parse_json(path)
        self.assertEqual(catch.exception.code, 1)

    def test_parse_missing_field(self) -> None:
        """Test JSON file with missing field"""
        cwd = os.getcwd()
        path = f"{cwd}/Data/test_missing_field.txt"
        with self.assertRaises(SystemExit) as catch:
            parse_json(path)
        self.assertEqual(catch.exception.code, 1)

    # Test good JSON
    def test_parse_good_entry(self) -> None:
        """Test a good single entry JSON file"""
        commodity = "mango"
        country_code = "MX"
        fixed_overhead = 32
        variable_overhead = 1.24
        test_fruit = (
            commodity, country_code, fixed_overhead, variable_overhead
        )
        cwd = os.getcwd()
        path = f"{cwd}/Data/test_single_entry.txt"
        parsed_fruit = parse_json(path)[0]
        self.assertEqual(parsed_fruit.commodity, test_fruit[0])
        self.assertEqual(parsed_fruit.country, test_fruit[1])
        self.assertEqual(parsed_fruit.fixed_overhead, test_fruit[2])
        self.assertEqual(parsed_fruit.variable_overhead, test_fruit[3])
    
    # Test good JSON file and CLI
    def test_given_example(self) -> None:
        """
        Test the given example for Fruitpal (mango, 53, 405)
        """
        # Run the cli script in isolation and capture the output
        runner = CliRunner()
        command = "cost"
        commodity = "mango"
        price_per_ton = "53"
        trade_volume = "405"
        result = runner.invoke(fruit_pal, 
                               [command, commodity, 
                                price_per_ton, trade_volume])
        out_string = (
            "BR   22060.10 | ((53.00 +  1.42) * 405.00) + 20.00\n"
            "MX   21999.20 | ((53.00 +  1.24) * 405.00) + 32.00\n"
        )
        self.assertIn(out_string,result.output)
        self.assertEqual(result.exit_code,0)


    def test_extended_example(self) -> None:
        """
        Test extended example for Fruitpal (mango, 53, 405)
        """
        # Run the cli script in isolation and capture the output
        cwd = os.getcwd()
        runner = CliRunner()
        file_path = f"--file_path={cwd}/Data/test_extended.txt"
        command = "cost"
        commodity = "mango"
        price_per_ton = "53"
        trade_volume = "405"
        result = runner.invoke(fruit_pal, 
                               [command, file_path, commodity, 
                                price_per_ton, trade_volume])

        out_string = (
            "FR   22382.20 | ((53.00 +  2.24) * 405.00) + 10.00\n"
            "US   22223.75 | ((53.00 +  1.75) * 405.00) + 50.00\n"
            "BR   22060.10 | ((53.00 +  1.42) * 405.00) + 20.00\n"
            "MX   21999.20 | ((53.00 +  1.24) * 405.00) + 32.00\n"
            "MY   21879.05 | ((53.00 +  1.01) * 405.00) +  5.00\n"
            "PH   21853.75 | ((53.00 +  0.95) * 405.00) +  4.00\n"
        )
        self.assertIn(out_string,result.output)
        self.assertEqual(result.exit_code,0)

    # Test the show command
    def test_cli_show_commodity(self) -> None:
        """
        Test the cli show command with commodity argument
        """
        # Run the cli script in isolation and capture the output
        runner = CliRunner()
        cwd = os.getcwd()
        file_path = f"--file_path={cwd}/Data/test_extended.txt"
        command = "show"
        key = "commodity"
        result = runner.invoke(fruit_pal, 
                               [command, key, file_path])
                               
        error_string = (
            "COMMODITY:\n"
            "apple\n"
            "banana\n"
            "mango\n"
            "orange\n"
            "pineapple\n"
        )
        self.assertIn(error_string,result.output)
        self.assertEqual(result.exit_code,0)
    
    def test_cli_show_country(self) -> None:
        """
        Test the cli show command with country argument
        """
        # Run the cli script in isolation and capture the output
        runner = CliRunner()
        cwd = os.getcwd()
        file_path = f"--file_path={cwd}/Data/test_extended.txt"
        command = "show"
        key = "country"
        result = runner.invoke(fruit_pal, 
                               [command, key, file_path])
                               
        error_string = (
            "COUNTRY:\n"
            "BR\n"      
            "FR\n"
            "MX\n"
            "MY\n"
            "PH\n"
            "US\n"
        )
        self.assertIn(error_string,result.output)
        self.assertEqual(result.exit_code,0)
    
    def test_cli_show_bad_key(self) -> None:
        """
        Test the cli show command with bad argument
        """
        # Run the cli script in isolation and capture the output
        runner = CliRunner()
        cwd = os.getcwd()
        file_path = f"--file_path={cwd}/Data/test_extended.txt"
        command = "show"
        key = "commodty"
        result = runner.invoke(fruit_pal, 
                               [command, key, file_path])
                               
        error_string = (
            "Error: List of the value commodty is not available.\n"
            "Please choose from these options:\n"
            "commodity\n"
            "country\n"
        )
        self.assertIn(error_string,result.output)
        self.assertEqual(result.exit_code,1)

def run_test() -> None:
    # Make sure that you are running the test file from its 
    # working directory
    cwd = os.getcwd()
    if not os.path.isdir(f"{cwd}/Data"):
        error_string = (
            "Current working directory is invalid for testing. "
            "Please set cwd to project root directory."
        )
        print(error_string)
        sys.exit(1)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestFruitpal)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()