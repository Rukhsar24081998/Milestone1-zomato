"""Raw Hugging Face column names → canonical :class:`~milestone_zomato.models.restaurant.Restaurant` fields.

Source dataset: ``ManikaSaini/zomato-restaurant-recommendation`` (``default`` config, ``train`` split).

+-------------------------------+------------------+------------------------------------------+
| HF column                     | Canonical field  | Notes                                    |
+===============================+==================+==========================================+
| ``url``                       | ``id``           | SHA-256 hex of URL (stable id).          |
+-------------------------------+------------------+------------------------------------------+
| ``name``                      | ``name``         | Required; rows without name dropped.     |
+-------------------------------+------------------+------------------------------------------+
| ``address``                   | (``city``)       | Last comma-separated segment → city.     |
+-------------------------------+------------------+------------------------------------------+
| ``location``                  | ``area``         | Locality / neighborhood label.         |
+-------------------------------+------------------+------------------------------------------+
| ``cuisines``                  | ``cuisines``     | Split on comma; strip tokens.            |
+-------------------------------+------------------+------------------------------------------+
| ``approx_cost(for two people)`` | ``cost_bucket`` | Parse INR int; map to low/med/high.    |
+-------------------------------+------------------+------------------------------------------+
| ``rate``                      | ``rating``       | Parse ``4.1/5`` style → float.           |
+-------------------------------+------------------+------------------------------------------+
"""

# Exact keys as returned by ``datasets`` for this repo.
COL_URL = "url"
COL_NAME = "name"
COL_ADDRESS = "address"
COL_LOCATION = "location"
COL_CUISINES = "cuisines"
COL_RATE = "rate"
COL_COST = "approx_cost(for two people)"
COL_LISTED_CITY = "listed_in(city)"

# INR "approx cost for two" → bucket (tunable).
COST_LOW_MAX_EXCL = 500
COST_MED_MAX_EXCL = 1200
