"""
Controllers package for CT Scanner Pre-installation System
Handles business logic and application flow
"""

# Import available controllers
from .authentification import Authentication
from .project import Project as ProjectController
from .scanner_analysis import ScannerAnalysis
from .scanner_comparison import ScannerComparison
from .client import Client
from .engineer import Engineer
from .report import ReportGenerator

__all__ = [
    'Authentication',
    'ScannerAnalysis',
    'ScannerComparison',
    'ProjectController',
    'Client',
    'Engineer',
    'ReportGenerator',
    'get_controller_status',
    'get_scanner_models',
    'get_neuViz_models',
    'is_neuViz_scanner',
    'get_scanner_specs',
    'calculate_room_area',
    'calculate_installation_cost',
    'calculate_conformity_score',
    'initialize_controllers'
]

# Version info
__version__ = '2.0.0'
__author__ = 'CT Scanner Pre-installation System Team'
__description__ = 'Business logic controllers for professional biomedical CT scanner analysis'

# Controller configurations
CONTROLLER_CONFIG = {
    'session_timeout': 3600,  # 1 hour
    'max_analysis_time': 300,  # 5 minutes
    'default_page_size': 20,
    'max_file_size': 10485760,  # 10MB
    'allowed_file_types': ['.pdf', '.jpg', '.jpeg', '.png', '.dwg'],
    'analysis_cache_duration': 1800  # 30 minutes
}

# Scanner specifications from Untitled22.ipynb
SCANNER_SPECIFICATIONS = {
    "NeuViz ACE (16-slice)": {
        "min_length": 6.5, "min_width": 4.2, "min_height": 2.43,
        "min_door_width": 1.2, "min_door_height": 2.0,
        "required_power": "triphasé 380V", "min_floor_capacity": 1000,
        "needs_shielding": True, "weight": 1120, "dimensions": "1.886 x 1.012 x 1.795",
        "kvp_max": 140, "tube_current_max": 800, "slice_thickness_min": 0.8,
        "gantry_opening": 70, "patient_table_capacity": 220, "heat_dissipation": 3500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air forcé + eau"
    },
    "NeuViz ACE SP (32-slice)": {
        "min_length": 6.5, "min_width": 4.2, "min_height": 2.43,
        "min_door_width": 1.2, "min_door_height": 2.0,
        "required_power": "triphasé 380V", "min_floor_capacity": 1000,
        "needs_shielding": True, "weight": 1120, "dimensions": "1.886 x 1.012 x 1.795",
        "kvp_max": 140, "tube_current_max": 900, "slice_thickness_min": 0.6,
        "gantry_opening": 70, "patient_table_capacity": 220, "heat_dissipation": 3500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air forcé + eau"
    },
    "GE Optima CT660": {
        "min_length": 6.0, "min_width": 3.8, "min_height": 2.6,
        "min_door_width": 1.3, "min_door_height": 2.1,
        "required_power": "triphasé 400V", "min_floor_capacity": 850,
        "needs_shielding": True, "weight": 2450, "dimensions": "2.1 x 0.9 x 1.7",
        "kvp_max": 140, "tube_current_max": 800, "slice_thickness_min": 0.625,
        "gantry_opening": 70, "patient_table_capacity": 220, "heat_dissipation": 8500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "eau fermée"
    },
    "Siemens SOMATOM X.cite": {
        "min_length": 5.8, "min_width": 3.6, "min_height": 2.5,
        "min_door_width": 1.25, "min_door_height": 2.0,
        "required_power": "triphasé 400V", "min_floor_capacity": 780,
        "needs_shielding": True, "weight": 2300, "dimensions": "2.0 x 1.0 x 1.8",
        "kvp_max": 130, "tube_current_max": 700, "slice_thickness_min": 0.6,
        "gantry_opening": 78, "patient_table_capacity": 227, "heat_dissipation": 7800,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air forcé"
    },
    "Philips Incisive CT": {
        "min_length": 5.5, "min_width": 3.4, "min_height": 2.4,
        "min_door_width": 1.2, "min_door_height": 1.95,
        "required_power": "triphasé 380V", "min_floor_capacity": 720,
        "needs_shielding": True, "weight": 2100, "dimensions": "1.9 x 0.9 x 1.7",
        "kvp_max": 120, "tube_current_max": 650, "slice_thickness_min": 0.5,
        "gantry_opening": 75, "patient_table_capacity": 200, "heat_dissipation": 6500,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "air + eau"
    },
    "Canon Aquilion Prime SP": {
        "min_length": 5.7, "min_width": 3.5, "min_height": 2.5,
        "min_door_width": 1.25, "min_door_height": 2.0,
        "required_power": "triphasé 400V", "min_floor_capacity": 760,
        "needs_shielding": True, "weight": 2250, "dimensions": "2.0 x 0.9 x 1.7",
        "kvp_max": 135, "tube_current_max": 750, "slice_thickness_min": 0.5,
        "gantry_opening": 72, "patient_table_capacity": 210, "heat_dissipation": 7200,
        "radiation_protection_level": "IEC 60601-2-44", "cooling_system": "eau fermée"
    }
}

