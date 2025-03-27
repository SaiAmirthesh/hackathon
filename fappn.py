import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
import time
from io import BytesIO

# App config
st.set_page_config(
    page_title="SCA Shield - Side-Channel Defense",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: #4CAF50;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App header
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://via.placeholder.com/150/4CAF50/FFFFFF?text=SCA", width=150)
with col2:
    st.title("SCA Shield")
    st.caption("AI-Powered Side-Channel Attack Prevention System")

# Sidebar - Connection check
with st.sidebar:
    st.header("Backend Status")
    backend_status = st.empty()
    
    if st.button("🔄 Check Connection"):
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                backend_status.success("✅ Backend Connected")
            else:
                backend_status.error("❌ Backend Error")
        except:
            backend_status.error("❌ Backend Offline")
    
    st.divider()
    st.markdown("### Sample Datasets")
    if st.button("Generate Demo Traces"):
        with st.spinner("Generating sample data..."):
            # Generate sample traces
            traces = np.random.rand(100, 1000)
            traces[:, 200] += np.random.randint(0, 8, 100) * 0.5  # Simulated leak
            
            # Save to buffer
            buffer = BytesIO()
            np.save(buffer, traces)
            buffer.seek(0)
            
            st.download_button(
                label="Download Sample Traces",
                data=buffer,
                file_name="sample_traces.npy",
                mime="application/octet-stream"
            )

# Main app
tab1, tab2 = st.tabs(["Protection Analyzer", "Dataset Inspector"])

with tab1:
    st.header("🛡️ Trace Protection")
    
    uploaded_file = st.file_uploader(
        "Upload Power Traces (NPY format)",
        type=["npy"],
        accept_multiple_files=False
    )
    
    if uploaded_file:
        try:
            traces = np.load(uploaded_file)
            
            # Original trace analysis
            with st.expander("Original Trace Analysis", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Single Trace")
                    trace_idx = st.slider("Select trace", 0, len(traces)-1, 0)
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(traces[trace_idx])
                    ax.set_xlabel("Sample Index")
                    ax.set_ylabel("Power Consumption")
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("Average Trace")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(traces.mean(axis=0))
                    ax.set_xlabel("Sample Index")
                    ax.set_ylabel("Average Power")
                    st.pyplot(fig)
            
            # Protection settings
            st.subheader("Protection Configuration")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                noise_type = st.selectbox(
                    "Noise Algorithm",
                    ["GAN-Based", "Gaussian", "Adaptive"]
                )
            
            with col2:
                intensity = st.slider(
                    "Noise Intensity",
                    min_value=0.1,
                    max_value=1.0,
                    value=0.3,
                    step=0.1
                )
            
            with col3:
                st.write("")  # Spacer
                protect_btn = st.button(
                    "Apply Protection",
                    type="primary",
                    use_container_width=True
                )
            
            if protect_btn:
                with st.spinner("Applying AI protection..."):
                    try:
                        start_time = time.time()
                        
                        # Send to backend
                        response = requests.post(
                            "http://localhost:5000/protect",
                            json={
                                "traces": traces.tolist(),
                                "noise_type": noise_type,
                                "intensity": intensity
                            },
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            processing_time = time.time() - start_time
                            
                            # Show results
                            st.success(f"Protection applied in {processing_time:.2f}s")
                            
                            # Protected trace display
                            protected_traces = np.array(result["protected_traces"])
                            
                            with st.expander("Protected Results", expanded=True):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.subheader("Protected Trace")
                                    fig, ax = plt.subplots(figsize=(10, 4))
                                    ax.plot(protected_traces[trace_idx])
                                    st.pyplot(fig)
                                
                                with col2:
                                    st.subheader("Noise Profile")
                                    noise = protected_traces[trace_idx] - traces[trace_idx]
                                    fig, ax = plt.subplots(figsize=(10, 4))
                                    ax.plot(noise)
                                    st.pyplot(fig)
                            
                            # Metrics
                            st.subheader("Protection Metrics")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("""
                                <div class="metric-card">
                                    <h3>Correlation Reduction</h3>
                                    <h2>{:.2f} → {:.2f}</h2>
                                </div>
                                """.format(
                                    result["original_corr"],
                                    result["protected_corr"]
                                ), unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("""
                                <div class="metric-card">
                                    <h3>SNR Reduction</h3>
                                    <h2>{:.1f}%</h2>
                                </div>
                                """.format(
                                    (1 - (result["protected_corr"] / result["original_corr"])) * 100
                                ), unsafe_allow_html=True)
                            
                            with col3:
                                st.markdown("""
                                <div class="metric-card">
                                    <h3>Trace Similarity</h3>
                                    <h2>{:.1f}%</h2>
                                </div>
                                """.format(
                                    result.get("similarity", 0)
                                ), unsafe_allow_html=True)
                            
                            # Download option
                            buffer = BytesIO()
                            np.save(buffer, protected_traces)
                            buffer.seek(0)
                            
                            st.download_button(
                                label="Download Protected Traces",
                                data=buffer,
                                file_name="protected_traces.npy",
                                mime="application/octet-stream"
                            )
                        else:
                            st.error(f"Backend error: {response.text}")
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {str(e)}")
                    except Exception as e:
                        st.error(f"Processing error: {str(e)}")
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

with tab2:
    st.header("🔍 Dataset Inspector")
    
    if uploaded_file:
        try:
            traces = np.load(uploaded_file)
            
            # Statistical analysis
            st.subheader("Statistical Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Number of Traces", len(traces))
                st.metric("Samples per Trace", traces.shape[1])
            
            with col2:
                st.metric("Average Power", f"{traces.mean():.2f} μV")
                st.metric("Max Variation", f"{traces.ptp():.2f} μV")
            
            # Heatmap visualization
            st.subheader("Trace Heatmap")
            fig, ax = plt.subplots(figsize=(12, 6))
            heatmap = ax.imshow(traces[:50], aspect='auto', cmap='viridis')
            plt.colorbar(heatmap, label='Power Consumption')
            ax.set_xlabel("Sample Index")
            ax.set_ylabel("Trace Number")
            st.pyplot(fig)
            
            # Leakage detection
            st.subheader("Leakage Detection")
            
            sample_idx = st.slider(
                "Analyze sample",
                0,
                traces.shape[1]-1,
                200
            )
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.hist(traces[:, sample_idx], bins=20)
            ax.set_xlabel("Power Value")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            
            # Automatic leak detection
            if st.button("Run Leak Detection"):
                with st.spinner("Analyzing traces..."):
                    try:
                        # Simple leak detection (variance-based)
                        variances = traces.var(axis=0)
                        leak_candidate = variances.argmax()
                        
                        st.info(f"Potential leak detected at sample {leak_candidate}")
                        
                        # Highlight in heatmap
                        fig, ax = plt.subplots(figsize=(12, 6))
                        heatmap = ax.imshow(traces[:50], aspect='auto', cmap='viridis')
                        ax.axvline(leak_candidate, color='red', linestyle='--')
                        plt.colorbar(heatmap, label='Power Consumption')
                        ax.set_xlabel("Sample Index")
                        ax.set_ylabel("Trace Number")
                        st.pyplot(fig)
                    
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

# Footer
st.divider()
st.caption("""
⚠️ **Ethical Use Notice**: This tool is for authorized security research only.  
Always obtain proper permissions before testing systems.
""")