"""
Data processor module for traffic data I/O operations.

This module provides functions for loading, processing, and saving traffic data
with comprehensive exception handling for data validation and I/O errors.
"""

import pandas as pd
import os


def load_traffic_data(file_path):
    """
    Load traffic data from CSV file.
    
    Handles FileNotFoundError and other I/O exceptions.
    Validates that the loaded data is not empty.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: Loaded traffic data
    
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is empty or invalid
        pd.errors.EmptyDataError: If the CSV file is empty
    
    Example:
        >>> df = load_traffic_data('data/traffic_signal_data.csv')
        >>> len(df) > 0
        True
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Traffic data file not found: {file_path}")
        
        # Attempt to read CSV file
        df = pd.read_csv(file_path)
        
        # Validate that data is not empty
        if df.empty:
            raise ValueError(f"Data file is empty: {file_path}")
        
        return df
        
    except FileNotFoundError as e:
        # Handle file not found exception (Part 1 requirement)
        print(f"Error: File not found - {e}")
        raise
    except pd.errors.EmptyDataError as e:
        # Handle empty CSV file
        print(f"Error: CSV file is empty - {e}")
        raise ValueError(f"CSV file is empty: {file_path}")
    except pd.errors.ParserError as e:
        # Handle CSV parsing errors
        print(f"Error: Failed to parse CSV file - {e}")
        raise ValueError(f"Invalid CSV format in file: {file_path}")
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error loading traffic data: {e}")
        raise


def aggregate_by_hour(data):
    """
    Aggregate data by hour with empty bin handling.
    
    Handles empty data bins and missing hour data gracefully.
    
    Args:
        data (pd.DataFrame): Traffic data with 'hour' and 'volume' columns
    
    Returns:
        dict: Hourly aggregates, with 0 for empty bins
    
    Raises:
        ValueError: If data is empty or missing required columns
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'hour': [8, 9, 10], 'volume': [100, 150, 120]})
        >>> hourly = aggregate_by_hour(df)
        >>> hourly[8]
        100
    """
    try:
        # Validate input data
        if data is None:
            raise ValueError("Data is None, cannot aggregate")
        
        if isinstance(data, pd.DataFrame) and data.empty:
            raise ValueError("Data is empty, cannot aggregate")
        
        # Check for required columns
        if isinstance(data, pd.DataFrame):
            required_columns = ['hour', 'volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Initialize hourly data dictionary
        hourly_data = {}
        
        # Process each hour (0-23)
        for hour in range(24):
            try:
                # Filter data for this hour
                hour_data = data[data['hour'] == hour]
                
                if hour_data.empty:
                    # Handle empty bins (Part 1 requirement)
                    hourly_data[hour] = 0
                else:
                    # Sum volumes for this hour
                    hourly_data[hour] = hour_data['volume'].sum()
                    
            except KeyError:
                # Handle missing 'hour' or 'volume' column
                print(f"Warning: Missing data for hour {hour}, using 0")
                hourly_data[hour] = 0
            except Exception as e:
                # Handle unexpected errors for this hour
                print(f"Warning: Error processing hour {hour}: {e}, using 0")
                hourly_data[hour] = 0
        
        return hourly_data
        
    except ValueError as e:
        print(f"Error in aggregation: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error in aggregation: {e}")
        return {}


def save_results(results, output_path):
    """
    Save analysis results to CSV file.
    
    Handles file I/O errors and validates output data.
    
    Args:
        results (pd.DataFrame or dict): Results to save
        output_path (str): Path to save the results file
    
    Raises:
        ValueError: If results are empty or invalid
        PermissionError: If file cannot be written
        OSError: If directory does not exist
    
    Example:
        >>> import pandas as pd
        >>> results = pd.DataFrame({'metric': ['delay'], 'value': [10.5]})
        >>> save_results(results, 'outputs/results.csv')
    """
    try:
        # Validate results
        if results is None:
            raise ValueError("Results cannot be None")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                raise OSError(f"Cannot create output directory: {e}")
        
        # Convert dict to DataFrame if needed
        if isinstance(results, dict):
            if not results:
                raise ValueError("Results dictionary is empty")
            results = pd.DataFrame([results])
        
        # Validate DataFrame
        if isinstance(results, pd.DataFrame):
            if results.empty:
                raise ValueError("Results DataFrame is empty")
        
        # Save to CSV
        results.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
        
    except ValueError as e:
        print(f"Error saving results: {e}")
        raise
    except PermissionError as e:
        print(f"Error: Permission denied when writing to {output_path}")
        raise
    except OSError as e:
        print(f"Error: OS error when saving results: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error saving results: {e}")
        raise


def volume_stream(data, approach=None):
    """
    Generator function to stream volume data.
    
    Handles empty data and missing columns gracefully.
    
    Args:
        data (pd.DataFrame): Traffic data
        approach (str, optional): Filter by specific approach
    
    Yields:
        dict: Volume data for each record
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'approach': ['North'], 'volume': [100]})
        >>> for record in volume_stream(df):
        ...     print(record)
        {'approach': 'North', 'volume': 100}
    """
    try:
        # Validate input
        if data is None:
            raise ValueError("Data cannot be None")
        
        if isinstance(data, pd.DataFrame) and data.empty:
            print("Warning: Data is empty, no records to stream")
            return
        
        # Filter by approach if specified
        if approach:
            if 'approach' not in data.columns:
                raise ValueError("'approach' column not found in data")
            filtered_data = data[data['approach'] == approach]
        else:
            filtered_data = data
        
        # Stream records
        for index, row in filtered_data.iterrows():
            try:
                yield row.to_dict()
            except Exception as e:
                print(f"Warning: Error processing row {index}: {e}")
                continue
                
    except ValueError as e:
        print(f"Error in volume_stream: {e}")
        return
    except Exception as e:
        print(f"Unexpected error in volume_stream: {e}")
        return


def validate_traffic_data(data):
    """
    Validate traffic data for required fields and data quality.
    
    Checks for missing counts, zero volumes, and invalid data types.
    
    Args:
        data (pd.DataFrame): Traffic data to validate
    
    Returns:
        bool: True if data is valid, False otherwise
    
    Raises:
        ValueError: If data structure is invalid
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'count': [100, 150], 'volume': [100, 150]})
        >>> validate_traffic_data(df)
        True
    """
    try:
        # Validate input
        if data is None:
            raise ValueError("Data cannot be None")
        
        if isinstance(data, pd.DataFrame) and data.empty:
            raise ValueError("Data is empty")
        
        # Check for required columns
        required_columns = ['count', 'volume']
        if isinstance(data, pd.DataFrame):
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                print(f"Warning: Missing columns: {missing_columns}")
                return False
        
        # Check for missing/zero counts (Part 1 requirement)
        if 'count' in data.columns:
            zero_counts = (data['count'] == 0).sum()
            missing_counts = data['count'].isna().sum()
            
            if zero_counts > 0:
                print(f"Warning: Found {zero_counts} zero counts in data")
            if missing_counts > 0:
                print(f"Warning: Found {missing_counts} missing counts in data")
        
        # Check for negative values
        numeric_columns = data.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            negative_values = (data[col] < 0).sum()
            if negative_values > 0:
                print(f"Warning: Found {negative_values} negative values in column '{col}'")
        
        return True
        
    except ValueError as e:
        print(f"Error validating data: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error validating data: {e}")
        return False

