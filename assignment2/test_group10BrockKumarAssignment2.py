# -*- coding: utf-8 -*-
###############################################################################
# MIS 58600 - Group 10 - Assignment 2 unit tests
#
# Run from this folder (standard library only, no pip install needed):
#
#   python3 test_group10BrockKumarAssignment2.py -k Regression    # refactor net
#   python3 test_group10BrockKumarAssignment2.py -k Todo          # work remaining
#   python3 test_group10BrockKumarAssignment2.py                  # everything
#   python3 test_group10BrockKumarAssignment2.py -v -k TodoKpis   # one group
#
# How the tests are organized:
#
#   Regression*  Behavior that works today. These must stay green. Run them
#                after every refactor.
#   Todo*        Lab 2 requirements not built yet, and known bugs. These start
#                red and are the to-do list. Once they pass, run the whole file
#                after each refactor.
#
# How the tests work:
#
#   The program has a main loop at the top level, so a plain import would sit
#   waiting for input. The harness feeds in scripted answers and captures what
#   gets printed, so nothing in the program file has to change. It keeps working
#   if the main loop is later moved under `if __name__ == "__main__":`.
#
#   Each test loads a fresh copy of the program, so stock and sales from one
#   test never leak into another.
#
#   If the program asks for more input than a test scripted, the test fails with
#   a transcript. That is how endless re-prompt loops are reported.
#
# What refactoring can and cannot touch:
#
#   Most internals can change freely. The tests do rely on these names:
#     - product_catalog and sales_history, as module-level variables
#     - the 'Name', 'Price', 'Stock' product keys
#     - view_catalog(), make_sale(), view_sales_history(), display_kpis(),
#       update_product_details(), called with no arguments
#     - update_product_attribute(product_id, key)
#   Renaming one of these needs a matching change here. Sale dictionary keys are
#   flexible: see SALE_FIELD_NAMES below.
###############################################################################

import contextlib
import importlib.util
import io
import math
import re
import runpy
import signal
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True

PROGRAM_PATH = Path(__file__).resolve().parent / "group10BrockKumarAssignment2.py"

# A test is stopped if it runs this long, in case of a loop that never asks for
# input. Only enforced where the OS supports it (macOS and Linux, not Windows).
TEST_TIMEOUT_SECONDS = 5

# Safety limit for tests that answer prompts with a function, not a fixed list.
MAX_PROMPTS = 25

# Accepted spellings for each sale field, compared in lowercase letters only, so
# 'Sale ID', 'sale_id' and 'SaleID' are all the same. Add yours if it is missing.
SALE_FIELD_NAMES = {
    "sale_id": {"saleid", "id"},
    "datetime": {"datetime", "dateandtime", "date", "timestamp", "saledate"},
    "product_id": {"productid"},
    "quantity": {"quantity", "quantitysold", "qty"},
    "total": {"totalsaleamount", "totalamount", "total", "saletotal", "amount"},
}


###############################################################################
# Test harness
###############################################################################
class _ProgramStillWaiting(BaseException):
    """Raised when the scripted answers run out.

    Derives from BaseException so an `except Exception` in the program cannot
    swallow it and keep looping.
    """


class Session:
    """The result of one scripted run: what was printed and what was asked."""

    def __init__(self, answers):
        self._answers = answers if callable(answers) else list(answers)
        self.prompts = []
        self.buffer = io.StringIO()
        self.value = None

    @property
    def output(self):
        return self.buffer.getvalue()

    @property
    def unused_answers(self):
        return [] if callable(self._answers) else self._answers

    def fake_input(self, prompt=""):
        print(prompt, file=self.buffer)
        self.prompts.append(prompt)
        if callable(self._answers):
            if len(self.prompts) > MAX_PROMPTS:
                raise _ProgramStillWaiting()
            return self._answers(prompt, len(self.prompts))
        if not self._answers:
            raise _ProgramStillWaiting()
        return self._answers.pop(0)


