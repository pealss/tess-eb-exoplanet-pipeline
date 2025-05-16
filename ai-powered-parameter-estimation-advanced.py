import tensorflow as tf
from tensorflow.keras import mixed_precision
from tensorflow_probability import layers as tfp_layers

class EBHypernet(tf.keras.Model):
    """Multi-modal neural network with uncertainty estimation"""
    def __init__(self):
        super().__init__()
        policy = mixed_precision.Policy('mixed_float16')
        mixed_precision.set_global_policy(policy)
        
        self.encoder = tf.keras.Sequential([
            tf.keras.layers.Resizing(1024, 1),
            tf.keras.layers.Conv1D(64, 11, activation='swish'),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128)),
            tfp_layers.DenseVariational(256, activation='silu')
        ])
        
        self.parameter_heads = {
            'detached': self._build_head(7),
            'contact': self._build_head(5),
            'ellipsoidal': self._build_head(6)
        }
        
        self.uncertainty_estimator = tfp_layers.MC_Dropout(rate=0.3)

    def _build_head(self, output_dim):
        return tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='gelu'),
            tfp_layers.DistributionLambda(
                lambda t: tfp.Normal(loc=t[..., :output_dim],
                scale=tf.math.softplus(t[..., output_dim:]))
        ])

    def call(self, inputs, training=False):
        x = self.encoder(inputs)
        x = self.uncertainty_estimator(x, training=training)
        return {k: h(x) for k, h in self.parameter_heads.items()}

class ActiveLearningAgent:
    """Bayesian active learning for parameter estimation"""
    def __init__(self, strategy='bald'):
        self.acquisition_functions = {
            'bald': self._bald_acquisition,
            'max_entropy': self._max_entropy
        }
        
    def query(self, model, pool_data, batch_size=10):
        preds = model.predict(pool_data, num_samples=100)
        uncertainties = self.acquisition_functions[strategy](preds)
        return np.argsort(uncertainties)[-batch_size:]