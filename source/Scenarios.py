"""provide the :class:`Scenarios` class, which generates the training data for each of the emission scenarios."""

import numpy as np


class Scenarios:
    """Provide the training data for each scenario."""

    def __init__(self, historic_co2_from_luc: np.ndarray, historic_co2_excluding_luc: np.ndarray) -> None:
        self.rng = np.random.default_rng(32)
        self.historic_co2_from_luc = historic_co2_from_luc
        self.historic_co2_excluding_luc = historic_co2_excluding_luc
        self.co2_from_luc_scenarios = self.__co2_from_luc()

    def __co2_from_luc(self) -> np.ndarray:
        """Return CO2 emissions from Land Use Change (LUC) for all scenarios."""
        # luc co2 emission that is the same as historical data.
        last_20_values = self.historic_co2_from_luc[-50:]
        mean = np.mean(last_20_values)
        std = np.std(last_20_values)
        co2_from_luc_2021_2100 = self.rng.normal(loc=mean, scale=std, size=2100 - 2021)

        return np.append(self.historic_co2_from_luc, co2_from_luc_2021_2100)