def drive(action, answers, allow_unused=False):
    """Run action() with scripted input and captured output."""
    session = Session(answers)
    with mock.patch("builtins.input", session.fake_input):
        with contextlib.redirect_stdout(session.buffer):
            try:
                session.value = action()
            except _ProgramStillWaiting:
                raise AssertionError(
                    "The program was still asking for input after the script "
                    "ran out, so it may be stuck in a loop.\n"
                    f"Last prompt: {session.prompts[-1]!r}\n"
                    f"--- transcript (last 600 chars) ---\n{session.output[-600:]}"
                ) from None
    if session.unused_answers and not allow_unused:
        raise AssertionError(
            f"The program finished without using these answers: "
            f"{session.unused_answers}\n"
            f"--- transcript (last 600 chars) ---\n{session.output[-600:]}"
        )
    return session


def load_program():
    """Load a fresh copy of the program as a module, exiting its menu at once."""
    spec = importlib.util.spec_from_file_location(
        "assignment2_under_test", PROGRAM_PATH
    )
    module = importlib.util.module_from_spec(spec)
    silent_exit = mock.patch("builtins.input", return_value="6")
    with silent_exit, contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def sale_field(sale, field):
    """Read a sale field whatever the exact key spelling is."""
    wanted = SALE_FIELD_NAMES[field]
    for key, value in sale.items():
        if re.sub(r"[^a-z]", "", str(key).lower()) in wanted:
            return value
    raise AssertionError(
        f"Sale has no {field!r} field. Keys found: {list(sale)}. "
        f"Add yours to SALE_FIELD_NAMES if it is just spelled differently."
    )


class ProgramTestCase(unittest.TestCase):
    def setUp(self):
        self._start_timeout()
        self.program = load_program()

    def _start_timeout(self):
        if not hasattr(signal, "SIGALRM"):
            return

        def on_timeout(signum, frame):
            raise TimeoutError(
                f"Test ran longer than {TEST_TIMEOUT_SECONDS}s, likely a loop "
                f"that never exits."
            )

        previous = signal.signal(signal.SIGALRM, on_timeout)
        signal.alarm(TEST_TIMEOUT_SECONDS)
        self.addCleanup(signal.signal, signal.SIGALRM, previous)
        self.addCleanup(signal.alarm, 0)

    @property
    def catalog(self):
        return self.program.product_catalog

    @property
    def history(self):
        return self.program.sales_history

    def sell(self, product_id, quantity):
        return drive(self.program.make_sale, [product_id, str(quantity)])

    def update(self, product_id, key, *answers, **options):
        return drive(
            lambda: self.program.update_product_attribute(product_id, key),
            answers,
            **options,
        )

    def run_menu(self, *answers):
        """Run the whole program as a script. Returns (session, final_globals)."""
        final = {}

        def run():
            final.update(runpy.run_path(str(PROGRAM_PATH), run_name="__main__"))

        return drive(run, answers), final


###############################################################################
# Regression tests: all pass today and must stay green through refactors
###############################################################################
class RegressionCatalogData(ProgramTestCase):
    """Lab: Product Catalog requirement."""

    def test_catalog_is_a_dictionary_with_at_least_five_products(self):
        self.assertIsInstance(self.catalog, dict)
        self.assertGreaterEqual(len(self.catalog), 5)

    def test_every_product_has_valid_name_price_and_stock(self):
        for product_id, product in self.catalog.items():
            with self.subTest(product_id=product_id):
                self.assertIsInstance(product, dict)
                self.assertIsInstance(product["Name"], str)
                self.assertTrue(product["Name"].strip())
                self.assertIsInstance(product["Price"], float)
                self.assertGreater(product["Price"], 0)
                self.assertIsInstance(product["Stock"], int)
                self.assertGreaterEqual(product["Stock"], 0)

    def test_product_names_are_unique(self):
        names = [product["Name"] for product in self.catalog.values()]
        self.assertEqual(len(names), len(set(names)))

    def test_sales_history_starts_as_an_empty_list(self):
        self.assertEqual(self.history, [])


