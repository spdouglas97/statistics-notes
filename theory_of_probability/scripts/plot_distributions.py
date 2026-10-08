from pathlib import Path

import matplotlib
from scipy.stats import binom
from scipy.stats import poisson

matplotlib.use("Agg")

import matplotlib.pyplot as plt

poisson_lambda = 3.5
binomial_n = [5, 100]

for n in binomial_n:
    p = poisson_lambda / n
    bins = list(range(n + 1))
    prob = [binom.pmf(k, n, p) for k in bins]

    plt.bar(bins, prob, alpha=0.5, label=f"Binomial(n={n}, p={p:.3f})")

bins = list(range(100))
prob = [poisson.pmf(k, poisson_lambda) for k in bins]
plt.plot(bins, prob, color='k', label=f"Poisson(lambda={poisson_lambda})")

plt.xlabel("k")
plt.ylabel("Probability")
plt.legend()
output_path = (
    Path(__file__).resolve().parent.parent / "images" / "poisson_convergence.png"
)
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=200, bbox_inches="tight")
plt.close()
