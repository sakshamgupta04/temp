"""
Simplified Retention Risk Scorer
Rule-based system for immediate deployment
Predicts retention likelihood without requiring ML training data
"""

from typing import Dict, Any, List

class RetentionScorer:
    """
    Calculate retention risk based on multiple factors
    Uses research-backed indicators without requiring ML training
    """
    
    def __init__(self):
        self.risk_categories = {
            'Low': 'Low Risk - High retention likelihood',
            'Medium': 'Medium Risk - Monitor and support',
            'High': 'High Risk - Intervention recommended'
        }
    
    def calculate_job_stability_score(self, candidate_data: Dict[str, Any]) -> float:
        """
        Calculate job stability indicator (0-100)
        Based on tenure and job changes
        """
        longevity = candidate_data.get('longevity_years', 0)
        unique_jobs = candidate_data.get('number_of_unique_designations', 1)
        
        # Average tenure per job
        avg_tenure = longevity / max(unique_jobs, 1)
        
        # Scoring logic
        if avg_tenure >= 4:  # Very stable (4+ years per job)
            stability = 100
        elif avg_tenure >= 2.5:  # Stable (2.5-4 years)
            stability = 80
        elif avg_tenure >= 1.5:  # Moderate (1.5-2.5 years)
            stability = 60
        elif avg_tenure >= 1:  # Concerning (1-1.5 years)
            stability = 40
        else:  # High risk (<1 year per job)
            stability = 20
        
        return stability
    
    def calculate_personality_retention_score(self, big5_scores: Dict[str, int]) -> float:
        """
        Calculate retention likelihood from personality (0-100)
        Research shows Conscientiousness and Agreeableness are PRIMARY predictors
        """
        # Extract scores (0-40 range from your Big5 test)
        conscientiousness = big5_scores.get('conscientiousness', 20)
        agreeableness = big5_scores.get('agreeableness', 20)
        neuroticism = big5_scores.get('neuroticism', 20)
        
        # Normalize to 0-100
        conscientiousness_norm = (conscientiousness / 40) * 100
        agreeableness_norm = (agreeableness / 40) * 100
        neuroticism_norm = ((40 - neuroticism) / 40) * 100  # Inverted (low = good)
        
        # Weighted combination (research-based weights)
        personality_retention = (
            conscientiousness_norm * 0.50 +  # 50% - Most important
            agreeableness_norm * 0.35 +      # 35% - Second most important  
            neuroticism_norm * 0.15           # 15% - Emotional stability
        )
        
        return personality_retention
    
    def calculate_engagement_score(self, candidate_data: Dict[str, Any]) -> float:
        """
        Calculate professional engagement indicator (0-100)
        Based on development activities and achievements
        """
        workshops = candidate_data.get('workshops', 0)
        trainings = candidate_data.get('trainings', 0)
        papers = candidate_data.get('total_papers', 0)
        patents = candidate_data.get('total_patents', 0)
        achievements = candidate_data.get('achievements', 0)
        experience = candidate_data.get('average_experience', 1)
        
        # Calculate activity rate (normalized by experience)
        activity_rate = (workshops + trainings + papers*2 + patents*3 + achievements) / max(experience, 1)
        
        # Scoring
        if activity_rate >= 5:  # Highly engaged
            engagement = 100
        elif activity_rate >= 3:  # Very engaged
            engagement = 85
        elif activity_rate >= 2:  # Engaged
            engagement = 70
        elif activity_rate >= 1:  # Moderately engaged
            engagement = 55
        else:  # Low engagement
            engagement = 40
        
        return engagement
    
    def calculate_fitment_factor(self, fitment_score: float, category: str) -> float:
        """
        Adjust retention based on fitment score and category
        Higher fitment = higher retention likelihood
        """
        # Category-specific thresholds
        if category == 'Experienced':
            if fitment_score >= 75:
                return 100
            elif fitment_score >= 60:
                return 80
            elif fitment_score >= 45:
                return 60
            else:
                return 40
        else:  # Fresher/Inexperienced
            if fitment_score >= 70:
                return 100
            elif fitment_score >= 55:
                return 80
            elif fitment_score >= 40:
                return 60
            else:
                return 40
    
    def identify_risk_flags(self, candidate_data: Dict[str, Any], 
                           big5_scores: Dict[str, int]) -> List[str]:
        """
        Identify specific retention risk flags
        """
        flags = []
        
        # Job hopping
        unique_jobs = candidate_data.get('number_of_unique_designations', 0)
        longevity = candidate_data.get('longevity_years', 0)
        if unique_jobs >= 4 and longevity / max(unique_jobs, 1) < 1.5:
            flags.append('Job Hopper Pattern')
        
        # Low engagement
        workshops = candidate_data.get('workshops', 0)
        trainings = candidate_data.get('trainings', 0)
        if workshops + trainings < 2:
            flags.append('Low Professional Development')
        
        # Low conscientiousness (major retention predictor)
        conscientiousness = big5_scores.get('conscientiousness', 20)
        if conscientiousness < 20:
            flags.append('Low Conscientiousness (Retention Risk)')
        
        # High neuroticism
        neuroticism = big5_scores.get('neuroticism', 20)
        if neuroticism > 30:
            flags.append('High Emotional Instability')
        
        # Low fitment
        fitment = candidate_data.get('fitment_score', 0)
        if fitment < 45:
            flags.append('Low Overall Fitment')
        
        # Short average tenure
        avg_tenure = longevity / max(unique_jobs, 1)
        if avg_tenure < 1.5:
            flags.append('Short Average Tenure')
        
        return flags
    
    def generate_retention_insights(self, retention_data: Dict[str, Any]) -> List[str]:
        """
        Generate actionable insights based on retention analysis
        """
        insights = []
        risk_level = retention_data['retention_risk']
        risk_score = retention_data['retention_score']
        flags = retention_data['risk_flags']
        
        # Risk-based recommendations
        if risk_level == 'High':
            insights.append("⚠️ HIGH RETENTION RISK - Immediate intervention recommended")
            insights.append("→ Consider structured onboarding and mentorship program")
            insights.append("→ Schedule regular check-ins (bi-weekly for first 6 months)")
            insights.append("→ Assess role fit and career development opportunities")
            
        elif risk_level == 'Medium':
            insights.append("⚡ MEDIUM RETENTION RISK - Active monitoring advised")
            insights.append("→ Provide clear career progression path")
            insights.append("→ Encourage participation in professional development")
            insights.append("→ Monthly check-ins to assess satisfaction")
            
        else:  # Low risk
            insights.append("✅ LOW RETENTION RISK - Strong retention indicators")
            insights.append("→ Leverage for team stability and mentorship roles")
            insights.append("→ Consider for long-term projects and leadership development")
        
        # Flag-specific insights
        if 'Job Hopper Pattern' in flags:
            insights.append("→ Address: Frequent job changes - Discuss long-term goals early")
        
        if 'Low Professional Development' in flags:
            insights.append("→ Address: Limited development activities - Offer training stipend")
        
        if 'Low Conscientiousness (Retention Risk)' in flags:
            insights.append("→ Address: May need structured environment and clear expectations")
        
        if 'High Emotional Instability' in flags:
            insights.append("→ Address: May benefit from wellness programs and stress management")
        
        if 'Low Overall Fitment' in flags:
            insights.append("→ Address: Poor role match - Consider alternative positions")
        
        # Score-based insights
        if risk_score < 50:
            insights.append("→ Priority: High - Requires immediate attention and support")
        elif risk_score < 65:
            insights.append("→ Priority: Medium - Regular monitoring and engagement needed")
        else:
            insights.append("→ Priority: Low - Standard engagement practices sufficient")
        
        return insights
    
    def calculate_retention_risk(self, candidate_data: Dict[str, Any],
                                 fitment_score: float,
                                 big5_scores: Dict[str, int],
                                 category: str) -> Dict[str, Any]:
        """
        Calculate comprehensive retention risk assessment
        
        Returns:
            Dictionary with retention score, risk level, factors, and insights
        """
        # Calculate component scores
        stability_score = self.calculate_job_stability_score(candidate_data)
        personality_score = self.calculate_personality_retention_score(big5_scores)
        engagement_score = self.calculate_engagement_score(candidate_data)
        fitment_factor = self.calculate_fitment_factor(fitment_score, category)
        
        # Weighted retention score (0-100)
        # Weights based on retention research
        retention_score = (
            stability_score * 0.30 +      # 30% - Job history
            personality_score * 0.35 +    # 35% - Personality (strongest predictor)
            engagement_score * 0.20 +     # 20% - Professional engagement
            fitment_factor * 0.15         # 15% - Overall fitment
        )
        
        # Determine risk category
        if retention_score >= 70:
            risk_level = 'Low'
        elif retention_score >= 50:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        # Identify risk flags
        risk_flags = self.identify_risk_flags(candidate_data, big5_scores)
        
        # Compile results
        result = {
            'retention_score': round(retention_score, 2),
            'retention_risk': risk_level,
            'risk_description': self.risk_categories[risk_level],
            'component_scores': {
                'stability': round(stability_score, 2),
                'personality': round(personality_score, 2),
                'engagement': round(engagement_score, 2),
                'fitment_factor': round(fitment_factor, 2)
            },
            'risk_flags': risk_flags,
            'flag_count': len(risk_flags)
        }
        
        # Generate insights
        result['insights'] = self.generate_retention_insights(result)
        
        return result
    
    def get_retention_summary(self, retention_data: Dict[str, Any]) -> str:
        """
        Generate human-readable summary
        """
        score = retention_data['retention_score']
        risk = retention_data['retention_risk']
        flags = retention_data['flag_count']
        
        summary = f"""
RETENTION ANALYSIS SUMMARY
{'='*50}
Retention Score: {score}/100
Risk Level: {risk}
Risk Flags: {flags}

{retention_data['risk_description']}

COMPONENT BREAKDOWN:
• Job Stability: {retention_data['component_scores']['stability']}/100
• Personality Fit: {retention_data['component_scores']['personality']}/100
• Professional Engagement: {retention_data['component_scores']['engagement']}/100
• Fitment Factor: {retention_data['component_scores']['fitment_factor']}/100

RISK FLAGS:
"""
        
        if retention_data['risk_flags']:
            for flag in retention_data['risk_flags']:
                summary += f"  ⚠ {flag}\n"
        else:
            summary += "  ✓ No significant risk flags identified\n"
        
        summary += "\nRECOMMENDATIONS:\n"
        for insight in retention_data['insights'][:5]:  # Top 5
            summary += f"  {insight}\n"
        
        return summary