class RegressionViewCatalog(ProgramTestCase):
    """Lab: View Catalog requirement."""

    def test_shows_every_product_with_all_details(self):
        output = drive(self.program.view_catalog, []).output
        for product_id, product in self.catalog.items():
            with self.subTest(product_id=product_id):
                self.assertRegex(output, rf"\b{product_id}\b")
                self.assertIn(product["Name"], output)
                self.assertIn(f"${product['Price']}", output)
                self.assertRegex(output, rf"\b{product['Stock']}\b")

    def test_viewing_does_not_change_the_catalog(self):
        before = {key: dict(value) for key, value in self.catalog.items()}
        drive(self.program.view_catalog, [])
        self.assertEqual(self.catalog, before)


class RegressionMainMenu(ProgramTestCase):
    """Lab: Main Menu requirement. Runs the whole file as a script."""

    def test_exit_ends_the_program(self):
        session, _ = self.run_menu("6")
        self.assertIn("Goodbye", session.output)

    def test_menu_lists_every_option(self):
        output = self.run_menu("6")[0].output
        for label in ("View Catalog", "Make a Sale", "View Sales History",
                      "KPIs", "Update Product Details", "Exit"):
            with self.subTest(label=label):
                self.assertIn(label, output)

    def test_invalid_choices_show_the_menu_again(self):
        for choice in ("0", "7", "abc", "", "1.0"):
            with self.subTest(choice=choice):
                session, _ = self.run_menu(choice, "6")
                self.assertIn("Invalid choice", session.output)
                self.assertEqual(session.output.count("Main Menu"), 2)

    def test_option_1_views_the_catalog(self):
        self.assertIn("Product Catalog", self.run_menu("1", "6")[0].output)

    def test_option_2_starts_a_sale(self):
        self.assertRegex(self.run_menu("2", "P1", "2", "6")[0].output,
                         r"sold 2 of P1")

    def test_option_3_shows_sales_history(self):
        self.assertIn("Sales History", self.run_menu("3", "6")[0].output)

    def test_option_4_runs_with_no_sales(self):
        self.run_menu("4", "6")

    def test_option_5_updates_a_product(self):
        _, final = self.run_menu("5", "P1", "2", "9.49", "4", "6")
        self.assertEqual(final["product_catalog"]["P1"]["Price"], 9.49)

    def test_menu_returns_after_each_action(self):
        session, _ = self.run_menu("1", "3", "4", "6")
        self.assertEqual(session.output.count("Main Menu"), 4)


