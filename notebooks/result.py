import marimo

__generated_with = "0.23.4"
app = marimo.App(width="columns")


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    import src.helper_functions as helper_functions
    from src.scenarios import Scenarios
    from src.system import System

    return Path, Scenarios, System, helper_functions, mo, pd, plt


@app.cell
def _(pd):
    df = pd.read_csv("out/dataset.csv")

    # Inspect the first few rows
    print(df.head())
    return (df,)


@app.cell
def _(df):
    co2_excluding_luc = df["CO2_excluding_LUC_PgC"].to_numpy()
    co2_from_luc = df["CO2_from_LUC_PgC"].to_numpy()
    # total_co2_emission = df["Total_CO2_emission_PgC"].to_numpy()

    print(co2_excluding_luc[:5])
    return co2_excluding_luc, co2_from_luc


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Solve from 1750 to 2021(current time)
    """)
    return


@app.cell
def _(System, co2_excluding_luc, co2_from_luc, df, helper_functions, plt):
    t_start = 1750
    t_end = 2021
    sol = System().solve(t_start, t_end, co2_excluding_luc, co2_from_luc)

    fig_historic_emissions, _ax = plt.subplots(figsize=(6, 4))
    helper_functions.plot_dataframe(
        _ax,
        df,
        r"Historic $\mathrm{CO_2}$ emissions",
        "Emission (PgC/year)",
        [r"$\mathrm{CO_2}$ excluding LUC", r"$\mathrm{CO_2}$ from LUC", r"Total $\mathrm{CO_2}$ emission"],
    )
    plt.show()
    return fig_historic_emissions, sol


@app.cell
def _(helper_functions, pd, plt, sol):
    concentration = helper_functions.calculate_co2_concentration(sol.y[0])
    emissons = pd.DataFrame(
        {
            "year": range(1750, 2022),
            "co2_concentration": concentration,
        }
    )

    fig_historic_concentrations, _ax = plt.subplots(figsize=(6, 4))
    helper_functions.plot_dataframe(_ax, emissons, r"Historic $\mathrm{CO_2}$ concentrations", "Concentration (ppm")
    _ax.legend().set_visible(False)
    plt.show()

    """
    Should be close to 414ppm.
    See https://www.climate.gov/news-features/understanding-climate/climate-change-atmospheric-carbon-
    dioxide#:~:text=The%20global%20average%20carbon%20dioxide,in%20the%2063%2Dyear%20record.
    """
    print(sol.y[0][-1] / 2.13, sol.t[-1])
    return concentration, fig_historic_concentrations


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Solve Scenarios
    """)
    return


@app.cell
def _(Scenarios, System, co2_excluding_luc, co2_from_luc):
    scenarios = Scenarios(co2_from_luc, co2_excluding_luc).get_all()

    _t_start, _t_end = 1750, 2100

    solutions = [
        System().solve(
            _t_start,
            _t_end,
            scenario["co2_excluding_luc"].to_numpy(),
            scenario["co2_from_luc"].to_numpy(),
        )
        for scenario in scenarios
    ]
    return scenarios, solutions


@app.cell
def _(helper_functions, plt, scenarios):
    """Plot the emission for first 4 scenarios."""
    fig_emissions_scenarios_1_to_4, axs = plt.subplots(2, 2, figsize=(10, 6))
    legend = [r"$\mathrm{CO_2}$ excluding LUC", r"$\mathrm{CO_2}$ from LUC", r"Total $\mathrm{CO_2}$ emission"]

    helper_functions.plot_dataframe(axs[0, 0], scenarios[0], "Scenario 1", "Emission (PgC/year)", legend)
    helper_functions.plot_dataframe(axs[0, 1], scenarios[1], "Scenario 2", "Emission (PgC/year)", legend)
    helper_functions.plot_dataframe(axs[1, 0], scenarios[2], "Scenario 3", "Emission (PgC/year)", legend)
    helper_functions.plot_dataframe(axs[1, 1], scenarios[3], "Scenario 4", "Emission (PgC/year)", legend)

    plt.tight_layout()
    plt.show()

    """plot the emission for fifth scenario."""
    fig_emissions_scenario_5, axs = plt.subplots(figsize=(5, 3))
    axs.set_title(r"Plotting $CO_2$ concentration", fontsize=14)

    helper_functions.plot_dataframe(axs, scenarios[4], "Scenario 5", "Emission (PgC/year)", legend)
    plt.tight_layout()
    plt.show()
    return fig_emissions_scenario_5, fig_emissions_scenarios_1_to_4


