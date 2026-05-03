import marimo

__generated_with = "0.23.4"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    import src.helper_functions as helper_functions
    from src.scenarios import Scenarios
    from src.system import System

    return Scenarios, System, helper_functions, mo, pd, plt


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
    return (sol,)


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
    return (concentration,)


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
def _(helper_functions, mo, plt, scenarios):
    _legend = [r"$\mathrm{CO_2}$ excluding LUC", r"$\mathrm{CO_2}$ from LUC", r"Total $\mathrm{CO_2}$ emission"]

    # 1. Pre-compute all figures and store them in a dictionary
    precomputed_figs = {}
    for i, scenario in enumerate(scenarios, 1):
        _fig, _ax = plt.subplots(figsize=(6, 4))
        name = f"Scenario {i}"
        helper_functions.plot_dataframe(_ax, scenario, name, "Emission (PgC/year)", _legend)
        precomputed_figs[name] = _fig

    # 2. Create the dropdown widget
    scenario_selector = mo.ui.dropdown(
        options=list(precomputed_figs.keys()),
        value="Scenario 1",
        label="Select a Scenario:",
    )
    return precomputed_figs, scenario_selector


@app.cell
def _(mo, precomputed_figs, scenario_selector):
    # This cell re-runs on dropdown change, but dictionary lookup is instant!
    selected_figure = precomputed_figs[scenario_selector.value]

    mo.vstack(
        [
            scenario_selector,
            selected_figure,
        ]
    )
    return


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
    return (concentrations,)


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
    return


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
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
