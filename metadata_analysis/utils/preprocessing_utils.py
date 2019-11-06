import pandas as pd


def split_datetime(data, column_name: str = "Time", format: str = "%d.%m.%y, %H:%M"):
    """Separates date and time from a given datetime column

    Splits date and time from the given column by the given format and writes it so separate columns `Date` and `Time`

    Args:
        data: dataframe containing the datetime column
        column_name: datetime column name
        format: datetime format

    Returns:
        the input dataframe with the added columns `Date` and `Time`
    """
    data["Datetime"] = pd.to_datetime(data[column_name], format=format)
    data["Date"] = [t.date() for t in data["Datetime"]]
    data["Time"] = [t.time() for t in data["Datetime"]]
    return data
