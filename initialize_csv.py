#!/usr/bin/env python3
"""
CSV Initialization Script for Hospital Management System
Run this script before starting the application to ensure proper CSV structure.
"""

import csv
import os
from datetime import datetime

def initialize_csv_files():
    """Initialize all CSV files with proper headers."""
    
    csv_files = {
        'users.csv': ['id', 'username', 'password', 'role', 'email', 'company', 'created_at'],
        'appointments.csv': ['appointment_id', 'patient', 'medical_staff', 'date', 'status'],
        'booking.csv': ['patient_name', 'room_id', 'booking_date'],
        'biomedical_analysis_log.json': None  # JSON file, not CSV
    }
    
    print("🏥 Initializing Hospital Management System CSV files...")
    print("=" * 60)
    
    for filename, headers in csv_files.items():
        if filename.endswith('.json'):
            continue  # Skip JSON files
            
        try:
            file_exists = os.path.exists(filename)
            
            if not file_exists:
                # Create new file with headers
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                print(f"✅ Created {filename} with headers: {headers}")
            else:
                # Check if existing file has headers
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    
                if not content:
                    # File exists but is empty, add headers
                    with open(filename, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(headers)
                    print(f"✅ Added headers to empty {filename}")
                else:
                    # File has content, check if first line is header
                    with open(filename, 'r', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        first_row = next(reader, None)
                        
                    if first_row != headers:
                        # Backup existing file and recreate with headers
                        backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        os.rename(filename, backup_name)
                        
                        with open(filename, 'w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow(headers)
                        
                        print(f"⚠️  Backed up {filename} to {backup_name}")
                        print(f"✅ Recreated {filename} with proper headers")
                    else:
                        print(f"✅ {filename} already has correct headers")
                        
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    # Create a sample admin user
    create_sample_admin()
    
    print("\n🎯 CSV initialization complete!")
    print("You can now run your Flask application with: python app.py")

def create_sample_admin():
    """Create a sample admin user for testing."""
    try:
        from werkzeug.security import generate_password_hash
        
        # Check if admin already exists
        admin_exists = False
        try:
            with open('users.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row and len(row) >= 4 and row[3] == 'admin':
                        admin_exists = True
                        break
        except:
            pass
        
        if not admin_exists:
            # Create admin user
            admin_password = "admin123"  # Change this in production!
            hashed_password = generate_password_hash(admin_password)
            
            with open('users.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    1, 
                    'admin', 
                    hashed_password, 
                    'admin', 
                    'admin@hospital.com', 
                    'Hospital System', 
                    datetime.now().isoformat()
                ])
            
            print(f"✅ Created sample admin user:")
            print(f"   Username: admin")
            print(f"   Password: {admin_password}")
            print(f"   ⚠️  CHANGE THE PASSWORD AFTER FIRST LOGIN!")
        else:
            print("ℹ️  Admin user already exists")
            
    except ImportError:
        print("⚠️  Could not create admin user - werkzeug not available")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    initialize_csv_files()