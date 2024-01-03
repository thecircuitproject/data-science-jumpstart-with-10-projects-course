import numpy as np
import polars as pl
import pandas as pd


def jitter(df: pd.DataFrame, col: str, amt: int = 0.5) -> pd.DataFrame:
    return df[col] + np.random.random(len(df)) * amt - amt / 2


def jitter_polars(df: pl.DataFrame, col: str, amt: int = 0.5) -> pl.DataFrame:
    return df.select(pl.col(col)).to_series()


def debug(df: pd.DataFrame, extra: str = "") -> pd.DataFrame:
    print(f"{extra} {df.shape=}")
    return df


def limit_n(
    df: pd.DataFrame, col: str, n: int = 20, other: str = "Other"
) -> pl.DataFrame:
    top = df[col].value_counts()

    topn = top.index[:n]
    return df[col].where(df[col].isin(topn), other)
