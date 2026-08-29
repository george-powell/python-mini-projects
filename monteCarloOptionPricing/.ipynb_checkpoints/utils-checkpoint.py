import numpy as np
from numpy import random
from scipy.stats import norm
import matplotlib.pyplot as plt

#set seed for reproducibility
rng = np.random.default_rng(10)

def GBM_model(simulations, S_0, r, sigma, T, d_t, antithetic_var=False):

    steps = round(T / d_t)
    if antithetic_var:
        
        if antithetic_var and simulations % 2 != 0:
            raise ValueError("simulations must be even when using antithetic variates.")
            
        Z = rng.normal(size=(steps, simulations // 2))
        Z = np.concatenate((Z, -Z), axis=1)
    else:
        Z = rng.normal(size=(steps, simulations))

    increments = (
        (r - 0.5*(sigma**2)) * d_t
        + sigma * np.sqrt(d_t) * Z
    )

    log_paths = np.vstack([
        np.zeros(simulations),
        np.cumsum(increments, axis=0)
    ])
    paths = S_0 * np.exp(log_paths)
        
    return paths

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
def Black_Scholes(S_0, r, sigma, T, K, option_type):

    d_1 = (np.log(S_0 / K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))
    d_2 = d_1 - (sigma * np.sqrt(T))

    #put option (non dividend paying stock)
    if option_type == "put":
        P = K*np.exp(-r * T) * norm.cdf(-d_2) - S_0 * norm.cdf(-d_1)
        print(f"The Black-Scholes model gave a european put option price of £{P[0]:.2f}.")
        return P[0]
        
    #call option
    C = S_0*norm.cdf(d_1) - K*np.exp(-r * T) * norm.cdf(d_2)

    print(f"The Black-Scholes model gave a european call option price of £{C[0]:.2f}.")
    
    return C[0]

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
def payoff(paths, K, market_type, option_type):

    if market_type == "european":
        prices = paths[-1]

    elif market_type == "asian":
        prices = paths.mean(axis=0)

    if option_type == "call":
        return np.maximum(prices - K, 0)

    elif option_type == "put":
        return np.maximum(K - prices, 0)
        
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
def visualise_GBM(simulations, S_0, r, sigma, T, K, d_t, market_type, option_type, antithetic_var=False):

    paths = GBM_model(simulations, S_0, r, sigma, T, d_t, antithetic_var)

    market_type = market_type.lower()
    option_type = option_type.lower()
    
    if market_type not in ("european", "asian"):
        raise ValueError("set option_type to European or Asian")
    
    if option_type not in ("put", "call"):
        raise ValueError("option_type must be call or put.")

    payoffs = payoff(paths, K, market_type, option_type)
    optionPrice = np.exp(-r*T) * payoffs.mean()
    
    if market_type == "european":
        histogram_data = paths[-1]
        hist_title = "Visualisation of stock price distribution at expiry"

    elif market_type == "asian":
        histogram_data = paths.mean(axis=0)
        hist_title = "Visualisation of the distribution of lifetime average stock prices"

    else:
        raise ValueError("set option_type to European or Asian")

    # plotting paths
    fig, (ax_plot, ax_hist) = plt.subplots(
        1, 2, 
        figsize=(18,6), 
        width_ratios=[2,1],
        sharey = True
    )
    ax_plot.plot(paths)
    ax_plot.axhline(
        S_0,
        color="black",
        linestyle="--",
        label=f"Initial stock price: £{S_0:.1f}"
    )
    ax_plot.set_title(
        f"{simulations} GBM simulations\nEstimated {market_type} {option_type} option price = £{optionPrice:.2f}"
    )
    ax_plot.legend()
        
    ax_hist.hist(
        histogram_data, 
        bins=30,
        orientation = "horizontal"
    )
    ax_hist.set_title(hist_title)

    # Remove the gap between the axes
    fig.subplots_adjust(wspace=0)

    # Hide y-axis labels on histogram
    ax_hist.tick_params(axis="y", labelleft=False)

    plt.show()

    return optionPrice