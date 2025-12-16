"""
Test suite for TimingPlan class with operator overloading.

This test verifies that:
1. The class instantiates correctly
2. Operator overloading (__add__) works
3. Mutable objects (dict, list) function properly
4. __str__ method works correctly
"""

from timing_plan import TimingPlan


def test_timing_plan_instantiation():
    """Test that TimingPlan can be instantiated."""
    green_times = {'North': 30.0, 'South': 25.0, 'East': 20.0}
    plan = TimingPlan(green_times, cycle_length=120.0)
    
    assert plan is not None
    assert isinstance(plan, TimingPlan)
    assert plan.cycle_length == 120.0
    assert plan.green_times == green_times


def test_mutable_objects():
    """Test that mutable objects (dict, list) work correctly."""
    plan = TimingPlan({'North': 30.0}, 120.0)
    
    # Verify mutable dict
    assert isinstance(plan.green_times, dict)
    plan.green_times['South'] = 25.0  # Modify dict
    assert 'South' in plan.green_times
    assert plan.green_times['South'] == 25.0
    
    # Verify mutable list
    assert isinstance(plan.phase_durations, list)
    plan.add_phase_duration(30.0)
    plan.add_phase_duration(25.0)
    assert len(plan.phase_durations) == 2
    assert plan.phase_durations == [30.0, 25.0]


def test_operator_overloading_add():
    """Test operator overloading with + operator."""
    # Create two timing plans
    plan1 = TimingPlan(
        green_times={'North': 30.0, 'South': 25.0},
        cycle_length=120.0
    )
    
    plan2 = TimingPlan(
        green_times={'North': 35.0, 'East': 20.0},
        cycle_length=130.0
    )
    
    # Combine plans using + operator (Part 2 requirement: operator overloading)
    combined = plan1 + plan2
    
    # Verify combined plan
    assert isinstance(combined, TimingPlan)
    
    # Verify averaged cycle length
    assert combined.cycle_length == 125.0  # (120 + 130) / 2
    
    # Verify averaged green times for common approaches
    assert combined.green_times['North'] == 32.5  # (30 + 35) / 2
    
    # Verify approaches from both plans are included
    assert 'South' in combined.green_times
    assert 'East' in combined.green_times


def test_operator_overloading_different_approaches():
    """Test operator overloading with completely different approaches."""
    plan1 = TimingPlan({'North': 30.0, 'South': 25.0}, 120.0)
    plan2 = TimingPlan({'East': 20.0, 'West': 15.0}, 100.0)
    
    combined = plan1 + plan2
    
    # All approaches should be present
    assert 'North' in combined.green_times
    assert 'South' in combined.green_times
    assert 'East' in combined.green_times
    assert 'West' in combined.green_times
    
    # Cycle length should be averaged
    assert combined.cycle_length == 110.0  # (120 + 100) / 2


def test_operator_overloading_type_error():
    """Test that operator overloading raises TypeError for invalid types."""
    plan = TimingPlan({'North': 30.0}, 120.0)
    
    # Should raise TypeError when trying to add non-TimingPlan
    try:
        result = plan + "not a plan"
        assert False, "Should have raised TypeError"
    except TypeError:
        pass  # Expected


def test_str_method():
    """Test __str__ method implementation."""
    plan = TimingPlan(
        green_times={'North': 30.0, 'South': 25.0, 'East': 20.0},
        cycle_length=120.0
    )
    
    str_repr = str(plan)
    
    # Verify string representation
    assert isinstance(str_repr, str)
    assert 'TimingPlan' in str_repr
    assert '120.0s' in str_repr
    assert 'approaches=3' in str_repr


def test_helper_methods():
    """Test helper methods like get_total_green_time and get_approach_count."""
    plan = TimingPlan(
        green_times={'North': 30.0, 'South': 25.0, 'East': 20.0},
        cycle_length=120.0
    )
    
    # Test total green time
    total = plan.get_total_green_time()
    assert total == 75.0  # 30 + 25 + 20
    
    # Test approach count
    count = plan.get_approach_count()
    assert count == 3


def test_chain_operations():
    """Test chaining multiple + operations."""
    plan1 = TimingPlan({'North': 30.0}, 120.0)
    plan2 = TimingPlan({'North': 35.0}, 130.0)
    plan3 = TimingPlan({'North': 40.0}, 140.0)
    
    # Chain operations
    combined = plan1 + plan2 + plan3
    
    # Verify result
    assert isinstance(combined, TimingPlan)
    # North should be average of all three: (30 + 35 + 40) / 2 / 2 = 26.25
    # Actually, it's: ((30+35)/2 + 40)/2 = (32.5 + 40)/2 = 36.25
    assert combined.green_times['North'] == 36.25
    # Cycle: ((120+130)/2 + 140)/2 = (125 + 140)/2 = 132.5
    assert combined.cycle_length == 132.5


if __name__ == "__main__":
    """Run tests if executed directly."""
    print("Running TimingPlan tests...")
    
    test_timing_plan_instantiation()
    print("[PASS] TimingPlan instantiation test passed")
    
    test_mutable_objects()
    print("[PASS] Mutable objects test passed")
    
    test_operator_overloading_add()
    print("[PASS] Operator overloading (+) test passed")
    
    test_operator_overloading_different_approaches()
    print("[PASS] Operator overloading with different approaches test passed")
    
    test_operator_overloading_type_error()
    print("[PASS] Operator overloading type error test passed")
    
    test_str_method()
    print("[PASS] __str__ method test passed")
    
    test_helper_methods()
    print("[PASS] Helper methods test passed")
    
    test_chain_operations()
    print("[PASS] Chain operations test passed")
    
    print("\nAll tests passed!")

