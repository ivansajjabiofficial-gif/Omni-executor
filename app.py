"""
Omni Executor - Enterprise Business Problem-Solving Platform
A production-grade reasoning engine for business execution and decision support.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

from analysis.classifier import ProblemClassifier
from analysis.data_analyzer import DataAnalyzer
from analysis.diagnostics import DiagnosticsEngine
from architecture.togaf import TOGAFAnalyzer
from architecture.zachman import ZachmanAnalyzer
from architecture.baseline_target import BaselineTargetMapper
from architecture.gap_analysis import GapAnalyzer
from reports.formatter import ReportFormatter
from utils.config import AppConfig, ServiceTier, BusinessScale, BusinessCategory
from utils.file_handler import FileHandler
from utils.api_client import LLMClient
from utils.validators import InputValidator
from utils.logger import setup_logger
from memory.store import AnalysisStore

# Initialize logger
logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Omni Executor",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 0.5em;
        color: #1a1a1a;
    }
    .subheader {
        font-size: 1.2em;
        color: #4a4a4a;
        margin-bottom: 2em;
    }
    .section-title {
        font-size: 1.4em;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 0.5em;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1em;
        margin: 1em 0;
        border-radius: 4px;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #0066cc;
        padding: 1em;
        margin: 1em 0;
        border-radius: 4px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1em;
        margin: 1em 0;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "report_data" not in st.session_state:
        st.session_state.report_data = None
    if "uploaded_file_data" not in st.session_state:
        st.session_state.uploaded_file_data = None
    if "analysis_store" not in st.session_state:
        st.session_state.analysis_store = AnalysisStore()


def render_header():
    """Render application header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="header">⚙️ Omni Executor</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">Enterprise Reasoning Engine for Business Execution</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f"**Build Date:** 2026-05-14")


def render_sidebar():
    """Render sidebar with navigation and settings."""
    st.sidebar.markdown("## Settings & Configuration")
    
    # Service tier selection
    service_tier = st.sidebar.selectbox(
        "Service Tier",
        [tier.value for tier in ServiceTier],
        help="Choose your service tier for feature access and analysis depth"
    )
    
    # API Key input (optional)
    st.sidebar.markdown("### AI Integration")
    api_key_option = st.sidebar.radio(
        "AI Model",
        ["Rule-Based (Default)", "Claude API", "OpenAI API"],
        help="Choose reasoning engine. Rule-based works without API keys."
    )
    
    api_key = None
    if api_key_option != "Rule-Based (Default)":
        api_key = st.sidebar.text_input(
            "API Key",
            type="password",
            help="Provide API key for enhanced analysis. Leave blank to use rule-based reasoning."
        )
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About Omni Executor")
    st.sidebar.info(
        "A production-grade business problem-solving platform. "
        "Not a chatbot—a decision engine for real business execution."
    )
    
    return service_tier, api_key_option, api_key


def render_input_form():
    """Render the main input form for problem definition."""
    st.markdown('<div class="section-title">Step 1: Define Your Problem</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        business_problem = st.text_area(
            "Describe your business problem in plain English",
            height=150,
            placeholder="Example: We're losing clients due to slow delivery timelines. "
                       "Our team is working in silos and we don't have visibility into project status. "
                       "We need to improve internal communication and project delivery speed.",
            help="Be specific about what's happening and why it matters."
        )
        
        business_category = st.selectbox(
            "Business Category",
            [cat.value for cat in BusinessCategory],
            help="Select the primary category of your business"
        )
    
    with col2:
        business_scale = st.selectbox(
            "Business Scale",
            [scale.value for scale in BusinessScale],
            help="Select your organization size and type"
        )
        
        industry = st.text_input(
            "Industry / Sector",
            placeholder="e.g., Software, Healthcare, Retail, Manufacturing, Finance",
            help="Specify your industry to get more targeted recommendations"
        )
    
    return business_problem, business_category, business_scale, industry


def render_data_input_form():
    """Render file upload and optional data input form."""
    st.markdown('<div class="section-title">Step 2: Add Data (Optional)</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file (optional)",
        type=["csv", "xlsx"],
        help="Upload business data to inform the analysis"
    )
    
    file_data = None
    file_preview = None
    file_issues = None
    
    if uploaded_file is not None:
        file_handler = FileHandler()
        try:
            file_data, file_issues = file_handler.load_and_validate(uploaded_file)
            
            if file_data is not None:
                st.session_state.uploaded_file_data = file_data
                
                # Show file preview
                with st.expander("📊 Data Preview", expanded=False):
                    st.write(f"**Rows:** {len(file_data)} | **Columns:** {len(file_data.columns)}")
                    st.dataframe(file_data.head(10), use_container_width=True)
                
                # Show data quality issues
                if file_issues:
                    with st.expander("⚠️ Data Quality Notes", expanded=True):
                        for issue in file_issues:
                            st.warning(issue)
            else:
                st.error("Failed to load file. Please check the format.")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            logger.error(f"File upload error: {str(e)}")
    
    return file_data


