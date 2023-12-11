import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = pd.pivot_table(df,values= "car", index="id_1", columns = "id_2",fill_value=0)

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    car_type = []
    for i in df.car:
        if i <= 15:
            car_type.append("low")
        elif i >= 15 and i <= 25:
            car_type.append("medium")
        else:
            car_type.append("high")
    df['car_type'] = car_type
    d=df.car_type.value_counts()

    return dict(d)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    value = 2 * df.bus.mean()
    index = df[df['bus']> value].index.tolist()
    index.sort()

    return index


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck = df[df['truck']>7]
    routes = avg_truck['route'].unique().tolist()
    routes.sort()

    return routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix = matrix.applymap(lambda x:x * 0.75 if x>20 else x*1.25).round(1)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['startTimestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format="%A %H:%M:%S")
    df['endTimestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format="%A %H:%M:%S")
    df['duration'] = df['endTimestamp'] - df['startTimestamp']
    completeness_check = df.groupby(['id', 'id_2']).apply(
        lambda x: (
            x['duration'].sum() >= pd.Timedelta(days=7) and
            x['startTimestamp'].min().time() == pd.Timestamp.min.time() and
            x['endTimestamp'].max().time() == pd.Timestamp.max.time()
            )
        )

    return completeness_check
