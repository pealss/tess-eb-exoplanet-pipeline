import plotly.graph_objects as go
from scipy.spatial import ConvexHull

class BinaryVisualizer:
    def __init__(self, params):
        self.params = params
        
    def _calculate_orbital_path(self):
        t = np.linspace(0, 2*np.pi, 100)
        a = 1  # Normalized separation
        q = self.params['q']
        r1 = self.params['r_1']
        r2 = self.params['r_2']
        
        x1 = a * q/(1+q) * np.cos(t)
        y1 = a * q/(1+q) * np.sin(t)
        x2 = -a/(1+q) * np.cos(t)
        y2 = -a/(1+q) * np.sin(t)
        return (x1, y1), (x2, y2)

    def create_3d_plot(self):
        """Interactive 3D plot of the binary system"""
        fig = go.Figure()
        
        # Primary star
        fig.add_trace(go.Surface(
            x=self._generate_star_mesh(self.params['r_1'])[0],
            y=self._generate_star_mesh(self.params['r_1'])[1],
            z=self._generate_star_mesh(self.params['r_1'])[2],
            colorscale='thermal'
        ))
        
        # Secondary star
        fig.add_trace(go.Surface(
            x=self._generate_star_mesh(self.params['r_2'])[0] + self.params['sbratio'],
            y=self._generate_star_mesh(self.params['r_2'])[1],
            z=self._generate_star_mesh(self.params['r_2'])[2],
            colorscale='ice'
        ))
        
        fig.update_layout(scene=dict(
            xaxis_title='X [a]',
            yaxis_title='Y [a]',
            zaxis_title='Z [a]'))
        return fig

    def _generate_star_mesh(self, radius, num_points=50):
        θ, φ = np.mgrid[0:np.pi:num_points*1j, 0:2*np.pi:num_points*1j]
        x = radius * np.sin(θ) * np.cos(φ)
        y = radius * np.sin(θ) * np.sin(φ)
        z = radius * np.cos(θ)
        return x, y, z