"""
main.py
This script fetches proteins and genes data, exports it to a CSV file, and logs all actions to a log file.
"""

from dependencies import get_db_connection, pd, yaml, logging, io


# Configure logging
logging.basicConfig(
    filename="audit_log.log",  # Log file name
    level=logging.INFO,        # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
)

def load_queries():
    """
    Loads SQL queries from the queries.yaml file.
    Returns:
        dict: A dictionary containing the SQL queries.
    """
    with open("queries.yaml", "r") as file:
        return yaml.safe_load(file)

def log_audit(action, status, message=None):
    """
    Logs audit details into a log file.
    Args:
        action (str): The action performed (e.g., 'fetch_proteins_and_genes', 'save_to_csv').
        status (str): The status of the action ('success' or 'failure').
        message (str): Additional details about the action or error.
    """
    log_message = f"Action: {action}, Status: {status}, Message: {message or 'No additional details'}"
    if status.lower() == "success":
        logging.info(log_message)  # Log success as INFO
    else:
        logging.error(log_message)  # Log failure as ERROR

def fetch_proteins_and_genes():
    """
    Fetches the protein and gene data from the database.
    Returns:
        DataFrame: A pandas DataFrame containing the fetched data.
    """
    # Load queries
    queries = load_queries()

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Create the bb_protein_gene_list table if it doesn't exist
        cursor.execute(queries["create_table_query"])
        connection.commit()

        # Fetch protein and gene data
        cursor.execute(queries["protein_gene_list_query"])
        rows = cursor.fetchall()

        # Convert to DataFrame
        gene_df = pd.DataFrame(rows, columns=["Entity Type", "UNIPROT Id", "Title"])
        
        # Convert the DataFrame to a CSV format in memory
        csv_buffer = io.StringIO()
        gene_df.to_csv(csv_buffer, index=False, header=False)  # Exclude index and header
        csv_buffer.seek(0)

        # Use the COPY command to bulk insert
        with connection.cursor() as cursor:
            cursor.copy_expert(
                """
                COPY bb_schema.bb_protein_gene_list (entity_type, uniprot_id, title)
                FROM STDIN WITH CSV
                """,
                csv_buffer,
            )
        connection.commit()

        # Log success
        log_audit("fetch_proteins_and_genes", "success", "Protein and gene data fetched successfully.")
        return gene_df

    except Exception as error:
        # Log failure
        log_audit("fetch_proteins_and_genes", "failure", str(error))
        print("Error while fetching data:", error)
        return None

    finally:
        # Close the database connection
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()

def save_to_csv(gene_df, filename="protein_gene_list.csv"):
    """
    Saves the DataFrame to a CSV file.
    Args:
        gene_df (DataFrame): The DataFrame to save.
        filename (str): The name of the CSV file.
    """
    try:
        gene_df.to_csv(filename, index=False)
        print(f"Data successfully written to {filename}")

        # Log success
        log_audit("save_to_csv", "success", f"Data successfully written to {filename}")
    except Exception as error:
        # Log failure
        log_audit("save_to_csv", "failure", str(error))
        print(f"Error while saving to CSV: {error}")

if __name__ == "__main__":
    # Fetch protein and gene data
    proteins_and_genes_df = fetch_proteins_and_genes()

    if proteins_and_genes_df is not None:
        # Save to CSV
        save_to_csv(proteins_and_genes_df)