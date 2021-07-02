# -*- coding: utf-8 -*-
"""
###############################################################################
########################## NO IMPLEMENTATION NEEDED ###########################
###############################################################################
"""
from __future__ import print_function


import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# pylint: disable=wrong-import-position
import numpy as np

try:
    from dev_cell import Cell, logit, inv_logit
except ImportError:
    from student_cell import Cell, logit, inv_logit
from resources.results import (CELL_UPDATE_HASH, CELL_PROB_HASH, LOGIT_HASH,
                               INV_LOGIT_HASH)

from ksr_common.string_suite import TestSuite
from ksr_common.hash_function import js_hash


def _test_logit(ts):
    logit_test = True
    ts.testcase_open("Logit")
    zero_test = False
    ts.test_open("logit(0)", "Tests whether argument 0 is handled correctly.")

    ###########################################################################
    ################################## NOTE ###################################
    ###########################################################################
    # For anyone looking at the test code: usually there is no need to throw
    # any of the following exceptions in your own code. The underlying math
    # function, be it from Python's own math module or numpy, will throw these
    # exceptions. If you find this statement to be false, please send in your
    # implementation and tell something about the problem. If the implementation
    # is valid and does not pass the test, the test will have to be fixed.
    ###########################################################################
    ################################## NOTE ###################################
    ###########################################################################
    try:
        logit(0)
    except ValueError:
        zero_test = True
    except Exception:  # pylint: disable=broad-except
        zero_test = False
        ts.test_close(zero_test,
                      "Your logit function raised an unexpected exception!")
    else:
        zero_test = np.isneginf(logit(0))
        ts.test_close(zero_test,
                      "Your logit did not handle event=0 as expected.")
    logit_test = logit_test and zero_test

    ts.test_open("logit(1)", "Tests whether argument 1 is handled correctly.")
    one_test = True
    try:
        logit(1)
    except ZeroDivisionError:
        one_test = True
    except Exception:  # pylint: disable=broad-except
        one_test = False
        ts.test_close(
            one_test, "Your logit function raised an unexpected exception!"
        )
    else:
        one_test = np.isposinf(logit(1))
        ts.test_close(
            one_test, "Your logit did not handle event=1 as expected."
        )
    logit_test = logit_test and one_test

    ts.test_open(
        "logit()", [
            "Tests 100 sample values with the logit function",
            "and compares them with precomputed hash-values."
        ]
    )
    num_samples = 100
    # values increment in 0.01 steps, actually just 99 values
    probabilities = np.linspace(0.0, 1.0, num_samples, endpoint=False)[1:]
    range_test = True
    count_logit_false = 0
    for i, probability in enumerate(probabilities):
        res = logit(probability)
        res_hash = js_hash([np.around(res, 2)])
        if res_hash != LOGIT_HASH[i]:
            count_logit_false += 1

    if count_logit_false > 0:
        range_test = False
    ts.test_close(
        range_test, [
            "Your logit results do not match the precomputed hash values!",
            "mismatches: {}".format(count_logit_false)
        ]
    )
    logit_test = logit_test and range_test
    ts.testcase_close(logit_test)
    return logit_test


def _test_inv_logit(ts):
    inv_logit_test = True
    ts.testcase_open("InvLogit")
    sevenhundred_test = True
    try:
        inv_logit(-710)
    except OverflowError:
        ts.test_open(
            "inv_logit(-710)",
            "Tests whether an OverflowError is thrown when passing -710."
        )
        ts.test_close(
            sevenhundred_test,
            "Your inv_logit function raised an unexpected exception!"
        )
    inv_logit_test = inv_logit_test and sevenhundred_test

    ts.test_open(
        "inv_logit()", [
            "Tests 1400 sample values with the inv_logit function",
            "and compares them with precomputed hash-values."
        ]
    )
    my_range = [-700, 700]
    range_test = True
    count_logit_false = 0
    for i, value in enumerate(range(my_range[0], my_range[1])):
        res = inv_logit(value)
        res_hash = js_hash([np.around(res, 2)])
        if res_hash != INV_LOGIT_HASH[i]:
            count_logit_false += 1

    if count_logit_false > 0:
        range_test = False

    ts.test_close(
        range_test, [
            "Your inv_logit results do not match the precomputed hash values!",
            "mismatches: {}".format(count_logit_false)
        ]
    )
    inv_logit_test = inv_logit_test and range_test

    ts.testcase_close(inv_logit_test)
    return inv_logit_test


def _test_cell(ts):
    """tests Cell Class with a precomputed sequence of values"""
    cell_test = True
    ts.testcase_open("Cell")
    my_cell = Cell()
    test_update = []
    test_probability = []
    test_range = [46, 96, 46]
    for _ in range(test_range[0]):
        my_cell.update(0.9)
        test_update.append(js_hash([np.around(my_cell.occ_logit, 2)]))
        test_probability.append(js_hash([np.around(my_cell.probability(), 2)]))
    for _ in range(test_range[1]):
        my_cell.update(0.1)
        test_update.append(js_hash([np.around(my_cell.occ_logit, 2)]))
        test_probability.append(js_hash([np.around(my_cell.probability(), 2)]))
    for _ in range((test_range[2])):
        my_cell.update(0.9)
        test_update.append(js_hash([np.around(my_cell.occ_logit, 2)]))
        test_probability.append(js_hash([np.around(my_cell.probability(), 2)]))
    count_update_false = 0
    count_prob_false = 0
    for left, right, left2, right2 in zip(test_update, CELL_UPDATE_HASH,
                                          test_probability, CELL_PROB_HASH):
        if left != right:
            count_update_false += 1
        if left2 != right2:
            count_prob_false += 1
    cell_update_test = True

    ts.test_open(
        "Cell.update()", [
            "Test the update function using 192 values in 3",
            "batches: 46 updates with 0.9 followed by 96 updates",
            "with 0.1 followed by 46 updates with 0.9."
        ]
    )
    if count_update_false > 0:
        cell_update_test = False

    ts.test_close(
        cell_update_test, [
            "Your update results do not match the precomputed hash values!",
            "mismatches: {}".format(count_update_false)
        ]
    )
    cell_test = cell_test and count_update_false

    ts.test_open(
        "Cell.probability()", [
            "Test the probability function using 192 values from ",
            "the preceding test"
        ]
    )
    cell_probability_test = True
    if count_prob_false > 0:
        cell_probability_test = False
    ts.test_close(
        cell_probability_test, [
            "Your probability results do not match the precomputed hash values!",
            "mismatches: {}".format(count_prob_false)
        ]
    )
    cell_test = cell_test and cell_probability_test

    ts.testcase_close(cell_probability_test)
    return cell_probability_test


def test_cell():
    """Test the Cell implementation using precomputed result hashes"""
    ts = TestSuite("StudentCell")
    global_test_cell = True
    global_test_cell = _test_logit(ts) and global_test_cell
    global_test_cell = _test_inv_logit(ts) and global_test_cell
    global_test_cell = _test_cell(ts) and global_test_cell
    ts.suite_close(global_test_cell)
    if __name__ == "test_cell":
        assert global_test_cell


if __name__ == "__main__":
    test_cell()
