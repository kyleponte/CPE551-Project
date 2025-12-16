"""
SignalTimingAnalyzer module for analyzing traffic signal timing efficiency.

This module provides the SignalTimingAnalyzer class that uses composition
with IntersectionData to analyze signal timing plans and compute delay metrics.
"""


class SignalTimingAnalyzer:
    """
    Analyzes traffic signal timing efficiency.
    
    Uses composition to work with IntersectionData instances.
    Computes delay metrics and compares timing plans.
    
    Attributes:
        intersection_data (IntersectionData): The intersection data to analyze
        baseline_delays (list): List of baseline delay values (mutable)
        alternative_delays (list): List of alternative timing delay values (mutable)
        efficiency_metrics (dict): Dictionary of efficiency metrics (mutable)
    """
    
    def __init__(self, intersection_data):
        """
        Initialize analyzer with intersection data.
        
        Args:
            intersection_data (IntersectionData): Intersection data instance
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {"location": "Main St"}, [100, 150])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> analyzer.intersection_data.intersection_id
            'INT001'
        """
        # Composition relationship - store IntersectionData instance
        # This demonstrates composition: SignalTimingAnalyzer "has-a" IntersectionData
        self.intersection_data = intersection_data
        
        # Mutable list for baseline delay values (Part 2 requirement)
        self.baseline_delays = []
        
        # Mutable list for alternative timing delay values
        self.alternative_delays = []
        
        # Mutable dict for efficiency metrics (Part 2 requirement)
        self.efficiency_metrics = {}
    
    def compute_baseline_delays(self, green_time_baseline):
        """
        Compute delays for baseline timing plan.
        
        Calculates delay for each volume reading based on the baseline
        green time. Delay is computed using volume-to-capacity ratio.
        
        Args:
            green_time_baseline (float): Baseline green time in seconds
        
        Returns:
            list: List of delay values for each volume reading
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {}, [100, 150, 120])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> delays = analyzer.compute_baseline_delays(30.0)
            >>> len(delays)
            3
        """
        # Clear previous baseline delays
        self.baseline_delays = []
        
        # Saturation flow rate: typical value is 1800 vehicles/hour per lane
        # This represents maximum vehicles that can pass through per hour
        saturation_flow_rate = 1800.0  # vehicles per hour per lane
        
        # Convert green time to hours for capacity calculation
        green_time_hours = green_time_baseline / 3600.0
        
        # Calculate capacity: vehicles that can pass during green time
        # Capacity = green_time * saturation_flow_rate
        capacity = green_time_hours * saturation_flow_rate
        
        # Compute delay for each volume reading
        for volume in self.intersection_data.volumes:
            if capacity > 0:
                # Delay calculation: when volume exceeds capacity, delay occurs
                # Delay = (volume - capacity) / capacity * 100 (as percentage)
                # If volume <= capacity, minimal delay
                if volume > capacity:
                    delay = ((volume - capacity) / capacity) * 100.0
                else:
                    # Minimal delay even when volume is below capacity
                    # This accounts for queuing and signal cycle effects
                    delay = (volume / capacity) * 10.0
            else:
                # Handle edge case: zero capacity
                delay = 0.0
            
            # Store delay in mutable list
            self.baseline_delays.append(delay)
        
        return self.baseline_delays
    
    def compute_alternative_delays(self, green_time_alt):
        """
        Compute delays for alternative timing plan.
        
        Calculates delay for each volume reading based on the alternative
        green time. Uses same methodology as baseline but with different timing.
        
        Args:
            green_time_alt (float): Alternative green time in seconds
        
        Returns:
            list: List of delay values for each volume reading
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {}, [100, 150, 120])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> delays = analyzer.compute_alternative_delays(45.0)
            >>> len(delays)
            3
        """
        # Clear previous alternative delays
        self.alternative_delays = []
        
        # Saturation flow rate: typical value is 1800 vehicles/hour per lane
        saturation_flow_rate = 1800.0  # vehicles per hour per lane
        
        # Convert green time to hours for capacity calculation
        green_time_hours = green_time_alt / 3600.0
        
        # Calculate capacity for alternative timing plan
        capacity = green_time_hours * saturation_flow_rate
        
        # Compute delay for each volume reading
        for volume in self.intersection_data.volumes:
            if capacity > 0:
                # Same delay calculation as baseline
                if volume > capacity:
                    delay = ((volume - capacity) / capacity) * 100.0
                else:
                    delay = (volume / capacity) * 10.0
            else:
                delay = 0.0
            
            # Store delay in mutable list
            self.alternative_delays.append(delay)
        
        return self.alternative_delays
    
    def compare_plans(self):
        """
        Compare baseline vs alternative timing plans.
        
        Computes comparison metrics including average delay reduction,
        throughput change, and overall efficiency improvement.
        
        Returns:
            dict: Comparison metrics containing:
                - avg_delay_reduction (float): Average delay reduction percentage
                - throughput_change (float): Change in throughput percentage
                - baseline_avg_delay (float): Average baseline delay
                - alternative_avg_delay (float): Average alternative delay
                - improvement_percentage (float): Overall improvement percentage
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {}, [100, 150, 120])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> analyzer.compute_baseline_delays(30.0)
            >>> analyzer.compute_alternative_delays(45.0)
            >>> comparison = analyzer.compare_plans()
            >>> 'avg_delay_reduction' in comparison
            True
        """
        # Ensure both delay lists have been computed
        if not self.baseline_delays or not self.alternative_delays:
            # Return empty metrics if delays haven't been computed
            self.efficiency_metrics = {
                'avg_delay_reduction': 0.0,
                'throughput_change': 0.0,
                'baseline_avg_delay': 0.0,
                'alternative_avg_delay': 0.0,
                'improvement_percentage': 0.0
            }
            return self.efficiency_metrics
        
        # Calculate average delays
        baseline_avg = sum(self.baseline_delays) / len(self.baseline_delays)
        alternative_avg = sum(self.alternative_delays) / len(self.alternative_delays)
        
        # Calculate delay reduction (positive means improvement)
        avg_delay_reduction = baseline_avg - alternative_avg
        
        # Calculate throughput change
        # Throughput is inversely related to delay
        # Higher delay means lower effective throughput
        if baseline_avg > 0:
            throughput_change = ((baseline_avg - alternative_avg) / baseline_avg) * 100.0
        else:
            throughput_change = 0.0
        
        # Calculate overall improvement percentage
        if baseline_avg > 0:
            improvement_percentage = (avg_delay_reduction / baseline_avg) * 100.0
        else:
            improvement_percentage = 0.0
        
        # Store metrics in mutable dictionary (Part 2 requirement)
        self.efficiency_metrics = {
            'avg_delay_reduction': avg_delay_reduction,
            'throughput_change': throughput_change,
            'baseline_avg_delay': baseline_avg,
            'alternative_avg_delay': alternative_avg,
            'improvement_percentage': improvement_percentage
        }
        
        return self.efficiency_metrics