def render_api_settings(api_key_option, api_key):
    """Render and validate API settings."""
    st.markdown('<div class="section-title">Step 3: Configure Analysis (Optional)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_depth = st.slider(
            "Analysis Depth",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Quick analysis | 5 = Comprehensive deep-dive"
        )
    
    with col2:
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.5,
            max_value=1.0,
            value=0.8,
            help="Only include recommendations above this confidence level"
        )
    
    # Validate API key if provided
    llm_client = None
    if api_key_option != "Rule-Based (Default)" and api_key:
        try:
            llm_client = LLMClient(api_key, api_key_option.lower().split()[0])
            st.success("✓ API key validated successfully")
        except Exception as e:
            st.warning(f"Could not validate API key: {str(e)}. Using rule-based reasoning.")
            llm_client = None
    
    return analysis_depth, confidence_threshold, llm_client


def run_analysis(
    business_problem: str,
    business_category: str,
    business_scale: str,
    industry: str,
    file_data: pd.DataFrame = None,
    analysis_depth: int = 3,
    confidence_threshold: float = 0.8,
    llm_client = None
) -> dict:
    """
    Execute the full analysis pipeline.
    
    Returns:
        dict: Comprehensive analysis results with all required sections
    """
    
    logger.info(f"Starting analysis for {business_scale} in {industry}")
    
    # Input validation
    validator = InputValidator()
    validation_result = validator.validate_input(business_problem, business_category, business_scale)
    if not validation_result["valid"]:
        raise ValueError(f"Input validation failed: {validation_result['errors']}")
    
    # Initialize analysis components
    classifier = ProblemClassifier()
    data_analyzer = DataAnalyzer()
    diagnostics = DiagnosticsEngine()
    togaf_analyzer = TOGAFAnalyzer()
    zachman_analyzer = ZachmanAnalyzer()
    baseline_mapper = BaselineTargetMapper()
    gap_analyzer = GapAnalyzer()
    
    # Step 1: Classify the problem
    classification = classifier.classify(business_problem, business_category, business_scale)
    
    # Step 2: Analyze uploaded data if available
    data_insights = None
    if file_data is not None:
        data_insights = data_analyzer.analyze(file_data, classification["detected_categories"])
    
    # Step 3: Diagnostic analysis
    diagnostic_results = diagnostics.diagnose(business_problem, classification, data_insights)
    
    # Step 4: TOGAF architecture analysis
    togaf_result = togaf_analyzer.analyze(
        problem=business_problem,
        scale=business_scale,
        category=business_category,
        data_insights=data_insights,
        depth=analysis_depth
    )
    
    # Step 5: Zachman multi-view analysis
    zachman_result = zachman_analyzer.analyze(
        problem=business_problem,
        classification=classification,
        scale=business_scale,
        data_insights=data_insights
    )
    
    # Step 6: Baseline-to-target mapping
    baseline_target = baseline_mapper.map(
        current_state=classification.get("current_state"),
        togaf_vision=togaf_result.get("vision"),
        scale=business_scale,
        category=business_category
    )
    
    # Step 7: Gap analysis and actions
    gap_analysis = gap_analyzer.analyze(
        baseline=baseline_target.get("baseline"),
        target=baseline_target.get("target"),
        scale=business_scale,
        industry=industry,
        data_insights=data_insights,
        depth=analysis_depth
    )
    
    # Compile full report data
    report_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "business_problem": business_problem,
            "business_category": business_category,
            "business_scale": business_scale,
            "industry": industry,
            "has_file_data": file_data is not None,
            "analysis_depth": analysis_depth,
            "confidence_threshold": confidence_threshold,
            "used_llm": llm_client is not None,
        },
        "classification": classification,
        "diagnostic_results": diagnostic_results,
        "data_insights": data_insights,
        "togaf_analysis": togaf_result,
        "zachman_analysis": zachman_result,
        "baseline_target": baseline_target,
        "gap_analysis": gap_analysis,
    }
    
    return report_data


