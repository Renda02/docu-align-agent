import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from components.evaluation.evaluator import DocumentEvaluator

def show_evaluation_dashboard():
    """Display the enhanced evaluation dashboard with template compliance and style precision"""
    
    st.title("📊 DocuALIGN Enhanced Evaluation Dashboard")
    st.markdown("Template compliance and style violation precision/recall tracking")
    
    # Initialize evaluator
    evaluator = DocumentEvaluator()
    
    # Get evaluation data
    summary = evaluator.get_evaluation_summary()
    recent_evaluations = evaluator.get_recent_evaluations(20)
    
    if summary['total_evaluations'] == 0:
        st.info("🔄 No evaluation data available yet. Process some documents first!")
        return
    
    # Check if we have the expected columns (updated for new schema)
    expected_columns = ['e1_template_pass', 'e2_style_pass', 'h9_pass', 'e1_template_score', 'e2_style_score', 'h9_gap_resolution_score']
    missing_columns = [col for col in expected_columns if col not in recent_evaluations.columns]
    
    if missing_columns:
        st.error(f"⚠️ **Data Schema Issue**: Missing columns {missing_columns}. Please delete the old evaluation data and process a new document.")
        st.info("Run this command to reset: `rm components/data/evaluations.csv`")
        
        # Show available columns for debugging
        st.write("**Available columns:**", list(recent_evaluations.columns))
        return
    
    # Alert for critical issues
    if not recent_evaluations.empty:
        try:
            recent_failures = recent_evaluations[
                (recent_evaluations['e1_template_pass'] == False) | 
                (recent_evaluations['e2_style_pass'] == False) | 
                (recent_evaluations['h9_pass'] == False)
            ]
            
            if len(recent_failures) > 0:
                st.warning(
                    f"⚠️ **Attention Required**: {len(recent_failures)} documents failed critical "
                    f"evaluation criteria in recent processing. Review recommended."
                )
        except Exception as e:
            st.warning(f"⚠️ Could not check for recent failures: {e}")
    
    # Enhanced Key Metrics
    st.markdown("## 📈 Enhanced Evaluation Summary")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Documents", f"{summary['total_evaluations']:,}")
    
    with col2:
        st.metric(
            "Overall Pass Rate", 
            f"{summary['overall_pass_rate']:.1f}%",
            delta=f"{summary['overall_pass_rate'] - 85:.1f}%" if summary['overall_pass_rate'] > 0 else None
        )
    
    with col3:
        st.metric(
            "Template Compliance (E1)", 
            f"{summary['template_compliance_rate']:.1f}%",
            delta=f"{summary['template_compliance_rate'] - 90:.1f}%" if summary['template_compliance_rate'] > 0 else None,
            help="Adherence to Good Docs Project template structure"
        )
    
    with col4:
        st.metric(
            "Style Violation Reduction (E2)", 
            f"{summary['violation_reduction_rate']:.1f}%",
            delta=f"{summary['violation_reduction_rate'] - 85:.1f}%" if summary['violation_reduction_rate'] > 0 else None,
            help="Precision in removing style violations"
        )
    
    with col5:
        st.metric(
            "Gap Resolution (H9)", 
            f"{summary['gap_resolution_rate']:.1f}%",
            delta=f"{summary['gap_resolution_rate'] - 85:.1f}%" if summary['gap_resolution_rate'] > 0 else None,
            help="Effectiveness in resolving identified issues"
        )
    
    with col6:
        avg_score = summary.get('avg_overall_score', 0)
        st.metric(
            "Avg Quality Score", 
            f"{avg_score:.1f}/5.0",
            delta=f"{avg_score - 4.0:.1f}" if avg_score > 0 else None
        )
    
    # Enhanced Quality Trends Chart
    if not recent_evaluations.empty and len(recent_evaluations) >= 3:
        st.markdown("## 📊 Quality Trends")
        
        try:
            # Convert timestamp to datetime if it's not already
            recent_evaluations['timestamp'] = pd.to_datetime(recent_evaluations['timestamp'])
            
            # Create trend chart with new metrics
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=recent_evaluations['timestamp'],
                y=recent_evaluations['e1_template_score'],
                mode='lines+markers',
                name='Template Compliance (E1)',
                line=dict(color='#10b981'),
                marker=dict(size=6),
                hovertemplate='<b>Template Compliance (E1)</b><br>Date: %{x}<br>Score: %{y}/5<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=recent_evaluations['timestamp'],
                y=recent_evaluations['e2_style_score'],
                mode='lines+markers',
                name='Style Violation Reduction (E2)',
                line=dict(color='#3b82f6'),
                marker=dict(size=6),
                hovertemplate='<b>Style Violation Reduction (E2)</b><br>Date: %{x}<br>Score: %{y}/5<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=recent_evaluations['timestamp'],
                y=recent_evaluations['h9_gap_resolution_score'],
                mode='lines+markers',
                name='Gap Resolution (H9)',
                line=dict(color='#f59e0b'),
                marker=dict(size=6),
                hovertemplate='<b>Gap Resolution (H9)</b><br>Date: %{x}<br>Score: %{y}/5<extra></extra>'
            ))
            
            fig.update_layout(
                title="Enhanced Evaluation Scores Over Time",
                xaxis_title="Date",
                yaxis_title="Score (1-5)",
                yaxis=dict(range=[0, 5]),
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating trend chart: {e}")
            st.info("Try processing a few more documents to see trends.")
    
    # Template Compliance Details
    if not recent_evaluations.empty:
        st.markdown("## 🏗️ Template Compliance Analysis")
        
        try:
            # Parse missing elements from the most recent evaluations
            recent_eval = recent_evaluations.iloc[-1]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Most Recent Evaluation")
                template_score = recent_eval.get('e1_template_score', 0)
                compliance_rate = recent_eval.get('e1_template_compliance_rate', 0) * 100
                
                if template_score >= 4:
                    st.success(f"✅ **Template Compliant** ({compliance_rate:.1f}%)")
                else:
                    st.warning(f"⚠️ **Template Issues** ({compliance_rate:.1f}%)")
                
                # Show missing elements if available
                missing_elements_str = recent_eval.get('e1_missing_elements', '[]')
                try:
                    missing_elements = json.loads(missing_elements_str) if isinstance(missing_elements_str, str) else missing_elements_str
                    if missing_elements:
                        st.write("**Missing Template Elements:**")
                        for element in missing_elements:
                            st.write(f"• {element.replace('_', ' ').title()}")
                    else:
                        st.write("✅ All template elements present")
                except:
                    st.write("Template analysis available")
            
            with col2:
                st.markdown("### Style Violation Analysis")
                style_score = recent_eval.get('e2_style_score', 0)
                reduction_rate = recent_eval.get('e2_violation_reduction_rate', 0) * 100
                
                if style_score >= 4:
                    st.success(f"✅ **Style Compliant** ({reduction_rate:.1f}% violations removed)")
                else:
                    st.warning(f"⚠️ **Style Issues** ({reduction_rate:.1f}% violations removed)")
                
                # Show remaining violations if available
                remaining_violations_str = recent_eval.get('e2_remaining_violations', '{}')
                try:
                    remaining_violations = json.loads(remaining_violations_str) if isinstance(remaining_violations_str, str) else remaining_violations_str
                    total_remaining = sum(remaining_violations.values()) if isinstance(remaining_violations, dict) else 0
                    
                    if total_remaining > 0:
                        st.write("**Remaining Violations:**")
                        for violation_type, count in remaining_violations.items():
                            if count > 0:
                                st.write(f"• {violation_type.replace('_', ' ').title()}: {count}")
                    else:
                        st.write("✅ No style violations detected")
                except:
                    st.write("Style analysis available")
        
        except Exception as e:
            st.error(f"Error displaying template compliance details: {e}")
    
    # Filters (updated for new schema)
    st.markdown("## 🔍 Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_filter = st.selectbox(
            "Show:",
            ["All Evaluations", "Failed Evaluations", "Template Issues", "Style Issues"]
        )
    
    with col2:
        days_filter = st.selectbox(
            "Time Period:",
            [7, 30, 90, 365],
            format_func=lambda x: f"Last {x} days"
        )
    
    with col3:
        score_filter = st.selectbox(
            "Minimum Score:",
            [1, 2, 3, 4, 5],
            index=0
        )
    
    # Apply filters (updated for new schema)
    filtered_data = recent_evaluations.copy()
    
    try:
        if show_filter == "Failed Evaluations":
            filtered_data = filtered_data[filtered_data['overall_pass'] == False]
        elif show_filter == "Template Issues":
            filtered_data = filtered_data[filtered_data['e1_template_pass'] == False]
        elif show_filter == "Style Issues":
            filtered_data = filtered_data[filtered_data['e2_style_pass'] == False]
        
        if not filtered_data.empty:
            # Filter by score
            if 'overall_score' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['overall_score'] >= score_filter]
            
            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days_filter)
            filtered_data['timestamp'] = pd.to_datetime(filtered_data['timestamp'])
            filtered_data = filtered_data[filtered_data['timestamp'] >= cutoff_date]
        
    except Exception as e:
        st.error(f"Error applying filters: {e}")
        filtered_data = recent_evaluations.copy()
    
    # Enhanced Evaluations Table
    st.markdown("## 📋 Recent Evaluations")
    
    if filtered_data.empty:
        st.info("No evaluations match your filter criteria.")
    else:
        try:
            # Prepare display data (updated for new schema)
            display_data = filtered_data.copy()
            display_data['Date'] = display_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            
            # Create status indicators for new metrics
            def safe_create_status_indicator(score, passed):
                try:
                    if passed:
                        return f"✅ PASS ({score})"
                    else:
                        return f"❌ FAIL ({score})"
                except:
                    return "❓ UNKNOWN"
            
            # Create status columns for new evaluation criteria
            if all(col in display_data.columns for col in ['e1_template_score', 'e1_template_pass']):
                display_data['E1 Template Status'] = display_data.apply(
                    lambda row: safe_create_status_indicator(row['e1_template_score'], row['e1_template_pass']), axis=1
                )
            else:
                display_data['E1 Template Status'] = "❓ N/A"
                
            if all(col in display_data.columns for col in ['e2_style_score', 'e2_style_pass']):
                display_data['E2 Style Status'] = display_data.apply(
                    lambda row: safe_create_status_indicator(row['e2_style_score'], row['e2_style_pass']), axis=1
                )
            else:
                display_data['E2 Style Status'] = "❓ N/A"
                
            if all(col in display_data.columns for col in ['h9_gap_resolution_score', 'h9_pass']):
                display_data['H9 Gap Status'] = display_data.apply(
                    lambda row: safe_create_status_indicator(row['h9_gap_resolution_score'], row['h9_pass']), axis=1
                )
            else:
                display_data['H9 Gap Status'] = "❓ N/A"
                
            if 'overall_pass' in display_data.columns:
                display_data['Overall'] = display_data['overall_pass'].apply(
                    lambda x: "✅ PASS" if x else "❌ FAIL"
                )
            else:
                display_data['Overall'] = "❓ N/A"
                
            if 'overall_score' in display_data.columns:
                display_data['Quality Score'] = display_data['overall_score'].apply(
                    lambda x: f"{x:.1f}/5.0"
                )
            else:
                display_data['Quality Score'] = "❓ N/A"
            
            # Select columns to display (updated for new schema)
            base_columns = ['Date', 'E1 Template Status', 'E2 Style Status', 'H9 Gap Status', 'Overall', 'Quality Score']
            
            # Add word counts if available
            if 'original_word_count' in display_data.columns:
                base_columns.append('original_word_count')
            if 'final_word_count' in display_data.columns:
                base_columns.append('final_word_count')
            
            # Filter to only existing columns
            columns_to_show = [col for col in base_columns if col in display_data.columns]
            
            # Rename columns for display
            column_mapping = {
                'original_word_count': 'Original Words',
                'final_word_count': 'Final Words'
            }
            
            display_df = display_data[columns_to_show].rename(columns=column_mapping)
            
            # Display table
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
        except Exception as e:
            st.error(f"Error displaying evaluation table: {e}")
            st.write("**Raw data columns:**", list(filtered_data.columns))
            st.write("**Sample data:**")
            st.write(filtered_data.head(2))
    
    # Enhanced Export functionality
    st.markdown("## 📊 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Evaluation Data (CSV)"):
            if not recent_evaluations.empty:
                csv = recent_evaluations.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"docualign_enhanced_evaluations_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data to export")
    
    with col2:
        if st.button("📊 Generate Enhanced Quality Report"):
            # Create enhanced quality report
            report = f"""
# DocuALIGN Enhanced Quality Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics
- Total Documents Processed: {summary['total_evaluations']}
- Overall Pass Rate: {summary['overall_pass_rate']:.1f}%

## Enhanced Metrics
- Template Compliance Rate (E1): {summary['template_compliance_rate']:.1f}%
- Style Violation Reduction Rate (E2): {summary['violation_reduction_rate']:.1f}%
- Gap Resolution Rate (H9): {summary['gap_resolution_rate']:.1f}%

## Average Scores
- Average Template Score: {summary['avg_template_score']:.2f}/5.0
- Average Style Score: {summary['avg_style_score']:.2f}/5.0
- Average Overall Score: {summary['avg_overall_score']:.2f}/5.0

## Recommendations
{'Consider improving template compliance - focus on missing elements like prerequisites, success criteria.' if summary['template_compliance_rate'] < 90 else ''}
{'Review style guide enforcement - passive voice and long sentences may need attention.' if summary['violation_reduction_rate'] < 85 else ''}
{'Improve gap resolution effectiveness between analyzer and enforcer agents.' if summary['gap_resolution_rate'] < 85 else ''}
{'Quality performance is excellent across all metrics!' if summary['overall_pass_rate'] > 90 else ''}
            """
            
            st.download_button(
                label="Download Enhanced Quality Report",
                data=report,
                file_name=f"docualign_enhanced_quality_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

def show_evaluation_insights():
    """Show enhanced evaluation insights and recommendations"""
    
    st.markdown("## 💡 Enhanced Quality Insights")
    
    evaluator = DocumentEvaluator()
    summary = evaluator.get_evaluation_summary()
    
    if summary['total_evaluations'] == 0:
        st.info("Process some documents first to see insights!")
        return
    
    # Display current performance with enhanced metrics
    st.markdown("### 📊 Current Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📈 Quality Metrics:**
        • Documents Processed: {summary['total_evaluations']}
        • Overall Pass Rate: {summary['overall_pass_rate']:.1f}%
        • Avg Quality Score: {summary.get('avg_overall_score', 0):.2f}/5.0
        """)
    
    with col2:
        st.info(f"""
        **🎯 Enhanced Criteria:**
        • Template Compliance (E1): {summary['template_compliance_rate']:.1f}%
        • Violation Reduction (E2): {summary['violation_reduction_rate']:.1f}%
        • Gap Resolution (H9): {summary['gap_resolution_rate']:.1f}%
        """)
    
    # Enhanced insights based on data
    insights = []
    
    if summary['template_compliance_rate'] < 90:
        insights.append({
            'type': 'warning',
            'title': 'Template Compliance Needs Attention',
            'message': f"Template compliance is {summary['template_compliance_rate']:.1f}%. "
                      f"Focus on ensuring documents include prerequisites, numbered steps, "
                      f"success criteria, and troubleshooting sections."
        })
    
    if summary['violation_reduction_rate'] < 85:
        insights.append({
            'type': 'warning',
            'title': 'Style Violation Reduction Low',
            'message': f"Style violation reduction is {summary['violation_reduction_rate']:.1f}%. "
                      f"The Style Enforcer may need improvement in removing passive voice, "
                      f"long sentences, and corporate jargon."
        })
    
    if summary['gap_resolution_rate'] < 85:
        insights.append({
            'type': 'warning',
            'title': 'Gap Resolution Effectiveness Low',
            'message': f"Gap resolution rate is {summary['gap_resolution_rate']:.1f}%. "
                      f"The Style Enforcer may not be effectively addressing issues "
                      f"identified by the Document Analyzer."
        })
    
    if summary['overall_pass_rate'] > 90:
        insights.append({
            'type': 'success',
            'title': 'Excellent Quality Performance!',
            'message': f"Overall pass rate is {summary['overall_pass_rate']:.1f}%. "
                      f"Your DocuALIGN system is performing exceptionally well across all enhanced metrics."
        })
    
    # Display insights
    if insights:
        st.markdown("### 💡 Insights & Recommendations")
        
        for insight in insights:
            if insight['type'] == 'warning':
                st.warning(f"⚠️ **{insight['title']}**: {insight['message']}")
            elif insight['type'] == 'success':
                st.success(f"🎉 **{insight['title']}**: {insight['message']}")
            else:
                st.info(f"💡 **{insight['title']}**: {insight['message']}")
    else:
        st.success("🎯 **Good Quality Performance**: All enhanced evaluation criteria are performing well!")
    
    # Enhanced Action Items
    st.markdown("### 🎯 Action Items")
    
    recommendations = [
        "📋 **Monitor template compliance** - Focus on missing prerequisites and success criteria",
        "🔍 **Review style violations** - Check precision/recall of violation removal", 
        "📊 **Track consistency** - Ensure similar documents get similar treatment",
        "📝 **Update prompts based on patterns** - Use precision data to improve agents",
        "👥 **Conduct SME reviews** - Validate AI assessments against human experts",
        "📈 **Track improvement trends** - Watch for positive changes in compliance rates"
    ]
    
    for rec in recommendations:
        st.write(f"• {rec}")

# Helper function for navigation
def render_evaluation_section():
    """Render the enhanced evaluation section with tabs"""
    
    tab1, tab2 = st.tabs(["📊 Enhanced Dashboard", "💡 Insights"])
    
    with tab1:
        show_evaluation_dashboard()
    
    with tab2:
        show_evaluation_insights()