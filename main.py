# ==========================================
# 4. PLATFORM INITIALIZATION
# ==========================================

# 1. Instantiate the Data Processor and load the Ovako CSV
# (Uses the class defined in Block 2)
flange_test = MaterialDataProcessor('data/ovako_100cr6_variants.csv')
flange_test.load()

# 2. Define the global rotation range (0 to 180 degrees)
# 181 points ensures a data point for every single degree.
angle_range = np.linspace(0, 180, 181)

# 3. Initialize the Engine with the loaded data
# (Uses the class defined in Block 3)
engine = AnisotropyEngine(flange_test.df)

print(f"✅ Initialization Complete: Engine primed with {len(flange_test.df)} steel variants.")

# ==========================================
# 5. SPECIMEN SELECTION
# ==========================================

# 1. Identify the rows with the absolute Maximum and Minimum Yield Strength
# .idxmax() and .idxmin() return the index (row number) of these extremes
idx_max = flange_test.df['Yield_strength'].idxmax()
idx_min = flange_test.df['Yield_strength'].idxmin()

# 2. Extract the full data rows as separate DataFrames
# Using .copy() ensures we don't accidentally modify the original dataset
spec_high = flange_test.df.iloc[idx_max:idx_max+1].copy()
spec_low = flange_test.df.iloc[idx_min:idx_min+1].copy()

# 3. Log the selection for the debugging record
# This prints the Variant name (e.g., 803D_QTb) and its base strength
print(f"🎯 Analysis Target 1 (High): {spec_high['Variant'].values[0]} ({spec_high['Yield_strength'].values[0]} MPa)")
print(f"🎯 Analysis Target 2 (Low):  {spec_low['Variant'].values[0]} ({spec_low['Yield_strength'].values[0]} MPa)")

# ==========================================
# 6. SIMULATION EXECUTION: ANISOTROPY SWEEP
# ==========================================

# 1. Initialize fresh containers for the results
results_high_yield = []
results_low_yield = []

# 2. Perform the sweep across the angle_range (0 to 180 degrees)
for angle in angle_range:
    
    # --- Process High Strength Specimen ---
    spec_high['Angle_deg'] = angle
    engine.set_data(spec_high)
    # Extract only the predicted yield point [0] from the engine's 3-part return
    res_h = engine.predict(0, 1)[0]
    results_high_yield.append(res_h)
    
    # --- Process Low Strength Specimen ---
    spec_low['Angle_deg'] = angle
    engine.set_data(spec_low)
    res_l = engine.predict(0, 1)[0]
    results_low_yield.append(res_l)

print(f"✅ Simulation Complete: {len(results_high_yield)} data points generated.")

# ==========================================
# 7. FINAL VISUALIZATION & COMPARISON
# ==========================================
plt.figure(figsize=(12, 6))

# Plot the Max/Min curves
# These lists were populated in the previous Simulation Loop block
plt.plot(angle_range, results_high_yield, label='Max Yield Variant (High Strength)', color='royalblue', linewidth=2)
plt.plot(angle_range, results_low_yield, label='Min Yield Variant (Low Strength)', color='crimson', linewidth=2, linestyle='--')

# Styling and Annotations
plt.title("Directional Yield Strength Comparison (Ovako Dataset)", fontsize=14, fontweight='bold')
plt.xlabel("Rolling Direction Angle (Degrees)", fontsize=12)
plt.ylabel("Predicted Yield Stress (MPa)", fontsize=12)

# Major marks at 0, 45, 90, 135, 180 to highlight anisotropy peaks
plt.xticks(np.arange(0, 181, 45)) 

plt.grid(True, which='both', linestyle=':', alpha=0.6)
plt.legend(frameon=True, shadow=True, loc='best')

# Final output
plt.tight_layout()
plt.show()
plt.savefig("outputs/comparison_plot.png")

# ==========================================
# 8. RESULTS VALIDATION & DATA EXPORT
# ==========================================

# 1. Validation: Extracting values at the 90-degree transverse point (Index 90)
# This confirms the vertical gap seen on your 'M-graph'
val_h = results_high_yield[90]
val_l = results_low_yield[90]
diff = val_h - val_l

# 2. Summary Report
print("-" * 40)
print(f"ANISOTROPY PERFORMANCE SUMMARY (at 90°)")
print("-" * 40)
print(f"High Strength Variant: {val_h:.2f} MPa")
print(f"Low Strength Variant:  {val_l:.2f} MPa")
print(f"Absolute Difference:   {diff:.2f} MPa")
print(f"Performance Ratio:     {(val_h/val_l):.2f}x")
print("-" * 40)

# Optional: Log the final validation to your WSL logger
logger.info(f"Validation complete. Max/Min gap is {diff:.2f} MPa.")
