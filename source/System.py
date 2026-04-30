"""
Create the system of differensial equations.

The system will produce the future CO2 concentrations based on each scenario.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import scipy.integrate as integrate

if TYPE_CHECKING:
    # This import ONLY happens for the linter, not at runtime
    from scipy.integrate._ivp.ivp import OdeResult

# preindustrial transfer coefficients.
k_12 = 60 / 615
k_21 = 60 / 842
k_32 = 52 / 9744
k_43 = 205 / 26280
k_51 = 0.2 / 90000000
k_67 = 62 / 731
k_71 = 62 / 1238
k_23 = 9 / 842
k_34 = 162 / 9744
k_45 = 0.2 / 26280
k_24 = 43 / 842

# preindustrial flux
f_0 = 62

# preindustrial content of carbon in the sea surface
N_2_0 = 842

# pre-industrial concentration.
P_0 = 289

# Define the initial values for amount of carbon in each compartment.
N1_0 = 615
N2_0 = 842
N3_0 = 9744
N4_0 = 26280
N5_0 = 90000000
N6_0 = 731
N7_0 = 1238
y0 = [N1_0, N2_0, N3_0, N4_0, N5_0, N6_0, N7_0]

# fertilization factor the default value is 0.42, but a few values were tried to tune the parameter.
beta = 0.568


def f(p: float) -> float:
    """
    Calculate the net CO2 flux to the biosphere.

    :param p: co2 concentration
    :return: net co2 flux to the biosphere.
    """
    return f_0 * (1 + beta * np.log(p / P_0))


def xi(p: float) -> float:
    """
    Calculate buffer factor.

    :param p: co2 concentration.
    :return: buffer factor.
    """
    return 3.69 + 1.86 * 10 ** (-2) * p - 1.80 * 10 ** (-6) * p**2


def delta(t: int, carbon_emission_from_luc: np.ndarray) -> float:
    """Calculate carbon emission from land usage for year t."""
    t_start = 1750

    return carbon_emission_from_luc[t - t_start]


def gamma(t: int, carbon_emission_execluding_luc: np.ndarray) -> float:
    """Return carbon emission from fossil fuel burning for year t."""
    t_start = 1750
    return carbon_emission_execluding_luc[t - t_start]


class System:
    """Methods N_1 to N_7: The rate equation for each compartment."""

    def solve(self, t_start: int, t_end: int, co2_execluding_luc: np.ndarray, co2_from_luc: np.ndarray) -> OdeResult:
        """Solve the Carbon cycle box model."""
        # the years to solve for.
        time_grid = np.arange(t_start, t_end + 1)

        # Solve the differential equations
        sol = integrate.solve_ivp(
            self.system,
            [t_start, t_end],
            y0,
            args=(co2_execluding_luc, co2_from_luc),
            t_eval=time_grid,
        )

        return sol

    def system(self, t: float, y: np.ndarray, co2_execluding_luc: np.ndarray, co2_from_luc: np.ndarray) -> list:
        """Represent the Carbon cycle box model."""
        # convert carbon dioxide to carbon.
        carbon_emission_execluding_luc = co2_execluding_luc * 0.27
        carbon_emission_from_luc = co2_from_luc * 0.27

        return [
            self.n_1(t, y, carbon_emission_execluding_luc, carbon_emission_from_luc),
            self.n_2(t, y),
            self.n_3(t, y),
            self.n_4(t, y),
            self.n_5(t, y),
            self.n_6(t, y, carbon_emission_from_luc),
            self.n_7(t, y, carbon_emission_from_luc),
        ]

    @staticmethod
    def n_1(
        t: float, y: np.ndarray, carbon_emission_execluding_luc: np.ndarray, carbon_emission_from_luc: np.ndarray
    ) -> float:
        """Rate-equation for the atmosphere."""
        carbon_content = y[0]
        # co2 concentration
        p = carbon_content / 2.13

        gamma_term = gamma(int(t), carbon_emission_execluding_luc)
        delta_term = delta(int(t), carbon_emission_from_luc)

        return (
            -k_12 * y[0]
            + k_21 * (N_2_0 + xi(p) * (y[1] - N_2_0))
            + gamma_term
            - f(p)
            + delta_term
            + k_51 * y[4]
            + k_71 * y[6]
        )

    @staticmethod
    def n_2(_t: float, y: np.ndarray) -> np.ndarray:
        """Rate-equation for the surface of ocean."""
        carbon_content = y[0]
        # co2 concentration
        p = carbon_content / 2.13
        return k_12 * y[0] - k_21 * (N_2_0 + xi(p) * (y[1] - N_2_0) - k_23 * y[1] + k_32 * y[2] - k_24 * y[1])

    @staticmethod
    def n_3(_t: float, y: np.ndarray) -> float:
        """Rate-equation for the intermediate ocean."""
        return k_23 * y[1] - k_32 * y[2] - k_34 * y[2] + k_43 * y[3]

    @staticmethod
    def n_4(_t: float, y: np.ndarray) -> float:
        """Rate-equation for the deep ocean."""
        return k_34 * y[2] - k_43 * y[3] + k_24 * y[1] - k_45 * y[3]

    @staticmethod
    def n_5(_t: float, y: np.ndarray) -> float:
        """Rate-equation for the sediments."""
        return k_45 * y[3] - k_51 * y[4]

    @staticmethod
    def n_6(t: float, y: np.ndarray, carbon_emission_from_luc: np.ndarray) -> float:
        """Rate-equation for the biosphere."""
        carbon_content = y[0]
        # co2 concentration :math:`P`.
        p = carbon_content / 2.13

        delta_term = delta(int(t), carbon_emission_from_luc)

        return f(p) - k_67 * y[5] - 2 * delta_term

    @staticmethod
    def n_7(t: float, y: np.ndarray, carbon_emission_from_luc: np.ndarray) -> float:
        """Rate-equation for the soil."""
        delta_term = delta(int(t), carbon_emission_from_luc)
        return k_67 * y[5] - k_71 * y[6] + delta_term
