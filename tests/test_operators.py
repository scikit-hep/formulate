# Licensed under a 3-clause BSD style license, see LICENSE.
import pytest

test_add_root = pytest.helpers.create_formula_test("3.4 + 5e-7", input_backend="root")
test_add_numexpr = pytest.helpers.create_formula_test(
    "3.4 + 5e-7", input_backend="numexpr"
)
test_sub_root = pytest.helpers.create_formula_test("3.4 - 5e-7", input_backend="root")
test_sub_numexpr = pytest.helpers.create_formula_test(
    "3.4 - 5e-7", input_backend="numexpr"
)
test_mul_root = pytest.helpers.create_formula_test("3.4 * 5e-7", input_backend="root")
test_mul_numexpr = pytest.helpers.create_formula_test(
    "3.4 * 5e-7", input_backend="numexpr"
)
test_div_root = pytest.helpers.create_formula_test("3.4 / 5e-7", input_backend="root")
test_div_numexpr = pytest.helpers.create_formula_test(
    "3.4 / 5e-7", input_backend="numexpr"
)
test_mod_root = pytest.helpers.create_formula_test("3 % 5", input_backend="root")
test_mod_numexpr = pytest.helpers.create_formula_test("3 % 5", input_backend="numexpr")
test_pow_1_root = pytest.helpers.create_formula_test("3 ** 5", input_backend="root")
test_pow_1_numexpr = pytest.helpers.create_formula_test(
    "3 ** 5", input_backend="numexpr"
)
test_pow_2_root = pytest.helpers.create_formula_test("3 ** -1.5", input_backend="root")
test_pow_2_numexpr = pytest.helpers.create_formula_test(
    "3 ** -1.5", input_backend="numexpr"
)
test_pow_3_root = pytest.helpers.create_formula_test("3 **2", input_backend="root")
# test_pow_3_numexpr = pytest.helpers.create_formula_test('3 **2', input_backend='numexpr')
test_lshift_root = pytest.helpers.create_formula_test("3 << 5", input_backend="root")
test_lshift_numexpr = pytest.helpers.create_formula_test(
    "3 << 5", input_backend="numexpr"
)
test_rshift_root = pytest.helpers.create_formula_test("3 >> 5", input_backend="root")
test_rshift_numexpr = pytest.helpers.create_formula_test(
    "3 >> 5", input_backend="numexpr"
)

test_eq_1_root = pytest.helpers.create_formula_test("3 == 5", input_backend="root")
test_eq_1_numexpr = pytest.helpers.create_formula_test(
    "3 == 5", input_backend="numexpr"
)
test_eq_2_root = pytest.helpers.create_formula_test("3 == 3", input_backend="root")
test_eq_2_numexpr = pytest.helpers.create_formula_test(
    "3 == 3", input_backend="numexpr"
)

test_neq_1_root = pytest.helpers.create_formula_test("3 != 5", input_backend="root")
test_neq_1_numexpr = pytest.helpers.create_formula_test(
    "3 != 5", input_backend="numexpr"
)
test_neq_2_root = pytest.helpers.create_formula_test("3 != 3", input_backend="root")
test_neq_2_numexpr = pytest.helpers.create_formula_test(
    "3 != 3", input_backend="numexpr"
)
test_gt_1_root = pytest.helpers.create_formula_test("3 > 1", input_backend="root")
test_gt_1_numexpr = pytest.helpers.create_formula_test("3 > 1", input_backend="numexpr")
test_gt_2_root = pytest.helpers.create_formula_test("3 > 3", input_backend="root")
test_gt_2_numexpr = pytest.helpers.create_formula_test("3 > 3", input_backend="numexpr")
test_gt_3_root = pytest.helpers.create_formula_test("5 > 3", input_backend="root")
test_gt_3_numexpr = pytest.helpers.create_formula_test("5 > 3", input_backend="numexpr")
test_gteq_1_root = pytest.helpers.create_formula_test("3 >= 1", input_backend="root")
test_gteq_1_numexpr = pytest.helpers.create_formula_test(
    "3 >= 1", input_backend="numexpr"
)
test_gteq_2_root = pytest.helpers.create_formula_test("3 >= 3", input_backend="root")
test_gteq_2_numexpr = pytest.helpers.create_formula_test(
    "3 >= 3", input_backend="numexpr"
)
test_gteq_3_root = pytest.helpers.create_formula_test("5 >= 3", input_backend="root")
test_gteq_3_numexpr = pytest.helpers.create_formula_test(
    "5 >= 3", input_backend="numexpr"
)
test_lt_1_root = pytest.helpers.create_formula_test("3 < 1", input_backend="root")
test_lt_1_numexpr = pytest.helpers.create_formula_test("3 < 1", input_backend="numexpr")
test_lt_2_root = pytest.helpers.create_formula_test("3 < 3", input_backend="root")
test_lt_2_numexpr = pytest.helpers.create_formula_test("3 < 3", input_backend="numexpr")
test_lt_3_root = pytest.helpers.create_formula_test("5 < 3", input_backend="root")
test_lt_3_numexpr = pytest.helpers.create_formula_test("5 < 3", input_backend="numexpr")
test_lteq_1_root = pytest.helpers.create_formula_test("3 <= 1", input_backend="root")
test_lteq_1_numexpr = pytest.helpers.create_formula_test(
    "3 <= 1", input_backend="numexpr"
)
test_lteq_2_root = pytest.helpers.create_formula_test("3 <= 3", input_backend="root")
test_lteq_2_numexpr = pytest.helpers.create_formula_test(
    "3 <= 3", input_backend="numexpr"
)
test_lteq_3_root = pytest.helpers.create_formula_test("5 <= 3", input_backend="root")
test_lteq_3_numexpr = pytest.helpers.create_formula_test(
    "5 <= 3", input_backend="numexpr"
)

