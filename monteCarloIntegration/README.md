# Monte Carlo Integration
## Overview
Monte Carlo methods give an intuitive way of approximating solutions to problems where exact solutions are difficult or impossible to obtain.
For example, imagine you needed to find the area under a curve in a maths test. If you place thousands of dots randomly across the entire graph, the proportion of dots landing within the area scaled by the total area of the graph would give an estimate of the area under the curve! 

This is due to two key cornerstones of statistical theory: The law of large numbers and the central limit theorem. The law of large numbers states that as a sample size grows, its average grows closer to the population average. The central limit theorem states that if a sufficient number of random samples are taken of a population, the sample means will approach a normal distribution.

The central limit theorem becomes relevant when the simulation is repeated many times. Each simulation will produce a slightly different value, however the distribution of these values approaches a normal distribution with more repeats. Hence, averaging the results of independent simulations provides a more reliable estimate, and allows the uncertainty in the result to be quantified. Due to the variance being indirectly proportional to the number of samples, the random error and number of samples are theoretically related by: Error = $O(N^{-1/2})$. Together, these principles underpin the statistical convergence exhibited by Monte Carlo methods.

## Project Objectives

This project investigates the effectiveness of Monte Carlo simulations in estimating values of definite integrals, aiming to:
- Implement Monte Carlo algorithm in Python
- Compare Monte Carlo estimates to numerical integration through SciPy
- Assess how estimate error varies with sample size
- Determine the empirical convergence rate of the Monte Carlo method
- Explore how runtime varies with sample size

## Method
### 1. Simulation
The function `monteCarloSim()` estimates the definite integral by:
- Sampling (x,y) coordinates through `numpy.random`
- Comparing samples to the function to see if they are in the area being integrated
- Multiplying the percentage of samples in the region by the total area samples could be taken from
- This value is then returned as the estimate

NumPy arrays are used for their performance benefits over standard lists and loops.

Note, the function is assumed to be non-negative over the integration interval and that y_max bounds the function. Hence, integrating a function like $y = sin(x)$ over the interval $[0,2\pi]$ will cause `monteCarloSim()` to return an inaccurate positive value.

### 2. Accuracy Analysis

For each given sample size, the Monte Carlo simulation is repeated 100 times. The absolute error of each estimate is calculated from comparison to the value obtained by SciPy's numerical integration. The mean absolute error and standard deviation are then calculated, with results plotted on log-log graphs against sample size. A linear fit is applied to these logged derived values, giving a gradient with which the rate of convergence of the Monte Carlo method can be determined. 

### 3. Computational Cost Analysis

Using Python's built-in time library, runtime was measured for the 100 simulation loop done during accuracy analysis. This was done for each sample size, with results plotted on log-log graphs.

## Results

With the random number generation seed set at 10, the first run of 10,000 samples gave a percentage error of 0.51%. Averaging over 100 simulations for sample sizes increasing ten-fold from 10 to 1,000,000, the empirical convergence rate was estimated at $O(N^{-0.507})$, agreeing with the theoretical $O(N^{-1/2})$. The computational cost analysis was expected to show a linear relationship of gradient 1 between runtime and sample size, with the variables theoretically being $O(N^{1})$. 

However, empirical runtime measurements gave unexpected results. Whilst the theoretical value of 1 did lie in the range experimental values, the scaling factor increased from 0.04 for 10 to 100 samples to 1.29 for 100,000 to 1,000,000 samples. The log-log plot clearly displayed an increasing gradient, instead of the expected straight line of gradient 1 seen in ideal linear scaling. This is likely due to software and hardware bottlenecks not accounted for. At low sample sizes, fixed computational overhead dominates, resulting in sublinear observed scaling, while at very large sample sizes, the runtime increases faster than linearly, indicating the observed behaviour likely reflects memory and hardware limitations. 

## Key Findings
The estimates output by the Monte Carlo simulation agree with the precise values given by SciPy's numerical integration. As expected, as the number of random samples increases, error on the estimates decreases (although with diminishing returns), in accordance with the central limit theorem. 

Digging further, log-log analysis of mean absolute error against number of samples gave a gradient within $\pm{2}$% of −0.5. This agrees with theoretical Monte Carlo convergence rate of $O(N^{-1/2})$.

Larger sample sizes therefore improve accuracy. However, they also increase computational cost.
The Monte Carlo algorithm is theoretically $O(N)$, but empirical runtime measurements show that the observed scaling depends on the sample size. 

## Requirements

The project requires Python and the following third-party packages:
- numpy
- pandas
- matplotlib
- scipy

## Running the Project

Clone the repository and install the required dependencies:

pip install -r requirements.txt

Then open and run the jupyter notebook `main.ipynb`.
The notebook contains the complete implementation, analysis, visualisations and results. 
