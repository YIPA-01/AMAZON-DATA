"""Loaders for the raw datasets in data/raw/."""
import pandas as pd

from amazon_data.paths import RAW_DIR

_CATALOG_CATS = {"product_category": "category"}


def load_catalog() -> pd.DataFrame:
    """Product catalog: one row per SKU (item_id)."""
    return pd.read_csv(RAW_DIR / "catalog.csv", dtype=_CATALOG_CATS)


def load_interactions() -> pd.DataFrame:
    """Model 1 (recommender): one row per user-item interaction event."""
    return pd.read_csv(
        RAW_DIR / "interactions.csv",
        dtype={**_CATALOG_CATS, "interaction_type": "category"},
    )


def load_baskets() -> pd.DataFrame:
    """Model 2 (market basket): one row per item in an order (cart_id)."""
    return pd.read_csv(RAW_DIR / "baskets.csv", dtype=_CATALOG_CATS)


def load_sessions() -> pd.DataFrame:
    """Model 3 (session next-item): one row per step in a browsing session."""
    return pd.read_csv(RAW_DIR / "sessions.csv", dtype=_CATALOG_CATS)


def load_abandonment() -> pd.DataFrame:
    """Model 4 (abandonment propensity): one row per session with engineered features."""
    cats = ["customer_tier", "device_type", "browser", "traffic_source", "user_location_region"]
    return pd.read_csv(RAW_DIR / "abandonment_features.csv", dtype={c: "category" for c in cats})
