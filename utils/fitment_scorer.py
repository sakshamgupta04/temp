import pandas as pd
import numpy as np
from typing import Dict, Any

class FitmentScorer:
    """Calculate fitment score based on candidate data"""
    
    @staticmethod
    def categorize_candidate(longevity_years: float, average_experience: float) -> str:
        """Determine candidate category"""
        if (longevity_years >= 5) and (average_experience >= 3):
            return "Experienced"
        elif (longevity_years > 1) and (average_experience > 1):
            return "Inexperienced"
        else:
            return "Fresher"
    
    @staticmethod
    def score_longevity(val: float) -> float:
        if val >= 6: return 100
        elif val >= 4: return 75
        elif val >= 1: return 50
        else: return 20
    
    @staticmethod
    def score_avg_exp(val: float) -> float:
        if val >= 3: return 100
        elif val >= 1.8: return 75
        elif val >= 1: return 50
        else: return 20
    
    @staticmethod
    def score_workshops(val: int) -> float:
        if val >= 12.73: return 100
        elif val >= 7: return 75
        elif val >= 3: return 50
        else: return 20
    
    @staticmethod
    def score_trainings(val: int) -> float:
        if val >= 12.90: return 100
        elif val >= 7: return 75
        elif val >= 3: return 50
        else: return 20
    
    @staticmethod
    def score_papers(val: int) -> float:
        if val >= 1.18: return 100
        elif val >= 0.5: return 75
        elif val >= 0.2: return 50
        else: return 0
    
    @staticmethod
    def score_patents(val: int) -> float:
        return 100 if val >= 0.04 else 0
    
    @staticmethod
    def score_achievements(val: int) -> float:
        if val >= 7.54: return 100
        elif val >= 4: return 75
        elif val >= 1: return 50
        else: return 0
    
    @staticmethod
    def score_books(val: int) -> float:
        return 100 if val >= 0.81 else 0
    
    @staticmethod
    def score_state(val: int) -> float:
        return 100 if val == 1 else 0
    
    @staticmethod
    def score_jobs(val: int) -> float:
        return 100 if val >= 0.17 else 0
    
    @staticmethod
    def score_institute(val: int) -> float:
        return 100 if val == 1 else 0
    
    def calculate_dataset_score(self, data: Dict[str, Any]) -> float:
        """Calculate raw dataset score (0-100)"""
        
        scores = {}
        scores['longevity'] = self.score_longevity(data['longevity_years']) * 0.30
        scores['avg_exp'] = self.score_avg_exp(data['average_experience']) * 0.30
        scores['workshops'] = self.score_workshops(data['workshops']) * 0.045
        scores['trainings'] = self.score_trainings(data['trainings']) * 0.045
        scores['papers'] = self.score_papers(data['total_papers']) * 0.05
        scores['patents'] = self.score_patents(data['total_patents']) * 0.07
        scores['achievements'] = self.score_achievements(data['achievements']) * 0.04
        scores['books'] = self.score_books(data['books']) * 0.02
        scores['state'] = self.score_state(data['state_jk']) * 0.02
        scores['jobs'] = self.score_jobs(data['number_of_unique_designations']) * 0.01
        scores['ug'] = self.score_institute(data['ug_institute']) * 0.02
        scores['pg'] = self.score_institute(data['pg_institute']) * 0.03
        scores['phd'] = self.score_institute(data['phd_institute']) * 0.05
        
        return sum(scores.values())
    
    def scale_dataset_score(self, raw_score: float, category: str) -> float:
        """Scale dataset score based on category"""
        if category == "Experienced":
            return (raw_score / 100) * 70
        else:  # Inexperienced & Fresher
            return (raw_score / 100) * 30
    
    def calculate_big5_score(self, big5_data: Dict[str, float], category: str) -> Dict[str, float]:
        """Calculate Big Five personality score"""
        
        scores = {}
        
        # Openness
        O = big5_data.get('openness', 0)
        if O <= 10: scores['O'] = 0.25
        elif O <= 20: scores['O'] = 0.50
        elif O <= 30: scores['O'] = 0.75
        else: scores['O'] = 1.0
        
        # Conscientiousness
        C = big5_data.get('conscientiousness', 0)
        if C <= 10: scores['C'] = 0.25
        elif C <= 20: scores['C'] = 0.50
        elif C <= 30: scores['C'] = 0.75
        else: scores['C'] = 1.0
        
        # Extraversion
        E = big5_data.get('extraversion', 0)
        if E <= 10: scores['E'] = 0.50
        elif E <= 20: scores['E'] = 0.75
        elif E <= 30: scores['E'] = 1.0
        else: scores['E'] = 0.75
        
        # Agreeableness
        A = big5_data.get('agreeableness', 0)
        if A <= 10: scores['A'] = 0.25
        elif A <= 20: scores['A'] = 0.50
        elif A <= 30: scores['A'] = 1.0
        else: scores['A'] = 0.75
        
        # Neuroticism (reverse scored)
        N = big5_data.get('neuroticism', 0)
        if N <= 10: scores['N'] = 1.0
        elif N <= 20: scores['N'] = 0.75
        elif N <= 30: scores['N'] = 0.50
        else: scores['N'] = 0.25
        
        # Weight per trait based on category
        if category == "Experienced":
            weight_per_trait = 30 / 5
        else:
            weight_per_trait = 70 / 5
        
        # Total Big5 score
        big5_total = sum(v * weight_per_trait for v in scores.values())
        
        return {
            'trait_scores': scores,
            'total_score': big5_total,
            'weight_per_trait': weight_per_trait
        }
    
    def calculate_overall_fitment(self, candidate_data: Dict[str, Any], 
                                   big5_data: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Calculate complete fitment score for a candidate
        
        Args:
            candidate_data: Dictionary with parsed resume data
            big5_data: Dictionary with Big5 personality scores (optional for now)
        
        Returns:
            Dictionary with all scores and category
        """
        
        # Determine category
        category = self.categorize_candidate(
            candidate_data['longevity_years'],
            candidate_data['average_experience']
        )
        
        # Calculate raw dataset score
        raw_dataset_score = self.calculate_dataset_score(candidate_data)
        
        # Scale dataset score
        fitment_score = self.scale_dataset_score(raw_dataset_score, category)
        
        # Calculate Big5 score (placeholder if not provided)
        if big5_data is None:
            # For now, use neutral values (will be replaced with actual personality test)
            big5_data = {
                'openness': 25,
                'conscientiousness': 25,
                'extraversion': 25,
                'agreeableness': 25,
                'neuroticism': 25
            }
        
        big5_result = self.calculate_big5_score(big5_data, category)
        big5_score = big5_result['total_score']
        
        # Overall fitment score
        overall_score = fitment_score + big5_score
        
        return {
            'category': category,
            'raw_dataset_score': round(raw_dataset_score, 2),
            'fitment_score': round(fitment_score, 2),
            'big5_score': round(big5_score, 2),
            'big5_trait_scores': big5_result['trait_scores'],
            'overall_fitment_score': round(overall_score, 2),
            'breakdown': {
                'dataset_contribution': f"{fitment_score:.2f} ({'70%' if category == 'Experienced' else '30%'} weight)",
                'big5_contribution': f"{big5_score:.2f} ({'30%' if category == 'Experienced' else '70%'} weight)"
            }
        }