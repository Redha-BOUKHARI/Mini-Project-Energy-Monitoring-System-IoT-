from pymongo import MongoClient, errors


class DatabaseHandler:
    """
    Class responsible for handling MongoDB database operations.
    """

    def __init__(
        self,
        # connection_uri="mongodb://localhost:27017/", for local testing
        # CONNECT TO THE DOCKER CONTAINER MONGODB
        connection_uri="mongodb://admin:securepassword@localhost:27018/?authSource=admin",
        db_name="energy_db",
        collection_name="measures"
    ):
        """
        Initialize the connection to MongoDB.

        :param connection_uri: URI string to connect to MongoDB
                               (default: local).
        :param db_name: Name of the database to use.
        :param collection_name: Name of the collection where data will
                                be stored.
        """
        self.collection = None
        self.client = None

        try:
            # Establish connection to the client
            self.client = MongoClient(
                connection_uri,
                serverSelectionTimeoutMS=2000
            )

            # Check server availability
            self.client.server_info()

            # Select database and collection
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"[DB] Successfully connected to database '{db_name}'")

        except errors.ServerSelectionTimeoutError:
            print(
                "[DB] Error: Could not connect to MongoDB. "
                "Is the server running?"
            )
        except Exception as e:
            print(f"[DB] Unexpected error: {e}")

    def insert_data(self, data):
        """
        Insert a single document into the collection.

        :param data: Dictionary containing the sensor data.
        :return: Boolean indicating success or failure.
        """
        if self.collection is not None:
            try:
                result = self.collection.insert_one(data)
                print(f"[DB] Data inserted with ID: {result.inserted_id}")
                return True
            except Exception as e:
                print(f"[DB] Error inserting data: {e}")
                return False
        else:
            print("[DB] Warning: No database connection. Data not saved.")
            return False

    def close_connection(self):
        """
        Close the MongoDB client connection.
        """
        if self.client:
            self.client.close()
            print("[DB] Connection closed.")


# --- Test block ---
if __name__ == "__main__":
    # Test the database connection independently
    db_handler = DatabaseHandler()

    # Dummy data for testing
    test_data = {
        "sensor_id": "Test-Sensor",
        "location": "Test Lab",
        "value_kwh": 10.5,
        "timestamp": 123456789.0
    }

    db_handler.insert_data(test_data)
    db_handler.close_connection()
