import tensorflow as tf
from astroNN.datasets import load_galaxy10

class EBParameterEstimator:
    def __init__(self, input_shape=(1000, 1)):
        self.model = self._build_model(input_shape)
        
    def _build_model(self, input_shape):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv1D(32, 5, activation='relu', input_shape=input_shape),
            tf.keras.layers.MaxPooling1D(2),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(7)  # q, r1, r2, sbratio, incl, f_s, f_c
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, X_train, y_train):
        """Train on synthetic EB light curves"""
        # Generate synthetic data using ellc
        history = self.model.fit(X_train, y_train, epochs=50, validation_split=0.2)
        return history

    def predict_parameters(self, lc_flux):
        """Predict initial parameters for optimization"""
        return self.model.predict(np.expand_dims(lc_flux, axis=(0, -1))[0]