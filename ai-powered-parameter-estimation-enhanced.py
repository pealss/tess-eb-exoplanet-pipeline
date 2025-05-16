import tensorflow as tf
from stellargraph import layers as sg_layers

class EBParameterEstimator(tf.keras.Model):
    def __init__(self, num_parameters=7):
        super().__init__()
        self.preprocessor = tf.keras.Sequential([
            sg_layers.GATv2Conv(32, num_heads=3),
            tf.keras.layers.GlobalMaxPool1D()
        ])
        self.main_network = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='swish'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(num_parameters)
        ])

    def call(self, inputs):
        x = self.preprocessor(inputs)
        return self.main_network(x)

class SyntheticDataGenerator:
    def __init__(self, num_samples=10000):
        self.num_samples = num_samples
        
    def generate_light_curves(self):
        """Generate synthetic EB light curves with realistic noise"""
        params = {
            'q': np.random.uniform(0.1, 1, self.num_samples),
            'r_1': np.random.uniform(0.01, 0.5, self.num_samples),
            # ... other parameters ...
        }
        
        lcs = []
        for i in range(self.num_samples):
            lc = ellc.lc(..., **params[i])
            lc += np.random.normal(0, 0.002, len(lc))  # TESS-like noise
            lcs.append(lc)
            
        return np.array(lcs), np.array(params)