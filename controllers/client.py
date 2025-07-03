import csv
import os
import json
import logging
from datetime import datetime, timedelta
from controllers.project import Project
from controllers.authentification import Authentication
from config import Config

logger = logging.getLogger(__name__)

class Client:
    """Client management for CT Scanner preinstallation projects."""
    
    def __init__(self):
        self.project_manager = Project()
        self.auth_manager = Authentication()
    
    def get_user_projects(self, client_id):
        """Get all projects for a specific client."""
        return self.project_manager.get_user_projects(client_id, role='client')
    
    def get_client_dashboard_data(self, client_id):
        """Get comprehensive dashboard data for client."""
        projects = self.get_user_projects(client_id)
        client_info = self.auth_manager.get_user_by_id(client_id)
        
        # Basic dashboard data
        return {
            'client_info': client_info,
            'statistics': {
                'total_projects': len(projects),
                'active_projects': 0,
                'completed_projects': 0,
                'urgent_projects': 0
            },
            'projects': projects,
            'recent_projects': projects[:5] if projects else []
        }
    
    def generate_client_alerts(self, projects):
        """Generate alerts and notifications for client."""
        alerts = []
        
        for project in projects:
            # Urgent deadline alerts
            if project['installation_date']:
                try:
                    install_date = datetime.strptime(project['installation_date'], '%Y-%m-%d')
                    days_until = (install_date - datetime.now()).days
                    
                    if days_until <= 7 and project['status'] not in ['COMPLETED', 'APPROVED']:
                        alerts.append({
                            'type': 'critical',
                            'title': 'Installation Deadline Approaching',
                            'message': f"Project '{project['project_name']}' installation is in {days_until} days but analysis is not complete.",
                            'project_id': project['id'],
                            'action': 'Contact engineer immediately'
                        })
                    elif days_until <= 30 and project['status'] == 'DRAFT':
                        alerts.append({
                            'type': 'warning',
                            'title': 'Project Needs Submission',
                            'message': f"Project '{project['project_name']}' needs to be submitted for analysis.",
                            'project_id': project['id'],
                            'action': 'Submit for analysis'
                        })
                except:
                    pass
            
            # Status-based alerts
            if project['status'] == 'REJECTED':
                alerts.append({
                    'type': 'error',
                    'title': 'Project Requires Modifications',
                    'message': f"Project '{project['project_name']}' has been rejected and needs modifications.",
                    'project_id': project['id'],
                    'action': 'Review analysis report'
                })
            
            elif project['status'] == 'ON_HOLD':
                alerts.append({
                    'type': 'info',
                    'title': 'Project On Hold',
                    'message': f"Project '{project['project_name']}' is currently on hold.",
                    'project_id': project['id'],
                    'action': 'Contact project manager'
                })
        
        # NeuViz specific alerts
        neuViz_projects = [p for p in projects if 'NeuViz' in p['scanner_model']]
        for project in neuViz_projects:
            if project['status'] in ['SUBMITTED', 'IN_ANALYSIS']:
                alerts.append({
                    'type': 'info',
                    'title': 'NeuViz Special Requirements',
                    'message': f"Project '{project['project_name']}' requires Neusoft engineer coordination.",
                    'project_id': project['id'],
                    'action': 'Ensure Neusoft coordination is planned'
                })
        
        return alerts[:10]  # Limit to 10 most important alerts
    
    def create_project_request(self, client_id, project_data):
        """Create new project request."""
        try:
            # Validate client
            client_info = self.auth_manager.get_user_by_id(client_id)
            if not client_info:
                return None
            
            # Enhanced project data with client information
            enhanced_data = {
                **project_data,
                'client_id': client_id,
                'client_company': client_info.get('company', ''),
                'request_type': 'PREINSTALLATION_VERIFICATION',
                'submission_method': 'WEB_PORTAL',
                'client_preferences': {
                    'preferred_communication': 'email',
                    'report_format': 'digital',
                    'timeline_flexibility': project_data.get('timeline_flexibility', 'standard')
                }
            }
            
            project_id = self.project_manager.create_project(enhanced_data)
            
            if project_id:
                logger.info(f"Client {client_id} created project {project_id}")
                return project_id
            
        except Exception as e:
            logger.error(f"Error creating client project request: {e}")
            return None
    
    def update_project_info(self, client_id, project_id, updates):
        """Update project information (client can only update their own projects)."""
        try:
            # Verify ownership
            project = self.project_manager.get_project(project_id)
            if not project or project['client_id'] != str(client_id):
                return False
            
            # Only allow certain fields to be updated by client
            allowed_updates = [
                'contact_person', 'email', 'phone', 'notes',
                'installation_date', 'special_requirements'
            ]
            
            # Filter updates to only allowed fields
            filtered_updates = {k: v for k, v in updates.items() if k in allowed_updates}
            
            if filtered_updates:
                # Implementation would update the project file
                logger.info(f"Client {client_id} updated project {project_id}")
                return True
            
        except Exception as e:
            logger.error(f"Error updating project info: {e}")
            return False
    
    def request_project_modification(self, client_id, project_id, modification_request):
        """Request modification of completed analysis."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project or project['client_id'] != str(client_id):
                return False
            
            # Add modification request to project data
            modification_data = {
                'timestamp': datetime.now().isoformat(),
                'client_id': client_id,
                'request_type': 'MODIFICATION',
                'description': modification_request.get('description', ''),
                'reason': modification_request.get('reason', ''),
                'priority': modification_request.get('priority', 'MEDIUM'),
                'status': 'PENDING'
            }
            
            # In a real implementation, this would update the project file
            logger.info(f"Client {client_id} requested modification for project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error requesting project modification: {e}")
            return False
    
    def get_project_timeline(self, client_id, project_id):
        """Get detailed project timeline for client."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project or project['client_id'] != str(client_id):
                return None
            
            # Generate timeline based on project status and data
            timeline = []
            
            # Project creation
            timeline.append({
                'phase': 'Project Initiated',
                'date': project['created_date'],
                'status': 'completed',
                'description': 'Project request submitted and registered'
            })
            
            # Engineer assignment
            if project['engineer_id']:
                timeline.append({
                    'phase': 'Engineer Assigned',
                    'date': project.get('assignment_date', project['created_date']),
                    'status': 'completed',
                    'description': 'Biomedical engineer assigned to project'
                })
            else:
                timeline.append({
                    'phase': 'Engineer Assignment',
                    'date': 'TBD',
                    'status': 'pending',
                    'description': 'Waiting for engineer assignment'
                })
            
            # Analysis phases
            analysis_phases = [
                ('Site Survey', 'Site assessment and measurements'),
                ('Technical Analysis', 'CT scanner compatibility analysis'),
                ('Compliance Verification', 'Regulatory compliance check'),
                ('Report Generation', 'Final analysis report preparation'),
                ('Client Review', 'Report review and feedback'),
                ('Final Approval', 'Project completion and approval')
            ]
            
            current_status = project['status']
            for i, (phase, description) in enumerate(analysis_phases):
                if current_status == 'COMPLETED' or current_status == 'APPROVED':
                    status = 'completed'
                elif current_status == 'IN_ANALYSIS' and i < 3:
                    status = 'in_progress' if i == 0 else 'pending'
                elif current_status == 'SUBMITTED' and i == 0:
                    status = 'in_progress'
                else:
                    status = 'pending'
                
                timeline.append({
                    'phase': phase,
                    'date': 'TBD',
                    'status': status,
                    'description': description
                })
            
            return timeline
            
        except Exception as e:
            logger.error(f"Error getting project timeline: {e}")
            return None
    
    def get_client_preferences(self, client_id):
        """Get client preferences and settings."""
        client_info = self.auth_manager.get_user_by_id(client_id)
        if not client_info:
            return None
        
        # Default preferences
        preferences = {
            'communication': {
                'email_notifications': True,
                'sms_notifications': False,
                'report_delivery': 'email',
                'language': 'fr'
            },
            'reporting': {
                'format': 'digital',
                'detail_level': 'comprehensive',
                'include_photos': True,
                'include_recommendations': True
            },
            'project_management': {
                'default_priority': 'MEDIUM',
                'timeline_flexibility': 'standard',
                'auto_reminders': True
            }
        }
        
        return preferences
    
    def update_client_preferences(self, client_id, preferences):
        """Update client preferences."""
        try:
            # In a real implementation, this would update the user profile
            logger.info(f"Client {client_id} updated preferences")
            return True
        except Exception as e:
            logger.error(f"Error updating client preferences: {e}")
            return False
    
    def get_cost_estimates(self, client_id, project_id):
        """Get cost estimates for project modifications."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project or project['client_id'] != str(client_id):
                return None
            
            # Extract analysis results
            analysis_results = project.get('analysis_results', {})
            if not analysis_results:
                return None
            
            cost_breakdown = analysis_results.get('cost_breakdown', [])
            
            # Format for client display
            formatted_costs = {
                'total_estimated_cost': sum(item[1] for item in cost_breakdown if isinstance(item, (list, tuple)) and len(item) >= 2),
                'breakdown_by_category': {},
                'critical_items': [],
                'optional_items': []
            }
            
            for item in cost_breakdown:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    category = self.categorize_cost_item(item[0])
                    if category not in formatted_costs['breakdown_by_category']:
                        formatted_costs['breakdown_by_category'][category] = 0
                    formatted_costs['breakdown_by_category'][category] += item[1]
                    
                    # Categorize as critical or optional
                    if any(keyword in item[0].lower() for keyword in ['obligatoire', 'critique', 'minimum']):
                        formatted_costs['critical_items'].append({
                            'description': item[0],
                            'cost': item[1]
                        })
                    else:
                        formatted_costs['optional_items'].append({
                            'description': item[0],
                            'cost': item[1]
                        })
            
            return formatted_costs
            
        except Exception as e:
            logger.error(f"Error getting cost estimates: {e}")
            return None
    
    def categorize_cost_item(self, item_description):
        """Categorize cost items for better organization."""
        description_lower = item_description.lower()
        
        if any(keyword in description_lower for keyword in ['électrique', 'alimentation', 'transformateur']):
            return 'Electrical'
        elif any(keyword in description_lower for keyword in ['blindage', 'radioprotection', 'plomb']):
            return 'Radiation Safety'
        elif any(keyword in description_lower for keyword in ['cvc', 'climatisation', 'ventilation']):
            return 'HVAC'
        elif any(keyword in description_lower for keyword in ['structure', 'sol', 'renforcement']):
            return 'Structural'
        elif any(keyword in description_lower for keyword in ['incendie', 'sécurité', 'détection']):
            return 'Safety Systems'
        elif any(keyword in description_lower for keyword in ['neusoft', 'transport', 'ingénieur']):
            return 'Specialized Services'
        else:
            return 'General'
    
    def generate_client_report_summary(self, client_id, project_id):
        """Generate client-friendly report summary."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project or project['client_id'] != str(client_id):
                return None
            
            analysis_results = project.get('analysis_results', {})
            if not analysis_results:
                return None
            
            # Generate summary
            summary = {
                'project_info': {
                    'name': project['project_name'],
                    'facility': project['facility_name'],
                    'scanner_model': project['scanner_model'],
                    'installation_date': project['installation_date']
                },
                'compliance_status': {
                    'overall_score': analysis_results.get('conformity_score', 0),
                    'status': self.get_compliance_status_text(analysis_results.get('conformity_score', 0)),
                    'critical_issues': analysis_results.get('critical_issues', 0)
                },
                'timeline': {
                    'estimated_weeks': analysis_results.get('timeline', 'TBD'),
                    'can_proceed': analysis_results.get('conformity_score', 0) >= 70
                },
                'budget': {
                    'total_cost': analysis_results.get('total_cost', 0),
                    'cost_category': self.get_cost_category(analysis_results.get('total_cost', 0))
                },
                'next_steps': self.generate_next_steps(analysis_results),
                'key_recommendations': analysis_results.get('action_items', [])[:3]
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating client report summary: {e}")
            return None
    
    def get_compliance_status_text(self, score):
        """Convert compliance score to user-friendly text."""
        if score >= 90:
            return "Excellent - Ready for installation"
        elif score >= 80:
            return "Good - Minor adjustments needed"
        elif score >= 70:
            return "Acceptable - Some modifications required"
        elif score >= 60:
            return "Needs work - Several issues to address"
        else:
            return "Significant modifications required"
    
    def get_cost_category(self, cost):
        """Categorize total cost for client understanding."""
        if isinstance(cost, str):
            # Remove formatting and convert to number
            cost_num = float(cost.replace(',', '').replace('€', '').replace(' ', ''))
        else:
            cost_num = float(cost)
        
        if cost_num <= 50000:
            return "Standard installation cost"
        elif cost_num <= 100000:
            return "Moderate complexity installation"
        elif cost_num <= 200000:
            return "Complex installation requirements"
        else:
            return "Highly complex installation"
    
    def generate_next_steps(self, analysis_results):
        """Generate next steps based on analysis results."""
        score = analysis_results.get('conformity_score', 0)
        
        if score >= 85:
            return [
                "Proceed with final installation planning",
                "Schedule equipment delivery",
                "Coordinate with installation team"
            ]
        elif score >= 70:
            return [
                "Address identified modifications",
                "Obtain updated quotes for required work",
                "Schedule re-evaluation after modifications"
            ]
        else:
            return [
                "Review detailed analysis report",
                "Plan major facility modifications",
                "Consider alternative scanner models",
                "Consult with facility planning team"
            ]