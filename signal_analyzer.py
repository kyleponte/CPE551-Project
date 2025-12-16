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
        
        Raises:
            TypeError: If intersection_data is not an IntersectionData instance
            ValueError: If intersection_data is None
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {"location": "Main St"}, [100, 150])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> analyzer.intersection_data.intersection_id
            'INT001'
        """
        try:
            # Validate input
            if intersection_data is None:
                raise ValueError("intersection_data cannot be None")
            
            # Check if it's the correct type (basic validation)
            # Note: We use hasattr to check for expected attributes rather than isinstance
            # to be more flexible, but we could also use: from intersection_data import IntersectionData
            if not hasattr(intersection_data, 'volumes'):
                raise TypeError("intersection_data must have 'volumes' attribute")
            
            # Composition relationship - store IntersectionData instance
            # This demonstrates composition: SignalTimingAnalyzer "has-a" IntersectionData
            self.intersection_data = intersection_data
            
            # Mutable list for baseline delay values (Part 2 requirement)
            self.baseline_delays = []
            
            # Mutable list for alternative timing delay values
            self.alternative_delays = []
            
            # Mutable dict for efficiency metrics (Part 2 requirement)
            self.efficiency_metrics = {}
            
        except (TypeError, ValueError) as e:
            print(f"Error initializing SignalTimingAnalyzer: {e}")
            raise
    
    def compute_baseline_delays(self, green_time_baseline):
        """
        Compute delays for baseline timing plan.
        
        Calculates delay for each volume reading based on the baseline
        green time. Delay is computed using volume-to-capacity ratio.
        Includes exception handling for divide-by-zero and invalid inputs.
        
        Args:
            green_time_baseline (float): Baseline green time in seconds
        
        Returns:
            list: List of delay values for each volume reading, or empty list on error
        
        Raises:
            ValueError: If green_time_baseline is zero or negative
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {}, [100, 150, 120])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> delays = analyzer.compute_baseline_delays(30.0)
            >>> len(delays)
            3
        """
        try:
            # Validate green time input
            if green_time_baseline <= 0:
                raise ValueError("Green time cannot be zero or negative")
            
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
            
            # Handle empty volumes list
            if not self.intersection_data.volumes:
                print("Warning: No volume data available, returning empty delay list")
                return self.baseline_delays
            
            # Compute delay for each volume reading
            for volume in self.intersection_data.volumes:
                try:
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
                        # Handle edge case: zero capacity (shouldn't happen with valid green_time)
                        delay = 0.0
                    
                    # Store delay in mutable list
                    self.baseline_delays.append(delay)
                    
                except ZeroDivisionError:
                    # Handle divide-by-zero exception (Part 1 requirement)
                    print("Warning: Division by zero in delay calculation, using 0.0")
                    self.baseline_delays.append(0.0)
                except (TypeError, ValueError) as e:
                    # Handle invalid volume data
                    print(f"Warning: Invalid volume data: {e}, using 0.0")
                    self.baseline_delays.append(0.0)
            
            return self.baseline_delays
            
        except ValueError as e:
            # Handle invalid green_time input
            print(f"Error: {e}")
            return []
        except Exception as e:
            # Handle unexpected errors
            print(f"Unexpected error in compute_baseline_delays: {e}")
            return []
    
    def compute_alternative_delays(self, green_time_alt):
        """
        Compute delays for alternative timing plan.
        
        Calculates delay for each volume reading based on the alternative
        green time. Uses same methodology as baseline but with different timing.
        Includes exception handling for divide-by-zero and invalid inputs.
        
        Args:
            green_time_alt (float): Alternative green time in seconds
        
        Returns:
            list: List of delay values for each volume reading, or empty list on error
        
        Raises:
            ValueError: If green_time_alt is zero or negative
        
        Example:
            >>> from intersection_data import IntersectionData
            >>> data = IntersectionData("INT001", {}, [100, 150, 120])
            >>> analyzer = SignalTimingAnalyzer(data)
            >>> delays = analyzer.compute_alternative_delays(45.0)
            >>> len(delays)
            3
        """
        try:
            # Validate green time input
            if green_time_alt <= 0:
                raise ValueError("Green time cannot be zero or negative")
            
            # Clear previous alternative delays
            self.alternative_delays = []
            
            # Saturation flow rate: typical value is 1800 vehicles/hour per lane
            saturation_flow_rate = 1800.0  # vehicles per hour per lane
            
            # Convert green time to hours for capacity calculation
            green_time_hours = green_time_alt / 3600.0
            
            # Calculate capacity for alternative timing plan
            capacity = green_time_hours * saturation_flow_rate
            
            # Handle empty volumes list
            if not self.intersection_data.volumes:
                print("Warning: No volume data available, returning empty delay list")
                return self.alternative_delays
            
            # Compute delay for each volume reading
            for volume in self.intersection_data.volumes:
                try:
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
                    
                except ZeroDivisionError:
                    # Handle divide-by-zero exception (Part 1 requirement)
                    print("Warning: Division by zero in delay calculation, using 0.0")
                    self.alternative_delays.append(0.0)
                except (TypeError, ValueError) as e:
                    # Handle invalid volume data
                    print(f"Warning: Invalid volume data: {e}, using 0.0")
                    self.alternative_delays.append(0.0)
            
            return self.alternative_delays
            
        except ValueError as e:
            # Handle invalid green_time input
            print(f"Error: {e}")
            return []
        except Exception as e:
            # Handle unexpected errors
            print(f"Unexpected error in compute_alternative_delays: {e}")
            return []
    
    def compare_plans(self):
        """
        Compare baseline vs alternative timing plans.
        
        Computes comparison metrics including average delay reduction,
        throughput change, and overall efficiency improvement.
        Includes exception handling for empty data and divide-by-zero.
        
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
        try:
            # Ensure both delay lists have been computed
            if not self.baseline_delays or not self.alternative_delays:
                # Return empty metrics if delays haven't been computed
                print("Warning: Delays not computed yet, returning zero metrics")
                self.efficiency_metrics = {
                    'avg_delay_reduction': 0.0,
                    'throughput_change': 0.0,
                    'baseline_avg_delay': 0.0,
                    'alternative_avg_delay': 0.0,
                    'improvement_percentage': 0.0
                }
                return self.efficiency_metrics
            
            # Handle empty delay lists
            if len(self.baseline_delays) == 0 or len(self.alternative_delays) == 0:
                raise ValueError("Cannot compare plans with empty delay lists")
            
            # Calculate average delays with exception handling
            try:
                baseline_avg = sum(self.baseline_delays) / len(self.baseline_delays)
            except ZeroDivisionError:
                print("Warning: Division by zero when calculating baseline average, using 0.0")
                baseline_avg = 0.0
            
            try:
                alternative_avg = sum(self.alternative_delays) / len(self.alternative_delays)
            except ZeroDivisionError:
                print("Warning: Division by zero when calculating alternative average, using 0.0")
                alternative_avg = 0.0
            
            # Calculate delay reduction (positive means improvement)
            avg_delay_reduction = baseline_avg - alternative_avg
            
            # Calculate throughput change
            # Throughput is inversely related to delay
            # Higher delay means lower effective throughput
            try:
                if baseline_avg > 0:
                    throughput_change = ((baseline_avg - alternative_avg) / baseline_avg) * 100.0
                else:
                    throughput_change = 0.0
            except ZeroDivisionError:
                print("Warning: Division by zero in throughput calculation, using 0.0")
                throughput_change = 0.0
            
            # Calculate overall improvement percentage
            try:
                if baseline_avg > 0:
                    improvement_percentage = (avg_delay_reduction / baseline_avg) * 100.0
                else:
                    improvement_percentage = 0.0
            except ZeroDivisionError:
                print("Warning: Division by zero in improvement calculation, using 0.0")
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
            
        except ValueError as e:
            print(f"Error in compare_plans: {e}")
            # Return zero metrics on error
            self.efficiency_metrics = {
                'avg_delay_reduction': 0.0,
                'throughput_change': 0.0,
                'baseline_avg_delay': 0.0,
                'alternative_avg_delay': 0.0,
                'improvement_percentage': 0.0
            }
            return self.efficiency_metrics
        except Exception as e:
            print(f"Unexpected error in compare_plans: {e}")
            # Return zero metrics on unexpected error
            self.efficiency_metrics = {
                'avg_delay_reduction': 0.0,
                'throughput_change': 0.0,
                'baseline_avg_delay': 0.0,
                'alternative_avg_delay': 0.0,
                'improvement_percentage': 0.0
            }
            return self.efficiency_metrics

