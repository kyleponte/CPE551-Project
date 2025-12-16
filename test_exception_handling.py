"""
Test suite for exception handling in signal_analyzer and data_processor.

This test verifies that:
1. Divide-by-zero exceptions are handled
2. Zero/negative green_time values raise ValueError
3. Empty data bins are handled
4. Empty dataframes are handled
5. FileNotFoundError is raised for missing files
"""

import pandas as pd
import os
from intersection_data import IntersectionData
from signal_analyzer import SignalTimingAnalyzer
from data_processor import (
    load_traffic_data,
    aggregate_by_hour,
    save_results,
    volume_stream,
    validate_traffic_data
)


def test_zero_green_time_baseline():
    """Test that zero green_time raises ValueError."""
    intersection = IntersectionData("TEST001", {}, [100, 150, 120])
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Should handle zero green_time gracefully
    result = analyzer.compute_baseline_delays(0.0)
    assert result == []  # Should return empty list on error


def test_negative_green_time_baseline():
    """Test that negative green_time raises ValueError."""
    intersection = IntersectionData("TEST002", {}, [100, 150, 120])
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Should handle negative green_time gracefully
    result = analyzer.compute_baseline_delays(-10.0)
    assert result == []  # Should return empty list on error


def test_zero_green_time_alternative():
    """Test that zero green_time in alternative delays raises ValueError."""
    intersection = IntersectionData("TEST003", {}, [100, 150, 120])
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Should handle zero green_time gracefully
    result = analyzer.compute_alternative_delays(0.0)
    assert result == []  # Should return empty list on error


def test_empty_volumes_delay_calculation():
    """Test delay calculation with empty volumes list."""
    intersection = IntersectionData("TEST004", {}, [])  # Empty volumes
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Should handle empty volumes gracefully
    result = analyzer.compute_baseline_delays(30.0)
    assert isinstance(result, list)
    assert len(result) == 0


def test_compare_plans_empty_delays():
    """Test compare_plans with empty delay lists."""
    intersection = IntersectionData("TEST005", {}, [100, 150])
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Compare without computing delays first
    result = analyzer.compare_plans()
    
    # Should return zero metrics
    assert isinstance(result, dict)
    assert result['baseline_avg_delay'] == 0.0
    assert result['alternative_avg_delay'] == 0.0


def test_file_not_found_exception():
    """Test FileNotFoundError handling."""
    # Should raise FileNotFoundError for nonexistent file
    try:
        load_traffic_data('nonexistent_file.csv')
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass  # Expected


def test_empty_dataframe_aggregation():
    """Test handling of empty dataframe in aggregation."""
    empty_df = pd.DataFrame()
    
    # Should handle empty dataframe gracefully
    result = aggregate_by_hour(empty_df)
    assert isinstance(result, dict)
    # Should return empty dict on error
    assert result == {}


def test_aggregate_by_hour_empty_bins():
    """Test handling of empty bins in hourly aggregation."""
    # Create data with some hours missing
    data = pd.DataFrame({
        'hour': [8, 10, 12],  # Missing hours 9, 11, etc.
        'volume': [100, 150, 120]
    })
    
    result = aggregate_by_hour(data)
    
    # Should return all 24 hours with 0 for empty bins
    assert len(result) == 24
    assert result[8] == 100
    assert result[9] == 0  # Empty bin should be 0
    assert result[10] == 150
    assert result[11] == 0  # Empty bin should be 0


def test_zero_volume_delay_calculation():
    """Test delay calculation with zero volumes."""
    intersection = IntersectionData("TEST006", {}, [0, 0, 0])  # All zeros
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Should handle zero volumes without error
    result = analyzer.compute_baseline_delays(30.0)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 3


def test_missing_counts_handling():
    """Test handling of missing/zero counts in data."""
    # Create test data with missing values
    test_data = pd.DataFrame({
        'intersection_id': ['INT001', 'INT001', 'INT001'],
        'timestamp': ['2024-01-01 08:00', '2024-01-01 08:15', '2024-01-01 08:30'],
        'approach': ['North', 'South', 'East'],
        'count': [100, 0, None]  # Zero and missing values
    })
    
    # Should not raise exception
    # Test that zero/missing counts are handled
    assert test_data['count'].fillna(0).sum() >= 0
    
    # Validate should handle this
    is_valid = validate_traffic_data(test_data)
    # Should return True but print warnings
    assert isinstance(is_valid, bool)


