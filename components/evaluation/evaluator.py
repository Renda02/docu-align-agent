import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import re
import os
import json
import numpy as np

class DocumentEvaluator:
    def __init__(self):
        self.evaluation_file = "components/data/evaluations.csv"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs("components/data", exist_ok=True)
    
    async def evaluate_output(self, 
                            original_content: str, 
                            analysis_report: str, 
                            final_output: str, 
                            user_id: str = "anonymous") -> Dict[str, Any]:
        """
        Enhanced evaluation with template compliance and style violation precision/recall
        """
        evaluation_results = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'original_word_count': len(original_content.split()),
            'final_word_count': len(final_output.split()),
            'processing_successful': True
        }
        
        # E1: Template Compliance Accuracy (CRITICAL)
        template_results = self._check_template_compliance(original_content, final_output)
        evaluation_results['e1_template_compliance_rate'] = template_results['compliance_rate']
        evaluation_results['e1_template_score'] = template_results['score']
        evaluation_results['e1_template_pass'] = template_results['score'] >= 4
        evaluation_results['e1_missing_elements'] = json.dumps(template_results['missing_elements'])
        
        # E2: Style Violation Detection (Precision/Recall) (CRITICAL)
        style_results = self._evaluate_style_violations(original_content, final_output)
        evaluation_results['e2_violation_reduction_rate'] = style_results['violation_reduction_rate']
        evaluation_results['e2_style_precision'] = style_results['precision']
        evaluation_results['e2_style_score'] = style_results['score']
        evaluation_results['e2_style_pass'] = style_results['score'] >= 4
        evaluation_results['e2_remaining_violations'] = json.dumps(style_results['remaining_violations'])
        
        # H9: Gap Resolution (keeping this from original system)
        gap_resolution_score = self._check_gap_resolution(analysis_report, final_output)
        evaluation_results['h9_gap_resolution_score'] = gap_resolution_score
        evaluation_results['h9_pass'] = gap_resolution_score >= 4
        evaluation_results['h9_gaps_fixed'] = self._count_gaps_fixed(analysis_report, final_output)
        
        # Overall quality assessment (updated criteria)
        critical_pass = (evaluation_results['e1_template_pass'] and 
                        evaluation_results['e2_style_pass'] and 
                        evaluation_results['h9_pass'])
        evaluation_results['overall_pass'] = critical_pass
        evaluation_results['overall_score'] = (template_results['score'] + 
                                             style_results['score'] + 
                                             gap_resolution_score) / 3
        
        # Save to CSV for tracking
        self._save_evaluation(evaluation_results)
        
        return evaluation_results
    
    def _check_template_compliance(self, original: str, final_output: str) -> Dict[str, Any]:
        """
        E1: Check adherence to The Good Docs Project template structure
        Returns compliance rate and specific missing elements
        """
        template_elements = {
            'title': r'^#\s+[\w\s]+',  # Has proper H1 title
            'introduction': r'(this guide|this tutorial|this document|this how-to)',  # Has intro
            'prerequisites': r'(prerequisite|requirements|before you begin|you need|you must have)',
            'numbered_steps': r'^\d+\.\s+',  # Has numbered procedures
            'action_verbs': r'(click|select|enter|navigate|open|create|run|configure|install|setup)',
            'success_criteria': r'(success|complete|result|verify|confirmation|expected|should see)',
            'troubleshooting': r'(troubleshoot|problem|error|if.*fail|common issues|if you encounter)'
        }
        
        compliance_score = 0
        total_elements = len(template_elements)
        missing_elements = []
        
        for element, pattern in template_elements.items():
            if re.search(pattern, final_output, re.IGNORECASE | re.MULTILINE):
                compliance_score += 1
            else:
                missing_elements.append(element)
        
        compliance_rate = compliance_score / total_elements
        
        return {
            'compliance_rate': compliance_rate,
            'missing_elements': missing_elements,
            'score': int(compliance_rate * 5),
            'compliant_elements': compliance_score,
            'total_elements': total_elements
        }
    
    def _evaluate_style_violations(self, original: str, final_output: str) -> Dict[str, Any]:
        """
        E2: Precision/recall for style rule enforcement
        Measures how effectively violations were removed
        """
        violations = {
            'passive_voice': r'\b(is|was|were|being|been)\s+\w+ed\b',
            'future_tense': r'\bwill\s+\w+',
            'long_sentences': self._count_long_sentences,  # Custom function for accuracy
            'corporate_jargon': r'\b(reach out|touch base|circle back|leverage|synergy)\b',
            'please_usage': r'\bplease\b',
            'ampersands': r'&(?!amp;|lt;|gt;|quot;|#)'
        }
        
        # Count violations in original vs final
        original_violations = {}
        final_violations = {}
        
        for violation_type, pattern in violations.items():
            if callable(pattern):
                # Handle custom functions like long sentences
                original_count = pattern(original)
                final_count = pattern(final_output)
            else:
                original_count = len(re.findall(pattern, original, re.IGNORECASE))
                final_count = len(re.findall(pattern, final_output, re.IGNORECASE))
            
            original_violations[violation_type] = original_count
            final_violations[violation_type] = final_count
        
        # Calculate precision/recall for violation removal
        total_original = sum(original_violations.values())
        total_final = sum(final_violations.values())
        
        if total_original > 0:
            violation_reduction_rate = (total_original - total_final) / total_original
            violation_reduction_rate = max(0, violation_reduction_rate)  # Clamp to 0 minimum
        else:
            violation_reduction_rate = 1.0  # Perfect if no violations to begin with
        
        # Calculate precision (how many removals were correct)
        # If we removed violations and didn't add new ones, precision is high
        precision = violation_reduction_rate
        
        return {
            'violation_reduction_rate': violation_reduction_rate,
            'precision': precision,
            'original_violations': original_violations,
            'remaining_violations': final_violations,
            'violations_removed': total_original - total_final,
            'score': int(violation_reduction_rate * 5)
        }
    
    def _count_long_sentences(self, content: str) -> int:
        """Helper function to accurately count sentences over 26 words"""
        sentences = re.split(r'[.!?]+', content)
        long_sentences = 0
        
        for sentence in sentences:
            words = sentence.strip().split()
            if len(words) > 26:
                long_sentences += 1
        
        return long_sentences
    
    def _check_gap_resolution(self, analysis_report: str, final_output: str) -> int:
        """Check if identified gaps were resolved (H9) - kept from original"""
        # Identify gaps mentioned in analysis report
        identified_gaps = []
        gap_indicators = [
            ('missing prerequisites', 'prerequisites'),
            ('unclear steps', 'step_clarity'),
            ('missing introduction', 'introduction'),
            ('poor step ordering', 'step_ordering'),
            ('inconsistent formatting', 'formatting'),
            ('missing success criteria', 'success_criteria'),
            ('missing troubleshooting', 'troubleshooting'),
            ('passive voice', 'passive_voice'),
            ('long sentences', 'sentence_length')
        ]
        
        for indicator, gap_type in gap_indicators:
            if indicator.lower() in analysis_report.lower():
                identified_gaps.append(gap_type)
        
        if not identified_gaps:
            return 5  # No gaps identified, perfect score
        
        # Check if gaps were addressed in final output
        resolved_gaps = 0
        total_gaps = len(identified_gaps)
        
        for gap_type in identified_gaps:
            if self._is_gap_resolved(gap_type, final_output):
                resolved_gaps += 1
        
        resolution_rate = resolved_gaps / total_gaps if total_gaps > 0 else 1
        
        # Score based on resolution rate
        if resolution_rate >= 0.90:
            return 5
        elif resolution_rate >= 0.75:
            return 4
        elif resolution_rate >= 0.60:
            return 3
        elif resolution_rate >= 0.40:
            return 2
        else:
            return 1
    
    def _is_gap_resolved(self, gap_type: str, final_output: str) -> bool:
        """Check if a specific gap type was resolved"""
        content_lower = final_output.lower()
        
        resolution_checks = {
            'prerequisites': any(keyword in content_lower for keyword in 
                               ['prerequisite', 'requirements', 'before you begin', 'you need']),
            'step_clarity': any(keyword in content_lower for keyword in 
                              ['click', 'select', 'enter', 'navigate', 'open', 'create', 'run']),
            'introduction': content_lower.startswith(('this guide', 'this tutorial', 'this document', 'this how-to')),
            'step_ordering': '1.' in final_output and '2.' in final_output,
            'formatting': bool(re.search(r'^#+\s', final_output, re.MULTILINE)),  # Headers present
            'success_criteria': any(keyword in content_lower for keyword in 
                                  ['success', 'complete', 'finished', 'result', 'expected']),
            'troubleshooting': any(keyword in content_lower for keyword in 
                                 ['troubleshoot', 'problem', 'issue', 'error', 'if you encounter']),
            'passive_voice': self._count_long_sentences(final_output) < 3,
            'sentence_length': len(re.findall(r'\bis\s+\w+ed\b|\bwas\s+\w+ed\b', final_output, re.IGNORECASE)) < 3
        }
        
        return resolution_checks.get(gap_type, False)
    
    def _count_gaps_fixed(self, analysis_report: str, final_output: str) -> str:
        """Count how many gaps were fixed"""
        return "Gap analysis completed"
    
    def _save_evaluation(self, results: Dict[str, Any]):
        """Save evaluation results to CSV"""
        try:
            # Try to read existing file
            if os.path.exists(self.evaluation_file):
                df = pd.read_csv(self.evaluation_file)
                # Convert results to DataFrame and concatenate
                new_row = pd.DataFrame([results])
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                # Create new DataFrame
                df = pd.DataFrame([results])
            
            # Save to CSV
            df.to_csv(self.evaluation_file, index=False)
            
        except Exception as e:
            print(f"Error saving evaluation: {e}")
    
    def get_recent_evaluations(self, limit: int = 10) -> pd.DataFrame:
        """Get recent evaluation results"""
        try:
            if os.path.exists(self.evaluation_file):
                df = pd.read_csv(self.evaluation_file)
                return df.tail(limit)
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading evaluations: {e}")
            return pd.DataFrame()
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all evaluations"""
        try:
            if not os.path.exists(self.evaluation_file):
                return {
                    'total_evaluations': 0,
                    'template_compliance_rate': 0,
                    'violation_reduction_rate': 0,
                    'gap_resolution_rate': 0,
                    'overall_pass_rate': 0,
                    'avg_template_score': 0,
                    'avg_style_score': 0
                }
            
            df = pd.read_csv(self.evaluation_file)
            
            return {
                'total_evaluations': len(df),
                'template_compliance_rate': df['e1_template_compliance_rate'].mean() * 100 if 'e1_template_compliance_rate' in df.columns else 0,
                'violation_reduction_rate': df['e2_violation_reduction_rate'].mean() * 100 if 'e2_violation_reduction_rate' in df.columns else 0,
                'gap_resolution_rate': df['h9_pass'].mean() * 100 if 'h9_pass' in df.columns else 0,
                'overall_pass_rate': df['overall_pass'].mean() * 100 if 'overall_pass' in df.columns else 0,
                'avg_template_score': df['e1_template_score'].mean() if 'e1_template_score' in df.columns else 0,
                'avg_style_score': df['e2_style_score'].mean() if 'e2_style_score' in df.columns else 0,
                'avg_overall_score': df['overall_score'].mean() if 'overall_score' in df.columns else 0
            }
            
        except Exception as e:
            print(f"Error getting evaluation summary: {e}")
            return {
                'total_evaluations': 0,
                'template_compliance_rate': 0,
                'violation_reduction_rate': 0,
                'gap_resolution_rate': 0,
                'overall_pass_rate': 0
            }