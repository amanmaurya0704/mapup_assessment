import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    
    distance_dict = {}
    
    for index, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']
        distance = row['distance']
        
        # Add distances to the dictionary for both directions (A to B and B to A)
        distance_dict[(id_start, id_end)] = distance
        distance_dict[(id_end, id_start)] = distance

    # Get unique IDs and create a DataFrame with zeros
    unique_ids = sorted(set(df['id_start']).union(set(df['id_end'])))
    distance_matrix = pd.DataFrame(0, columns=unique_ids, index=unique_ids)

    # Populate the distance matrix with cumulative distances along known routes
    for id_row in unique_ids:
        for id_col in unique_ids:
            if (id_row, id_col) in distance_dict:
                distance_matrix.loc[id_row, id_col] = distance_dict[(id_row, id_col)]

    # Set diagonal values to 0
    distance_matrix.values[[range(len(unique_ids))]*2] = 0
    

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    distance_df = unroll_distance_matrix(df)
    
    distance_df.reset_index(inplace=True)

    # Melt the DataFrame to get distance values
    melted_df = distance_df.melt(id_vars='index', var_name='id_end', value_name='distance')

    # Rename columns
    melted_df.columns = ['id_start', 'id_end', 'distance']

    # Filter rows where id_start is not equal to id_end
    unrolled_distance_df = melted_df[melted_df['id_start'] != melted_df['id_end']]

    # Reset index of the resulting DataFrame
    unrolled_distance_df.reset_index(drop=True, inplace=True)

    return unrolled_distance_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    unrolled_distance_df = unroll_distance_matrix(df)
    
    # Calculate average distance for the reference value
    reference_avg_distance = unrolled_distance_df[unrolled_distance_df['id_start'] == reference_value]['distance'].mean()

    # Calculate the threshold range
    lower_threshold = reference_avg_distance - (reference_avg_distance * 0.10)
    upper_threshold = reference_avg_distance + (reference_avg_distance * 0.10)

    # Filter IDs within the threshold range
    filtered_ids = unrolled_distance_df[
        (unrolled_distance_df['distance'] >= lower_threshold) &
        (unrolled_distance_df['distance'] <= upper_threshold)
    ]['id_start'].unique()

    # Sort the filtered IDs
    filtered_ids.sort()


    return list(filtered_ids)


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type
    for vehicle, rate in rate_coefficients.items():
        df[vehicle] = df['distance'] * rate

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    import datetime
    unrolled_distance_df = unroll_distance_matrix(df)
    
    # Function to calculate toll rates based on time intervals
    def calculate_toll_based_on_time(timestamp):
        weekday = timestamp.weekday()
        time_val = timestamp.time()

        if weekday < 5:  # Weekdays (Monday - Friday)
            if time_val < datetime.time(10, 0, 0):
                return 0.8
            elif time_val < datetime.time(18, 0, 0):
                return 1.2
            else:
                return 0.8
        else:  # Weekends (Saturday and Sunday)
            return 0.7

    # Generate timestamps covering a full 24-hour period and all 7 days of the week
    start_datetime = datetime.combine(datetime.today(), datetime.time(0, 0, 0))
    end_datetime = start_datetime + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
    timestamps = pd.date_range(start=start_datetime, end=end_datetime, freq='15T')

    # Create a list to store time-based toll rates data
    time_based_toll_data = []

    # Iterate through unique (id_start, id_end) pairs
    for idx, row in unrolled_distance_df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        
        for i in range(len(timestamps) - 1):
            start_ts, end_ts = timestamps[i], timestamps[i + 1]
            start_day, end_day = start_ts.strftime('%A'), end_ts.strftime('%A')
            start_time, end_time = start_ts.time(), end_ts.time()

            # Calculate toll rates based on time intervals
            discount_factor = calculate_toll_based_on_time(start_ts)

            # Append calculated data to the list
            time_based_toll_data.append({
                'id_start': id_start,
                'id_end': id_end,
                'start_day': start_day,
                'start_time': start_time,
                'end_day': end_day,
                'end_time': end_time,
                'moto': distance * 0.8 * discount_factor,
                'car': distance * 1.2 * discount_factor,
                'rv': distance * 1.5 * discount_factor,
                'bus': distance * 2.2 * discount_factor,
                'truck': distance * 3.6 * discount_factor
            })

    # Create DataFrame from the list of dictionaries
    time_based_toll_df = pd.DataFrame(time_based_toll_data)

    return time_based_toll_df