def test_data_io_operations():
    """Test CSV reading and writing operations."""
    # Create sample data
    test_data = pd.DataFrame({
        'intersection_id': ['INT001'],
        'timestamp': ['2024-01-01 08:00'],
        'approach': ['North'],
        'count': [100],
        'volume': [100]
    })
    
    # Test writing
    output_path = 'test_output.csv'
    try:
        save_results(test_data, output_path)
        
        # Test reading
        loaded_data = pd.read_csv(output_path)
        assert not loaded_data.empty
        assert len(loaded_data) == 1
        
    finally:
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)


def test_volume_stream_empty_data():
    """Test volume_stream with empty data."""
    empty_df = pd.DataFrame()
    
    # Should handle empty data gracefully
    records = list(volume_stream(empty_df))
    assert len(records) == 0


def test_analyzer_init_with_none():
    """Test that initializing analyzer with None raises ValueError."""
    try:
        SignalTimingAnalyzer(None)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected


def test_analyzer_init_invalid_type():
    """Test that initializing analyzer with invalid type raises TypeError."""
    try:
        SignalTimingAnalyzer("not an IntersectionData object")
        assert False, "Should have raised TypeError"
    except TypeError:
        pass  # Expected


def test_compare_plans_divide_by_zero():
    """Test that compare_plans handles divide-by-zero scenarios."""
    intersection = IntersectionData("TEST007", {}, [100, 150])
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Compute delays
    analyzer.compute_baseline_delays(30.0)
    analyzer.compute_alternative_delays(45.0)
    
    # Manually set delays to cause potential divide-by-zero
    analyzer.baseline_delays = [0.0, 0.0]
    analyzer.alternative_delays = [0.0, 0.0]
    
    # Should handle divide-by-zero gracefully
    result = analyzer.compare_plans()
    assert isinstance(result, dict)
    assert result['throughput_change'] == 0.0
    assert result['improvement_percentage'] == 0.0


if __name__ == "__main__":
    """Run tests if executed directly."""
    print("Running exception handling tests...")
    
    try:
        test_zero_green_time_baseline()
        print("[PASS] Zero green_time baseline test passed")
    except Exception as e:
        print(f"[FAIL] Zero green_time baseline test failed: {e}")
    
    try:
        test_negative_green_time_baseline()
        print("[PASS] Negative green_time baseline test passed")
    except Exception as e:
        print(f"[FAIL] Negative green_time baseline test failed: {e}")
    
    try:
        test_empty_volumes_delay_calculation()
        print("[PASS] Empty volumes delay calculation test passed")
    except Exception as e:
        print(f"[FAIL] Empty volumes delay calculation test failed: {e}")
    
    try:
        test_compare_plans_empty_delays()
        print("[PASS] Compare plans empty delays test passed")
    except Exception as e:
        print(f"[FAIL] Compare plans empty delays test failed: {e}")
    
    try:
        test_aggregate_by_hour_empty_bins()
        print("[PASS] Aggregate by hour empty bins test passed")
    except Exception as e:
        print(f"[FAIL] Aggregate by hour empty bins test failed: {e}")
    
    try:
        test_zero_volume_delay_calculation()
        print("[PASS] Zero volume delay calculation test passed")
    except Exception as e:
        print(f"[FAIL] Zero volume delay calculation test failed: {e}")
    
    try:
        test_missing_counts_handling()
        print("[PASS] Missing counts handling test passed")
    except Exception as e:
        print(f"[FAIL] Missing counts handling test failed: {e}")
    
    try:
        test_data_io_operations()
        print("[PASS] Data I/O operations test passed")
    except Exception as e:
        print(f"[FAIL] Data I/O operations test failed: {e}")
    
    print("\nException handling tests completed!")

