"""
Simple test to verify SignalTimingAnalyzer class instantiation and composition.

This test verifies that:
1. The class instantiates correctly
2. The composition relationship with IntersectionData works
3. Basic methods can be called without errors
"""

from intersection_data import IntersectionData
from signal_analyzer import SignalTimingAnalyzer


def test_analyzer_instantiation():
    """Test that SignalTimingAnalyzer can be instantiated."""
    # Create IntersectionData instance
    intersection = IntersectionData(
        intersection_id="TEST001",
        metadata={"location": "Test Street"},
        volumes=[100, 150, 120]
    )
    
    # Create SignalTimingAnalyzer using composition
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Verify instantiation
    assert analyzer is not None
    assert isinstance(analyzer, SignalTimingAnalyzer)


def test_composition_relationship():
    """Test that composition relationship with IntersectionData works."""
    # Create IntersectionData instance
    intersection = IntersectionData(
        intersection_id="TEST002",
        metadata={"location": "Main Street"},
        volumes=[200, 180, 160]
    )
    
    # Create analyzer with composition
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Verify composition: analyzer "has-a" intersection_data
    assert analyzer.intersection_data is not None
    assert isinstance(analyzer.intersection_data, IntersectionData)
    assert analyzer.intersection_data.intersection_id == "TEST002"
    assert analyzer.intersection_data.metadata["location"] == "Main Street"
    
    # Verify mutable attributes are initialized
    assert isinstance(analyzer.baseline_delays, list)
    assert isinstance(analyzer.alternative_delays, list)
    assert isinstance(analyzer.efficiency_metrics, dict)
    assert len(analyzer.baseline_delays) == 0
    assert len(analyzer.alternative_delays) == 0
    assert len(analyzer.efficiency_metrics) == 0


def test_compute_baseline_delays():
    """Test that compute_baseline_delays method works."""
    intersection = IntersectionData(
        intersection_id="TEST003",
        metadata={},
        volumes=[100, 150, 120]
    )
    
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Compute baseline delays
    delays = analyzer.compute_baseline_delays(green_time_baseline=30.0)
    
    # Verify delays were computed
    assert delays is not None
    assert isinstance(delays, list)
    assert len(delays) == 3  # Should match number of volumes
    assert all(isinstance(d, (int, float)) for d in delays)
    
    # Verify delays are stored in mutable list
    assert analyzer.baseline_delays == delays


def test_compute_alternative_delays():
    """Test that compute_alternative_delays method works."""
    intersection = IntersectionData(
        intersection_id="TEST004",
        metadata={},
        volumes=[100, 150, 120]
    )
    
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Compute alternative delays
    delays = analyzer.compute_alternative_delays(green_time_alt=45.0)
    
    # Verify delays were computed
    assert delays is not None
    assert isinstance(delays, list)
    assert len(delays) == 3
    assert all(isinstance(d, (int, float)) for d in delays)
    
    # Verify delays are stored in mutable list
    assert analyzer.alternative_delays == delays


def test_compare_plans():
    """Test that compare_plans method works."""
    intersection = IntersectionData(
        intersection_id="TEST005",
        metadata={},
        volumes=[100, 150, 120]
    )
    
    analyzer = SignalTimingAnalyzer(intersection)
    
    # Compute both delay sets
    analyzer.compute_baseline_delays(green_time_baseline=30.0)
    analyzer.compute_alternative_delays(green_time_alt=45.0)
    
    # Compare plans
    comparison = analyzer.compare_plans()
    
    # Verify comparison results
    assert comparison is not None
    assert isinstance(comparison, dict)
    assert 'avg_delay_reduction' in comparison
    assert 'throughput_change' in comparison
    assert 'baseline_avg_delay' in comparison
    assert 'alternative_avg_delay' in comparison
    assert 'improvement_percentage' in comparison
    
    # Verify metrics are stored in mutable dict
    assert analyzer.efficiency_metrics == comparison


if __name__ == "__main__":
    """Run tests if executed directly."""
    print("Running SignalTimingAnalyzer tests...")
    
    test_analyzer_instantiation()
    print("[PASS] Analyzer instantiation test passed")
    
    test_composition_relationship()
    print("[PASS] Composition relationship test passed")
    
    test_compute_baseline_delays()
    print("[PASS] Compute baseline delays test passed")
    
    test_compute_alternative_delays()
    print("[PASS] Compute alternative delays test passed")
    
    test_compare_plans()
    print("[PASS] Compare plans test passed")
    
    print("\nAll tests passed!")

