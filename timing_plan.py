"""
TimingPlan module for representing traffic signal timing plans.

This module provides the TimingPlan class that supports operator overloading
to combine multiple timing plans using the + operator.
"""


class TimingPlan:
    """
    Represents a traffic signal timing plan.
    
    Supports operator overloading to combine multiple timing plans.
    Uses mutable objects (dict, list) for timing data storage.
    
    Attributes:
        green_times (dict): Green times for each approach (mutable)
        cycle_length (float): Total cycle length in seconds
        phase_durations (list): Duration of each phase (mutable)
    """
    
    def __init__(self, green_times, cycle_length):
        """
        Initialize timing plan.
        
        Args:
            green_times (dict): Dictionary mapping approach to green time in seconds
            cycle_length (float): Total cycle length in seconds
        
        Example:
            >>> plan = TimingPlan(
            ...     green_times={'North': 30.0, 'South': 25.0, 'East': 20.0},
            ...     cycle_length=120.0
            ... )
            >>> plan.cycle_length
            120.0
        """
        # Mutable dict for green times (Part 2 requirement)
        self.green_times = green_times if green_times is not None else {}
        
        # Cycle length in seconds
        self.cycle_length = cycle_length
        
        # Mutable list for phase durations (Part 2 requirement)
        self.phase_durations = []
    
    def __add__(self, other):
        """
        Combine two timing plans using + operator.
        
        Part 2 requirement: Operator overloading implementation.
        Averages green times and cycle lengths from both plans.
        
        Args:
            other (TimingPlan): Another timing plan to combine with
        
        Returns:
            TimingPlan: New combined timing plan with averaged values
        
        Raises:
            TypeError: If other is not a TimingPlan instance
        
        Example:
            >>> plan1 = TimingPlan({'North': 30.0, 'South': 25.0}, 120.0)
            >>> plan2 = TimingPlan({'North': 35.0, 'East': 20.0}, 130.0)
            >>> combined = plan1 + plan2
            >>> combined.green_times['North']
            32.5
            >>> combined.cycle_length
            125.0
        """
        # Verify that other is a TimingPlan instance
        if not isinstance(other, TimingPlan):
            raise TypeError(f"Cannot combine TimingPlan with {type(other).__name__}")
        
        # Get all unique approaches from both plans
        all_approaches = set(list(self.green_times.keys()) + list(other.green_times.keys()))
        
        # Combine green times by averaging values for each approach
        # If an approach exists in only one plan, use its value (not divided by 2)
        combined_greens = {}
        for approach in all_approaches:
            self_time = self.green_times.get(approach, 0)
            other_time = other.green_times.get(approach, 0)
            
            # Average if both plans have the approach, otherwise use the existing value
            if approach in self.green_times and approach in other.green_times:
                combined_greens[approach] = (self_time + other_time) / 2.0
            else:
                # If only one plan has this approach, use that value
                combined_greens[approach] = self_time if self_time > 0 else other_time
        
        # Average cycle lengths from both plans
        combined_cycle = (self.cycle_length + other.cycle_length) / 2.0
        
        # Create and return new combined timing plan
        return TimingPlan(combined_greens, combined_cycle)
    
    def __str__(self):
        """
        Return string representation of timing plan.
        
        Part 2 requirement: __str__ method implementation.
        
        Returns:
            str: Formatted string with cycle length and number of approaches
        
        Example:
            >>> plan = TimingPlan({'North': 30.0, 'South': 25.0}, 120.0)
            >>> str(plan)
            'TimingPlan(cycle=120.0s, approaches=2)'
        """
        num_approaches = len(self.green_times)
        return f"TimingPlan(cycle={self.cycle_length}s, approaches={num_approaches})"
    
    def __repr__(self):
        """
        Return detailed string representation for debugging.
        
        Returns:
            str: Detailed representation including green times
        
        Example:
            >>> plan = TimingPlan({'North': 30.0}, 120.0)
            >>> repr(plan)
            "TimingPlan(green_times={'North': 30.0}, cycle_length=120.0)"
        """
        return f"TimingPlan(green_times={self.green_times}, cycle_length={self.cycle_length})"
    
    def add_phase_duration(self, duration):
        """
        Add a phase duration to the timing plan.
        
        Args:
            duration (float): Duration of a phase in seconds
        """
        # Mutable list operation (Part 2 requirement)
        self.phase_durations.append(duration)
    
    def get_total_green_time(self):
        """
        Calculate total green time across all approaches.
        
        Returns:
            float: Sum of all green times
        """
        return sum(self.green_times.values())
    
    def get_approach_count(self):
        """
        Get the number of approaches in this timing plan.
        
        Returns:
            int: Number of approaches
        """
        return len(self.green_times)

