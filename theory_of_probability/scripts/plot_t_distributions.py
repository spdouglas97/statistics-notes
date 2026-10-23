from pathlib import Path

import matplotlib
import numpy as np
from scipy.stats import norm
from scipy.stats import t

matplotlib.use("Agg")

import matplotlib.pyplot as plt

degrees_of_freedom = [3, 20]
x_values = np.linspace(-5, 5, 1000)

for df in degrees_of_freedom:
    density = t.pdf(x_values, df=df)
    plt.plot(x_values, density, linewidth=2, label=f"t(df={df})")

normal_density = norm.pdf(x_values)
plt.plot(
    x_values,
    normal_density,
    color="k",
    linestyle="--",
    linewidth=2,
    label="Normal(0,1)",
)

plt.xlabel("x")
plt.ylabel("Density")
plt.legend()
output_path = (
    Path(__file__).resolve().parent.parent / "images" / "t_distribution_comparison.png"
)
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=200, bbox_inches="tight")
plt.close()
