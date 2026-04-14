# ==========================================
# 2. DATA MANAGEMENT LAYER
# ==========================================

class MaterialDataProcessor:
    def __init__(self, file_path, separator=';'):
        """Identity: Sets up the path and name for the dataset."""
        self.file_path = file_path
        self.separator = separator
        # Handles the name correctly whether you are on Windows or WSL/Linux
        self.file_name = os.path.basename(file_path)
        self.df = None

    def load(self):
        """Reaches into the WSL filesystem to fill the DataFrame with data."""
        try:
            self.df = pd.read_csv(self.file_path, sep=self.separator)
            print(f"✅ Loaded: {self.file_name}")
        except Exception as e:
            print(f"❌ Error loading file: {e}")

    def check_data(self):
        """Simple safety check to ensure data is present before analysis."""
        return self.df is not None

    def create_graph(self, x_col, y_col, title="Data Plot"):
        """Creates a basic scatter plot for initial data exploration."""
        if not self.check_data():
            print("Error! No data loaded.")
            return

        plt.figure(figsize=(10, 5))
        # Coerce handles any stray strings in the numeric columns
        x = pd.to_numeric(self.df[x_col], errors='coerce')
        y = pd.to_numeric(self.df[y_col], errors='coerce')

        plt.scatter(x, y, alpha=0.7, color="blue")
        plt.title(title)
        plt.xlabel(str(x_col))
        plt.ylabel(str(y_col))
        plt.grid(True)
        plt.show()

# ==========================================
# 3. ANISOTROPY COMPUTATION ENGINE
# ==========================================

class AnisotropyEngine:
    def __init__(self, specimen_data=None):
        """Initializes the engine with Hill 1948 parameters."""
        self.data = specimen_data
        # Standard Lankford coefficients for anisotropy
        self.r0 = 0.85
        self.r45 = 1.10
        self.r90 = 0.95
        self.logger = logging.getLogger("AnisotropyEngine")

    def set_data(self, new_data):
        """Updates the material data for the engine."""
        self.data = new_data

    def _get_yield_ratio(self, angle_rad):
        """INTERNAL HELPER: The Hill 1948 Anisotropy Formula. This provides the multiplier for yield stress at a specific angle."""
        # Hill's coefficients based on R-values
        f = 1 / (self.r0 * (1 + self.r90))
        g = self.r0 / (self.r0 * (1 + self.r90))
        h = 1 - g
        n = (self.r45 + 0.5) * (f + g)
        
        c = np.cos(angle_rad)
        s = np.sin(angle_rad)
        
        # The yield ratio calculation
        ratio = np.sqrt(f * s**4 + g * c**4 + h * (c**2 - s**2)**2 + 2 * n * s**2 * c**2)
        return ratio

    def predict(self, start=0, end=1):
        """Calculates yield stress and generates a stress-strain curve."""
        if self.data is None:
            return None

        # 1. Get Base Properties (Force scalar conversion to avoid ValueErrors)
        base_yield = float(self.data['Yield_strength'].iloc[0])
        angle_deg = float(self.data['Angle_deg'].iloc[0])
        angle_rad = np.radians(angle_deg)

        # 2. Apply Anisotropy using the helper method below
        # This is where your error was occurring!
        yield_ratio = self._get_yield_ratio(angle_rad)
        predicted_yield = base_yield * yield_ratio

        # 3. Generate Stress-Strain Curve Data
        strain = np.linspace(start, end, 100)
        stress = predicted_yield * (strain**0.2)
        
        uts_val = np.max(stress)
        uts_idx = np.argmax(stress)

        return predicted_yield, (strain, stress), (strain[uts_idx], uts_val)
