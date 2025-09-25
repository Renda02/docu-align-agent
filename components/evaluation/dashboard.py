import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.evaluation.evaluator import DocumentEvaluator

def show_evaluation_dashboard():
    """Display the evaluation dashboard"""
    
    st.title("📊 DocuALIGN Evaluation Dashboard")
    st.markdown("Real-time quality assessment and performance tracking")
    
    # Initialize evaluator
    evaluator = DocumentEvaluator()
    
    # Get evaluation data
    summary = evaluator.get_evaluation_summary()
    recent_evaluations = evaluator.get_recent_evaluations(20)
    
    if summary['total_evaluations'] == 0:
        st.info("🔄 No evaluation data available yet. Process some documents first!")
        return
    
    # Check if we have the expected columns
    expected_columns = ['h7_pass', 'h8_pass', 'h9_pass', 'h7_accuracy_score', 'h8_style_score', 'h9_gap_resolution_score']
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
                (recent_evaluations['h7_pass'] == False) | 
                (recent_evaluations['h8_pass'] == False) | 
                (recent_evaluations['h9_pass'] == False)
            ]
            
            if len(recent_failures) > 0:
                st.warning(
                    f"⚠️ **Attention Required**: {len(recent_failures)} documents failed critical "
                    f"evaluation criteria in recent processing. Review recommended."
                )
        except Exception as e:
            st.warning(f"⚠️ Could not check for recent failures: {e}")
    
    # Key Metrics
    st.markdown("## 📈 Evaluation Summary")
    
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
            "Technical Accuracy (H7)", 
            f"{summary['h7_pass_rate']:.1f}%",
            delta=f"{summary['h7_pass_rate'] - 95:.1f}%" if summary['h7_pass_rate'] > 0 else None
        )
    
    with col4:
        st.metric(
            "Style Compliance (H8)", 
            f"{summary['h8_pass_rate']:.1f}%",
            delta=f"{summary['h8_pass_rate'] - 85:.1f}%" if summary['h8_pass_rate'] > 0 else None
        )
    
    with col5:
        st.metric(
            "Gap Resolution (H9)", 
            f"{summary['h9_pass_rate']:.1f}%",
            delta=f"{summary['h9_pass_rate'] - 85:.1f}%" if summary['h9_pass_rate'] > 0 else None
        )
    
    with col6:
        avg_score = summary.get('avg_overall_score', 0)
        st.metric(
            "Avg Quality Score", 
            f"{avg_score:.1f}/5.0",
            delta=f"{avg_score - 4.0:.1f}" if avg_score > 0 else None
        )
    
    # Quality Trends Chart
    if not recent_evaluations.empty and len(recent_evaluations) >= 3:
        st.markdown("## 📊 Quality Trends")
        
        try:
            # Convert timestamp to datetime if it's not already
            recent_evaluations['timestamp'] = pd.to_datetime(recent_evaluations['timestamp'])
            
            # Create trend chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=recent_evaluations['timestamp'],
                y=recent_evaluations['h7_accuracy_score'],
                mode='lines+markers',
                name='Technical Accuracy (H7)',
                line=dict(color='#10b981'),
                marker=dict(size=6),
                hovertemplate='<b>Technical Accuracy (H7)</b><br>Date: %{x}<br>Score: %{y}/5<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=recent_evaluations['timestamp'],
                y=recent_evaluations['h8_style_score'],
                mode='lines+markers',
                name='Style Compliance (H8)',
                line=dict(color='#3b82f6'),
                marker=dict(size=6),
                hovertemplate='<b>Style Compliance (H8)</b><br>Date: %{x}<br>Score: %{y}/5<extra></extra>'
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
                title="Evaluation Scores Over Time",
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
    
    # Filters
    st.markdown("## 🔍 Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_filter = st.selectbox(
            "Show:",
            ["All Evaluations", "Failed Evaluations", "Critical Failures Only"]
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
    
    # Apply filters
    filtered_data = recent_evaluations.copy()
    
    try:
        if show_filter == "Failed Evaluations":
            filtered_data = filtered_data[filtered_data['overall_pass'] == False]
        elif show_filter == "Critical Failures Only":
            filtered_data = filtered_data[
                (filtered_data['h7_pass'] == False) | 
                (filtered_data['h8_pass'] == False) | 
                (filtered_data['h9_pass'] == False)
            ]
        
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
    
    # Recent Evaluations Table
    st.markdown("## 📋 Recent Evaluations")
    
    if filtered_data.empty:
        st.info("No evaluations match your filter criteria.")
    else:
        try:
            # Prepare display data
            display_data = filtered_data.copy()
            display_data['Date'] = display_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            
            # Create status indicators - SAFE VERSION
            def safe_create_status_indicator(score, passed):
                try:
                    if passed:
                        return f"✅ PASS ({score})"
                    else:
                        return f"❌ FAIL ({score})"
                except:
                    return "❓ UNKNOWN"
            
            # Safely create status columns
            if all(col in display_data.columns for col in ['h7_accuracy_score', 'h7_pass']):
                display_data['H7 Status'] = display_data.apply(
                    lambda row: safe_create_status_indicator(row['h7_accuracy_score'], row['h7_pass']), axis=1
                )
            else:
                display_data['H7 Status'] = "❓ N/A"
                
            if all(col in display_data.columns for col in ['h8_style_score', 'h8_pass']):
                display_data['H8 Status'] = display_data.apply(
                    lambda row: safe_create_status_indicator(row['h8_style_score'], row['h8_pass']), axis=1
                )
            else:
                display_data['H8 Status'] = "❓ N/A"
                
            if all(col in display_data.columns for col in ['h9_gap_resolution_score', 'h9_pass']):
                display_data['H9 Status'] = display_data.apply(
                    lambda row: safe_create_status_indicator(row['h9_gap_resolution_score'], row['h9_pass']), axis=1
                )
            else:
                display_data['H9 Status'] = "❓ N/A"
                
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
            
            # Select columns to display
            base_columns = ['Date', 'H7 Status', 'H8 Status', 'H9 Status', 'Overall', 'Quality Score']
            
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
    
    # Export functionality
    st.markdown("## 📊 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Evaluation Data (CSV)"):
            if not recent_evaluations.empty:
                csv = recent_evaluations.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"docualign_evaluations_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data to export")
    
    with col2:
        if st.button("📊 Generate Quality Report"):
            # Create a simple text report
            report = f"""
# DocuALIGN Quality Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics
- Total Documents Processed: {summary['total_evaluations']}
- Overall Pass Rate: {summary['overall_pass_rate']:.1f}%
- Technical Accuracy Pass Rate: {summary['h7_pass_rate']:.1f}%
- Style Compliance Pass Rate: {summary['h8_pass_rate']:.1f}%
- Gap Resolution Pass Rate: {summary['h9_pass_rate']:.1f}%
- Average Quality Score: {summary.get('avg_overall_score', 0):.2f}/5.0

## Recommendations
{'Consider reviewing technical accuracy preservation processes.' if summary['h7_pass_rate'] < 95 else ''}
{'Review style guide enforcement settings.' if summary['h8_pass_rate'] < 85 else ''}
{'Improve gap resolution effectiveness.' if summary['h9_pass_rate'] < 85 else ''}
{'Quality performance is excellent!' if summary['overall_pass_rate'] > 90 else ''}
            """
            
            st.download_button(
                label="Download Quality Report",
                data=report,
                file_name=f"docualign_quality_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

def show_evaluation_insights():
    """Show evaluation insights and recommendations"""
    
    st.markdown("## 💡 Quality Insights")
    
    evaluator = DocumentEvaluator()
    summary = evaluator.get_evaluation_summary()
    
    if summary['total_evaluations'] == 0:
        st.info("Process some documents first to see insights!")
        return
    
    # Display current performance
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
        **🎯 Critical Criteria:**
        • Technical Accuracy (H7): {summary['h7_pass_rate']:.1f}%
        • Style Compliance (H8): {summary['h8_pass_rate']:.1f}%
        • Gap Resolution (H9): {summary['h9_pass_rate']:.1f}%
        """)
    
    # Insights based on data
    insights = []
    
    if summary['h7_pass_rate'] < 95:
        insights.append({
            'type': 'warning',
            'title': 'Technical Accuracy Attention Needed',
            'message': f"Technical accuracy pass rate is {summary['h7_pass_rate']:.1f}%. "
                      f"Consider reviewing your document processing to ensure code, URLs, and "
                      f"technical elements are preserved exactly."
        })
    
    if summary['h8_pass_rate'] < 85:
        insights.append({
            'type': 'warning',
            'title': 'Style Guide Improvements Needed',
            'message': f"Style compliance pass rate is {summary['h8_pass_rate']:.1f}%. "
                      f"Review the Style Enforcer agent's prompt to better follow "
                      f"active voice, present tense, and sentence length rules."
        })
    
    if summary['h9_pass_rate'] < 85:
        insights.append({
            'type': 'warning',
            'title': 'Gap Resolution Effectiveness Low',
            'message': f"Gap resolution pass rate is {summary['h9_pass_rate']:.1f}%. "
                      f"The Style Enforcer may not be effectively addressing issues "
                      f"identified by the Document Analyzer."
        })
    
    if summary['overall_pass_rate'] > 90:
        insights.append({
            'type': 'success',
            'title': 'Excellent Quality Performance!',
            'message': f"Overall pass rate is {summary['overall_pass_rate']:.1f}%. "
                      f"Your DocuALIGN system is performing exceptionally well."
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
        st.success("🎯 **Good Quality Performance**: All evaluation criteria are performing well!")
    
    # Recommendations
    st.markdown("### 🎯 Action Items")
    
    recommendations = [
        "📊 **Monitor trends weekly** - Check the evaluation dashboard regularly",
        "🔍 **Review failed evaluations** - Use filters to focus on problem areas", 
        "📝 **Update prompts based on patterns** - Use evaluation data to improve agents",
        "👥 **Conduct monthly SME reviews** - Use the full HHH framework for deep evaluation",
        "📈 **Track improvement over time** - Watch for positive trends in quality scores"
    ]
    
    for rec in recommendations:
        st.write(f"• {rec}")

# Helper function for navigation
def render_evaluation_section():
    """Render the full evaluation section with tabs"""
    
    tab1, tab2 = st.tabs(["📊 Dashboard", "💡 Insights"])
    
    with tab1:
        show_evaluation_dashboard()
    
    with tab2:
        show_evaluation_insights()