@app.cell
def _(helper_functions, pd, plt, solutions):
    # calculate concentrations.
    concentrations = [helper_functions.calculate_co2_concentration(sol.y[0]) for sol in solutions]

    # build dataframe for plotting.
    _df = pd.DataFrame(
        {
            "year": range(1750, 2101),
            **{f"scenario_{i + 1}": conc for i, conc in enumerate(concentrations)},
        }
    )

    # plot
    fig_future_concentrations, _ax = plt.subplots(figsize=(6, 4))
    helper_functions.plot_dataframe(
        _ax,
        _df,
        r"Historic and future $\mathrm{CO_2}$ concentrations",
        "Concentration (ppm)",
        [f"Scenario {i + 1}" for i in range(len(concentrations))],
    )
    plt.show()

    # concentrations at year 2100
    for conc in concentrations:
        print(conc[-1])
    return concentrations, fig_future_concentrations


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Calculate temperature change
    """)
    return


@app.cell
def _(concentration, helper_functions, pd, plt):
    delta_t = helper_functions.calculate_delta_t(concentration)

    temperature_change = pd.DataFrame(
        {
            "year": range(1750, 2022),
            "temperature_change": delta_t,
        }
    )

    fig_historic_temperature_change, ax = plt.subplots(figsize=(6, 4))
    helper_functions.plot_dataframe(
        ax,
        temperature_change,
        "Historic temperature change since 1750",
        "Change in degrees",
    )
    plt.show()

    delta_t_1850 = delta_t[100]
    """
    temperataure increase from 1850 to 2021
    should be 1.1 degrees increase since 1850.
    see: https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_LongerReport.pdf
    """
    print(delta_t[-1] - delta_t_1850)
    return (fig_historic_temperature_change,)


@app.cell
def _(concentrations, helper_functions, pd, plt):
    # get the change in temperature for each scenario.
    _delta_t = [helper_functions.calculate_delta_t(conc) for conc in concentrations]

    # build dataframe for visualization
    df_temp = pd.DataFrame(
        {
            "year": range(1750, 2101),
            **{f"Scenario {i + 1}": dt for i, dt in enumerate(_delta_t)},
        }
    )

    # plot
    fig_future_temperature_change, _ax = plt.subplots(figsize=(6, 4))
    helper_functions.plot_dataframe(
        _ax,
        df_temp,
        "Change in temperatures from 1750 to 2100",
        "Change in degrees",
    )
    plt.show()

    print(
        """
    Temperature between 1850 and 2100.

    This is used to compare the results of the project with the IPCC report which provide the temperature
    change from 1850 to 2100.
    """
    )
    for _dt in _delta_t:
        print(_dt[-1] - _dt[100])
    return (fig_future_temperature_change,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # save figs
    """)
    return


@app.cell
def _(
    Path,
    fig_emissions_scenario_5,
    fig_emissions_scenarios_1_to_4,
    fig_future_concentrations,
    fig_future_temperature_change,
    fig_historic_concentrations,
    fig_historic_emissions,
    fig_historic_temperature_change,
):
    # Create the directory if it doesn't exist
    Path("out/images").mkdir(parents=True, exist_ok=True)

    fig_historic_emissions.savefig("out/images/historic_emissions.pdf")
    fig_historic_concentrations.savefig("out/images/historic_concentrations.pdf")
    fig_emissions_scenarios_1_to_4.savefig("out/images/emissions_scenarios_1_to_4.pdf")
    fig_emissions_scenario_5.savefig("out/images/emissions_scenario_5.pdf")
    fig_future_concentrations.savefig("out/images/future_concentrations.pdf")
    fig_historic_temperature_change.savefig("out/images/temperature_change.pdf")
    fig_future_temperature_change.savefig("out/images/future_temperature_change.pdf")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
