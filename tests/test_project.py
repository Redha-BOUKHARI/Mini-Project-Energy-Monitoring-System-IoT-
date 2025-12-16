import pytest
import sys
import os

# 1. Setup path to import modules from 'src'
# We add the parent directory to sys.path so python can find 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sensor import Sensor
from analyzer import Analyzer

# --- Sensor Tests ---

def test_sensor_initialization():
    """
    Test if the sensor is initialized with correct attributes.
    """
    sensor = Sensor(sensor_id="Test-01", location="LARI Lab")
    assert sensor.sensor_id == "Test-01"
    assert sensor.location == "LARI Lab"

def test_sensor_data_structure():
    """
    Test if the generated data contains all required keys.
    """
    sensor = Sensor("Test-02")
    data = sensor.generate_measure()
    
    # Check keys
    assert "sensor_id" in data
    assert "location" in data
    assert "value_kwh" in data
    assert "timestamp" in data
    
    # Check value types
    assert isinstance(data["value_kwh"], float)
    assert data["value_kwh"] > 0

# --- Analyzer Tests ---

def test_analyzer_normal_value():
    """
    Test that a value below the threshold is NOT flagged as an anomaly.
    """
    analyzer = Analyzer(alert_threshold=10.0)
    data = {"value_kwh": 5.0}
    
    is_anomaly, message = analyzer.check_anomaly(data)
    
    assert is_anomaly is False
    assert "normal" in message

def test_analyzer_high_value():
    """
    Test that a value above the threshold IS flagged as an anomaly.
    """
    analyzer = Analyzer(alert_threshold=10.0)
    data = {"value_kwh": 15.0}
    
    is_anomaly, message = analyzer.check_anomaly(data)
    
    assert is_anomaly is True
    assert "ALERT" in message