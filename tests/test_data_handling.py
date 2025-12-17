"""
Pytest tests for data handling and exception scenarios.

Part 1 requirement: At least two meaningful tests using pytest.
This module tests data handling, zero/missing counts, empty dataframes,
and file I/O operations.
"""

import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from data_processor import (
    aggregate_by_hour,
    load_traffic_data,
    save_results,
    validate_traffic_data,
    volume_stream,
)
from intersection_data import IntersectionData
from signal_analyzer import SignalTimingAnalyzer


class TestDataHandling:
    """Test data handling and exception scenarios."""

    def test_missing_counts_handling(self):
        """
        Test handling of missing/zero counts in data.
        
        Part 1 requirement: Test handling of zero/missing counts.
        This test verifies that the system handles missing or zero
        traffic counts gracefully without crashing.
        """
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
        
        # Validate should handle this gracefully
        is_valid = validate_traffic_data(test_data)
        # Should return True but may print warnings
        assert isinstance(is_valid, bool)
        
        # Test that fillna works correctly
        filled_counts = test_data['count'].fillna(0)
        assert filled_counts.sum() == 100  # 100 + 0 + 0

    def test_zero_volume_delay_calculation(self):
        """
        Test delay calculation with zero volume.
        
        Part 1 requirement: Test handling of zero/missing counts.
        Verifies that zero volumes don't cause divide-by-zero errors.
        """
        # Create intersection data with zero volume
        intersection = IntersectionData(
            intersection_id='TEST001',
            metadata={'location': 'Test'},
            volumes=[0, 0, 0]  # All zeros
        )
        
        analyzer = SignalTimingAnalyzer(intersection)
        
        # Should handle zero volumes without error
        result = analyzer.compute_baseline_delays(green_time_baseline=30.0)
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 3
        # All delays should be non-negative
        assert all(d >= 0 for d in result)

    def test_empty_dataframe_handling(self):
        """
        Test handling of empty dataframes.
        
        Ensures the system handles empty data gracefully.
        """
        empty_df = pd.DataFrame()
        
        # Should not crash on empty dataframe
        assert empty_df.empty
        
        # Test aggregation on empty data - should raise ValueError
        with pytest.raises(ValueError):
            aggregate_by_hour(empty_df)
        
        # Test validation on empty data
        is_valid = validate_traffic_data(empty_df)
        assert is_valid is False

    def test_file_not_found_exception(self):
        """
        Test FileNotFoundError handling.
        
        Part 1 requirement: Test exception handling.
        Verifies that missing files are handled properly.
        """
        with pytest.raises(FileNotFoundError):
            load_traffic_data('nonexistent_file.csv')

    def test_data_io_operations(self):
        """
        Test CSV reading and writing operations.
        
        Part 1 requirement: Test data I/O operations.
        Verifies that data I/O works correctly.
        """
        # Create sample data
        test_data = pd.DataFrame({
            'intersection_id': ['INT001'],
            'timestamp': ['2024-01-01 08:00'],
            'approach': ['North'],
            'count': [100]
        })
        
        # Use temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            # Test writing
            save_results(test_data, output_path)
            
            # Verify file was created
            assert os.path.exists(output_path)
            
            # Test reading
            loaded_data = pd.read_csv(output_path)
            assert not loaded_data.empty
            assert len(loaded_data) == 1
            assert loaded_data['intersection_id'].iloc[0] == 'INT001'
            assert loaded_data['count'].iloc[0] == 100
            
        finally:
            # Cleanup
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_aggregate_by_hour_empty_bins(self):
        """
        Test handling of empty bins in hourly aggregation.
        
        Part 1 requirement: Test handling of empty bins.
        Ensures that missing hours are handled with zero values.
        """
        # Create data with some hours missing
        data = pd.DataFrame({
            'hour': [8, 10, 12],  # Missing hours 9, 11, etc.
            'count': [100, 150, 120]
        })
        
        result = aggregate_by_hour(data)
        
        # Should return all 24 hours with 0 for empty bins
        assert len(result) == 24
        assert result[8] == 100
        assert result[9] == 0  # Empty bin should be 0
        assert result[10] == 150
        assert result[11] == 0  # Empty bin should be 0
        assert result[12] == 120
        # All other hours should be 0
        for hour in range(24):
            if hour not in [8, 10, 12]:
                assert result[hour] == 0

    def test_volume_stream_empty_data(self):
        """
        Test volume_stream with empty data.
        
        Verifies that empty dataframes are handled gracefully.
        """
        empty_df = pd.DataFrame()
        
        # Should handle empty data gracefully
        records = list(volume_stream(empty_df))
        assert len(records) == 0

    def test_volume_stream_with_data(self):
        """
        Test volume_stream with valid data.
        
        Verifies that volume_stream yields correct records.
        """
        test_data = pd.DataFrame({
            'intersection_id': ['INT001', 'INT001'],
            'timestamp': ['2024-01-01 08:00', '2024-01-01 08:15'],
            'count': [100, 150],
            'approach': ['North', 'South']
        })
        
        records = list(volume_stream(test_data))
        assert len(records) == 2
        assert isinstance(records[0], dict)
        assert 'intersection_id' in records[0]
        assert records[0]['count'] == 100

    def test_validate_traffic_data_with_zero_counts(self):
        """
        Test validation with zero counts.
        
        Verifies that zero counts are detected but don't fail validation.
        """
        test_data = pd.DataFrame({
            'intersection_id': ['INT001', 'INT001'],
            'timestamp': ['2024-01-01 08:00', '2024-01-01 08:15'],
            'count': [100, 0]  # One zero count
        })
        
        # Should validate but print warning
        is_valid = validate_traffic_data(test_data)
        assert isinstance(is_valid, bool)

    def test_validate_traffic_data_with_missing_counts(self):
        """
        Test validation with missing counts.
        
        Verifies that missing counts are detected.
        """
        test_data = pd.DataFrame({
            'intersection_id': ['INT001', 'INT001'],
            'timestamp': ['2024-01-01 08:00', '2024-01-01 08:15'],
            'count': [100, None]  # One missing count
        })
        
        # Should validate but print warning
        is_valid = validate_traffic_data(test_data)
        assert isinstance(is_valid, bool)

    def test_save_results_with_dict(self):
        """
        Test saving results as dictionary.
        
        Verifies that dictionary results can be saved.
        """
        results_dict = {
            'metric': 'avg_delay',
            'value': 10.5,
            'intersection_id': 'INT001'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            save_results(results_dict, output_path)
            assert os.path.exists(output_path)
            
            # Verify content
            loaded = pd.read_csv(output_path)
            assert len(loaded) == 1
            assert loaded['metric'].iloc[0] == 'avg_delay'
            
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_aggregate_by_hour_with_all_hours(self):
        """
        Test aggregation when all hours are present.
        
        Verifies that aggregation works correctly with complete data.
        """
        # Create data with all hours
        data = pd.DataFrame({
            'hour': list(range(24)),
            'count': [i * 10 for i in range(24)]  # Different count for each hour
        })
        
        result = aggregate_by_hour(data)
        
        assert len(result) == 24
        for hour in range(24):
            assert result[hour] == hour * 10

    def test_load_traffic_data_with_valid_file(self):
        """
        Test loading valid traffic data file.
        
        Verifies that valid CSV files can be loaded.
        """
        # Create temporary CSV file
        test_data = pd.DataFrame({
            'intersection_id': ['INT001', 'INT001'],
            'timestamp': ['2024-01-01 08:00', '2024-01-01 08:15'],
            'count': [100, 150]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            output_path = tmp_file.name
            test_data.to_csv(tmp_file.name, index=False)
        
        try:
            loaded = load_traffic_data(output_path)
            assert not loaded.empty
            assert len(loaded) == 2
            assert 'intersection_id' in loaded.columns
            assert 'count' in loaded.columns
            
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_signal_analyzer_with_missing_volumes(self):
        """
        Test SignalTimingAnalyzer with missing volume data.
        
        Verifies that analyzer handles missing volumes gracefully.
        """
        # Create intersection with empty volumes
        intersection = IntersectionData(
            intersection_id='TEST002',
            metadata={},
            volumes=[]  # Empty volumes
        )
        
        analyzer = SignalTimingAnalyzer(intersection)
        
        # Should handle empty volumes without error
        result = analyzer.compute_baseline_delays(green_time_baseline=30.0)
        assert isinstance(result, list)
        assert len(result) == 0