# Biomedical constraints from Untitled22.ipynb
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
        "temperature_tolerance": 4.1,  # ±°C/h (NeuViz specific)
        "humidity_range": [30, 60],  # %RH (NeuViz: 30-60% vs standard 40-60%)
        "filtration_efficiency": 95,  # %
        "emergency_ventilation": True,
        "co2_monitoring": True,
        "differential_pressure_monitoring": True,
        "atmospheric_pressure_range": [70, 106],  # kPa
    },
    "electrical_safety": {
        "isolation_transformer_required": True,
        "neuViz_power_rating": "50kVA",  # Specific NeuViz requirement
        "neuViz_frequency": "50/60Hz ±1Hz",
        "neuViz_power_factor": 0.84,  # Minimum
        "neuViz_voltage_tolerance": 10,  # ±%
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
        "grounding_resistance_independent": 4,  # Ω
        "grounding_resistance_common": 1,  # Ω
        "ground_cable_section": 16,  # mm² minimum
    }
}

# Installation costs from Untitled22.ipynb
INSTALLATION_COSTS = {
    "base_installation": 25000,
    "neusoft_service_engineer": 8000,  # Mandatory for NeuViz
    "shielding_cost_per_m2": 380,
    "hvac_specialized": 20000,
    "electrical_upgrade": {
        "triphasé 380V": 10000,
        "triphasé 400V": 12000,
        "triphasé 480V": 18000
    },
    "isolation_transformer_50kva": 15000,
    "radiation_safety_equipment": 15000,
    "floor_reinforcement_per_m2": 220,
    "seismic_isolation": 12000,
    "fire_suppression_system": 25000,
    "infection_control_upgrades": 8000,
    "workflow_optimization": 15000,
    "certification_and_testing": 10000,
    "transport_handling_neuViz": 6000,
    "grounding_system_enhanced": 5000,
}

def get_scanner_models():
    """Get list of supported scanner models"""
    return list(SCANNER_SPECIFICATIONS.keys())

def get_neuViz_models():
    """Get list of NeuViz scanner models"""
    return [model for model in SCANNER_SPECIFICATIONS.keys() if 'NeuViz' in model]

def is_neuViz_scanner(model):
    """Check if scanner model is NeuViz"""
    return 'NeuViz' in (model or '')

def get_scanner_specs(model):
    """Get specifications for a specific scanner model"""
    return SCANNER_SPECIFICATIONS.get(model, {})

def calculate_room_area(length, width):
    """Calculate room area in square meters"""
    try:
        return float(length) * float(width)
    except (ValueError, TypeError):
        return 0.0

def calculate_installation_cost(room_data, scanner_specs):
    """Calculate estimated installation cost"""
    try:
        length = float(room_data.get('length', 0))
        width = float(room_data.get('width', 0))
        area = calculate_room_area(length, width)
        
        cost = INSTALLATION_COSTS["base_installation"]
        
        # NeuViz specific costs
        scanner_model = room_data.get('scanner_model', '')
        if is_neuViz_scanner(scanner_model):
            cost += INSTALLATION_COSTS["neusoft_service_engineer"]
            cost += INSTALLATION_COSTS["transport_handling_neuViz"]
            cost += INSTALLATION_COSTS["grounding_system_enhanced"]
        
        # Shielding costs
        if (room_data.get('primary_shielding', 'aucun') == 'aucun' and 
            scanner_specs.get('needs_shielding', False)):
            cost += area * INSTALLATION_COSTS["shielding_cost_per_m2"]
        
        # Electrical upgrade costs
        if room_data.get('electricity') != scanner_specs.get('required_power'):
            required_power = scanner_specs.get('required_power', '')
            cost += INSTALLATION_COSTS["electrical_upgrade"].get(required_power, 15000)
        
        # HVAC costs
        if room_data.get('air_conditioning', 'aucune') in ['aucune', 'split system']:
            cost += INSTALLATION_COSTS["hvac_specialized"]
        
        # Floor reinforcement
        weight_capacity = float(room_data.get('weight_capacity', 0))
        min_capacity = scanner_specs.get('min_floor_capacity', 0)
        if weight_capacity < min_capacity:
            cost += area * INSTALLATION_COSTS["floor_reinforcement_per_m2"]
        
        # Fire suppression
        if room_data.get('fire_suppression', 'aucun') == 'aucun':
            cost += INSTALLATION_COSTS["fire_suppression_system"]
        
        # Standard additions
        cost += INSTALLATION_COSTS["seismic_isolation"]
        cost += INSTALLATION_COSTS["certification_and_testing"]
        
        return cost
        
    except Exception as e:
        print(f"Error calculating installation cost: {e}")
        return INSTALLATION_COSTS["base_installation"]

