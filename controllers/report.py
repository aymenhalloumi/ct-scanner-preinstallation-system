import json
import logging
from datetime import datetime
from controllers.project import Project
from controllers.authentification import Authentication
from config import SCANNER_SPECS, BIOMEDICAL_CONSTRAINTS, INSTALLATION_COSTS, REPORT_TEMPLATES

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Professional report generation for CT Scanner preinstallation analysis."""
    
    def __init__(self):
        self.project_manager = Project()
        self.auth_manager = Authentication()
        self.scanner_specs = SCANNER_SPECS
        self.biomedical_constraints = BIOMEDICAL_CONSTRAINTS
        self.installation_costs = INSTALLATION_COSTS
    
    def generate_report(self, project_id, report_type='DETAILED'):
        """Generate comprehensive analysis report."""
        try:
            project = self.project_manager.get_project(project_id)
            if not project:
                return None
            
            # Get client and engineer information
            client_info = self.auth_manager.get_user_by_id(project['client_id'])
            engineer_info = None
            if project['engineer_id']:
                engineer_info = self.auth_manager.get_user_by_id(project['engineer_id'])
            
            # Get analysis results
            analysis_results = project.get('analysis_results', {})
            
            # Generate report based on type
            if report_type == 'EXECUTIVE':
                return self.generate_executive_summary(project, client_info, engineer_info, analysis_results)
            elif report_type == 'NEUVIZ':
                return self.generate_neuViz_report(project, client_info, engineer_info, analysis_results)
            elif report_type == 'BASIC':
                return self.generate_basic_report(project, client_info, engineer_info, analysis_results)
            else:  # DETAILED
                return self.generate_detailed_report(project, client_info, engineer_info, analysis_results)
                
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None
    
    def generate_detailed_report(self, project, client_info, engineer_info, analysis_results):
        """Generate detailed technical report."""
        scanner_model = project['scanner_model']
        is_neuViz = 'NeuViz' in scanner_model
        
        report = {
            'report_type': 'DETAILED',
            'generation_date': datetime.now().isoformat(),
            'project_info': self.format_project_info(project, client_info),
            'executive_summary': self.create_executive_summary(project, analysis_results),
            'technical_analysis': self.create_technical_analysis(project, analysis_results),
            'compliance_matrix': self.create_compliance_matrix(project, analysis_results),
            'cost_analysis': self.create_cost_analysis(analysis_results),
            'risk_assessment': self.create_risk_assessment(project, analysis_results),
            'recommendations': self.create_recommendations(project, analysis_results),
            'implementation_plan': self.create_implementation_plan(project, analysis_results),
            'appendices': self.create_appendices(project, analysis_results),
            'certifications': self.create_certification_section(engineer_info),
            'neuViz_compliance': self.create_neuViz_section(project, analysis_results) if is_neuViz else None
        }
        
        return report
    
    def generate_executive_summary(self, project, client_info, engineer_info, analysis_results):
        """Generate executive summary report."""
        report = {
            'report_type': 'EXECUTIVE',
            'generation_date': datetime.now().isoformat(),
            'project_info': self.format_project_info(project, client_info),
            'key_findings': self.create_key_findings(analysis_results),
            'financial_summary': self.create_financial_summary(analysis_results),
            'timeline_summary': self.create_timeline_summary(project, analysis_results),
            'decision_matrix': self.create_decision_matrix(analysis_results),
            'next_steps': self.create_next_steps(project, analysis_results),
            'executive_recommendations': self.create_executive_recommendations(analysis_results)
        }
        
        return report
    
    def generate_neuViz_report(self, project, client_info, engineer_info, analysis_results):
        """Generate NeuViz-specific compliance report."""
        report = {
            'report_type': 'NEUVIZ',
            'generation_date': datetime.now().isoformat(),
            'compliance_document': 'NPS-CT-0651 Rev.B',
            'project_info': self.format_project_info(project, client_info),
            'neuViz_compliance_summary': self.create_neuViz_compliance_summary(analysis_results),
            'nps_ct_0651_checklist': self.create_nps_checklist(project, analysis_results),
            'neusoft_coordination': self.create_neusoft_coordination_plan(project),
            'environmental_specifications': self.create_neuViz_environmental_specs(analysis_results),
            'electrical_specifications': self.create_neuViz_electrical_specs(analysis_results),
            'transport_requirements': self.create_transport_requirements(project),
            'installation_timeline': self.create_neuViz_timeline(project, analysis_results),
            'cost_breakdown': self.create_neuViz_cost_breakdown(analysis_results),
            'critical_requirements': self.create_neuViz_critical_requirements(analysis_results)
        }
        
        return report
    
    def generate_basic_report(self, project, client_info, engineer_info, analysis_results):
        """Generate basic compliance report."""
        report = {
            'report_type': 'BASIC',
            'generation_date': datetime.now().isoformat(),
            'project_info': self.format_project_info(project, client_info),
            'compliance_status': self.create_basic_compliance_status(analysis_results),
            'major_findings': self.create_major_findings(analysis_results),
            'cost_estimate': self.create_basic_cost_estimate(analysis_results),
            'action_items': self.create_basic_action_items(analysis_results),
            'approval_status': self.create_approval_status(analysis_results)
        }
        
        return report
    
    def format_project_info(self, project, client_info):
        """Format project information section."""
        return {
            'project_id': project['id'],
            'project_name': project['project_name'],
            'facility_name': project['facility_name'],
            'scanner_model': project['scanner_model'],
            'installation_date': project['installation_date'],
            'client_information': {
                'name': project['contact_person'],
                'company': client_info.get('company', '') if client_info else '',
                'email': project['email'],
                'phone': project['phone']
            },
            'facility_details': {
                'address': project['address'],
                'facility_type': project.get('project_data', {}).get('facility_type', 'Hospital'),
                'project_priority': project['priority']
            },
            'analysis_date': project['last_updated'],
            'project_status': project['status']
        }
    
    def create_executive_summary(self, project, analysis_results):
        """Create executive summary section."""
        conformity_score = analysis_results.get('conformity_score', 0)
        critical_issues = analysis_results.get('critical_issues', 0)
        
        status_text = "APPROVED" if conformity_score >= 85 else "CONDITIONAL" if conformity_score >= 70 else "NOT APPROVED"
        
        return {
            'overall_assessment': status_text,
            'conformity_score': conformity_score,
            'compliance_percentage': f"{conformity_score}%",
            'critical_issues_count': critical_issues,
            'installation_feasibility': "Feasible" if conformity_score >= 70 else "Requires major modifications",
            'key_challenges': self.extract_key_challenges(analysis_results),
            'major_cost_impacts': self.extract_major_costs(analysis_results),
            'timeline_impact': analysis_results.get('timeline', 'TBD'),
            'recommendation_summary': self.create_recommendation_summary(conformity_score, critical_issues)
        }
    
    def create_technical_analysis(self, project, analysis_results):
        """Create detailed technical analysis section."""
        scanner_model = project['scanner_model']
        constraints = self.scanner_specs.get(scanner_model, {})
        
        return {
            'scanner_specifications': {
                'model': scanner_model,
                'manufacturer': constraints.get('manufacturer', 'Unknown'),
                'weight': f"{constraints.get('weight', 0)} kg",
                'dimensions': constraints.get('dimensions', 'N/A'),
                'power_requirements': constraints.get('required_power', 'N/A'),
                'minimum_room_size': f"{constraints.get('min_length', 0)} x {constraints.get('min_width', 0)} x {constraints.get('min_height', 0)} m"
            },
            'facility_analysis': {
                'dimensional_compliance': self.analyze_dimensional_compliance(analysis_results),
                'structural_compliance': self.analyze_structural_compliance(analysis_results),
                'electrical_compliance': self.analyze_electrical_compliance(analysis_results),
                'environmental_compliance': self.analyze_environmental_compliance(analysis_results),
                'safety_compliance': self.analyze_safety_compliance(analysis_results)
            },
            'gap_analysis': self.create_gap_analysis(analysis_results),
            'technical_recommendations': self.create_technical_recommendations(analysis_results)
        }
    
    def create_compliance_matrix(self, project, analysis_results):
        """Create compliance matrix showing conformity status."""
        compliance_areas = [
            'Dimensional Requirements',
            'Structural Requirements',
            'Electrical Safety',
            'Radiation Protection',
            'Environmental Control',
            'Fire Safety',
            'Network Infrastructure',
            'Workflow Design'
        ]
        
        matrix = []
        for area in compliance_areas:
            status = self.determine_compliance_status(area, analysis_results)
            matrix.append({
                'requirement_area': area,
                'status': status['status'],
                'score': status['score'],
                'issues': status['issues'],
                'actions_required': status['actions']
            })
        
        return matrix
    
    def create_cost_analysis(self, analysis_results):
        """Create detailed cost analysis section."""
        cost_breakdown = analysis_results.get('cost_breakdown', [])
        total_cost = sum(item[1] for item in cost_breakdown if isinstance(item, (list, tuple)) and len(item) >= 2)
        
        # Categorize costs
        categories = {
            'Infrastructure': [],
            'Electrical': [],
            'Safety Systems': [],
            'Environmental': [],
            'Specialized Services': [],
            'Other': []
        }
        
        for item in cost_breakdown:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                category = self.categorize_cost_item(item[0])
                categories[category].append({
                    'description': item[0],
                    'cost': item[1],
                    'percentage': round((item[1] / total_cost) * 100, 1) if total_cost > 0 else 0
                })
        
        return {
            'total_estimated_cost': total_cost,
            'cost_by_category': categories,
            'cost_distribution': self.calculate_cost_distribution(categories),
            'contingency_analysis': self.create_contingency_analysis(total_cost),
            'financing_options': self.suggest_financing_options(total_cost),
            'cost_optimization': self.suggest_cost_optimizations(cost_breakdown)
        }
    
    def create_risk_assessment(self, project, analysis_results):
        """Create risk assessment section."""
        risks = []
        
        # Technical risks
        conformity_score = analysis_results.get('conformity_score', 0)
        if conformity_score < 70:
            risks.append({
                'category': 'Technical',
                'risk': 'Low conformity score may delay installation',
                'probability': 'High',
                'impact': 'High',
                'mitigation': 'Address critical non-conformities immediately'
            })
        
        # Timeline risks
        installation_date = project.get('installation_date')
        if installation_date:
            try:
                install_date = datetime.strptime(installation_date, '%Y-%m-%d')
                days_until = (install_date - datetime.now()).days
                if days_until <= 60:
                    risks.append({
                        'category': 'Timeline',
                        'risk': 'Insufficient time for major modifications',
                        'probability': 'Medium',
                        'impact': 'High',
                        'mitigation': 'Consider installation date adjustment'
                    })
            except:
                pass
        
        # Cost risks
        total_cost = analysis_results.get('total_cost', 0)
        if isinstance(total_cost, str):
            total_cost = float(total_cost.replace(',', '').replace('€', '').replace(' ', ''))
        
        if total_cost > 150000:
            risks.append({
                'category': 'Financial',
                'risk': 'High modification costs may exceed budget',
                'probability': 'Medium',
                'impact': 'High',
                'mitigation': 'Explore alternative solutions and phased implementation'
            })
        
        # NeuViz specific risks
        if 'NeuViz' in project['scanner_model']:
            risks.append({
                'category': 'Coordination',
                'risk': 'Neusoft engineer availability may impact timeline',
                'probability': 'Low',
                'impact': 'Medium',
                'mitigation': 'Coordinate with Neusoft early in project timeline'
            })
        
        return {
            'risk_summary': f"{len(risks)} risks identified",
            'high_priority_risks': [r for r in risks if r['impact'] == 'High'],
            'all_risks': risks,
            'risk_mitigation_plan': self.create_risk_mitigation_plan(risks)
        }
    
    def create_recommendations(self, project, analysis_results):
        """Create recommendations section."""
        conformity_score = analysis_results.get('conformity_score', 0)
        critical_issues = analysis_results.get('critical_issues', 0)
        action_items = analysis_results.get('action_items', [])
        
        recommendations = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'optional_improvements': []
        }
        
        # Categorize action items by priority and timeline
        for item in action_items:
            priority = item.get('priority', 'MEDIUM')
            
            if priority == 'CRITIQUE':
                recommendations['immediate_actions'].append(item)
            elif priority == 'ÉLEVÉ':
                recommendations['short_term_actions'].append(item)
            else:
                recommendations['long_term_actions'].append(item)
        
        # Add general recommendations based on conformity score
        if conformity_score >= 85:
            recommendations['optional_improvements'].append({
                'text': 'Consider future-proofing upgrades for enhanced performance',
                'category': 'Enhancement',
                'estimated_benefit': 'Improved long-term reliability'
            })
        
        return recommendations
    
    def create_implementation_plan(self, project, analysis_results):
        """Create implementation plan section."""
        timeline = analysis_results.get('timeline', '8-12')
        
        # Parse timeline
        try:
            if '-' in timeline:
                min_weeks, max_weeks = map(int, timeline.split('-'))
            else:
                min_weeks = max_weeks = int(timeline.split()[0])
        except:
            min_weeks, max_weeks = 8, 12
        
        phases = [
            {
                'phase': 'Planning and Permits',
                'duration': '2-3 weeks',
                'description': 'Obtain necessary permits and finalize detailed plans',
                'dependencies': 'Approved analysis report'
            },
            {
                'phase': 'Infrastructure Modifications',
                'duration': f'{min_weeks-4}-{max_weeks-4} weeks',
                'description': 'Implement structural, electrical, and environmental modifications',
                'dependencies': 'Permits obtained, contractors selected'
            },
            {
                'phase': 'Safety Systems Installation',
                'duration': '2-3 weeks',
                'description': 'Install radiation shielding, fire safety, and monitoring systems',
                'dependencies': 'Infrastructure work completed'
            },
            {
                'phase': 'Testing and Commissioning',
                'duration': '1-2 weeks',
                'description': 'Test all systems and obtain final certifications',
                'dependencies': 'All installations completed'
            }
        ]
        
        # Add NeuViz specific phases
        if 'NeuViz' in project['scanner_model']:
            phases.insert(-1, {
                'phase': 'Neusoft Coordination',
                'duration': '1 week',
                'description': 'Coordinate with Neusoft engineer for installation preparation',
                'dependencies': 'Infrastructure ready for scanner installation'
            })
        
        return {
            'total_duration': f'{min_weeks}-{max_weeks} weeks',
            'implementation_phases': phases,
            'critical_path': self.identify_critical_path(phases),
            'resource_requirements': self.define_resource_requirements(analysis_results),
            'quality_checkpoints': self.define_quality_checkpoints(phases)
        }
    
    def create_appendices(self, project, analysis_results):
        """Create appendices section."""
        return {
            'regulatory_references': self.compile_regulatory_references(project),
            'technical_specifications': self.compile_technical_specifications(project),
            'vendor_information': self.compile_vendor_information(project),
            'calculation_details': self.compile_calculation_details(analysis_results),
            'photographs_and_diagrams': self.compile_visual_documentation(project)
        }
    
    def create_certification_section(self, engineer_info):
        """Create certification and validation section."""
        return {
            'analyzing_engineer': {
                'name': engineer_info.get('username', 'Unknown') if engineer_info else 'System Generated',
                'credentials': 'Certified Biomedical Engineer',
                'specializations': ['CT Scanner Installation', 'Medical Device Compliance'],
                'certification_number': 'BME-2025-001'
            },
            'validation_standards': [
                'IEC 60601-2-44 (Medical electrical equipment - CT scanners)',
                'NF C 15-211 (Medical electrical installations)',
                'ANSM Guidelines (Medical device installations)',
                'Local building codes and regulations'
            ],
            'report_validity': '12 months from generation date',
            'revision_tracking': {
                'version': '1.0',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'changes': 'Initial analysis report'
            }
        }
    
    def create_neuViz_section(self, project, analysis_results):
        """Create NeuViz-specific compliance section."""
        return {
            'nps_ct_0651_compliance': {
                'document_version': 'Rev.B',
                'compliance_status': 'Under Review',
                'mandatory_requirements': self.list_neuViz_mandatory_requirements(),
                'compliance_checklist': self.create_neuViz_checklist(analysis_results)
            },
            'neusoft_coordination': {
                'engineer_required': True,
                'coordination_timeline': 'Must be scheduled 4 weeks before installation',
                'contact_information': 'To be provided by Neusoft Medical Systems'
            },
            'special_considerations': {
                'temperature_stability': '±4.1°C/h maximum variation',
                'humidity_range': '30-60% RH (wider than standard 40-60%)',
                'fire_suppression': 'Water-based systems NOT recommended',
                'transport_requirements': 'Wooden crates with pallets - do not separate'
            }
        }
    
    # Helper methods for specific report sections
    
    def extract_key_challenges(self, analysis_results):
        """Extract key challenges from analysis results."""
        penalties = analysis_results.get('penalties', [])
        return penalties[:3] if penalties else ['No major challenges identified']
    
    def extract_major_costs(self, analysis_results):
        """Extract major cost impacts."""
        cost_breakdown = analysis_results.get('cost_breakdown', [])
        major_costs = []
        
        for item in cost_breakdown:
            if isinstance(item, (list, tuple)) and len(item) >= 2 and item[1] > 10000:
                major_costs.append(f"{item[0]}: {item[1]:,} €")
        
        return major_costs[:3] if major_costs else ['No major cost impacts identified']
    
    def create_recommendation_summary(self, conformity_score, critical_issues):
        """Create summary recommendation."""
        if conformity_score >= 85:
            return "Proceed with installation as planned"
        elif conformity_score >= 70:
            return "Proceed with specified modifications"
        else:
            return "Major facility modifications required before installation"
    
    def categorize_cost_item(self, description):
        """Categorize cost items for analysis."""
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ['électrique', 'alimentation', 'transformateur']):
            return 'Electrical'
        elif any(keyword in description_lower for keyword in ['blindage', 'radioprotection', 'plomb']):
            return 'Safety Systems'
        elif any(keyword in description_lower for keyword in ['cvc', 'climatisation', 'ventilation']):
            return 'Environmental'
        elif any(keyword in description_lower for keyword in ['structure', 'sol', 'renforcement']):
            return 'Infrastructure'
        elif any(keyword in description_lower for keyword in ['neusoft', 'ingénieur', 'transport']):
            return 'Specialized Services'
        else:
            return 'Other'
    
    def list_neuViz_mandatory_requirements(self):
        """List mandatory NeuViz requirements from NPS-CT-0651."""
        return [
            'Room dimensions: 6.5m x 4.2m x 2.43m minimum',
            'Isolation transformer: 50kVA minimum',
            'Temperature stability: ±4.1°C/hour maximum',
            'Humidity range: 30-60% RH',
            'Neusoft engineer coordination mandatory',
            'Primary shielding: 2.5mm Pb minimum',
            'Grounding: ≤4Ω independent or ≤1Ω common',
            'Floor capacity: ≥1000 kg/m²'
        ]
    
    def create_neuViz_checklist(self, analysis_results):
        """Create NeuViz compliance checklist."""
        # This would be populated based on actual analysis data
        return {
            'dimensional_compliance': 'Pending verification',
            'electrical_compliance': 'Pending verification',
            'environmental_compliance': 'Pending verification',
            'transport_readiness': 'Pending coordination',
            'engineer_coordination': 'Not scheduled',
            'documentation_complete': 'In progress'
        }