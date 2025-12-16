import random
import time


class Sensor:
    """
    Class simulating an IoT energy consumption sensor
    located in the LARI research laboratory.
    """

    def __init__(self, sensor_id, location="Laboratoire de recherche LARI"):
        """
        Initialize the sensor.

        :param sensor_id: Unique identifier (e.g., 'Sensor-LARI-01').
        :param location: Location of the sensor, default is LARI lab.
        """
        self.sensor_id = sensor_id
        self.location = location

    def generate_measure(self):
        """
        Simulate an energy consumption measurement in kWh.
        Generates a random value with a probability of a peak (anomaly).

        :return: A dictionary containing sensor data.
        """
        # 1. Random behavior simulation
        # 40% probability of having an anomaly (high consumption peak)
        # to see the result more frequently during tests.
        peak_probability = 40 / 100

        if random.random() < peak_probability:
            # Consumption peak simulation
            consumption = random.uniform(8.0, 15.0)
        else:
            # Standard laboratory consumption
            consumption = random.uniform(0.8, 2.5)

        # 2. Constructing the structured data to return
        data = {
            "sensor_id": self.sensor_id,
            "location": self.location,
            "value_kwh": round(consumption, 2),
            "timestamp": time.time()
        }

        return data


# --- Test block (to verify this file independently) ---
if __name__ == "__main__":
    # Creating a specific sensor for LARI
    lari_sensor = Sensor("Sensor-LARI-01")

    print(f"--- Starting sensor at {lari_sensor.location} ---")
    while True:
        measure = lari_sensor.generate_measure()
        print(f"Measure : {measure}")
        time.sleep(0.5)
