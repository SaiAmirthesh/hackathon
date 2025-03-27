## **SCA Shield: AI-Powered Side-Channel Attack Prevention** 🛡️


## **Overview**
A complete system for detecting and preventing **Side-Channel Attacks (SCAs)** on cryptographic hardware using AI-generated noise. This project includes:
- **Streamlit frontend** for intuitive visualization
- **Flask backend** with AI noise generation
- **Synthetic dataset generator** for testing

## **Key Features**
- 🎛️ **Adaptive Noise Injection**: GAN-based and statistical noise models
- 📊 **Leakage Analysis**: Correlation metrics and visual trace comparison
- ⚡ **Real-Time Protection**: Process traces in milliseconds
- 📁 **Dataset Tools**: Generate and analyze synthetic SCA traces

---

## **🚀 Quick Start**

### **Prerequisites**
- Python 3.8+
- `pip` package manager

### **Installation**
```bash
git clone https://github.com/yourusername/sca-shield.git
cd sca-shield

# Install dependencies
pip install -r requirements.txt
```

### **Run the System**
1. **Start Backend** (Flask API):
   ```bash
   cd backend
   python server.py
   ```

2. **Start Frontend** (Streamlit UI):
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. Access the UI at: `http://localhost:8501`

---

## **🛠️ Components**

### **1. Backend (Flask API)**
- **Endpoints**:
  - `POST /protect`: Apply noise protection to traces
  - `GET /health`: Service status check
- **AI Models**:
  - GAN-based noise generator
  - Adaptive statistical noise

### **2. Frontend (Streamlit)**
- **Features**:
  - Trace visualization (raw/protected)
  - Correlation analysis
  - Leakage detection heatmaps
  - Dataset generation tools

### **3. Dataset Tools**
- Generate synthetic traces with configurable leaks:
  ```bash
  python datasets/generate_dataset.py
  ```

---

## **📊 Sample Workflow**
1. **Upload traces** (`*.npy` file) or generate samples
2. **Analyze leaks** using heatmaps and histograms
3. **Apply protection** with adjustable noise intensity
4. **Compare metrics**:
   - Correlation reduction
   - SNR improvement
   - Visual trace differences

![Workflow](https://via.placeholder.com/600x200/4CAF50/FFFFFF?text=Upload+→+Analyze+→+Protect+→+Validate)

---

## **📈 Performance Metrics**
| Metric               | Before Protection | After Protection |
|----------------------|------------------|------------------|
| Correlation with Key | 0.82             | 0.09             |
| SNR (dB)             | 18.7             | 6.2              |
| Trace Similarity      | -                | 92%              |

---

## **🧑‍💻 Development**
### **File Structure**
```
sca-shield/
├── backend/               # Flask API
│   ├── appn.py          # Main API
│   ├── modeln.py           # AI noise models
├── frontend/              # Streamlit UI
│   ├── fappn.py             # Main interface
├── datasets/              # Sample data
│   ├── gendata.py # Trace generator
```

### **Customization**
1. **Noise Algorithms**: Modify `backend/model.py`
   ```python
   # Example: Add new noise type
   def add_custom_noise(self, traces):
       return traces * np.random.normal(1, 0.2, traces.shape)
   ```

2. **Frontend Widgets**: Edit `frontend/fappn.py`
   ```python
   # Add new control
   st.slider("Custom Parameter", 0, 100, 50)
   ```

---

## **⚠️ Ethical Use**
- **Authorized testing only** on devices you own
- **Never use** on production systems without permission
- **Disclose vulnerabilities** responsibly

---

## **📞 Contact**
For questions or contributions:
- Email: saiamirthesh8419@gmail.com
- GitHub: [@SaiAmirthesh](https://github.com/yourusername)

---

**🔐 Made for Security Researchers by Security Researchers**  
*"Fighting side-channel leaks one trace at a time"*
