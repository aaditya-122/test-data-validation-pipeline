"""Pipeline validation tests."""
from data_pipeline.generator import generate
from data_pipeline.validation import validate, valid_customers, valid_orders

def test_standard_profile_generates_valid_rows():
    customers, orders = generate(100, "standard", seed=123)
    assert len(customers) == len(orders) == 100
    assert validate(customers, orders) == []

def test_seed_is_repeatable():
    assert generate(5, "standard", seed=7) == generate(5, "standard", seed=7)

def test_edge_profile_finds_expected_issue_types():
    customers, orders = generate(100, "edge-cases", seed=11)
    issues = validate(customers, orders)
    kinds = {row["error_type"] for row in issues}
    assert {"out_of_range", "invalid_format", "missing_required", "duplicate", "foreign_key"} <= kinds

def test_invalid_rows_are_excluded_from_persistence_subset():
    customers, orders = generate(100, "edge-cases", seed=11)
    issues = validate(customers, orders)
    clean_customers = valid_customers(customers, issues)
    clean_orders = valid_orders(orders, issues)
    assert all(row["age"] >= 18 for row in clean_customers)
    assert all(row["amount"] > 0 for row in clean_orders)

def test_invalid_configuration_is_rejected():
    import pytest
    with pytest.raises(ValueError): generate(0)
    with pytest.raises(ValueError): generate(2, "unknown")
