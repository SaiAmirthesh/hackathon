from flask import Flask, request, jsonify
import numpy as np
from modeln import NoiseGenerator

app = Flask(__name__)
model = NoiseGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/protect', methods=['POST'])
def protect():
    try:
        data = request.get_json()
        traces = np.array(data['traces'])
        
        # Apply protection
        noisy_traces = model.add_noise(
            traces,
            intensity=float(data.get('intensity', 0.3)))
        
        # Calculate metrics
        labels = np.random.randint(0, 256, len(traces))  # Mock labels for demo
        original_corr = model.calculate_correlation(traces, labels)
        protected_corr = model.calculate_correlation(noisy_traces, labels)
        
        return jsonify({
            "status": "success",
            "protected_traces": noisy_traces.tolist(),
            "original_corr": original_corr,
            "protected_corr": protected_corr,
            "similarity": 100 * (1 - abs(original_corr - protected_corr))
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)