def calculate_conformity_score(room_data, scanner_specs):
    """Calculate conformity score and identify issues"""
    try:
        score = 100
        penalties = []
        
        # Dimensional compliance
        length = float(room_data.get('length', 0))
        width = float(room_data.get('width', 0))
        height = float(room_data.get('height', 0))
        door_width = float(room_data.get('door_width', 0))
        door_height = float(room_data.get('door_height', 0))
        weight_capacity = float(room_data.get('weight_capacity', 0))
        
        min_length = scanner_specs.get('min_length', 0)
        min_width = scanner_specs.get('min_width', 0)
        min_height = scanner_specs.get('min_height', 0)
        min_door_width = scanner_specs.get('min_door_width', 0)
        min_door_height = scanner_specs.get('min_door_height', 0)
        min_floor_capacity = scanner_specs.get('min_floor_capacity', 0)
        required_power = scanner_specs.get('required_power', '')
        
        if length < min_length:
            score -= 15
            penalties.append("Longueur insuffisante")
        
        if width < min_width:
            score -= 15
            penalties.append("Largeur insuffisante")
        
        if height < min_height:
            score -= 10
            penalties.append("Hauteur insuffisante")
        
        if door_width < min_door_width:
            score -= 10
            penalties.append("Porte trop étroite")
        
        if door_height < min_door_height:
            score -= 5
            penalties.append("Porte trop basse")
        
        if weight_capacity < min_floor_capacity:
            score -= 20
            penalties.append("Capacité portante insuffisante")
        
        # Electrical compliance
        if room_data.get('electricity') != required_power:
            score -= 15
            penalties.append("Alimentation non conforme")
        
        # NeuViz specific checks
        scanner_model = room_data.get('scanner_model', '')
        if is_neuViz_scanner(scanner_model):
            if room_data.get('isolation_transformer', 'non') == 'non':
                score -= 25
                penalties.append("Transformateur isolement obligatoire NeuViz")
            
            if height < 2.43:
                score -= 10
                penalties.append("Hauteur sous-optimale pour NeuViz")
        
        # Radiation safety
        if scanner_specs.get('needs_shielding', False):
            if room_data.get('primary_shielding', 'aucun') == 'aucun':
                score -= 30
                penalties.append("Blindage primaire manquant")
            
            if room_data.get('secondary_shielding', 'aucun') == 'aucun':
                score -= 15
                penalties.append("Blindage secondaire manquant")
        
        # Environmental controls
        if room_data.get('air_conditioning', 'aucune') == 'aucune':
            score -= 10
            penalties.append("Climatisation manquante")
        
        # Fire safety
        if room_data.get('fire_detection', 'aucun') == 'aucun':
            score -= 15
            penalties.append("Détection incendie manquante")
        
        if room_data.get('fire_suppression', 'aucun') == 'aucun':
            score -= 10
            penalties.append("Extinction incendie manquante")
        
        return max(0, min(100, score)), penalties
        
    except Exception as e:
        print(f"Error calculating conformity score: {e}")
        return 0, ["Erreur de calcul"]

def initialize_controllers():
    """Initialize all controllers with proper configuration"""
    try:
        print("🔧 Initializing CT Scanner System Controllers...")
        
        # Import and initialize each controller
        auth = Authentication()
        scanner_analysis = ScannerAnalysis()
        project_controller = ProjectController()
        client_controller = Client()
        engineer_controller = Engineer()
        report_generator = ReportGenerator()
        
        print("✅ All controllers initialized successfully")
        
        return {
            'auth': auth,
            'scanner_analysis': scanner_analysis,
            'project_controller': project_controller,
            'client_controller': client_controller,
            'engineer_controller': engineer_controller,
            'report_generator': report_generator
        }
        
    except Exception as e:
        print(f"❌ Error initializing controllers: {e}")
        return {}

def get_controller_status():
    """Get status of all controllers"""
    return {
        'scanner_models_loaded': len(SCANNER_SPECIFICATIONS),
        'neuViz_models_available': len(get_neuViz_models()),
        'biomedical_constraints_loaded': len(BIOMEDICAL_CONSTRAINTS),
        'installation_costs_loaded': len(INSTALLATION_COSTS),
        'system_version': __version__,
        'config_status': 'ready'
    }