# Amazon Synthetic Data

Analysis and modeling on a synthetic Amazon-style e-commerce dataset: a shared product
catalog plus four datasets, each aimed at a different model.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -e .
.venv/bin/jupyter lab
```

The `-e .` installs `src/amazon_data` in editable mode so notebooks can `from amazon_data.io import ...`.

## Layout

```
data/raw/          original CSVs (git-ignored, never edited)
data/processed/    derived tables (git-ignored)
notebooks/         one notebook per analysis/model
src/amazon_data/   shared code: paths.py (project paths), io.py (dataset loaders)
reports/figures/   exported charts
models/            saved model artifacts (git-ignored)
```

## Data dictionary

All item-level files join to the catalog on `item_id` (`SKU_xxxxxx`). `interactions.csv` and
`sessions.csv` already denormalize the catalog columns (`product_name`, `product_category`,
`product_price`, `stars_given`, `review_count`, `product_description`).

| File | Loader | Grain | Rows | Key columns | Intended model |
|---|---|---|---|---|---|
| `catalog.csv` | `load_catalog` | one SKU | 20,500 | `item_id`, `product_category`, `product_price`, `stars_given`, `review_count`, `product_description` | shared reference |
| `interactions.csv` | `load_interactions` | user × item event | 120,000 | `user_id` (`CUST_xxxxx`), `item_id`, `interaction_type`, `interaction_strength` | 1 — recommender |
| `baskets.csv` | `load_baskets` | item in an order | 43,354 (10,000 orders) | `cart_id` (`ORDER_xxxxx`), `item_id` | 2 — market basket |
| `sessions.csv` | `load_sessions` | step in a session | 45,000 (7,977 sessions) | `session_id` (`SESSION_xxxxx`), `sequence_step`, `item_id`, `dwell_time_seconds`, `scroll_depth_pct` | 3 — session next-item |
| `abandonment_features.csv` | `load_abandonment` | one session | 20,000 | `user_id`, `session_id` (`SESS_xxxxxx`) + 30 features | 4 — abandonment propensity |

Notes:

- `interaction_type` values: `page_view`, `product_click`, `add_to_cart`, `add_to_wishlist`, `purchase`.
- Abandonment features cover customer profile (`customer_tier`, `account_age_days`, lifetime value…),
  context (device, browser, traffic source, region, day/hour, weekend/holiday), and session behavior
  (pages/PDP/images/reviews viewed, scroll depth, cart adds/removes, wishlist, cart value, shipping cost,
  `exit_intent_triggered`). Candidate targets: `should_receive_discount` (~14% positive) and
  `did_convert_organically` (~15% positive).
- Session IDs use different formats across files (`SESS_` vs `SESSION_`) — they are **not** joinable.

### Original filenames

| New | Original |
|---|---|
| `catalog.csv` | `amazon_synthetic_data_catalog.csv` |
| `interactions.csv` | `amazon_synthetic_data_model_1_interactions.csv` |
| `baskets.csv` | `amazon_synthetic_data_model_2_baskets (1).csv` |
| `sessions.csv` | `amazon_synthetic_data_model_3_sessions.csv` |
| `abandonment_features.csv` | `amazon_synthetic_data_abandonment_propensity_32_features.csv` |