class RegressionSaleValidation(ProgramTestCase):
    """Lab: error handling for invalid input and overselling."""

    def test_catalog_is_shown_before_asking_for_a_product(self):
        session = self.sell("P1", 1)
        self.assertLess(session.output.index("Product 1"),
                        session.output.index(session.prompts[0]))

    def test_confirmation_names_the_product_and_quantity(self):
        self.assertRegex(self.sell("P2", 3).output,
                         r"sold 3 of P2 \(Product 2\)")

    def test_unknown_product_ids_are_rejected_then_reprompted(self):
        for bad_id in ("P99", "", "abc", "p1", "P1 5"):
            with self.subTest(bad_id=bad_id):
                self.program = load_program()
                session = drive(self.program.make_sale, [bad_id, "P1", "1"])
                self.assertIn("Invalid id", session.output)

    def test_bad_quantities_are_rejected_then_reprompted(self):
        # P1 has 100 in stock.
        for bad_quantity in ("abc", "", "2.5", "0", "-1", "101"):
            with self.subTest(bad_quantity=bad_quantity):
                self.program = load_program()
                session = drive(self.program.make_sale,
                                ["P1", bad_quantity, "1"])
                self.assertEqual(len(session.prompts), 3)

    def test_rejected_quantities_never_create_a_sale_or_touch_stock(self):
        drive(self.program.make_sale, ["P1", "abc", "0", "-1", "101", "1"])
        # Only the final valid "1" may have any effect.
        self.assertIn(self.catalog["P1"]["Stock"], (99, 100))
        self.assertLessEqual(len(self.history), 1)

    def test_selling_exactly_the_stock_on_hand_is_allowed(self):
        session = self.sell("P7", 1)  # P7 has exactly 1 in stock
        self.assertEqual(len(session.prompts), 2)

    def test_one_more_than_stock_on_hand_is_rejected(self):
        session = drive(self.program.make_sale, ["P5", "11", "10"])
        self.assertEqual(len(session.prompts), 3)

    def test_quantity_limit_follows_updated_stock(self):
        self.update("P1", "Stock", "2")
        session = drive(self.program.make_sale, ["P1", "3", "2"])
        self.assertEqual(len(session.prompts), 3)

    def test_sale_does_not_change_price_name_or_other_products(self):
        before = {key: dict(value) for key, value in self.catalog.items()}
        self.sell("P1", 2)
        self.assertEqual(self.catalog["P1"]["Name"], before["P1"]["Name"])
        self.assertEqual(self.catalog["P1"]["Price"], before["P1"]["Price"])
        del before["P1"]
        for product_id, product in before.items():
            self.assertEqual(self.catalog[product_id], product)


class RegressionUpdateProduct(ProgramTestCase):
    """Lab: update product details, including price and stock."""

    def test_updates_each_field(self):
        self.update("P1", "Name", "Deluxe Widget")
        self.update("P1", "Price", "12.50")
        self.update("P1", "Stock", "7")
        self.assertEqual(self.catalog["P1"],
                         {"Name": "Deluxe Widget", "Price": 12.5, "Stock": 7})

    def test_values_keep_their_types(self):
        self.update("P1", "Price", "10")
        self.update("P1", "Name", "123")
        self.assertIsInstance(self.catalog["P1"]["Price"], float)
        self.assertEqual(self.catalog["P1"]["Name"], "123")

    def test_stock_can_be_set_to_zero(self):
        self.update("P1", "Stock", "0")
        self.assertEqual(self.catalog["P1"]["Stock"], 0)

    def test_non_numeric_price_is_rejected_then_reprompted(self):
        session = self.update("P1", "Price", "abc", "", "$5", "12.50")
        self.assertEqual(len(session.prompts), 4)
        self.assertEqual(self.catalog["P1"]["Price"], 12.5)

    def test_non_integer_stock_is_rejected_then_reprompted(self):
        session = self.update("P1", "Stock", "abc", "", "2.5", "7")
        self.assertEqual(len(session.prompts), 4)
        self.assertEqual(self.catalog["P1"]["Stock"], 7)

    def test_update_changes_only_the_chosen_product(self):
        p2_before = dict(self.catalog["P2"])
        self.update("P1", "Price", "1.00")
        self.assertEqual(self.catalog["P2"], p2_before)

    def test_unknown_product_id_is_refused_without_prompting(self):
        session = self.update("P99", "Price")
        self.assertIn("Invalid Product id", session.output)
        self.assertEqual(session.prompts, [])

    def test_unknown_attribute_is_refused_without_prompting(self):
        session = self.update("P1", "Colour")
        self.assertIn("Invalid Product Catalog Attribute", session.output)
        self.assertEqual(session.prompts, [])
        self.assertNotIn("Colour", self.catalog["P1"])

    def test_edit_menu_applies_several_edits_in_one_session(self):
        drive(self.program.update_product_details,
              ["P2", "1", "Gadget", "2", "6.49", "3", "75", "4"])
        self.assertEqual(self.catalog["P2"],
                         {"Name": "Gadget", "Price": 6.49, "Stock": 75})

    def test_edit_menu_done_changes_nothing(self):
        before = dict(self.catalog["P2"])
        drive(self.program.update_product_details, ["P2", "4"])
        self.assertEqual(self.catalog["P2"], before)

    def test_edit_menu_reprompts_for_unknown_product(self):
        session = drive(self.program.update_product_details,
                        ["P99", "P1", "4"])
        self.assertIn("Invalid id", session.output)

    def test_edit_menu_rejects_invalid_choice(self):
        session = drive(self.program.update_product_details,
                        ["P1", "9", "4"])
        self.assertIn("Invalid choice", session.output)


