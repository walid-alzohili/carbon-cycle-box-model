"""provide the :class:`Scenarios` class, which generates the training data for each of the emission scenarios."""

import numpy as np
import pandas as pd


class Scenarios:
    """Provide the emission data for each scenario."""

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

    def get_all(self) -> tuple[pd.DataFrame, ...]:
        """Return the emission data for each scenario."""
        return self.scenario_1(), self.scenario_2(), self.scenario_3(), self.scenario_4(), self.scenario_5()

    def scenario_1(self) -> pd.DataFrame:
        """Return emission data for scenario 1."""
        # linearly decreasing co2 emissions to reach 0 by 2050.
        co2_excluding_luc_2021_2050 = np.linspace(self.historic_co2_excluding_luc[-1], 0, 2050 - 2021)

        # linearly decreasing co2 emissions to reach -20 by 2100.
        co2_excluding_luc_2050_2100 = np.linspace(co2_excluding_luc_2021_2050[-1], -15, 2100 - 2050)

        # values from 1750 to 2100.
        co2_excluding_luc = np.append(
            np.append(self.historic_co2_excluding_luc, co2_excluding_luc_2021_2050), co2_excluding_luc_2050_2100
        )

        return pd.DataFrame(
            {
                "year": range(1750, 2101),
                "co2_excluding_luc": co2_excluding_luc,
                "co2_from_luc": self.co2_from_luc_scenarios,
                "total": co2_excluding_luc + self.co2_from_luc_scenarios,
            }
        )

    def scenario_2(self) -> pd.DataFrame:
        """Return emission data for scenario 2."""
        # linearly decreasing co2 emissions to reach 0 by 2050.
        scenario_2_part_1 = np.linspace(self.historic_co2_excluding_luc[-1], -10, 2090 - 2021)

        """sabelize at -10 after 2090."""
        mean = -10
        # Calculate 10% of the absolute magnitude
        offset = abs(mean) * 0.1  # result is 1.0

        # -10 minus 1 is -11 (The actual "low" value)
        range_min = mean - offset
        # -10 plus 1 is -9 (The actual "high" value)
        range_max = mean + offset

        scenario_2_part_2 = self.rng.uniform(low=range_min, high=range_max, size=10)

        """values from 1750 to 2100."""
        co2_excluding_luc = np.append(
            np.append(self.historic_co2_excluding_luc, scenario_2_part_1),
            scenario_2_part_2,
        )

        return pd.DataFrame(
            {
                "year": range(1750, 2101),
                "co2_excluding_luc": co2_excluding_luc,
                "co2_from_luc": self.co2_from_luc_scenarios,
                "total": co2_excluding_luc + self.co2_from_luc_scenarios,
            }
        )

    def scenario_3(self) -> pd.DataFrame:
        """Return emission data for scenario 3."""
        # linearly decreasing co2 emissions to reach 0 by 2050.
        scenario_3_part_1 = np.linspace(self.historic_co2_excluding_luc[-1], 45, 2045 - 2021)

        scenario_3_part_2 = np.linspace(scenario_3_part_1[-1], 10, 2100 - 2045)

        # values from 1750 to 2100.
        co2_excluding_luc = np.append(
            np.append(self.historic_co2_excluding_luc, scenario_3_part_1),
            scenario_3_part_2,
        )

        return pd.DataFrame(
            {
                "year": range(1750, 2101),
                "co2_excluding_luc": co2_excluding_luc,
                "co2_from_luc": self.co2_from_luc_scenarios,
                "total": co2_excluding_luc + self.co2_from_luc_scenarios,
            }
        )

    def scenario_4(self) -> pd.DataFrame:
        """Return emission data for scenario 4."""
        # linearly decreasing co2 emissions to reach 0 by 2050.
        scenario_4_part_1 = np.linspace(self.historic_co2_excluding_luc[-1], 80, 2100 - 2021)

        # values from 1750 to 2100.
        co2_excluding_luc = np.append(self.historic_co2_excluding_luc, scenario_4_part_1)

        return pd.DataFrame(
            {
                "year": range(1750, 2101),
                "co2_excluding_luc": co2_excluding_luc,
                "co2_from_luc": self.co2_from_luc_scenarios,
                "total": co2_excluding_luc + self.co2_from_luc_scenarios,
            }
        )

    def scenario_5(self) -> pd.DataFrame:
        """Return emission data for scenario 5."""
        # linearly decreasing co2 emissions to reach 0 by 2050.
        scenario_5_part_1 = np.linspace(self.historic_co2_excluding_luc[-1], 130, 2080 - 2021)

        # sabelize at 130 after 2080.
        mean = 130
        # 10% below the mean
        range_min = mean * 0.9
        # 10% above the mean
        range_max = mean * 1.1
        scenario_5_part_2 = self.rng.uniform(low=range_min, high=range_max, size=2100 - 2080)

        # values from 1750 to 2100.
        co2_excluding_luc = np.append(
            np.append(self.historic_co2_excluding_luc, scenario_5_part_1),
            scenario_5_part_2,
        )

        return pd.DataFrame(
            {
                "year": range(1750, 2101),
                "co2_excluding_luc": co2_excluding_luc,
                "co2_from_luc": self.co2_from_luc_scenarios,
                "total": co2_excluding_luc + self.co2_from_luc_scenarios,
            }
        )
