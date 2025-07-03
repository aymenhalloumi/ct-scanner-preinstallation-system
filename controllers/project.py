import csv
import os
import json
import logging
from datetime import datetime
from config import Config, PROJECT_STATUS, ANALYSIS_PRIORITY

logger = logging.getLogger(__name__)

class Project:
    """Project management for CT Scanner preinstallation verification."""
    
    def __init__(self):
        self.projects_file = Config.PROJECTS_FILE
        self.ensure_projects_file_exists()
    
    def ensure_projects_file_exists(self):
        """Ensure projects.csv file exists with proper headers."""
        if not os.path.exists(self.projects_file):
            os.makedirs(os.path.dirname(self.projects_file), exist_ok=True)
            with open(self.projects_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id', 'client_id', 'engineer_id', 'project_name', 'facility_name',
                    'contact_person', 'email', 'phone', 'address', 'scanner_model',
                    'installation_date', 'priority', 'status', 'created_date',
                    'last_updated', 'notes', 'project_data', 'analysis_results'
                ])
    
    def generate_project_id(self):
        """Generate unique project ID."""
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                project_ids = [int(row[0]) for row in reader if row and row[0].isdigit()]
                return max(project_ids) + 1 if project_ids else 3001
        except (FileNotFoundError, ValueError):
            return 3001
    
    def create_project(self, project_data):
        """Create new preinstallation project."""
        try:
            project_id = self.generate_project_id()
            current_time = datetime.now().isoformat()
            
            # Determine priority based on installation date
            priority = self.calculate_project_priority(project_data.get('installation_date', ''))
            
            # Enhanced project data structure
            enhanced_data = {
                'facility_type': project_data.get('facility_type', 'Hospital'),
                'project_type': 'CT_SCANNER_PREINSTALLATION',
                'room_specifications': {},
                'environmental_requirements': {},
                'electrical_specifications': {},
                'safety_requirements': {},
                'timeline_milestones': self.generate_default_milestones(),
                'budget_range': project_data.get('budget_range', ''),
                'special_requirements': project_data.get('special_requirements', ''),
                'site_constraints': project_data.get('site_constraints', ''),
                'regulatory_requirements': ['IEC 60601-2-44', 'NF C 15-211', 'ANSM'],
                'stakeholders': {
                    'client': project_data.get('client_id', ''),
                    'facility_manager': project_data.get('contact_person', ''),
                    'technical_contact': project_data.get('email', ''),
                    'project_manager': '',
                    'engineer': ''
                }
            }
            
            # Add NeuViz specific requirements if applicable
            if 'NeuViz' in project_data.get('scanner_model', ''):
                enhanced_data['regulatory_requirements'].append('NPS-CT-0651')
                enhanced_data['special_requirements'] += '; Ingénieur Neusoft obligatoire'
            
            with open(self.projects_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    project_id,
                    project_data.get('client_id', ''),
                    '',  # engineer_id (assigned later)
                    project_data.get('project_name', ''),
                    project_data.get('facility_name', ''),
                    project_data.get('contact_person', ''),
                    project_data.get('email', ''),
                    project_data.get('phone', ''),
                    project_data.get('address', ''),
                    project_data.get('scanner_model', ''),
                    project_data.get('installation_date', ''),
                    priority,
                    'DRAFT',
                    current_time,
                    current_time,
                    project_data.get('notes', ''),
                    json.dumps(enhanced_data, ensure_ascii=False),
                    ''  # analysis_results (populated later)
                ])
            
            logger.info(f"Project {project_id} created successfully")
            return project_id
            
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return None
    
    def calculate_project_priority(self, installation_date):
        """Calculate project priority based on installation timeline."""
        if not installation_date:
            return 'MEDIUM'
        
        try:
            install_date = datetime.strptime(installation_date, '%Y-%m-%d')
            days_until = (install_date - datetime.now()).days
            
            if days_until <= 30:
                return 'URGENT'
            elif days_until <= 60:
                return 'HIGH'
            elif days_until <= 120:
                return 'MEDIUM'
            else:
                return 'LOW'
                
        except ValueError:
            return 'MEDIUM'
    
    def generate_default_milestones(self):
        """Generate default project milestones."""
        return {
            'project_initiation': {'status': 'pending', 'estimated_duration': '1 week'},
            'site_survey': {'status': 'pending', 'estimated_duration': '1-2 weeks'},
            'technical_analysis': {'status': 'pending', 'estimated_duration': '2-3 weeks'},
            'compliance_verification': {'status': 'pending', 'estimated_duration': '1-2 weeks'},
            'report_generation': {'status': 'pending', 'estimated_duration': '1 week'},
            'client_review': {'status': 'pending', 'estimated_duration': '1-2 weeks'},
            'final_approval': {'status': 'pending', 'estimated_duration': '1 week'}
        }
    
    def get_project(self, project_id):
        """Get project by ID."""
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and row[0] == str(project_id):
                        project_data = None
                        analysis_results = None
                        
                        try:
                            project_data = json.loads(row[16]) if row[16] else {}
                        except:
                            project_data = {}
                        
                        try:
                            analysis_results = json.loads(row[17]) if row[17] else {}
                        except:
                            analysis_results = {}
                        
                        return {
                            'id': row[0],
                            'client_id': row[1],
                            'engineer_id': row[2],
                            'project_name': row[3],
                            'facility_name': row[4],
                            'contact_person': row[5],
                            'email': row[6],
                            'phone': row[7],
                            'address': row[8],
                            'scanner_model': row[9],
                            'installation_date': row[10],
                            'priority': row[11],
                            'status': row[12],
                            'created_date': row[13],
                            'last_updated': row[14],
                            'notes': row[15],
                            'project_data': project_data,
                            'analysis_results': analysis_results
                        }
        except FileNotFoundError:
            pass
        
        return None
    
    def get_user_projects(self, user_id, role='client'):
        """Get projects for a specific user."""
        projects = []
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 18:
                        # Check if user has access to this project
                        if ((role == 'client' and row[1] == str(user_id)) or
                            (role == 'engineer' and row[2] == str(user_id)) or
                            role == 'admin'):
                            
                            projects.append({
                                'id': row[0],
                                'client_id': row[1],
                                'engineer_id': row[2],
                                'project_name': row[3],
                                'facility_name': row[4],
                                'contact_person': row[5],
                                'email': row[6],
                                'phone': row[7],
                                'address': row[8],
                                'scanner_model': row[9],
                                'installation_date': row[10],
                                'priority': row[11],
                                'status': row[12],
                                'created_date': row[13],
                                'last_updated': row[14],
                                'notes': row[15]
                            })
        except FileNotFoundError:
            pass
        
        return projects
    
    def update_project_status(self, project_id, new_status, user_id=None):
        """Update project status."""
        if new_status not in PROJECT_STATUS:
            return False
        
        try:
            projects = []
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                projects = list(reader)
            
            # Find and update project
            for i, row in enumerate(projects):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(project_id):
                    row[12] = new_status  # status
                    row[14] = datetime.now().isoformat()  # last_updated
                    
                    # Add status change to project data
                    try:
                        project_data = json.loads(row[16]) if row[16] else {}
                        if 'status_history' not in project_data:
                            project_data['status_history'] = []
                        
                        project_data['status_history'].append({
                            'status': new_status,
                            'timestamp': datetime.now().isoformat(),
                            'user_id': user_id or 'system'
                        })
                        
                        row[16] = json.dumps(project_data, ensure_ascii=False)
                    except:
                        pass
                    
                    break
            
            # Write back to file
            with open(self.projects_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(projects)
            
            logger.info(f"Project {project_id} status updated to {new_status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating project status: {e}")
            return False
    
    def assign_engineer(self, project_id, engineer_id):
        """Assign engineer to project."""
        try:
            projects = []
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                projects = list(reader)
            
            # Find and update project
            for i, row in enumerate(projects):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(project_id):
                    row[2] = str(engineer_id)  # engineer_id
                    row[14] = datetime.now().isoformat()  # last_updated
                    
                    # Update status if it's still DRAFT
                    if row[12] == 'DRAFT':
                        row[12] = 'SUBMITTED'
                    
                    # Update project data
                    try:
                        project_data = json.loads(row[16]) if row[16] else {}
                        project_data['stakeholders']['engineer'] = str(engineer_id)
                        project_data['assignment_date'] = datetime.now().isoformat()
                        row[16] = json.dumps(project_data, ensure_ascii=False)
                    except:
                        pass
                    
                    break
            
            # Write back to file
            with open(self.projects_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(projects)
            
            logger.info(f"Engineer {engineer_id} assigned to project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error assigning engineer: {e}")
            return False
    
    def update_project_analysis(self, project_id, analysis_results):
        """Update project with analysis results."""
        try:
            projects = []
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                projects = list(reader)
            
            # Find and update project
            for i, row in enumerate(projects):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == str(project_id):
                    row[17] = json.dumps(analysis_results, ensure_ascii=False)  # analysis_results
                    row[14] = datetime.now().isoformat()  # last_updated
                    
                    # Update status based on analysis results
                    conformity_score = analysis_results.get('conformity_score', 0)
                    if conformity_score >= 85:
                        new_status = 'APPROVED'
                    elif conformity_score >= 70:
                        new_status = 'COMPLETED'
                    else:
                        new_status = 'REJECTED'
                    
                    row[12] = new_status  # status
                    
                    break
            
            # Write back to file
            with open(self.projects_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(projects)
            
            logger.info(f"Project {project_id} analysis updated")
            return True
            
        except Exception as e:
            logger.error(f"Error updating project analysis: {e}")
            return False
    
    def get_projects_by_status(self, status):
        """Get all projects with specific status."""
        projects = []
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 18 and row[12] == status:
                        projects.append({
                            'id': row[0],
                            'client_id': row[1],
                            'engineer_id': row[2],
                            'project_name': row[3],
                            'facility_name': row[4],
                            'contact_person': row[5],
                            'scanner_model': row[9],
                            'installation_date': row[10],
                            'priority': row[11],
                            'status': row[12],
                            'created_date': row[13],
                            'last_updated': row[14]
                        })
        except FileNotFoundError:
            pass
        
        return projects
    
    def get_projects_by_priority(self, priority):
        """Get all projects with specific priority."""
        projects = []
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 18 and row[11] == priority:
                        projects.append({
                            'id': row[0],
                            'client_id': row[1],
                            'engineer_id': row[2],
                            'project_name': row[3],
                            'facility_name': row[4],
                            'scanner_model': row[9],
                            'installation_date': row[10],
                            'priority': row[11],
                            'status': row[12],
                            'created_date': row[13]
                        })
        except FileNotFoundError:
            pass
        
        return projects
    
    def search_projects(self, search_term, user_id=None, role=None):
        """Search projects by various criteria."""
        projects = []
        search_term = search_term.lower()
        
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 18:
                        # Check user access
                        if user_id and role:
                            if not ((role == 'client' and row[1] == str(user_id)) or
                                   (role == 'engineer' and row[2] == str(user_id)) or
                                   role == 'admin'):
                                continue
                        
                        # Search in multiple fields
                        searchable_text = ' '.join([
                            row[3],  # project_name
                            row[4],  # facility_name
                            row[5],  # contact_person
                            row[9],  # scanner_model
                            row[12], # status
                            row[15]  # notes
                        ]).lower()
                        
                        if search_term in searchable_text:
                            projects.append({
                                'id': row[0],
                                'client_id': row[1],
                                'engineer_id': row[2],
                                'project_name': row[3],
                                'facility_name': row[4],
                                'contact_person': row[5],
                                'scanner_model': row[9],
                                'installation_date': row[10],
                                'priority': row[11],
                                'status': row[12],
                                'created_date': row[13],
                                'last_updated': row[14]
                            })
        except FileNotFoundError:
            pass
        
        return projects
    
    def get_project_statistics(self):
        """Get project statistics for dashboard."""
        stats = {
            'total_projects': 0,
            'active_projects': 0,
            'completed_projects': 0,
            'urgent_projects': 0,
            'neuViz_projects': 0,
            'status_breakdown': {},
            'priority_breakdown': {},
            'scanner_breakdown': {},
            'monthly_projects': {}
        }
        
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row and len(row) >= 18:
                        stats['total_projects'] += 1
                        
                        status = row[12]
                        priority = row[11]
                        scanner_model = row[9]
                        
                        # Status breakdown
                        stats['status_breakdown'][status] = stats['status_breakdown'].get(status, 0) + 1
                        
                        # Priority breakdown
                        stats['priority_breakdown'][priority] = stats['priority_breakdown'].get(priority, 0) + 1
                        
                        # Scanner breakdown
                        stats['scanner_breakdown'][scanner_model] = stats['scanner_breakdown'].get(scanner_model, 0) + 1
                        
                        # Count specific categories
                        if status in ['SUBMITTED', 'IN_ANALYSIS']:
                            stats['active_projects'] += 1
                        elif status in ['COMPLETED', 'APPROVED']:
                            stats['completed_projects'] += 1
                        
                        if priority == 'URGENT':
                            stats['urgent_projects'] += 1
                        
                        if 'NeuViz' in scanner_model:
                            stats['neuViz_projects'] += 1
                        
                        # Monthly breakdown
                        try:
                            created_date = datetime.fromisoformat(row[13])
                            month_key = created_date.strftime('%Y-%m')
                            stats['monthly_projects'][month_key] = stats['monthly_projects'].get(month_key, 0) + 1
                        except:
                            pass
                            
        except FileNotFoundError:
            pass
        
        return stats
    
    def delete_project(self, project_id, user_id=None):
        """Delete project (admin only)."""
        try:
            projects = []
            project_found = False
            
            with open(self.projects_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                projects = list(reader)
            
            # Remove project
            projects = [row for i, row in enumerate(projects) 
                       if i == 0 or row[0] != str(project_id)]
            
            # Write back to file
            with open(self.projects_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(projects)
            
            logger.info(f"Project {project_id} deleted by user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            return False