import time
from sensor import Sensor
from database import DatabaseHandler
from analyzer import Analyzer


def main():
    """
    Main entry point for the LARI Lab Energy Monitoring System.
    Orchestrates the data flow: Sensor -> Analyzer -> Database.
    """
    print("--- ⚡ Starting Energy Monitoring System (LARI Lab) ⚡ ---")

    # 1. Initialize Components
    # ------------------------

    # Create the sensor specifically for the LARI laboratory
    lari_sensor = Sensor(
        sensor_id="Sensor-LARI-01",
        location="LARI Research Lab"
    )

    # Initialize the MongoDB connection
    db = DatabaseHandler(db_name="energy_db", collection_name="measures")

    # Initialize the Analyzer with a threshold of 12.0 kWh
    # (Values above 12.0 are considered abnormal peaks)
    analyzer = Analyzer(alert_threshold=12.0)

    try:
        print(f"[System] Simulation running for: {lari_sensor.location}")

        # 2. Simulation Loop
        # ------------------
        while True:
            # A. Generate Data (Simulate IoT Device)
            data = lari_sensor.generate_measure()

            # B. Analyze Data (Business Logic)
            is_anomaly, message = analyzer.check_anomaly(data)

            # C. Enrich Data before storage
            # We add the analysis result to the document saved in MongoDB
            data['is_anomaly'] = is_anomaly
            data['status_message'] = message

            # D. Store Data (Persistence)
            db.insert_data(data)

            # E. User Interface (Console Logs)
            icon = "🔴" if is_anomaly else "🟢"
            timestamp = time.strftime(
                "%H:%M:%S",
                time.localtime(data['timestamp'])
            )

            print(f"{icon} [{timestamp}] {message}")
            if is_anomaly:
                print(f"    └── ⚠️  Action required at {data['location']}!")

            # Pause for 2 seconds to simulate real-time interval
            time.sleep(2)

    except KeyboardInterrupt:
        # Manual stop (Ctrl+C) by the user
        print("\n[System] 🛑 Simulation stopped by user.")

    except Exception as e:
        # Handle unexpected errors
        print(f"\n[System] ❌ Critical Error: {e}")

    finally:
        # 3. Cleanup
        # ----------
        db.close_connection()
        print("[System] Database connection closed. Goodbye.")


if __name__ == "__main__":
    main()
