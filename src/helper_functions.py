"""Provide helper functions for plotting and performing calculations."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .system import P_0

if TYPE_CHECKING:
    import matplotlib.axes
    import pandas as pd

# found by experiment (value should be higher than 0.27)
climate_sensitivity_parameter_lambda = 0.62


def plot_dataframe(
    ax: matplotlib.axes.Axes,
    df: pd.DataFrame,
    title: str,
    y_label: str,
    legend: str | list | None = None,
) -> None:
    """Plot a dataframe with standardized formatting."""
    df.plot(x="year", ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel("Time(year)", fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    if legend:
        ax.legend(legend)
    else:
        ax.legend().remove()


def calculate_co2_concentration(total_amount_of_carbon: np.ndarray) -> np.ndarray:
    """
    Calculate atmospheric concentration of CO2 in ppm.

    :param total_amount_of_carbon: one dimentional array.
    :returns One dimentional array:  Atmospheric concentration of CO2 in ppm.
    """
    return total_amount_of_carbon / 2.13


def radiative_forcing(p: np.ndarray, p_0: int) -> np.ndarray:
    r"""
    Calculate radioactive forcing :math:`\Delta F`.

    :param p: current concentration.
    :param p_0: pre-industrial concentration.
    """
    return 5.35 * np.log(p / p_0)


def calculate_delta_t(concentration: np.ndarray) -> np.ndarray:
    r"""
    Calculate the change in temperature :math:`\Delta T` since 1850.

    :param concentration: current concentration.
    """
    return climate_sensitivity_parameter_lambda * radiative_forcing(concentration, P_0)
