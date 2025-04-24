# import time
# import main  # Import your script

# start = time.time()

# # Run the main function
# proteins_and_genes_df = main.fetch_proteins_and_genes()
# if proteins_and_genes_df is not None:
#     main.save_to_csv(proteins_and_genes_df)

# end = time.time()

# print(f"Total execution time: {end - start:.4f} seconds")

import pytest
from main import fetch_proteins_and_genes, save_to_csv

def test_fetch_proteins_and_genes(benchmark):
    proteins_and_genes_df = benchmark(fetch_proteins_and_genes)
    assert proteins_and_genes_df is not None

def test_save_to_csv(benchmark):
    import pandas as pd
    df = pd.DataFrame({"Entity Type": ["Protein"], "UNIPROT Id": ["P12345"], "Title": ["Title"]})
    benchmark(lambda: save_to_csv(df))