class RegressionEmptySalesScreens(ProgramTestCase):
    """Must not crash before any sale exists. Watch for max() on an empty list."""

    def test_history_with_no_sales(self):
        self.assertIn("Sales History",
                      drive(self.program.view_sales_history, []).output)

    def test_kpis_with_no_sales(self):
        drive(self.program.display_kpis, [])


###############################################################################
# Todo tests: Lab 2 requirements still to build
###############################################################################
class TodoSaleRecording(ProgramTestCase):
    """Lab: Make a Sale updates stock and records a sale dictionary."""

    def test_sale_reduces_stock(self):
        self.sell("P1", 3)
        self.assertEqual(self.catalog["P1"]["Stock"], 97)

    def test_several_sales_reduce_stock_cumulatively(self):
        self.sell("P1", 3)
        self.sell("P1", 4)
        self.assertEqual(self.catalog["P1"]["Stock"], 93)

    def test_selling_everything_leaves_zero_stock(self):
        self.sell("P5", 10)
        self.assertEqual(self.catalog["P5"]["Stock"], 0)

    def test_second_sale_is_limited_by_remaining_stock(self):
        self.sell("P5", 7)  # 3 left of 10
        session = drive(self.program.make_sale, ["P5", "4", "3"])
        self.assertEqual(len(session.prompts), 3)
        self.assertEqual(self.catalog["P5"]["Stock"], 0)

    def test_sale_is_appended_to_the_history_list(self):
        self.sell("P1", 3)
        self.assertIsInstance(self.history, list)
        self.assertEqual(len(self.history), 1)
        self.assertIsInstance(self.history[0], dict)

    def test_sale_record_has_the_required_values(self):
        self.sell("P1", 3)
        sale = self.history[0]
        self.assertEqual(sale_field(sale, "product_id"), "P1")
        self.assertEqual(sale_field(sale, "quantity"), 3)
        self.assertAlmostEqual(sale_field(sale, "total"), 32.97, places=2)

    def test_quantity_is_stored_as_a_number(self):
        self.sell("P1", 3)
        self.assertIsInstance(sale_field(self.history[0], "quantity"), int)

    def test_sale_record_has_a_current_date_and_time(self):
        self.sell("P1", 1)
        stamp = sale_field(self.history[0], "datetime")
        self.assertTrue(stamp)
        self.assertIn(str(datetime.now().year), str(stamp))

    def test_sale_ids_are_unique(self):
        for _ in range(5):
            self.sell("P1", 1)
        ids = [sale_field(sale, "sale_id") for sale in self.history]
        self.assertEqual(len(ids), len(set(ids)))

    def test_sales_stay_in_the_order_they_happened(self):
        self.sell("P1", 1)
        self.sell("P2", 1)
        self.sell("P3", 1)
        self.assertEqual([sale_field(s, "product_id") for s in self.history],
                         ["P1", "P2", "P3"])

    def test_total_uses_the_current_price(self):
        self.update("P1", "Price", "2.50")
        self.sell("P1", 4)
        self.assertAlmostEqual(sale_field(self.history[0], "total"), 10.00,
                               places=2)

    def test_past_sale_total_does_not_change_when_price_changes(self):
        self.sell("P1", 2)
        self.update("P1", "Price", "99.99")
        self.assertAlmostEqual(sale_field(self.history[0], "total"), 21.98,
                               places=2)

    def test_sold_out_product_does_not_trap_the_user(self):
        # Today nothing can satisfy the quantity prompt at zero stock, so the
        # only way out of the screen is to quit the program. Either refusing at
        # the id prompt or returning to the menu passes this test.
        self.catalog["P7"]["Stock"] = 0

        def answer(prompt, prompt_number):
            if prompt_number == 1:
                return "P7"
            return "P1" if re.search(r"\bid\b", prompt, re.I) else "1"

        drive(self.program.make_sale, answer)
        self.assertEqual(self.catalog["P7"]["Stock"], 0)
        sold = [sale_field(sale, "product_id") for sale in self.history]
        self.assertNotIn("P7", sold)


