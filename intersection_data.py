"""
IntersectionData module for storing traffic intersection information.

This module provides the IntersectionData class to store and manage
traffic volume data for signalized intersections.
"""


class IntersectionData:
    """
    Stores traffic intersection data including ID, metadata, and volumes.
    
    Uses immutable objects (tuples, strings) for IDs and mutable objects
    (lists, dicts) for working data.
    
    Attributes:
        intersection_id (str): Unique identifier for the intersection (immutable)
        metadata (dict): Dictionary containing intersection metadata (mutable)
        volumes (list): List of traffic volumes over time (mutable)
        timestamps (tuple): Tuple of timestamps (immutable)
    """
    
    def __init__(self, intersection_id, metadata=None, volumes=None):
        """
        Initialize IntersectionData instance.
        
        Args:
            intersection_id (str): Unique intersection identifier
            metadata (dict, optional): Dictionary with intersection metadata.
                Defaults to empty dict.
            volumes (list, optional): List of traffic volumes.
                Defaults to empty list.
        
        Example:
            >>> data = IntersectionData(
            ...     intersection_id="INT001",
            ...     metadata={"location": "Main St & 1st Ave"},
            ...     volumes=[100, 150, 120]
            ... )
        """
        # Immutable: use string for ID
        self.intersection_id = str(intersection_id)
        
        # Mutable: use dict for metadata
        self.metadata = metadata if metadata is not None else {}
        
        # Mutable: use list for volumes
        self.volumes = volumes if volumes is not None else []
        
        # Immutable: use tuple for timestamps (if provided)
        self.timestamps = tuple()
    
    def add_volume(self, volume, timestamp=None):
        """
        Add a volume reading to the intersection data.
        
        Args:
            volume (int): Traffic volume count
            timestamp (str, optional): Timestamp for the reading
        """
        self.volumes.append(volume)  # Mutable list operation
        if timestamp:
            # Convert to tuple (immutable) for timestamps
            self.timestamps = self.timestamps + (timestamp,)
    
    def get_total_volume(self):
        """
        Calculate total volume across all readings.
        
        Returns:
            int: Sum of all volume readings
        """
        return sum(self.volumes)
    
    def get_average_volume(self):
        """
        Calculate average volume.
        
        Returns:
            float: Average volume, or 0.0 if no volumes
        """
        if len(self.volumes) == 0:
            return 0.0
        return sum(self.volumes) / len(self.volumes)
    
    def __str__(self):
        """
        Return readable string representation of intersection data.
        
        Part 2 requirement: __str__ method implementation.
        
        Returns:
            str: Formatted string with ID, location, and average volume info
        
        Example:
            >>> data = IntersectionData("INT001", {"location": "Main St"}, [100, 150])
            >>> print(data)
            Intersection INT001: Location=Main St, Avg Volume=125.0, Total Readings=2
        """
        location = self.metadata.get('location', 'Unknown')
        avg_vol = self.get_average_volume()
        total_readings = len(self.volumes)
        
        return (f"Intersection {self.intersection_id}: "
                f"Location={location}, "
                f"Avg Volume={avg_vol:.1f}, "
                f"Total Readings={total_readings}")

