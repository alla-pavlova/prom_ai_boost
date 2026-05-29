import pandas as pd

def read_excel_file(path: str):
    return pd.read_excel(
        path,
        engine="openpyxl"
    )


def save_excel_file(df, path: str):
    df.to_excel(
        path,
        index=False,
        engine="openpyxl"
    )