class TodoSalesHistory(ProgramTestCase):
    """Lab: View Sales History shows id, date/time, name, quantity and total."""

    def test_shows_every_required_detail(self):
        self.sell("P1", 3)
        sale = self.history[0]
        output = drive(self.program.view_sales_history, []).output
        self.assertIn(str(sale_field(sale, "sale_id")), output)
        self.assertIn(str(datetime.now().year), output)
        self.assertIn("Product 1", output)
        self.assertRegex(output, r"\b3\b")
        self.assertIn("32.97", output)

    def test_shows_the_product_name_not_just_the_id(self):
        self.update("P2", "Name", "Blue Widget")
        self.sell("P2", 1)
        self.assertIn("Blue Widget",
                      drive(self.program.view_sales_history, []).output)

    def test_shows_every_sale(self):
        self.sell("P1", 1)
        self.sell("P3", 2)
        output = drive(self.program.view_sales_history, []).output
        self.assertIn("Product 1", output)
        self.assertIn("Product 3", output)
        self.assertIn("10.99", output)
        self.assertIn("3.98", output)

    def test_totals_are_shown_to_two_decimals(self):
        # 2 * 5.0 is 10.0 as a float, which should display as 10.00.
        self.update("P1", "Price", "5")
        self.sell("P1", 2)
        self.assertIn("10.00",
                      drive(self.program.view_sales_history, []).output)


class TodoKpis(ProgramTestCase):
    """Lab: total revenue, best-selling product, highest-revenue product."""

    def product_after_label(self, output, label_pattern):
        """Return the first product mentioned after a label, like 'P3' """
        label = re.search(label_pattern, output, re.I)
        self.assertIsNotNone(label, f"No {label_pattern!r} in:\n{output}")
        found = re.search(r"\bP(?:roduct\s*)?(\d+)\b", output[label.end():])
        self.assertIsNotNone(found, f"No product after label in:\n{output}")
        return "P" + found.group(1)

    def best_seller(self, output):
        return self.product_after_label(
            output, r"best|top[- ]?selling|most sold")

    def top_earner(self, output):
        return self.product_after_label(
            output, r"highest|top[- ]?revenue|top[- ]?grossing|most revenue")

    def kpis(self):
        return drive(self.program.display_kpis, []).output

    def test_total_revenue_adds_up_every_sale(self):
        self.sell("P3", 10)  # 19.90
        self.sell("P7", 1)   # 100.99
        self.assertIn("120.89", self.kpis())

    def test_best_seller_and_top_earner_can_be_different_products(self):
        self.sell("P3", 10)  # most units, little revenue
        self.sell("P7", 1)   # fewest units, most revenue
        output = self.kpis()
        self.assertEqual(self.best_seller(output), "P3")
        self.assertEqual(self.top_earner(output), "P7")

    def test_best_seller_adds_up_several_sales_of_one_product(self):
        self.sell("P1", 5)
        for _ in range(3):
            self.sell("P3", 2)  # 6 units in total beats 5 in one sale
        self.assertEqual(self.best_seller(self.kpis()), "P3")

    def test_top_earner_adds_up_several_sales_of_one_product(self):
        self.sell("P7", 1)  # 100.99 in one sale
        for _ in range(3):
            self.sell("P4", 10)  # 479.70 across three sales
        self.assertEqual(self.top_earner(self.kpis()), "P4")

    def test_revenue_uses_the_price_at_time_of_sale(self):
        self.sell("P1", 2)  # 21.98
        self.update("P1", "Price", "99.99")
        self.assertIn("21.98", self.kpis())

    def test_full_session_through_the_menu(self):
        session, final = self.run_menu(
            "2", "P3", "10",        # sale of 19.90
            "2", "P7", "1",         # sale of 100.99
            "3",                    # history
            "4",                    # KPIs
            "6",
        )
        self.assertEqual(final["product_catalog"]["P3"]["Stock"], 190)
        self.assertEqual(final["product_catalog"]["P7"]["Stock"], 0)
        self.assertEqual(len(final["sales_history"]), 2)
        self.assertIn("120.89", session.output)


