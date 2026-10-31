###############################################################################
# MIS 58600
# Group 29 - Ryan Brock and Thomas Adams
# Lab 1 - Unit tests for group29BrockAdamsAssignment1.py
#
# How to run (from this folder):
#     python3 test_calculator.py
#
# How it works:
#   The calculator functions ask for input() and print() their results, so
#   each test feeds in a list of "typed" answers and checks the printed text.
#   Tests check for the numeric answer (e.g. "12.57") rather than the full
#   sentence, so rewording a message will not break them.
#
# Reading the results:
#   ok                   -> working
#   FAIL / ERROR         -> something that used to work is now broken
#   expected failure     -> a known bug that has not been fixed yet
#   unexpected success   -> a known bug is now FIXED; delete the
#                           @unittest.expectedFailure line above that test
###############################################################################

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import group29BrockAdamsAssignment1 as calc


class OutOfInputs(Exception):
    """Raised when the program asks for more input than the test provided."""


##############################################################################
# Desc: Runs a calculator function with pretend keyboard input
# Parameters: func: the function to run
#             inputs: list of strings, one per input() prompt
# Returns: everything the function printed, as one string
##############################################################################
def run_function(func, inputs, *args):
    answers = iter(inputs)

    def fake_input(prompt=""):
        print(prompt, end="")
        try:
            return next(answers)
        except StopIteration:
            raise OutOfInputs("Program asked for more input than the test gave")

    output = io.StringIO()
    with patch("builtins.input", fake_input), redirect_stdout(output):
        func(*args)
    return output.getvalue()


##############################################################################
# Desc: Like run_function, but stops quietly if the program re-prompts
#       (used by tests that only care that the program did not crash)
# Returns: everything the function printed, as one string
##############################################################################
def run_until_out_of_inputs(func, inputs, *args):
    answers = iter(inputs)

    def fake_input(prompt=""):
        print(prompt, end="")
        try:
            return next(answers)
        except StopIteration:
            raise OutOfInputs()

    output = io.StringIO()
    with patch("builtins.input", fake_input), redirect_stdout(output):
        try:
            func(*args)
        except OutOfInputs:
            pass
    return output.getvalue()


###############################################################################
# Basic Calculator Operations
###############################################################################
class TestBasicCalculator(unittest.TestCase):

    def test_addition(self):
        output = run_function(calc.basic_calculator_operations, ["+", "7", "3"])
        self.assertIn("= 10", output)

    def test_subtraction_order(self):
        # left side minus right side: 10 - 3, not 3 - 10
        output = run_function(calc.basic_calculator_operations, ["-", "10", "3"])
        self.assertIn("= 7", output)

    def test_multiplication(self):
        output = run_function(calc.basic_calculator_operations, ["*", "6", "7"])
        self.assertIn("= 42", output)

    def test_division(self):
        output = run_function(calc.basic_calculator_operations, ["/", "7", "2"])
        self.assertIn("= 3.5", output)

    def test_modulus(self):
        output = run_function(calc.basic_calculator_operations, ["mod", "7", "3"])
        self.assertIn("= 1", output)

    def test_exponent(self):
        output = run_function(calc.basic_calculator_operations, ["^", "2", "3"])
        self.assertIn("= 8", output)

    def test_letters_instead_of_number_reprompts(self):
        # "abc" is rejected, then the user re-enters both numbers
        output = run_function(calc.basic_calculator_operations,
                              ["+", "abc", "1", "2"])
        self.assertIn("error", output.lower())
        self.assertIn("= 3", output)

    def test_invalid_operation_reports_error(self):
        with self.assertRaises(ValueError):
            run_function(calc.basic_calculator_operations, ["foo", "1", "2"])

    def test_divide_by_zero_does_not_crash(self):
        try:
            output = run_until_out_of_inputs(calc.basic_calculator_operations,
                                             ["/", "5", "0"])
        except ZeroDivisionError:
            self.fail("Dividing by zero crashed the program")
        self.assertIn("error", output.lower())

    def test_mod_by_zero_does_not_crash(self):
        try:
            output = run_until_out_of_inputs(calc.basic_calculator_operations,
                                             ["mod", "5", "0"])
        except ZeroDivisionError:
            self.fail("mod by zero crashed the program")
        self.assertIn("error", output.lower())

    def test_zero_to_negative_power_does_not_crash(self):
        # 0 ^ -1 means 1 / 0, which is also a divide by zero
        try:
            output = run_until_out_of_inputs(calc.basic_calculator_operations,
                                             ["^", "0", "-1"])
        except ZeroDivisionError:
            self.fail("0 ^ -1 crashed the program")
        self.assertIn("error", output.lower())

    # ---- Known bugs (remove the decorator once fixed) ----

    @unittest.expectedFailure
    def test_decimal_input_accepted(self):
        output = run_until_out_of_inputs(calc.basic_calculator_operations,
                                         ["+", "2.5", "1"])
        self.assertIn("= 3.5", output)


