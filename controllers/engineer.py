import csv
import os
import json
import logging
from datetime import datetime, timedelta
from controllers.project import Project
from controllers.authentification import Authentication
from controllers.scanner_analysis import ScannerAnalysis
from config import Config

logger = logging.getLogger(__name__)

class Engineer:
    """Engineer management for CT Scanner analysis and verification."""
    
    def __init__(self):
        self.project_manager = Project()
        self.auth_manager = Authentication()
        self.scanner_analysis = ScannerAnalysis()
    
    def get_assigned_projects(self, engineer_id):
        """Get all projects assigned to a specific engineer."""
        return self.project_manager.get_user_projects(engineer_id, role='engineer')
    
    def get_pending_analyses(self):
        """Get all projects pending analysis assignment."""
        return self.project_manager.get_projects_by_status('SUBMITTED')
    
    def get_engineer_dashboard_data(self, engineer_id):
        """Get comprehensive dashboard data for engineer."""
        assigned_projects = self.get_assigned_projects(engineer_id)
        pending_projects = self.get_pending_analyses()
        engineer_info = self.auth_manager.get_user_by_id(engineer_id)
        
        # Basic dashboard data
        return {
            'engineer_info': engineer_info,
            'workload_statistics': {
                'total_assigned': len(assigned_projects),
                'active_analyses': 0,
                'completed_analyses': 0,
                'urgent_projects': 0,
                'pending_assignments': len(pending_projects)
            },
            'assigned_projects': assigned_projects,
            'pending_projects': pending_projects
        }
    
    def calculate_engineer_performance(self, engineer_id):
        """Calculate performance metrics for engineer."""
        assigned_projects = self.get_assigned_projects(engineer_id)
        
        if not assigned_projects:
            return {
                'projects_completed': 0,
                'average_completion_time': 0,
                'success_rate': 0,
                'client_satisfaction': 0
            }
        
        completed_projects = [p for p in assigned_projects if p['status'] in ['COMPLETED', 'APPROVED']]
        
        # Calculate average completion time
        completion_times = []
        for project in completed_projects:
            try:
                start_date = datetime.fromisoformat(project['created_date'])
                end_date = datetime.fromisoformat(project['last_updated'])
                completion_time = (end_date - start_date).days
                completion_times.append(completion_time)
            except:
                pass
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Calculate success rate (approved vs total completed)
        approved_projects = len([p for p in completed_projects if p['status'] == 'APPROVED'])
        success_rate = (approved_projects / len(completed_projects) * 100) if completed_projects else 0
        
        return {
            'projects_completed': len(completed_projects),
            'average_completion_time': round(avg_completion_time, 1),
            'success_rate': round(success_rate, 1),
            'client_satisfaction': 85,  # This would come from client feedback in a real system
            'specializations': self.get_engineer_specializations(assigned_projects)
        }
    
    def get_engineer_specializations(self, projects):
        """Identify engineer specializations based on project history."""
        scanner_counts = {}
        for project in projects:
            scanner = project['scanner_model']
            scanner_counts[scanner] = scanner_counts.get(scanner, 0) + 1
        
        # Determine specializations (scanners with 3+ projects)
        specializations = []
        for scanner, count in scanner_counts.items():
            if count >= 3:
                specializations.append(scanner)
        
        # Add NeuViz specialization if applicable
        neuViz_count = sum(1 for scanner in scanner_counts.keys() if 'NeuViz' in scanner)
        if neuViz_count >= 2:
            specializations.append('NeuViz Systems (NPS-CT-0651)')
        
        return specializations
    
    def analyze_project_timelines(self, projects):
        """Analyze project timeline performance."""
        timeline_data = {
            'on_time_projects': 0,
            'delayed_projects': 0,
            'ahead_of_schedule': 0,
            'average_delay_days': 0
        }
        
        delays = []
        for project in projects:
            if project['installation_date'] and project['status'] in ['COMPLETED', 'APPROVED']:
                try:
                    install_date = datetime.strptime(project['installation_date'], '%Y-%m-%d')
                    completion_date = datetime.fromisoformat(project['last_updated'])
                    
                    # Assume 4 weeks before installation should be completion target
                    target_completion = install_date - timedelta(weeks=4)
                    delay_days = (completion_date - target_completion).days
                    
                    if delay_days <= 0:
                        timeline_data['ahead_of_schedule'] += 1
                    elif delay_days <= 7:
                        timeline_data['on_time_projects'] += 1
                    else:
                        timeline_data['delayed_projects'] += 1
                        delays.append(delay_days)
                except:
                    pass
        
        if delays:
            timeline_data['average_delay_days'] = sum(delays) / len(delays)
        
        return timeline_data
    
    def get_upcoming_deadlines(self, projects):
        """Get upcoming project deadlines."""
        deadlines = []
        
        for project in projects:
            if project['installation_date'] and project['status'] not in ['COMPLETED', 'APPROVED']:
                try:
                    install_date = datetime.strptime(project['installation_date'], '%Y-%m-%d')
                    # Analysis should be completed 4 weeks before installation
                    deadline = install_date - timedelta(weeks=4)
                    days_until = (deadline - datetime.now()).days
                    
                    if days_until <= 30:  # Show deadlines within 30 days
                        urgency = 'critical' if days_until <= 7 else 'warning' if days_until <= 14 else 'info'
                        
                        deadlines.append({
                            'project': project,
                            'deadline': deadline.strftime('%Y-%m-%d'),
                            'days_until': days_until,
                            'urgency': urgency,
                            'installation_date': project['installation_date']
                        })
                except:
                    pass
        
        return sorted(deadlines, key=lambda x: x['days_until'])
    
    def calculate_quality_metrics(self, projects):
        """Calculate analysis quality metrics."""
        completed_projects = [p for p in projects if p['status'] in ['COMPLETED', 'APPROVED']]
        
        if not completed_projects:
            return {
                'average_conformity_score': 0,
                'high_quality_analyses': 0,
                'revision_rate': 0
            }
        
        # This would come from analysis results in a real implementation
        # For now, we'll simulate some metrics
        quality_metrics = {
            'average_conformity_score': 82.5,  # Average compliance score achieved
            'high_quality_analyses': 75,  # Percentage of analyses with >85% conformity
            'revision_rate': 15,  # Percentage requiring revisions
            'neuViz_expertise': len([p for p in projects if 'NeuViz' in p['scanner_model']]) > 0
        }
        
        return quality_metrics
    
    def accept_project_assignment(self, engineer_id, project_id):
        """Accept a project assignment."""
        try:
            success = self.project_manager.assign_engineer(project_id, engineer_id)
            if success:
                # Update project status to IN_ANALYSIS
                self.project_manager.update_project_status(project_id, 'IN_ANALYSIS', engineer_id)
                logger.info(f"Engineer {engineer_id} accepted project {project_id}")
                return True
        except Exception as e:
            logger.error(f"Error accepting project assignment: {e}")
        return False
    
    def submit_analysis_results(self, engineer_id, project_id, analysis_data):
        """Submit analysis results for a project."""
        try:
            # Verify engineer is assigned to this project
            project = self.project_manager.get_project(project_id)
            if not project or project['engineer_id'] != str(engineer_id):
                return False
            
            # Perform the analysis
            analysis_results = self.scanner_analysis.analyze_room(analysis_data)
            
            if analysis_results:
                # Update project with analysis results
                success = self.project_manager.update_project_analysis(project_id, analysis_results)
                
                if success:
                    logger.info(f"Engineer {engineer_id} submitted analysis for project {project_id}")
                    return analysis_results
            
        except Exception as e:
            logger.error(f"Error submitting analysis results: {e}")
        
        return None
    
    def request_additional_information(self, engineer_id, project_id, request_details):
        """Request additional information from client."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project or project['engineer_id'] != str(engineer_id):
                return False
            
            # Create information request
            info_request = {
                'timestamp': datetime.now().isoformat(),
                'engineer_id': engineer_id,
                'request_type': 'ADDITIONAL_INFO',
                'details': request_details.get('details', ''),
                'urgency': request_details.get('urgency', 'MEDIUM'),
                'expected_response_time': request_details.get('response_time', '48 hours'),
                'status': 'PENDING'
            }
            
            # Update project status
            self.project_manager.update_project_status(project_id, 'ON_HOLD', engineer_id)
            
            logger.info(f"Engineer {engineer_id} requested additional info for project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error requesting additional information: {e}")
            return False
    
    def create_preliminary_assessment(self, engineer_id, project_id, assessment_data):
        """Create preliminary assessment before full analysis."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project or project['engineer_id'] != str(engineer_id):
                return False
            
            # Create preliminary assessment
            assessment = {
                'timestamp': datetime.now().isoformat(),
                'engineer_id': engineer_id,
                'assessment_type': 'PRELIMINARY',
                'scanner_model': project['scanner_model'],
                'initial_findings': assessment_data.get('findings', ''),
                'estimated_conformity': assessment_data.get('estimated_conformity', ''),
                'major_concerns': assessment_data.get('concerns', []),
                'recommended_next_steps': assessment_data.get('next_steps', []),
                'full_analysis_required': assessment_data.get('full_analysis_required', True),
                'estimated_completion_time': assessment_data.get('completion_time', '2-3 weeks')
            }
            
            logger.info(f"Engineer {engineer_id} created preliminary assessment for project {project_id}")
            return assessment
            
        except Exception as e:
            logger.error(f"Error creating preliminary assessment: {e}")
            return None
    
    def generate_engineer_recommendations(self, project_data, analysis_results):
        """Generate engineer-specific recommendations."""
        recommendations = []
        
        scanner_model = project_data.get('scanner_model', '')
        conformity_score = analysis_results.get('conformity_score', 0)
        critical_issues = analysis_results.get('critical_issues', 0)
        
        # General recommendations based on conformity score
        if conformity_score >= 85:
            recommendations.append({
                'category': 'Approval',
                'priority': 'HIGH',
                'text': 'Project meets compliance standards and can proceed to installation planning.'
            })
        elif conformity_score >= 70:
            recommendations.append({
                'category': 'Conditional Approval',
                'priority': 'MEDIUM',
                'text': 'Project can proceed with specified modifications. Schedule follow-up verification.'
            })
        else:
            recommendations.append({
                'category': 'Major Modifications Required',
                'priority': 'CRITICAL',
                'text': 'Significant facility modifications required before installation can proceed.'
            })
        
        # NeuViz specific recommendations
        if 'NeuViz' in scanner_model:
            recommendations.extend([
                {
                    'category': 'NeuViz Compliance',
                    'priority': 'CRITICAL',
                    'text': 'Ensure Neusoft engineer coordination is scheduled per NPS-CT-0651 requirements.'
                },
                {
                    'category': 'Environmental Control',
                    'priority': 'HIGH',
                    'text': 'Verify temperature stability ±4.1°C/h capability and 30-60% humidity range.'
                },
                {
                    'category': 'Electrical Requirements',
                    'priority': 'HIGH',
                    'text': 'Confirm 50kVA isolation transformer and proper grounding system installation.'
                }
            ])
        
        # Critical issues recommendations
        if critical_issues > 0:
            recommendations.append({
                'category': 'Critical Issues',
                'priority': 'CRITICAL',
                'text': f'{critical_issues} critical issues identified. Address before proceeding with installation.'
            })
        
        # Timeline recommendations
        installation_date = project_data.get('installation_date')
        if installation_date:
            try:
                install_date = datetime.strptime(installation_date, '%Y-%m-%d')
                days_until = (install_date - datetime.now()).days
                
                if days_until <= 30 and conformity_score < 85:
                    recommendations.append({
                        'category': 'Timeline Risk',
                        'priority': 'CRITICAL',
                        'text': 'Installation date approaching with outstanding compliance issues. Consider postponement.'
                    })
                elif days_until <= 60 and critical_issues > 0:
                    recommendations.append({
                        'category': 'Timeline Concern',
                        'priority': 'HIGH',
                        'text': 'Limited time available for addressing critical issues. Expedite modifications.'
                    })
            except:
                pass
        
        return recommendations[:8]  # Limit to 8 most important recommendations
    
    def get_engineer_workload_analysis(self, engineer_id):
        """Analyze engineer workload and capacity."""
        assigned_projects = self.get_assigned_projects(engineer_id)
        
        # Calculate current workload
        active_projects = [p for p in assigned_projects if p['status'] in ['IN_ANALYSIS', 'SUBMITTED']]
        
        # Estimate hours per project type
        project_hours = {
            'URGENT': 40,
            'HIGH': 30,
            'MEDIUM': 25,
            'LOW': 20
        }
        
        total_estimated_hours = sum(project_hours.get(p['priority'], 25) for p in active_projects)
        
        # Calculate capacity (assuming 40 hours/week, 75% utilization)
        weekly_capacity = 30  # hours
        weeks_to_complete = total_estimated_hours / weekly_capacity if weekly_capacity > 0 else 0
        
        # Identify bottlenecks
        bottlenecks = []
        urgent_count = len([p for p in active_projects if p['priority'] == 'URGENT'])
        if urgent_count > 3:
            bottlenecks.append('Too many urgent projects')
        
        if weeks_to_complete > 6:
            bottlenecks.append('Overloaded schedule')
        
        # Check for upcoming deadlines
        upcoming_deadlines = self.get_upcoming_deadlines(assigned_projects)
        critical_deadlines = [d for d in upcoming_deadlines if d['urgency'] == 'critical']
        if len(critical_deadlines) > 2:
            bottlenecks.append('Multiple critical deadlines')
        
        return {
            'active_projects_count': len(active_projects),
            'total_estimated_hours': total_estimated_hours,
            'weeks_to_complete': round(weeks_to_complete, 1),
            'capacity_utilization': min(100, round((total_estimated_hours / (weekly_capacity * 4)) * 100, 1)),
            'bottlenecks': bottlenecks,
            'recommendations': self.generate_workload_recommendations(weeks_to_complete, bottlenecks)
        }
    
    def generate_workload_recommendations(self, weeks_to_complete, bottlenecks):
        """Generate workload management recommendations."""
        recommendations = []
        
        if weeks_to_complete > 8:
            recommendations.append('Consider requesting additional engineering support')
        elif weeks_to_complete > 6:
            recommendations.append('Prioritize urgent projects and defer non-critical tasks')
        
        if 'Too many urgent projects' in bottlenecks:
            recommendations.append('Coordinate with project management to redistribute urgent projects')
        
        if 'Multiple critical deadlines' in bottlenecks:
            recommendations.append('Schedule additional hours or request deadline extensions where possible')
        
        if not recommendations:
            recommendations.append('Current workload is manageable within normal capacity')
        
        return recommendations
    
    def get_knowledge_base_suggestions(self, scanner_model, issue_keywords):
        """Get knowledge base suggestions for common issues."""
        suggestions = []
        
        # NeuViz specific knowledge
        if 'NeuViz' in scanner_model:
            neuViz_suggestions = [
                {
                    'title': 'NeuViz Temperature Requirements',
                    'content': 'Temperature stability ±4.1°C/h is critical for NeuViz operation',
                    'reference': 'NPS-CT-0651 Section 4.5.2'
                },
                {
                    'title': 'NeuViz Electrical Specifications',
                    'content': '50kVA isolation transformer mandatory, power factor ≥0.84',
                    'reference': 'NPS-CT-0651 Section 4.10'
                },
                {
                    'title': 'NeuViz Transport Requirements',
                    'content': 'Neusoft engineer mandatory for installation and transport',
                    'reference': 'NPS-CT-0651 Section 4.1'
                }
            ]
            suggestions.extend(neuViz_suggestions)
        
        # Issue-specific suggestions
        for keyword in issue_keywords:
            if 'shielding' in keyword.lower():
                suggestions.append({
                    'title': 'Radiation Shielding Guidelines',
                    'content': 'Primary barrier: 2.5mm Pb for NeuViz, 2.0mm Pb standard',
                    'reference': 'IEC 60601-2-44'
                })
            elif 'electrical' in keyword.lower():
                suggestions.append({
                    'title': 'Medical Electrical Safety',
                    'content': 'IT isolation transformer and equipotential bonding required',
                    'reference': 'NF C 15-211'
                })
            elif 'hvac' in keyword.lower():
                suggestions.append({
                    'title': 'HVAC Requirements',
                    'content': 'Precision air conditioning with continuous operation capability',
                    'reference': 'IEC 60601-2-44'
                })
        
        return suggestions[:5]  # Limit to 5 most relevant suggestions