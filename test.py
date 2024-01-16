import numpy as np
import polars as pl
import duckdb
import plotly.express as px
marques_array = duckdb.sql(
    """Select marque from (
    SELECT COUNT(*) as nb_annonces,
    marque
    FROM 'data/database.parquet'
    GROUP BY marque
    ORDER BY nb_annonces DESC)
    """).pl().head(40)
marques_array = marques_array.to_numpy()
for marque in marques_array:
    print(marque[0])