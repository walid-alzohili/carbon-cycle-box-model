# Modeling The Carbon Cycle With A Box-Model


## 📖 Description
This project predicts global temperature changes from the year 2022 (present day) through the year 2100 using a **Carbon Cycle Box-Model** based on the work of **Akira Tomizuka (2009)**.

The model functions in two primary stages:
1. **CO2 Projection:** Predicts atmospheric CO2 concentrations based on various future CO2 emission scenarios.
2. **Climate Response:** Translates those concentrations into global temperature anomalies.

By comparing different emission pathways, this project highlights the direct impact of human activity on the climate and the necessity of mitigation strategies.


## ⚙️ Requirements
- This project uses [uv](https://docs.astral.sh/uv/) to manage the dependencies.
- All dependencies are listed in `pyproject.toml`
- Using PyCharm as an IDE is recommended, but not a strict requirement.


## 🚀 Quick Start

### 1. Setup Environment
- Clone the repository.
- Install dependencies using `uv` by running `uv sync`.
- If using PyCharm, point PyCharm to the local virtual environment, then open new terminal windowm, otherwise activate the environment by running `source .venv/bin/activate`.
- Activate Git hooks: Run `pre-commit install`.
- Install the assets:
    - Run the script `./setup_remote_files.py`, this downloades a zip file with the
      necessary assets. Those assets are not in the repo because they are not source code.
    - Unzip the file by running `unzip assets.zip`.
    - Delete the zip file it is no longer needed.

### 2. Data Pre-processing
- Clean and prepare the raw data by running the pre-processing script `./data_pre_processing.py`
- This will create a csv dataset with the needed columns only.

### 3. Run the predictive model and visualize the results.
- For this project we use marimo notebooks, run the result.py notebook by running `marimo edit notebooks/result.py`
- The notebook will open in a browser, run all cells to visualize the results.


## 📄 Report
A detailed breakdown of the mathematical model and findings can be found in the report: [https://vormada.com/share/carbon_modeling/modeling_the_carbon_cycle_with_a_box_model.pdf](https://vormada.com/share/carbon_modeling/modeling_the_carbon_cycle_with_a_box_model.pdf)