def render_report(report_data: dict):
    """Render the final consulting-grade report."""
    
    formatter = ReportFormatter()
    sections = formatter.generate_report_sections(report_data)
    
    # Problem Summary
    st.markdown('<div class="section-title">1. Problem Summary</div>', unsafe_allow_html=True)
    st.write(sections.get("problem_summary", ""))
    
    # Current State
    st.markdown('<div class="section-title">2. Current State</div>', unsafe_allow_html=True)
    st.write(sections.get("current_state", ""))
    
    # Root Causes
    st.markdown('<div class="section-title">3. Likely Root Causes</div>', unsafe_allow_html=True)
    st.write(sections.get("root_causes", ""))
    
    # Target State
    st.markdown('<div class="section-title">4. Target State</div>', unsafe_allow_html=True)
    st.write(sections.get("target_state", ""))
    
    # Priority Level
    st.markdown('<div class="section-title">5. Priority Level</div>', unsafe_allow_html=True)
    priority_badge = sections.get("priority_level", "")
    st.markdown(f'<div class="info-box">{priority_badge}</div>', unsafe_allow_html=True)
    
    # Recommended Actions
    st.markdown('<div class="section-title">6. Recommended Actions</div>', unsafe_allow_html=True)
    st.write(sections.get("recommended_actions", ""))
    
    # Quick Wins (7 Days)
    st.markdown('<div class="section-title">7. Quick Wins in 7 Days</div>', unsafe_allow_html=True)
    st.write(sections.get("quick_wins", ""))
    
    # 30-Day Plan
    st.markdown('<div class="section-title">8. 30-Day Plan</div>', unsafe_allow_html=True)
    st.write(sections.get("thirty_day_plan", ""))
    
    # KPIs to Track
    st.markdown('<div class="section-title">9. KPIs to Track</div>', unsafe_allow_html=True)
    st.write(sections.get("kpis", ""))
    
    # Risks and Cautions
    st.markdown('<div class="section-title">10. Risks and Cautions</div>', unsafe_allow_html=True)
    st.write(sections.get("risks", ""))
    
    # Automation Opportunities
    st.markdown('<div class="section-title">11. Automation Opportunities</div>', unsafe_allow_html=True)
    st.write(sections.get("automation", ""))
    
    # Governance Notes
    st.markdown('<div class="section-title">12. Governance Notes</div>', unsafe_allow_html=True)
    st.write(sections.get("governance", ""))
    
    # Final Recommendation
    st.markdown('<div class="section-title">13. Final Recommendation</div>', unsafe_allow_html=True)
    st.write(sections.get("final_recommendation", ""))
    
    # Confidence and Assumptions
    st.markdown("---")
    st.markdown('<div class="section-title">Confidence & Assumptions</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        confidence = report_data.get("metadata", {}).get("confidence_threshold", 0.8)
        st.metric("Analysis Confidence", f"{confidence*100:.0f}%")
    with col2:
        st.write(sections.get("assumptions", ""))
    
    # Export options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Download as JSON"):
            json_str = json.dumps(report_data, indent=2, default=str)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"omni_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📄 Download as Text"):
            text_report = formatter.export_text(report_data, sections)
            st.download_button(
                label="Download Text",
                data=text_report,
                file_name=f"omni_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("💾 Save to History"):
            st.session_state.analysis_store.save_analysis(report_data)
            st.success("✓ Analysis saved to history")


def main():
    """Main application entry point."""
    
    init_session_state()
    render_header()
    
    # Sidebar
    service_tier, api_key_option, api_key = render_sidebar()
    
    # Main form
    st.markdown("---")
    
    # Input section
    business_problem, business_category, business_scale, industry = render_input_form()
    
    # Data input section
    file_data = render_data_input_form()
    
    # API and config section
    analysis_depth, confidence_threshold, llm_client = render_api_settings(api_key_option, api_key)
    
    # Submit button
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
            
            # Validate required inputs
            if not business_problem or not business_problem.strip():
                st.error("❌ Please describe your business problem.")
            elif not industry or not industry.strip():
                st.error("❌ Please specify your industry.")
            else:
                with st.spinner("Analyzing your business problem..."):
                    try:
                        report_data = run_analysis(
                            business_problem=business_problem,
                            business_category=business_category,
                            business_scale=business_scale,
                            industry=industry,
                            file_data=file_data,
                            analysis_depth=analysis_depth,
                            confidence_threshold=confidence_threshold,
                            llm_client=llm_client
                        )
                        
                        st.session_state.report_data = report_data
                        st.session_state.analysis_complete = True
                        st.success("✓ Analysis complete")
                        
                    except ValueError as e:
                        st.error(f"❌ Validation error: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        logger.error(f"Analysis pipeline error: {str(e)}", exc_info=True)
    
    # Display report if analysis is complete
    if st.session_state.analysis_complete and st.session_state.report_data:
        st.markdown("---")
        render_report(st.session_state.report_data)


if __name__ == "__main__":
    main()
