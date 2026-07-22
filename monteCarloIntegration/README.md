Monte Carlo methods give an intuitive way of approximating solutions to problems where exact solutions are difficult or impossible to obtain.
For example, imagine you needed to find the area under a curve in a maths test. If you place thousands of dots randomly across the entire graph, the proportion of dots landing within the area scaled by the total area of the graph would give an estimate of the area under the curve! 

This is due to two key cornerstones of statistical theory: The law of large numbers and the central limit theorem. The law of large numbers states that as a sample size grows, its average grows closer to the population average. The central limit theorem states that if a sufficient number of random samples are taken of a population, the sample means will follow a normal distribution.

The central limit theorem become relevant when the simulation is repeated many times $(n>30)$. Each simulation will produce a slightly different value, however the distribution of these values approaches a normal distribution with more repeats. Hence, averaging the reults of independent simulations provides a more reliable estimate, and allows the uncertainty in the result to be quantified. Together, these principles underpin the statistical convergence exhibited by Monte Carlo methods.

## Conclusion
The estimates output by the Monte Carlo simulation agree with the precise values given by SciPy's numerical integration. As expected, as the number of random samples increases, error on the estimates decreases (although with diminishing returns), in accordance with the central limit theorem. 

Digging further, log-log analysis of mean absolute error against number of samples gives a gradient close to −0.5. This agrees with theoretical Monte Carlo convergence rate of $O(N^{-1/2})$.

Larger sample sizes therefore improve accuracy. However, they also increase computational cost.
The Monte Carlo algorithm is theoretically $O(N)$, but empirical runtime measurements show that the observed scaling depends on the sample size. At low sample sizes, fixed computational overhead dominates, resulting in sublinear observed scaling, while at very large sample sizes, the runtime increases faster than linearly, indicating the bottlenecks here are closer related to memory and hardware. Hence, an increasing curve is observed in the log-log plot of runtime vs number of samples, instead of the expected straight line of gradient 1 seen in ideal linear scaling.
