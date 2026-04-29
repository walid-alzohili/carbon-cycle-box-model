"""Create a new dataset with only the data that we need from the original dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

original_data_path = "assets/owid-co2-data.csv"
save_path = Path("out/dataset.csv")
save_path.parent.mkdir(parents=True, exist_ok=True)


def __extract_needed_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Extract the needed data from the original dataset.

    :returns:
        - co2_excluding_luc: Annual total production-based emissions of carbon dioxide (CO2), excluding land-use change,
        measured in millions of tonnes. From 1750 to 2021.
        - co2_from_luc_from_1850: emissions of carbon dioxide from land-use change from 1850 5o 2021.
    """
    # load the data.
    dataset_original = pd.read_csv(original_data_path)
    # create a new dataset with only the rows "world".
    dataset = dataset_original[dataset_original["country"] == "World"]

    co2_excluding_luc = dataset["co2"].to_numpy()

    # co2_including_luc_from_1850: Annual total production-based emissions of carbon dioxide (CO2), including
    # land-use change, measured in millions of tonnes. The data is not available before 1850, so we only take the
    # rows from 1850. From 1850 to 2021.
    co2_including_luc_from_1850 = dataset[dataset["year"] >= 1850]["co2_including_luc"].to_numpy()
    # co2_excluding_luc_from_1850: Annual total production-based emissions of carbon dioxide (CO2), excluding
    # land-use change. From 1850 to 2021.
    co2_excluding_luc_from_1850 = dataset[dataset["year"] >= 1850]["co2"].to_numpy()
    co2_from_luc_from_1850 = co2_including_luc_from_1850 - co2_excluding_luc_from_1850

    return co2_excluding_luc, co2_from_luc_from_1850


def preprocess_data() -> None:
    """Create all the data that we need and store then in a new csv file."""
    co2_excluding_luc, co2_from_luc_from_1850 = __extract_needed_data()

    """the data from luc is not availabe from 1750 to 1850 so we generate by assuming that luc was zero in the year
    1750 and growing linearly to year 1850, as suggested in the project description."""
    co2_from_luc_between_1750_and_1850 = np.linspace(0, co2_from_luc_from_1850[0], 1850 - 1750)

    # combine the data before 1850 and after.
    co2_from_luc = np.append(co2_from_luc_between_1750_and_1850, co2_from_luc_from_1850)

    """Annual total production-based emissions of carbon dioxide (CO2), including land-use change
    from 1750 to 2021"""
    total_co2_emission = co2_excluding_luc + co2_from_luc

    """These values are in million tonnes, but we want them in PgC (petagrams of carbon)"""
    co2_excluding_luc = co2_excluding_luc / 1000
    co2_from_luc = co2_from_luc / 1000
    total_co2_emission = total_co2_emission / 1000

    """Create a new cleaned dataset."""
    # Create a year array
    years = np.arange(1750, 1750 + len(total_co2_emission))

    # Build a DataFrame
    df = pd.DataFrame(
        {
            "year": years,
            "CO2_excluding_LUC_PgC": co2_excluding_luc,
            "CO2_from_LUC_PgC": co2_from_luc,
            "Total_CO2_emission_PgC": total_co2_emission,
        }
    )

    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"\n✅ Done! pre-processed dataset created in {save_path}")


if __name__ == "__main__":
    preprocess_data()