test_and_1_root = pytest.helpers.create_formula_test("0 && 0", input_backend="root")
test_and_1_numexpr = pytest.helpers.create_formula_test(
    "0 & 0", input_backend="numexpr"
)
test_and_2_root = pytest.helpers.create_formula_test("0 && 1", input_backend="root")
test_and_2_numexpr = pytest.helpers.create_formula_test(
    "0 & 1", input_backend="numexpr"
)
test_and_3_root = pytest.helpers.create_formula_test("1 && 0", input_backend="root")
test_and_3_numexpr = pytest.helpers.create_formula_test(
    "1 & 0", input_backend="numexpr"
)
test_and_4_root = pytest.helpers.create_formula_test("1 && 1", input_backend="root")
test_and_4_numexpr = pytest.helpers.create_formula_test(
    "1 & 1", input_backend="numexpr"
)
test_and_5_root = pytest.helpers.create_formula_test("3 && 5", input_backend="root")
test_and_5_numexpr = pytest.helpers.create_formula_test(
    "3 & 5", input_backend="numexpr"
)

test_or_1_root = pytest.helpers.create_formula_test("0 || 0", input_backend="root")
test_or_1_numexpr = pytest.helpers.create_formula_test("0 | 0", input_backend="numexpr")
test_or_2_root = pytest.helpers.create_formula_test("0 || 1", input_backend="root")
test_or_2_numexpr = pytest.helpers.create_formula_test("0 | 1", input_backend="numexpr")
test_or_3_root = pytest.helpers.create_formula_test("1 || 0", input_backend="root")
test_or_3_numexpr = pytest.helpers.create_formula_test("1 | 0", input_backend="numexpr")
test_or_4_root = pytest.helpers.create_formula_test("1 || 1", input_backend="root")
test_or_4_numexpr = pytest.helpers.create_formula_test("1 | 1", input_backend="numexpr")
test_or_5_root = pytest.helpers.create_formula_test("3 || 5", input_backend="root")
test_or_5_numexpr = pytest.helpers.create_formula_test("3 | 5", input_backend="numexpr")

test_xor_1_root = pytest.helpers.create_formula_test("0 ^ 0", input_backend="root")
test_xor_1_numexpr = pytest.helpers.create_formula_test(
    "0 ^ 0", input_backend="numexpr"
)
test_xor_2_root = pytest.helpers.create_formula_test("0 ^ 1", input_backend="root")
test_xor_2_numexpr = pytest.helpers.create_formula_test(
    "0 ^ 1", input_backend="numexpr"
)
test_xor_3_root = pytest.helpers.create_formula_test("1 ^ 0", input_backend="root")
test_xor_3_numexpr = pytest.helpers.create_formula_test(
    "1 ^ 0", input_backend="numexpr"
)
test_xor_4_root = pytest.helpers.create_formula_test("1 ^ 1", input_backend="root")
test_xor_4_numexpr = pytest.helpers.create_formula_test(
    "1 ^ 1", input_backend="numexpr"
)
test_xor_5_root = pytest.helpers.create_formula_test("3 ^ 5", input_backend="root")
test_xor_5_numexpr = pytest.helpers.create_formula_test(
    "3 ^ 5", input_backend="numexpr"
)

test_not_1_root = pytest.helpers.create_formula_test("!0", input_backend="root")
test_not_1_numexpr = pytest.helpers.create_formula_test("~0", input_backend="numexpr")
test_not_2_root = pytest.helpers.create_formula_test("!1", input_backend="root")
test_not_2_numexpr = pytest.helpers.create_formula_test("~1", input_backend="numexpr")
test_not_3_root = pytest.helpers.create_formula_test("!0", input_backend="root")
test_not_3_numexpr = pytest.helpers.create_formula_test("~0", input_backend="numexpr")
test_not_4_root = pytest.helpers.create_formula_test("!1", input_backend="root")
test_not_4_numexpr = pytest.helpers.create_formula_test("~1", input_backend="numexpr")
test_not_5_root = pytest.helpers.create_formula_test("!5", input_backend="root")
test_not_5_numexpr = pytest.helpers.create_formula_test("~5", input_backend="numexpr")
