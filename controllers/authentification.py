import csv
import os
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

class Authentication:
    """Enhanced authentication system for CT Scanner Verification System."""
    
    def __init__(self):
        self.users_file = Config.USERS_FILE
        self.ensure_users_file_exists()
    
    def ensure_users_file_exists(self):
        """Ensure users.csv file exists with proper headers."""
        if not os.path.exists(self.users_file):
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id', 'username', 'password_hash', 'role', 'email', 
                    'company', 'created_date', 'last_login', 'is_active', 'profile_data'
                ])
    
    def create_default_admin(self):
        """Create default admin user if none exists."""
        if not self.user_exists('admin'):
            admin_data = {
                'username': 'admin',
                'password': 'admin123',  # Change this in production!
                'role': 'admin',
                'email': 'admin@ct-scanner-system.com',
                'company': 'System Administration'
            }
            self.register_user(**admin_data)
            print("✅ Default admin user created (username: admin, password: admin123)")
    
    def generate_user_id(self):
        """Generate unique user ID."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                user_ids = [int(row[0]) for row in reader if row and row[0].isdigit()]
                return max(user_ids) + 1 if user_ids else 1001
        except (FileNotFoundError, ValueError):
            return 1001
    
    def user_exists(self, username):
        """Check if username already exists."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row and len(row) >= 2 and row[1].lower() == username.lower():
                        return True
        except FileNotFoundError:
            return False
        return False
    
    def register_user(self, username, password, role, email='', company=''):
        """Register new user with enhanced profile data."""
        if self.user_exists(username):
            return False
        
        # Validate role
        if role not in ['client', 'engineer', 'admin']:
            return False
        
        user_id = self.generate_user_id()
        password_hash = generate_password_hash(password)
        created_date = datetime.now().isoformat()
        
        # Enhanced profile data
        profile_data = {
            'registration_ip': 'system',
            'preferences': {
                'language': 'fr',
                'timezone': 'Europe/Paris',
                'notifications': True
            },
            'specializations': [] if role != 'engineer' else ['CT_SCANNERS'],
            'certifications': [],
            'contact_preferences': 'email'
        }
        
        try:
            with open(self.users_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    user_id, username, password_hash, role, email, 
                    company, created_date, '', True, str(profile_data)
                ])
            return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def login_user(self, username, password):
        """Authenticate user and return user data."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 9:
                        stored_id, stored_username, stored_hash, role, email, company, created_date, last_login, is_active = row[:9]
                        
                        if (stored_username.lower() == username.lower() and 
                            check_password_hash(stored_hash, password) and 
                            is_active.lower() == 'true'):
                            
                            # Update last login
                            self.update_last_login(stored_id)
                            
                            return {
                                'id': stored_id,
                                'username': stored_username,
                                'role': role,
                                'email': email,
                                'company': company,
                                'created_date': created_date
                            }
        except FileNotFoundError:
            pass
        
        return None
    
    def update_last_login(self, user_id):
        """Update user's last login timestamp."""
        try:
            users = []
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                users = list(reader)
            
            # Update the specific user's last login
            for i, row in enumerate(users):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(user_id):
                    row[7] = datetime.now().isoformat()  # last_login column
                    break
            
            # Write back to file
            with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(users)
                
        except Exception as e:
            print(f"Error updating last login: {e}")
    
    def get_user_by_id(self, user_id):
        """Get user data by ID."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and row[0] == str(user_id):
                        return {
                            'id': row[0],
                            'username': row[1],
                            'role': row[3],
                            'email': row[4],
                            'company': row[5],
                            'created_date': row[6],
                            'last_login': row[7],
                            'is_active': row[8]
                        }
        except FileNotFoundError:
            pass
        
        return None
    
    def get_all_users(self):
        """Get all users (admin function)."""
        users = []
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 9:
                        users.append({
                            'id': row[0],
                            'username': row[1],
                            'role': row[3],
                            'email': row[4],
                            'company': row[5],
                            'created_date': row[6],
                            'last_login': row[7],
                            'is_active': row[8]
                        })
        except FileNotFoundError:
            pass
        
        return users
    
    def update_user_profile(self, user_id, profile_data):
        """Update user profile information."""
        try:
            users = []
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                users = list(reader)
            
            # Find and update user
            for i, row in enumerate(users):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(user_id):
                    # Update fields
                    if 'email' in profile_data:
                        row[4] = profile_data['email']
                    if 'company' in profile_data:
                        row[5] = profile_data['company']
                    break
            
            # Write back to file
            with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(users)
            
            return True
            
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def deactivate_user(self, user_id):
        """Deactivate user account (admin function)."""
        try:
            users = []
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                users = list(reader)
            
            # Find and deactivate user
            for i, row in enumerate(users):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(user_id):
                    row[8] = 'False'  # is_active
                    break
            
            # Write back to file
            with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(users)
            
            return True
            
        except Exception as e:
            print(f"Error deactivating user: {e}")
            return False
    
    def change_password(self, user_id, current_password, new_password):
        """Change user password."""
        # First verify current password
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Get current password hash
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and row[0] == str(user_id):
                        if not check_password_hash(row[2], current_password):
                            return False
                        break
                else:
                    return False
            
            # Update password
            users = []
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                users = list(reader)
            
            # Find and update password
            for i, row in enumerate(users):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(user_id):
                    row[2] = generate_password_hash(new_password)
                    break
            
            # Write back to file
            with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(users)
            
            return True
            
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
    
    def get_user_statistics(self):
        """Get user statistics for admin dashboard."""
        stats = {
            'total_users': 0,
            'active_users': 0,
            'clients': 0,
            'engineers': 0,
            'admins': 0,
            'recent_registrations': 0
        }
        
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 9:
                        stats['total_users'] += 1
                        
                        if row[8].lower() == 'true':
                            stats['active_users'] += 1
                        
                        role = row[3].lower()
                        if role == 'client':
                            stats['clients'] += 1
                        elif role == 'engineer':
                            stats['engineers'] += 1
                        elif role == 'admin':
                            stats['admins'] += 1
                        
                        # Check if registered in last 30 days
                        try:
                            created_date = datetime.fromisoformat(row[6])
                            if (datetime.now() - created_date).days <= 30:
                                stats['recent_registrations'] += 1
                        except:
                            pass
                            
        except FileNotFoundError:
            pass
        
        return stats