###############################################################################
# Engineering Calculations - Area
###############################################################################
class TestArea(unittest.TestCase):

    def test_triangle_area(self):
        output = run_function(calc.triangle_area, ["4", "5"])
        self.assertIn("= 10.0", output)

    def test_rectangle_area(self):
        output = run_function(calc.rectangle_area, ["3", "4"])
        self.assertIn("= 12.0", output)

    def test_circle_area(self):
        output = run_function(calc.circle_area, ["2"])
        self.assertIn("= 12.57", output)

    def test_bad_input_reprompts(self):
        output = run_function(calc.circle_area, ["two", "2"])
        self.assertIn("error", output.lower())
        self.assertIn("= 12.57", output)

    # ---- Known bugs (remove the decorator once fixed) ----

    @unittest.expectedFailure
    def test_negative_radius_rejected(self):
        output = run_until_out_of_inputs(calc.circle_area, ["-2"])
        self.assertNotIn("12.57", output)


###############################################################################
# Engineering Calculations - Volume
###############################################################################
class TestVolume(unittest.TestCase):

    def test_cube_volume(self):
        output = run_function(calc.cube_volume, ["3"])
        self.assertIn("= 27.0", output)

    def test_cylinder_volume(self):
        output = run_function(calc.cylinder_volume, ["2", "3"])
        self.assertIn("= 37.7", output)

    def test_cone_volume(self):
        output = run_function(calc.cone_volume, ["2", "3"])
        self.assertIn("= 12.57", output)


###############################################################################
# Engineering Calculations - Unit Conversions
###############################################################################
class TestUnitConversions(unittest.TestCase):

    def test_meters_to_feet(self):
        output = run_function(calc.meters_to_feet, ["10"])
        self.assertIn("32.81", output)

    def test_kilograms_to_pounds(self):
        output = run_function(calc.kilograms_to_pounds, ["10"])
        self.assertIn("22.05", output)

    def test_zero_converts_to_zero(self):
        output = run_function(calc.meters_to_feet, ["0"])
        self.assertIn("0.0 ft", output)


