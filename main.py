import os
import re
import shutil
import sqlite3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv


def read_query_from_file(file_path):
    """Reads the SQL query from a file."""
    with open(file_path, "r") as file:
        return file.read()


def execute_query(db_path, query):
    """Executes the SQL query and returns the results in a pandas DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def create_output_folder():
    """Creates a folder with the current timestamp and returns its path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join(os.getcwd(), timestamp)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder


def normalize_filename(title):
    """Normalizes the file name by reducing extra spaces, replacing spaces and hyphens with underscores,
    removing consecutive underscores, and converting to lowercase."""
    # Strip leading/trailing spaces, reduce multiple spaces to single
    normalized_title = "_".join(title.strip().split())
    # Replace hyphens with underscores
    normalized_title = normalized_title.replace("-", "_")
    # Remove any characters that are not alphanumeric, underscores, or periods
    normalized_title = "".join(
        c if c.isalnum() or c in ("_", ".") else "_" for c in normalized_title
    )
    # Replace multiple consecutive underscores with a single underscore
    normalized_title = re.sub(r"__+", "_", normalized_title)
    # Convert to lowercase
    return normalized_title.lower()


def copy_files(df, output_folder):
    """Copies files to the output folder, renaming them based on the title column."""
    idx = 1
    for _, row in df.iterrows():
        full_path = row["full_path"]
        partial_path = row["partial_path"]
        title = row["title"]

        # Sanitize the title to create a valid filename
        new_filename = normalize_filename(title) + ".pdf"
        new_file_path = os.path.join(output_folder, new_filename)

        # Copy the file
        try:
            print(f"Moving: {idx}/{df.shape[0]}")
            print(f"> root path : {partial_path}")
            print(f"> copy path : {new_file_path}")
            shutil.copy(full_path, new_file_path)
            print("Moved successfully!")
            print()
        except Exception as e:
            print(f"Error copying file {partial_path}: {e}")
        finally:
            idx += 1


def main():
    # Paths and variables
    load_dotenv()
    db_path = os.getenv("ZOTERO_SQLITE_PATH")
    query_file_path = "query.sql"

    # Read the query from the file
    query = read_query_from_file(query_file_path)

    # Execute the query and get the results in a pandas DataFrame
    df = execute_query(db_path, query)

    # Create an output folder
    output_folder = create_output_folder()

    # Copy files based on the DataFrame results
    copy_files(df, output_folder)


if __name__ == "__main__":
    main()
