import numpy as np
from numpy import random
from scipy.stats import norm
import matplotlib.pyplot as plt

class OptionPricer:
    """
    Option pricing models and visualisation functions.
    
    Parameters
    ----------
    S_0 : float
        Initial stock price.
    r : float
        Risk-free interest rate.
    sigma : float
        Volatility.
    T : float
        Time till expiry (years).
    K : float
        Strike price.
    seed : int
        Random number generator seed used in np.random.
    """

    def __init__(self, S_0, r, sigma, T, K, seed):
        self.S_0 = S_0
        self.r = r
        self.sigma = sigma
        self.T = T
        self.K = K
        self.rng = np.random.default_rng(seed)
    
    def GBM_model(self, simulations, d_t, antithetic_var=False):
        """
        Geometric Brownian Motion Monte Carlo simulation model for pricing options.
        
        Parameters
        ----------
        simulations : int
            The number of steps taken in the simulation.
        d_t : float
            Simulation time step.
        antithetic_var : bool
            Whether antithetic variates technique used.

        Returns 
        np.ndarray
            (simulation, step) matrix containing stock prices along all simulated paths.
        """

        steps = round(self.T / d_t)
        if antithetic_var:
        
            if antithetic_var and simulations % 2 != 0:
                raise ValueError("simulations must be even when using antithetic variates.")
            
            Z = self.rng.normal(size=(steps, simulations // 2))
            Z = np.concatenate((Z, -Z), axis=1)
        else:
            Z = self.rng.normal(size=(steps, simulations))

        increments = (
            (self.r - 0.5*(self.sigma**2)) * d_t
            + self.sigma * np.sqrt(d_t) * Z
        )

        log_paths = np.vstack([
            np.zeros(simulations),
            np.cumsum(increments, axis=0)
        ])
        paths = self.S_0 * np.exp(log_paths)
        
        return paths

    
    def Black_Scholes(self, option_type):
        """
        Black-Scholes formula for pricing European options.

        Parameters
        ----------
        option_type : str
            Takes values "call" or "put" for the type of option.

        Returns
        -------
        float
            Black-Scholes option price estimate.
        """

        d_1 = (np.log(self.S_0 / self.K) + (self.r + 0.5*self.sigma**2)*self.T) / (self.sigma * np.sqrt(self.T))
        d_2 = d_1 - (self.sigma * np.sqrt(self.T))

        #put option (non dividend paying stock)
        if option_type == "put":
            P = self.K*np.exp(-self.r * self.T) * norm.cdf(-d_2) - self.S_0 * norm.cdf(-d_1)
            return P
        
        #call option
        C = self.S_0*norm.cdf(d_1) - self.K*np.exp(-self.r * self.T) * norm.cdf(d_2)
    
        return C


    def payoff(self, paths, market_type, option_type):
        """
        Calculates and returns the expected payoff of an option.
        
        Parameters
        ----------
        paths : np.ndarray
            (simulation, step) matrix containing stock prices along all simulated paths.
        market_type : str
            Takes values "european" or "asian" for the market type.
        option_type : str
            Takes values "call" or "put" for the type of option.

        Returns
        -------
        float
            Expected payoff of the option.
        
        """

        if market_type == "european":
            prices = paths[-1]

        elif market_type == "asian":
            prices = paths.mean(axis=0)
            

        if option_type == "call":
            return np.maximum(prices - self.K, 0)

        elif option_type == "put":
            return np.maximum(self.K - prices, 0)
        

    def visualise_GBM(self, simulations, d_t, market_type, option_type, antithetic_var=False):
        """
        Plots all GBM stock price paths and a horisontal histogram 
        to the right showing the distribution of prices at expiry.

        Parameters
        ----------
        simulations : int
            The number of steps taken in the simulation.
        d_t : float
            Simulation time step.
        market_type : str
            Takes values "european" or "asian" for the market type.
        option_type : str
            Takes values "call" or "put" for the type of option.
        antithetic_var : bool
            Whether antithetic variates technique used.

        Returns
        -------
        float
            Monte Carlo option price estimate.
        """

        paths = self.GBM_model(simulations, d_t, antithetic_var)

        market_type = market_type.lower()
        option_type = option_type.lower()
    
        if market_type not in ("european", "asian"):
            raise ValueError("set option_type to European or Asian")
        if option_type not in ("put", "call"):
            raise ValueError("option_type must be Call or Put.")

        payoffs = self.payoff(paths, market_type, option_type)
        
        if antithetic_var:
            payoffs = (payoffs[:simulations // 2] + payoffs[simulations // 2:]) / 2
    
        Vns = np.exp(-self.r*self.T) * payoffs
        mean_Vn = Vns.mean()
        
        # For comparing ordinary and antithetic variate std's
        print(f"Monte Carlo Option Prices Standard Deviation: {Vns.std():.2f}")
    
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
            self.S_0,
            color="black",
            alpha=0.7,
            linestyle="--",
            label=f"Initial stock price: {self.S_0:.1f}GBX"
        )
        ax_plot.set_title(
            f"GBM for {market_type} {option_type} options"
        )
        
        ax_plot.set_ylabel("SHELL stock price (GBX)")
        ax_plot.set_xlabel("Days elapsed")
        
        ax_plot.legend()
        
        ax_hist.hist(
            histogram_data, 
            bins=30,
            orientation = "horizontal",
            label=f"Average price at expiry: {paths[:,-1].mean():.2f}GBX\nstandard deviation: {paths[:,-1].std():.2f}GBX"
        )
        ax_hist.set_title(hist_title)
        ax_hist.set_xlabel("Frequency")
        ax_hist.legend()

        # Remove the gap between the axes
        fig.subplots_adjust(wspace=0)

        # Hide y-axis labels on histogram
        ax_hist.tick_params(axis="y", labelleft=False)

        plt.show()
        plt.close()
        
        return mean_Vn