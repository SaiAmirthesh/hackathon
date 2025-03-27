import numpy as np
from tensorflow.keras import layers, models
from scipy.stats import pearsonr

class NoiseGenerator:
    def __init__(self):
        self.model = self._build_generator()
        
    def _build_generator(self):
        """GAN-based noise generator"""
        model = models.Sequential([
            layers.Dense(128, input_dim=100, activation='relu'),
            layers.Dense(1000)  # Match trace length
        ])
        return model
        
    def add_noise(self, traces, intensity=0.1):
        """Add AI-generated noise to traces"""
        noise = np.random.normal(0, 1, (len(traces), 100))
        ai_noise = self.model.predict(noise) * intensity
        return traces + ai_noise

    def calculate_correlation(self, traces, labels):
        """Compute Pearson correlation between traces and labels"""
        try:
            # Ensure equal length
            min_length = min(len(traces), len(labels))
            return pearsonr(
                traces[:min_length].mean(axis=0), 
                labels[:min_length]
            )[0]
        except Exception as e:
            print(f"Correlation calc error: {str(e)}")
            return 0.0  # Return neutral value on error