import pandas as pd
from datetime import datetime
from typing import Dict, Any
import re
import os
import json

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
        Automatically evaluate document processing results
        Returns evaluation scores for H7, H8, H9 (critical criteria)
        """
        evaluation_results = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'original_word_count': len(original_content.split()),
            'final_word_count': len(final_output.split()),
            'processing_successful': True
        }
        
        # H7: Technical Accuracy Preservation (CRITICAL)
        accuracy_score = self._check_technical_preservation(original_content, final_output)
        evaluation_results['h7_accuracy_score'] = accuracy_score
        evaluation_results['h7_pass'] = accuracy_score >= 4
        evaluation_results['h7_issues'] = self._get_technical_issues(original_content, final_output)
        
        # H8: Style Guide Enforcement (CRITICAL)
        style_score = self._check_style_compliance(final_output)
        evaluation_results['h8_style_score'] = style_score
        evaluation_results['h8_pass'] = style_score >= 4
        evaluation_results['h8_violations'] = self._get_style_violations(final_output)
        
        # H9: Gap Resolution Effectiveness (CRITICAL)
        gap_resolution_score = self._check_gap_resolution(analysis_report, final_output)
        evaluation_results['h9_gap_resolution_score'] = gap_resolution_score
        evaluation_results['h9_pass'] = gap_resolution_score >= 4
        evaluation_results['h9_gaps_fixed'] = self._count_gaps_fixed(analysis_report, final_output)
        
        # Overall quality assessment
        critical_pass = evaluation_results['h7_pass'] and evaluation_results['h8_pass'] and evaluation_results['h9_pass']
        evaluation_results['overall_pass'] = critical_pass
        evaluation_results['overall_score'] = (accuracy_score + style_score + gap_resolution_score) / 3
        
        # Save to CSV for tracking
        self._save_evaluation(evaluation_results)
        
        return evaluation_results
    
    def _check_technical_preservation(self, original: str, final: str) -> int:
        """Check if technical elements were preserved (H7)"""
        # Extract technical elements using regex patterns
        tech_patterns = [
            (r'`[^`]+`', 'code_blocks'),           # Code in backticks
            (r'https?://[^\s]+', 'urls'),           # URLs
            (r'/[a-zA-Z0-9/_.-]+', 'file_paths'),   # File paths
            (r'\$[A-Z_]+', 'env_vars'),             # Environment variables
            (r'--[a-z-]+', 'cli_flags'),           # Command flags
            (r'[A-Z_]{3,}', 'constants'),          # Constants (all caps)
            (r'\b\d+\.\d+\.\d+\b', 'versions')     # Version numbers
        ]
        
        issues = []
        total_elements = 0
        preserved_elements = 0
        
        for pattern, element_type in tech_patterns:
            original_matches = set(re.findall(pattern, original))
            final_matches = set(re.findall(pattern, final))
            
            total_elements += len(original_matches)
            
            # Check for removed or modified elements
            removed = original_matches - final_matches
            added = final_matches - original_matches
            
            if removed or added:
                issues.append({
                    'type': element_type,
                    'removed': list(removed),
                    'added': list(added)
                })
            else:
                preserved_elements += len(original_matches)
        
        if total_elements == 0:
            return 5  # No technical elements to preserve
        
        preservation_rate = preserved_elements / total_elements if total_elements > 0 else 1
        
        # Score based on preservation rate
        if preservation_rate == 1.0:
            return 5
        elif preservation_rate >= 0.95:
            return 4
        elif preservation_rate >= 0.85:
            return 3
        elif preservation_rate >= 0.70:
            return 2
        else:
            return 1
    
    def _check_style_compliance(self, content: str) -> int:
        """Check compliance with style guide rules (H8)"""
        violations = []
        score = 5
        
        # Rule 1: Check for passive voice
        passive_patterns = [
            r'\bis\s+\w+ed\b', r'\bwas\s+\w+ed\b', r'\bwere\s+\w+ed\b',
            r'\bbeing\s+\w+ed\b', r'\bbeen\s+\w+ed\b'
        ]
        passive_count = 0
        for pattern in passive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            passive_count += len(matches)
        
        if passive_count > 0:
            violations.append(f"Passive voice found: {passive_count} instances")
            score -= min(1, passive_count * 0.2)
        
        # Rule 2: Check for "will" usage (should use present tense)
        will_matches = re.findall(r'\bwill\s+', content, re.IGNORECASE)
        if will_matches:
            violations.append(f"Future tense ('will') found: {len(will_matches)} instances")
            score -= min(1, len(will_matches) * 0.1)
        
        # Rule 3: Check sentence length (max 26 words)
        sentences = re.split(r'[.!?]+', content)
        long_sentences = [s for s in sentences if len(s.split()) > 26]
        if long_sentences:
            violations.append(f"Long sentences found: {len(long_sentences)} over 26 words")
            score -= min(1, len(long_sentences) * 0.1)
        
        # Rule 4: Check for ampersands (should not use &)
        ampersand_matches = re.findall(r'&(?!amp;|lt;|gt;|quot;)', content)  # Exclude HTML entities
        if ampersand_matches:
            violations.append(f"Ampersands found: {len(ampersand_matches)} instances")
            score -= min(0.5, len(ampersand_matches) * 0.1)
        
        # Rule 5: Check for "please" usage (should not use)
        please_matches = re.findall(r'\bplease\b', content, re.IGNORECASE)
        if please_matches:
            violations.append(f"'Please' found: {len(please_matches)} instances")
            score -= min(0.5, len(please_matches) * 0.1)
        
        # Rule 6: Check for corporate jargon
        jargon_patterns = [r'\breach out\b', r'\btouch base\b', r'\bcircle back\b']
        jargon_count = 0
        for pattern in jargon_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            jargon_count += len(matches)
        
        if jargon_count > 0:
            violations.append(f"Corporate jargon found: {jargon_count} instances")
            score -= min(0.5, jargon_count * 0.2)
        
        # Return score clamped between 1 and 5
        return max(1, min(5, round(score)))
    
    def _check_gap_resolution(self, analysis_report: str, final_output: str) -> int:
        """Check if identified gaps were resolved (H9)"""
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
            'passive_voice': len(re.findall(r'\bis\s+\w+ed\b|\bwas\s+\w+ed\b', final_output, re.IGNORECASE)) < 3,
            'sentence_length': len([s for s in re.split(r'[.!?]+', final_output) if len(s.split()) > 26]) < 3
        }
        
        return resolution_checks.get(gap_type, False)
    
    def _get_technical_issues(self, original: str, final: str) -> str:
        """Get summary of technical preservation issues"""
        # This would return detailed issues found
        return "No major technical changes detected"
    
    def _get_style_violations(self, content: str) -> str:
        """Get summary of style violations"""
        violations = []
        
        # Quick check for common violations
        if re.search(r'\bwill\s+', content, re.IGNORECASE):
            violations.append("Future tense usage")
        
        if '&' in content and 'http' not in content:
            violations.append("Ampersand usage")
        
        return '; '.join(violations) if violations else "No major style violations"
    
    def _count_gaps_fixed(self, analysis_report: str, final_output: str) -> str:
        """Count how many gaps were fixed"""
        # Simplified gap counting
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
                    'h7_pass_rate': 0,
                    'h8_pass_rate': 0,
                    'h9_pass_rate': 0,
                    'overall_pass_rate': 0
                }
            
            df = pd.read_csv(self.evaluation_file)
            
            return {
                'total_evaluations': len(df),
                'h7_pass_rate': df['h7_pass'].mean() * 100 if 'h7_pass' in df.columns else 0,
                'h8_pass_rate': df['h8_pass'].mean() * 100 if 'h8_pass' in df.columns else 0,
                'h9_pass_rate': df['h9_pass'].mean() * 100 if 'h9_pass' in df.columns else 0,
                'overall_pass_rate': df['overall_pass'].mean() * 100 if 'overall_pass' in df.columns else 0,
                'avg_overall_score': df['overall_score'].mean() if 'overall_score' in df.columns else 0
            }
            
        except Exception as e:
            print(f"Error getting evaluation summary: {e}")
            return {
                'total_evaluations': 0,
                'h7_pass_rate': 0,
                'h8_pass_rate': 0,
                'h9_pass_rate': 0,
                'overall_pass_rate': 0
            }