###############################################################################
# Business Calculations
###############################################################################
class TestBusiness(unittest.TestCase):

    def test_compound_interest(self):
        # 1000 * (1.05)^2 - 1000 = 102.50 interest, 1102.50 balance
        output = run_function(calc.compound_interest, ["1000", "5", "2"])
        self.assertIn("$102.5", output)
        self.assertIn("$1102.5", output)

    def test_compound_interest_bad_input_reprompts(self):
        output = run_function(calc.compound_interest, ["lots", "1000", "5", "2"])
        self.assertIn("error", output.lower())
        self.assertIn("$102.5", output)

    def test_break_even_point(self):
        # 1000 / (10 - 5) = 200 units
        output = run_function(calc.break_even_point, ["1000", "10", "5"])
        self.assertIn("= 200.0 units", output)

    def test_break_even_zero_variable_costs(self):
        # 1000 / (10 - 0) = 100 units
        output = run_function(calc.break_even_point, ["1000", "10", "0"])
        self.assertIn("= 100.0 units", output)

    def test_compound_interest_accepts_rate_under_one_percent(self):
        # 1000 * 1.005 - 1000 = 5.00 interest
        output = run_until_out_of_inputs(calc.compound_interest,
                                         ["1000", "0.5", "1"])
        self.assertIn("$5.0", output)

    def test_break_even_price_equals_cost_does_not_crash(self):
        try:
            output = run_until_out_of_inputs(calc.break_even_point,
                                             ["1000", "10", "10"])
        except ZeroDivisionError:
            self.fail("Sales price equal to variable cost crashed the program")
        self.assertIn("error", output.lower())
        self.assertNotIn("units.", output)

    # ---- Known bugs (remove the decorator once fixed) ----

    @unittest.expectedFailure
    def test_break_even_no_negative_units(self):
        output = run_until_out_of_inputs(calc.break_even_point, ["1000", "5", "10"])
        self.assertNotIn("= -", output)


###############################################################################
# Menus and Program Flow
###############################################################################
class TestMenus(unittest.TestCase):

    def test_main_menu_returns_valid_choice(self):
        choice = None

        def read_choice():
            nonlocal choice
            choice = calc.read_user_menu_choice()

        run_function(read_choice, ["2"])
        self.assertEqual(choice, 2)

    def test_main_menu_option_4_exits(self):
        with self.assertRaises(SystemExit):
            run_function(calc.read_user_menu_choice, ["4"])

    def test_main_menu_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            run_function(calc.read_user_menu_choice, ["9"])

    def test_main_menu_letters_reprompt(self):
        choice = None

        def read_choice():
            nonlocal choice
            choice = calc.read_user_menu_choice()

        output = run_function(read_choice, ["x", "1"])
        self.assertIn("error", output.lower())
        self.assertEqual(choice, 1)

    def test_basic_path_through_main(self):
        # Menu 1 -> 2 + 3 -> exit
        with self.assertRaises(SystemExit):
            output = io.StringIO()
            with redirect_stdout(output):
                run_function(calc.main, ["1", "+", "2", "3", "4"])

    def test_engineering_area_path(self):
        # Engineering -> Geometry -> Area -> Rectangle 3 x 4
        output = run_function(calc.execute_user_option, ["1", "1", "2", "3", "4"], 2)
        self.assertIn("= 12.0", output)

    def test_engineering_volume_path(self):
        # Engineering -> Geometry -> Volume -> Cube side 3
        output = run_function(calc.execute_user_option, ["1", "2", "1", "3"], 2)
        self.assertIn("= 27.0", output)

    def test_engineering_unit_path(self):
        # Engineering -> Unit Conversions -> kg to lbs, 10 kg
        output = run_function(calc.execute_user_option, ["2", "2", "10"], 2)
        self.assertIn("22.05", output)

    def test_business_break_even_path(self):
        output = run_function(calc.execute_user_option, ["2", "1000", "10", "5"], 3)
        self.assertIn("= 200.0 units", output)

    def test_submenu_invalid_choice_reports_error(self):
        with self.assertRaises(ValueError):
            run_function(calc.business_calculations, ["7"])

    def test_main_recovers_from_bad_choice(self):
        # Bad main-menu choice prints an error, menu shows again, then exit
        output = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(output):
                run_function(calc.main, ["9", "4"])

    # ---- Known bugs (remove the decorator once fixed) ----

    @unittest.expectedFailure
    def test_area_menu_error_mentions_option_3(self):
        with self.assertRaises(ValueError) as error:
            run_function(calc.area_calculator, ["7"])
        self.assertIn("3", str(error.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