###############################################################################
# Todo tests: known bugs in the code that exists today
###############################################################################
class TodoKnownBugs(ProgramTestCase):

    def assert_rejected(self, key, bad_value, good_value):
        """A bad value must be refused, then a good one accepted."""
        self.update("P1", key, bad_value, good_value, allow_unused=True)
        self.assertEqual(self.catalog["P1"][key], good_value_as(key, good_value))

    def test_negative_price_is_rejected(self):
        self.assert_rejected("Price", "-5", "9.99")

    def test_negative_stock_is_rejected(self):
        self.assert_rejected("Stock", "-5", "12")

    def test_nan_price_is_rejected(self):
        self.update("P1", "Price", "nan", "9.99", allow_unused=True)
        self.assertFalse(math.isnan(self.catalog["P1"]["Price"]))

    def test_infinite_price_is_rejected(self):
        self.assert_rejected("Price", "inf", "9.99")

    def test_blank_name_is_rejected(self):
        self.assert_rejected("Name", "   ", "Good Name")

    def test_whole_number_price_in_catalog_can_still_be_updated(self):
        # The type check compares float to the stored int and never succeeds.
        self.catalog["P1"]["Price"] = 10
        self.update("P1", "Price", "12.50")
        self.assertEqual(self.catalog["P1"]["Price"], 12.5)

    def test_catalog_shows_prices_to_two_decimals(self):
        self.update("P1", "Price", "5.5")
        self.assertIn("$5.50", drive(self.program.view_catalog, []).output)

    def test_zero_quantity_message_is_not_about_overselling(self):
        session = drive(self.program.make_sale, ["P1", "0", "1"])
        self.assertNotIn("more items (0)", session.output)

    def test_sale_id_prompt_only_asks_for_what_it_reads(self):
        prompt = self.sell("P1", 1).prompts[0].lower()
        self.assertNotRegex(prompt, r"quan")

    def test_update_prompt_does_not_mention_a_sale(self):
        session = drive(self.program.update_product_details, ["P1", "4"])
        self.assertNotIn("sale", session.prompts[0].lower())

    def test_text_shown_to_the_user_has_no_typos(self):
        sale = drive(self.program.make_sale, ["P99", "P1", "abc", "999", "1"])
        update = drive(self.program.update_product_details, ["P99", "P1", "4"])
        output = sale.output + update.output
        self.assertNotIn("quanity", output.lower())
        self.assertNotIn("''", output)
        self.assertNotIn("that are in stock", output)


def good_value_as(key, text):
    return {"Price": float, "Stock": int}.get(key, str)(text)


###############################################################################
# Todo tests: checks before turning in the assignment
###############################################################################
class TodoSubmissionChecks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.source = PROGRAM_PATH.read_text(encoding="utf-8")

    def test_no_placeholder_comments_remain(self):
        self.assertNotRegex(self.source, r"(?i)your code")

    def test_collaboration_task_lists_are_filled_in(self):
        self.assertNotRegex(self.source, r"# 1\.[ \t]*\n")


if __name__ == "__main__":
    unittest.main()
