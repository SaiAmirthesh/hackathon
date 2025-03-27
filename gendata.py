import numpy as np
from tqdm import tqdm

def generate_traces(n_traces=1000, n_samples=500, key_byte=0x2B):
    """Generate synthetic power traces with simulated key-dependent leaks"""
    traces = np.zeros((n_traces, n_samples))
    labels = np.zeros(n_traces, dtype=np.uint8)
    
    # Simulate Hamming weight leakage (common in real SCAs)
    for i in tqdm(range(n_traces)):
        # Random plaintext byte
        plaintext = np.random.randint(0, 256)
        labels[i] = plaintext ^ key_byte  # Simulate AES SBox output
        
        # Create trace with:
        # 1. Random baseline noise
        trace = np.random.normal(0, 0.5, n_samples)
        
        # 2. Simulated "leak" at sample position 200
        hw = bin(labels[i]).count('1')  # Hamming weight (0-8)
        trace[200] += hw * 0.8  # Key-dependent peak
        
        # 3. Random spikes (simulate circuit activity)
        for _ in range(5):
            pos = np.random.randint(150, 250)
            trace[pos] += np.random.uniform(0.2, 1.0)
            
        traces[i] = trace
        
    return traces, labels

# Generate and save
traces, labels = generate_traces()
np.save("datasets/traces.npy", traces)
np.save("datasets/labels.npy", labels)
print(f"Generated {len(traces)} traces with key-dependent leaks at sample 200")