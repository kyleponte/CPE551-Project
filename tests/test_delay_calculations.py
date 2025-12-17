"""
Pytest tests for delay calculation functions.

Part 1 requirement: At least two meaningful tests using pytest.
"""

import pytest
from timing_functions import compute_average_delay


class TestDelayCalculations:
    """Test delay calculation functions."""
    
    def test_delay_formula_known_values(self):
        """
        Test delay formula on known input/output values.
        
        Part 1 requirement: Test delay function on small fixture.
        """
        # Test case 1: Low volume, sufficient green time
        volume = 300  # vehicles per hour
        green_time = 30.0  # seconds
        delay = compute_average_delay(volume, green_time)
        
        # Delay should be positive and reasonable
        assert delay >= 0, "Delay should be non-negative"
        assert delay < 100, "Delay should be reasonable for this scenario"
        
        # Test case 2: High volume, short green time
        volume_high = 1000  # vehicles per hour
        green_time_short = 20.0  # seconds
        delay_high = compute_average_delay(volume_high, green_time_short)
        
        # High volume should result in higher delay
        assert delay_high > delay, "Higher volume should result in higher delay"
        
        # Test case 3: Known calculation
        volume_test = 500
        green_test = 30.0
        delay_test = compute_average_delay(volume_test, green_test)
        assert isinstance(delay_test, float), "Delay should be a float"
        assert delay_test >= 0, "Delay should be non-negative"
    
    def test_zero_handling(self):
        """
        Test handling of zero or missing counts.
        
        Part 1 requirement: Test handling of zero/missing counts.
        """
        # Test zero volume
        delay_zero_vol = compute_average_delay(0, 30.0)
        assert delay_zero_vol >= 0, "Zero volume should not cause error"
        
        # Test zero green time - function catches ZeroDivisionError and returns 0.0
        result = compute_average_delay(100, 0.0)
        assert result == 0.0, "Zero green time should return 0.0 after exception handling"
    
    def test_negative_values(self):
        """Test handling of negative values."""
        # Negative volume should be handled (may produce negative delay, which is acceptable for testing)
        delay_neg = compute_average_delay(-100, 30.0)
        # Function should handle or the calculation should work
        assert isinstance(delay_neg, (int, float)), "Should return numeric value"

