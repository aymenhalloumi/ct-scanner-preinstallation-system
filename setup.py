#!/usr/bin/env python3
"""
Setup script for CT Scanner Pre-installation System
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        'controllers',
        'models', 
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'data',
        'logs',
        'backups'
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def create_init_files():
    """Create __init__.py files"""
    init_files = [
        'controllers/__init__.py',
        'models/__init__.py'
    ]
    
    print("\n📄 Creating __init__.py files...")
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
            print(f"✅ Created: {init_file}")

def create_env_template():
    """Create .env template file"""
    env_template = """# Flask Configuration
FLASK_SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# OpenAI Configuration  
OPENAI_API_KEY=your-openai-api-key-here

# Application Configuration
APP_NAME=CT Scanner Pre-installation System
APP_VERSION=2.0.0

# Data Configuration
DATA_DIR=data
USERS_CSV=data/users.csv
PROJECTS_CSV=data/projects.csv
ANALYSES_CSV=data/analyses.csv

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""

    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template)
        print("✅ Created: .env template")
        print("⚠️  Please update your API keys in .env file")
    else:
        print("ℹ️  .env file already exists")

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python requirements...")
    
    if os.path.exists('requirements.txt'):
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        print("✅ Requirements installed")
    else:
        print("❌ requirements.txt not found")

def initialize_data_files():
    """Initialize CSV data files"""
    print("\n💾 Initializing data files...")
    
    try:
        # Create headers for CSV files
        csv_files = {
            'data/users.csv': 'user_id,username,email,password_hash,role,full_name,company,certification,created_at,is_active',
            'data/projects.csv': 'project_id,client_id,engineer_id,project_name,scanner_model,facility_name,facility_address,project_status,room_specifications,analysis_results,estimated_cost,conformity_score,critical_issues,created_at,updated_at,completion_date,notes',
            'data/analyses.csv': 'analysis_id,project_id,engineer_id,scanner_model,room_data,conformity_score,critical_issues,penalties,estimated_cost,installation_timeline,ai_analysis,biomedical_assessment,safety_compliance,recommendations,created_at,status,approved_by,approval_date'
        }
        
        for file_path, headers in csv_files.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(headers + '\n')
                print(f"✅ Created: {file_path}")
            else:
                print(f"ℹ️  {file_path} already exists")
                
    except Exception as e:
        print(f"❌ Error initializing data files: {e}")

def main():
    """Main setup function"""
    print("🚀 CT Scanner Pre-installation System Setup")
    print("=" * 50)
    
    create_directory_structure()
    create_init_files() 
    create_env_template()
    initialize_data_files()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Update your API keys in .env file")
    print("2. Install requirements: pip install -r requirements.txt")
    print("3. Run the application: python app.py")
    print("\n🔗 Access the system at: http://localhost:5000")

if __name__ == "__main__":
    main()