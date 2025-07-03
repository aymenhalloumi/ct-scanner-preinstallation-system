import os
from datetime import timedelta

class Config:
    """Application configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ct-scanner-preinstallation-2025-secure-key'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=4)
    
    # OpenAI configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # File paths
    DATA_DIR = 'data'
    USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
    PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.csv')
    ANALYSES_FILE = os.path.join(DATA_DIR, 'analyses.csv')
    LOG_FILE = 'ct_scanner_analysis.log'
    
    # Application settings
    APP_NAME = "CT Scanner Preinstallation Verification System"
    APP_VERSION = "2.1"
    COMPANY_NAME = "Advanced Biomedical Engineering Solutions"

# CT Scanner Specifications Database
SCANNER_SPECS = {
    "NeuViz ACE (16-slice)": {
        # From NPS-CT-0651 document
        "min_length": 6.5, "min_width": 4.2, "min_height": 2.43,
        "min_door_width": 1.2, "min_door_height": 2.0,
        "required_power": "triphasé 380V", "min_floor_capacity": 1000,
        "needs_shielding": True, "weight": 1120, "dimensions": "1.886 x 1.012 x 1.795",
        "kvp_max": 140, "tube_current_max": 800, "slice_thickness_min": 0.8,
        "gantry_opening": 70, "patient_table_capacity": 220, "heat_dissipation": 3500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air forcé + eau",
        "manufacturer": "Neusoft Medical Systems", "compliance_doc": "NPS-CT-0651"
    },
    
    "NeuViz ACE SP (32-slice)": {
        # Enhanced version from NPS-CT-0651
        "min_length": 6.5, "min_width": 4.2, "min_height": 2.43,
        "min_door_width": 1.2, "min_door_height": 2.0,
        "required_power": "triphasé 380V", "min_floor_capacity": 1000,
        "needs_shielding": True, "weight": 1120, "dimensions": "1.886 x 1.012 x 1.795",
        "kvp_max": 140, "tube_current_max": 900, "slice_thickness_min": 0.6,
        "gantry_opening": 70, "patient_table_capacity": 220, "heat_dissipation": 3500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air forcé + eau",
        "manufacturer": "Neusoft Medical Systems", "compliance_doc": "NPS-CT-0651"
    },
    
    "GE Optima CT660": {
        "min_length": 6.0, "min_width": 3.8, "min_height": 2.6,
        "min_door_width": 1.3, "min_door_height": 2.1,
        "required_power": "triphasé 400V", "min_floor_capacity": 850,
        "needs_shielding": True, "weight": 2450, "dimensions": "2.1 x 0.9 x 1.7",
        "kvp_max": 140, "tube_current_max": 800, "slice_thickness_min": 0.625,
        "gantry_opening": 70, "patient_table_capacity": 220, "heat_dissipation": 8500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "eau fermée",
        "manufacturer": "GE HealthCare", "compliance_doc": "IEC 60601-2-44"
    },
    
    "Siemens SOMATOM X.cite": {
        "min_length": 5.8, "min_width": 3.6, "min_height": 2.5,
        "min_door_width": 1.25, "min_door_height": 2.0,
        "required_power": "triphasé 400V", "min_floor_capacity": 780,
        "needs_shielding": True, "weight": 2300, "dimensions": "2.0 x 1.0 x 1.8",
        "kvp_max": 130, "tube_current_max": 700, "slice_thickness_min": 0.6,
        "gantry_opening": 78, "patient_table_capacity": 227, "heat_dissipation": 7800,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air forcé",
        "manufacturer": "Siemens Healthineers", "compliance_doc": "IEC 60601-2-44"
    },
    
    "Philips Incisive CT": {
        "min_length": 5.5, "min_width": 3.4, "min_height": 2.4,
        "min_door_width": 1.2, "min_door_height": 1.95,
        "required_power": "triphasé 380V", "min_floor_capacity": 720,
        "needs_shielding": True, "weight": 2100, "dimensions": "1.9 x 0.9 x 1.7",
        "kvp_max": 120, "tube_current_max": 650, "slice_thickness_min": 0.5,
        "gantry_opening": 75, "patient_table_capacity": 200, "heat_dissipation": 6500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air + eau",
        "manufacturer": "Philips Healthcare", "compliance_doc": "IEC 60601-2-44"
    },
    
    "Canon Aquilion Prime SP": {
        "min_length": 5.7, "min_width": 3.5, "min_height": 2.5,
        "min_door_width": 1.25, "min_door_height": 2.0,
        "required_power": "triphasé 400V", "min_floor_capacity": 760,
        "needs_shielding": True, "weight": 2250, "dimensions": "2.0 x 0.9 x 1.7",
        "kvp_max": 135, "tube_current_max": 750, "slice_thickness_min": 0.5,
        "gantry_opening": 72, "patient_table_capacity": 210, "heat_dissipation": 7200,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "eau fermée",
        "manufacturer": "Canon Medical Systems", "compliance_doc": "IEC 60601-2-44"
    },
    
    "GE Revolution EVO": {
        "min_length": 6.2, "min_width": 4.0, "min_height": 2.8,
        "min_door_width": 1.4, "min_door_height": 2.2,
        "required_power": "triphasé 480V", "min_floor_capacity": 920,
        "needs_shielding": True, "weight": 2800, "dimensions": "2.3 x 1.0 x 1.9",
        "kvp_max": 140, "tube_current_max": 900, "slice_thickness_min": 0.625,
        "gantry_opening": 80, "patient_table_capacity": 250, "heat_dissipation": 9500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "eau fermée",
        "manufacturer": "GE HealthCare", "compliance_doc": "IEC 60601-2-44"
    }
}

# Biomedical Engineering Constraints
BIOMEDICAL_CONSTRAINTS = {
    "radiation_safety": {
        "primary_barrier_thickness_pb": 2.5,  # mm plomb (NeuViz requirement higher)
        "secondary_barrier_thickness_pb": 1.5,  # mm plomb
        "control_room_barrier_pb": 2.5,  # mm plomb
        "door_pb_thickness": 2.0,  # mm plomb
        "viewing_window_pb_equiv": 2.0,  # mm équivalent plomb
        "maze_design_required": True,
        "radiation_monitoring_points": 8,
        "max_dose_rate_outside": 2.0,  # µSv/h
        "shielding_overlap_min": 50,  # mm
    },
    "hvac_requirements": {
        "air_changes_per_hour": 15,
        "positive_pressure_pa": 12.5,
        "temperature_tolerance": 4.1,  # ±°C/h (NeuViz specific from document)
        "humidity_range": [30, 60],  # %RH (NeuViz: 30-60% vs standard 40-60%)
        "filtration_efficiency": 95,  # %
        "emergency_ventilation": True,
        "co2_monitoring": True,
        "differential_pressure_monitoring": True,
        "atmospheric_pressure_range": [70, 106],  # kPa (from NPS-CT-0651)
    },
    "electrical_safety": {
        "isolation_transformer_required": True,
        "neuViz_power_rating": "50kVA",  # Specific NeuViz requirement
        "neuViz_frequency": "50/60Hz ±1Hz",  # From document
        "neuViz_power_factor": 0.84,  # Minimum from document
        "neuViz_voltage_tolerance": 10,  # ±% from document
        "neuViz_phase_imbalance": 5,  # % maximum
        "neuViz_internal_resistance": 100,  # mΩ maximum at 380VAC
        "equipotential_bonding": True,
        "rcd_sensitivity_ma": 30,
        "surge_protection_class": "Type II",
        "emergency_stop_accessible": True,
        "backup_power_autonomy_min": 30,  # minutes
        "power_quality_monitoring": True,
        "harmonic_distortion_max": 5,  # %
        "voltage_stability_percent": 3,  # ±%
        "grounding_resistance_independent": 4,  # Ω (from NPS-CT-0651)
        "grounding_resistance_common": 1,  # Ω (from NPS-CT-0651)
        "ground_cable_section": 16,  # mm² minimum
    },
    "structural_requirements": {
        "concrete_thickness_min": 10,  # cm (from NPS-CT-0651)
        "concrete_strength": 1.7e3,  # N/cm² at 28 days (from document)
        "floor_levelness_tolerance": 4,  # mm (from document Figure 6)
        "anchor_bolt_length": 150,  # mm (from document)
        "anchor_bolt_diameter": 12,  # mm
        "anchor_embedment_gantry": 95,  # mm
        "anchor_embedment_table": 108,  # mm
        "anchor_tension": 14.7,  # kN (3300 lbs)
        "anchor_torque": 30,  # Nm (22 ft-lbs)
        "seismic_zone_compliance": True,
        "vibration_isolation_required": True,
        "floor_stability_factor": 2.0,
        "resonance_frequency_avoid": [5, 25],  # Hz
        "structural_engineering_cert": True
    },
    "fire_safety": {
        "detection_system_type": "photoélectrique + ionique",
        "suppression_system": "gaz inerte",  # Water NOT recommended per NPS-CT-0651
        "water_suppression_not_recommended": True,  # Specific from document
        "smoke_exhaust_system": True,
        "emergency_lighting_duration": 90,  # minutes
        "fire_rated_penetrations": True,
        "compartmentalization_ef": 60,  # minutes
    },
    "infection_control": {
        "surface_materials_cleanable": True,
        "antimicrobial_coating": True,
        "hand_hygiene_stations": 2,
        "waste_management_system": True,
        "uv_disinfection_capability": True,
        "air_filtration_hepa": True
    },
    "patient_safety": {
        "emergency_communication": True,
        "patient_monitoring_visual": True,
        "intercom_system": True,
        "emergency_access_door": True,
        "patient_positioning_aids": True,
        "contrast_injection_safety": True,
        "pregnancy_screening_protocol": True
    },
    "workflow_optimization": {
        "patient_flow_separation": True,
        "staff_changing_room": True,
        "equipment_storage_m2": 8,
        "report_viewing_station": True,
        "contrast_preparation_area": True,
        "waiting_area_capacity": 6  # patients
    },
    "neuViz_transport_requirements": {  # New section from NPS-CT-0651
        "neusoft_engineer_required": True,  # Mandatory per document
        "wooden_crates_with_pallets": True,
        "forklift_requirements": {
            "fork_width": 184,  # mm
            "fork_thickness": 57,  # mm max
            "fork_length": 1524,  # mm min
            "fork_spread": 610,  # mm center to center
            "capacity_min": 2000  # kg
        },
        "transport_inclination_max": 5,  # degrees
        "crane_capacity_min": 2000,  # kg
    }
}

# Installation Cost Database
INSTALLATION_COSTS = {
    "base_installation": 25000,
    "neusoft_service_engineer": 8000,  # Mandatory for NeuViz per document
    "shielding_cost_per_m2": 380,  # Higher for 2.5mm Pb requirement
    "hvac_specialized": 20000,  # Enhanced for NeuViz temperature stability
    "electrical_upgrade": {
        "triphasé 380V": 10000,  # NeuViz standard
        "triphasé 400V": 12000,
        "triphasé 480V": 18000
    },
    "isolation_transformer_50kva": 15000,  # NeuViz 50kVA requirement
    "radiation_safety_equipment": 15000,
    "floor_reinforcement_per_m2": 220,
    "seismic_isolation": 12000,
    "fire_suppression_system": 25000,
    "infection_control_upgrades": 8000,
    "workflow_optimization": 15000,
    "certification_and_testing": 10000,
    "transport_handling_neuViz": 6000,  # Special NeuViz transport with engineer
    "grounding_system_enhanced": 5000,  # Enhanced grounding per NPS-CT-0651
    "project_management": 8000,
    "documentation_and_training": 5000,
    "contingency_factor": 0.10  # 10% contingency
}

# User Role Definitions
USER_ROLES = {
    'client': {
        'permissions': ['view_own_projects', 'create_project', 'request_analysis'],
        'dashboard': 'client_dashboard.html'
    },
    'engineer': {
        'permissions': ['view_assigned_projects', 'perform_analysis', 'generate_reports', 'review_submissions'],
        'dashboard': 'engineer_dashboard.html'
    },
    'admin': {
        'permissions': ['view_all_projects', 'manage_users', 'system_settings', 'global_reports'],
        'dashboard': 'admin_dashboard.html'
    }
}

# Project Status Options
PROJECT_STATUS = {
    'DRAFT': 'Draft - In Preparation',
    'SUBMITTED': 'Submitted for Review',
    'IN_ANALYSIS': 'Under Analysis',
    'COMPLETED': 'Analysis Completed',
    'APPROVED': 'Approved for Installation',
    'REJECTED': 'Requires Modifications',
    'ON_HOLD': 'On Hold'
}

# Analysis Priority Levels
ANALYSIS_PRIORITY = {
    'LOW': 'Low Priority',
    'MEDIUM': 'Medium Priority', 
    'HIGH': 'High Priority',
    'URGENT': 'Urgent - Critical Timeline'
}

# Report Templates
REPORT_TEMPLATES = {
    'BASIC': 'Basic Compliance Report',
    'DETAILED': 'Detailed Engineering Report',
    'EXECUTIVE': 'Executive Summary',
    'NEUVIZ': 'NeuViz Specific Report (NPS-CT-0651)'
}