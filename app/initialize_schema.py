from app.schema import create_schema

def main():
    """Initialize the database schema."""
    try:
        create_schema()
        print("Database schema created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
