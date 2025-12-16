class Analyzer:
    """
    Class responsible for analyzing energy consumption data
    to detect anomalies (e.g., unexpected peaks).
    """

    def __init__(self, alert_threshold=10.0):
        """
        Initialize the analyzer.

        :param alert_threshold: The value (in kWh) above which a consumption
                                is considered an anomaly. Default is 10.0.
        """
        self.alert_threshold = alert_threshold

    def check_anomaly(self, data):
        """
        Analyze a single data point to check for anomalies.

        :param data: Dictionary containing sensor data.
                     Must include 'value_kwh'.
        :return: Tuple (is_anomaly, message)
                 - is_anomaly: Boolean (True if value exceeds threshold).
                 - message: A descriptive string.
        """
        # We safely retrieve the value; if missing, we assume 0.0
        value = data.get("value_kwh", 0.0)

        if value > self.alert_threshold:
            # Anomaly detected
            # We split the line to avoid E501 (Line too long)
            message = (
                f"ALERT: High consumption detected! "
                f"({value} kWh > {self.alert_threshold} kWh)"
            )
            return True, message

        # No anomaly
        return False, "Consumption is normal."


# --- Unit Test Block (to verify this file independently) ---
if __name__ == "__main__":
    print("--- Testing Analyzer ---")

    # 1. Setup the analyzer with a threshold of 5.0 kWh
    analyzer = Analyzer(alert_threshold=5.0)

    # 2. Test with a normal value (2.5 kWh)
    normal_data = {"value_kwh": 2.5}
    is_anomaly, msg = analyzer.check_anomaly(normal_data)
    print(f"Input: 2.5 kWh -> Anomaly: {is_anomaly} | Message: {msg}")

    # 3. Test with a high value (8.0 kWh)
    high_data = {"value_kwh": 8.0}
    is_anomaly, msg = analyzer.check_anomaly(high_data)
    print(f"Input: 8.0 kWh -> Anomaly: {is_anomaly} | Message: {msg}")
