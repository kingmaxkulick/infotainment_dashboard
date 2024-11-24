"""
Application-wide constants and configuration for the infotainment dashboard
"""

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "vehicle_data": "/vehicle_data",
    "vehicle_state": "/vehicle_state",
    "fault_status": "/fault_status",
    "metrics": {
        "powertrain": "/metrics/powertrain",
        "tires": "/metrics/tires"
    }
}

# Update intervals (in milliseconds)
UPDATE_INTERVALS = {
    "vehicle_state": 100,    # 100ms for state updates
    "fault_status": 100,     # 100ms for fault monitoring
    "metrics": 200          # 200ms for general metrics
}

# Colors
COLORS = {
    "BACKGROUND": "rgba(255, 255, 255, 0.85)",
    "BORDER": "rgba(0, 0, 0, 0.1)",
    "TEXT": "#333333",
    "PARK": "#2196F3",      # Blue
    "DRIVE": "#4CAF50",     # Green
    "REVERSE": "#FFC107",   # Amber
    "CHARGE": "#9C27B0",    # Purple
    "WARNING": "#FF9800",   # Orange
    "CRITICAL": "#F44336",  # Red
    "NORMAL": "#4CAF50",    # Green
    "FAULT_ACTIVE": "#F44336",    # Red
    "FAULT_CLEARED": "#4CAF50"    # Green
}

# Widget Styles
STYLES = {
    "main_window": """
        QMainWindow {
            background-color: white;
        }
    """,
    
    "vehicle_widget": """
        QWidget {
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
    """,
    
    "state_widget": """
        QWidget {
            background-color: transparent;
        }
        
        QLabel#state_label {
            font-size: 24px;
            font-weight: bold;
        }
        
        QLabel#substate_label {
            font-size: 16px;
            color: #666;
        }
    """,
    
    "fault_widget": """
        QWidget {
            background-color: transparent;
        }
        
        QLabel#fault_header {
            font-size: 16px;
            font-weight: bold;
        }
        
        QLabel#fault_active {
            font-size: 14px;
            margin: 5px;
        }
    """
}

# Connection Status
CONNECTION_STATUS = {
    "CONNECTED": "✓ Connected",
    "DISCONNECTED": "⚠ Connection Lost",
    "CONNECTING": "⟳ Connecting...",
    "ERROR": "✕ Connection Error"
}

# Vehicle States
VEHICLE_STATES = {
    "PARK": "PARK",
    "DRIVE": "DRIVE",
    "REVERSE": "REVERSE",
    "NEUTRAL": "NEUTRAL",
    "CHARGE": "CHARGE"
}

# Vehicle Substates
VEHICLE_SUBSTATES = {
    "INITIALIZING": "INITIALIZING",
    "READY": "READY",
    "ACTIVE": "ACTIVE",
    "COMPLETE": "COMPLETE"
}

# Status Flags
STATUS_FLAGS = {
    "DOOR_OPEN": "Door Open",
    "CHARGING_CONNECTED": "Charging Connected",
    "MOTOR_READY": "Motor Ready",
    "BATTERY_OK": "Battery OK",
    "SYSTEMS_CHECK_PASS": "Systems Check Pass"
}

# Fault Sources
FAULT_SOURCES = {
    "BATTERY": "Battery",
    "MOTOR": "Motor",
    "CHARGING": "Charging System",
    "TIRE": "Tire",
    "POWER": "Power System"
}

# Fault Types
FAULT_TYPES = {
    "TEMP_HIGH": "Temperature High",
    "TEMP_LOW": "Temperature Low",
    "PRESSURE_HIGH": "Pressure High",
    "PRESSURE_LOW": "Pressure Low",
    "CURRENT_HIGH": "Current High",
    "VOLTAGE_HIGH": "Voltage High",
    "VOLTAGE_LOW": "Voltage Low",
    "COMM_ERROR": "Communication Error"
}

# Metric Units
METRIC_UNITS = {
    "charge_percent": "%",
    "charging_rate": "kW",
    "battery_temp": "°C",
    "motor_temp": "°C",
    "inverter_temp": "°C",
    "tire_temp": "°C",
    "tire_pressure": "PSI",
    "power_output": "kW",
    "brake_temp": "°C"
}

# Warning Thresholds
WARNING_THRESHOLDS = {
    "battery_temp": {"warning": 40, "critical": 50},
    "motor_temp": {"warning": 70, "critical": 85},
    "tire_temp": {"warning": 70, "critical": 80},
    "tire_pressure": {"warning": 35, "critical": 38},
    "charge_percent": {"warning": 20, "critical": 10}
}