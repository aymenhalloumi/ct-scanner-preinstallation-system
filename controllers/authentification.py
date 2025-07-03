import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash

class Authentication:
    def __init__(self, users_file='users.csv'):
        self.users_file = users_file
        self.ensure_csv_structure()

    def ensure_csv_structure(self):
        """Ensure the CSV file exists with proper header."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'username', 'password', 'role', 'email', 'company', 'created_at'])
        else:
            # Check if file is empty and add header if needed
            try:
                with open(self.users_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow(['id', 'username', 'password', 'role', 'email', 'company', 'created_at'])
            except Exception as e:
                print(f"Error checking CSV structure: {e}")

    def user_exists(self, username):
        """Check if username already exists."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Safely skip header with default value
                header = next(reader, None)
                if header is None:
                    return False  # Empty file
                
                for row in reader:
                    if row and len(row) >= 2 and row[1].lower() == username.lower():
                        return True
        except FileNotFoundError:
            # Create the file if it doesn't exist
            self.ensure_csv_structure()
            return False
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
        return False

    def register_user(self, username, password, role, email='', company=''):
        """Register new user with enhanced profile data."""
        try:
            # Validate inputs
            if not username or not password or not role:
                return False
            
            if self.user_exists(username):
                return False

            # Validate role
            valid_roles = ['client', 'engineer', 'admin', 'patient', 'receptionist']
            if role not in valid_roles:
                return False

            # Generate user ID
            user_id = self.get_next_user_id()
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Get current timestamp
            from datetime import datetime
            created_at = datetime.now().isoformat()

            # Write to CSV
            with open(self.users_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, username, hashed_password, role, email, company, created_at])
            
            return True
            
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    def get_next_user_id(self):
        """Get the next available user ID."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header safely
                
                max_id = 0
                for row in reader:
                    if row and len(row) >= 1:
                        try:
                            user_id = int(row[0])
                            max_id = max(max_id, user_id)
                        except (ValueError, IndexError):
                            continue
                
                return max_id + 1
        except FileNotFoundError:
            return 1
        except Exception:
            return 1

    def login_user(self, username, password):
        """Authenticate user and return user info."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header safely
                
                for row in reader:
                    if row and len(row) >= 4:
                        stored_id, stored_username, stored_password, stored_role = row[0], row[1], row[2], row[3]
                        
                        if stored_username.lower() == username.lower():
                            if check_password_hash(stored_password, password):
                                return {
                                    'id': stored_id,
                                    'username': stored_username,
                                    'role': stored_role,
                                    'email': row[4] if len(row) > 4 else '',
                                    'company': row[5] if len(row) > 5 else ''
                                }
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error during login: {e}")
            return None
        
        return None

    def get_user_by_id(self, user_id):
        """Get user information by ID."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header safely
                
                for row in reader:
                    if row and len(row) >= 4 and row[0] == str(user_id):
                        return {
                            'id': row[0],
                            'username': row[1],
                            'role': row[3],
                            'email': row[4] if len(row) > 4 else '',
                            'company': row[5] if len(row) > 5 else ''
                        }
        except Exception as e:
            print(f"Error getting user by ID: {e}")
        
        return None

    def update_user(self, user_id, **kwargs):
        """Update user information."""
        try:
            rows = []
            updated = False
            
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader, ['id', 'username', 'password', 'role', 'email', 'company', 'created_at'])
                rows.append(header)
                
                for row in reader:
                    if row and len(row) >= 4 and row[0] == str(user_id):
                        # Update the row
                        if 'email' in kwargs and len(row) > 4:
                            row[4] = kwargs['email']
                        if 'company' in kwargs and len(row) > 5:
                            row[5] = kwargs['company']
                        updated = True
                    rows.append(row)
            
            if updated:
                with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            
            return updated
            
        except Exception as e:
            print(f"Error updating user: {e}")
            return False