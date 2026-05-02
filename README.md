# Modeling The Carbon Cycle With A Box-Model


## 📖 Description
This project predicts global temperature changes from the present day through the year 2100 using a **Carbon Cycle Box-Model** based on the work of **Akira Tomizuka (2009)**.

The model functions in two primary stages:
1. **CO2 Projection:** Predicts atmospheric CO2 concentrations based on various anthropogenic emission scenarios.
2. **Climate Response:** Translates those concentrations into global temperature anomalies.

By comparing different emission pathways, this project highlights the direct impact of human activity on the climate and the necessity of mitigation strategies.


## 📄 Report
A detailed breakdown of the mathematical model and findings can be found in the report: [https://vormada.com/share/carbon_modeling/modeling_the_carbon_cycle_with_a_box_model.pdf](https://vormada.com/share/carbon_modeling/modeling_the_carbon_cycle_with_a_box_model.pdf)


## ⚙️ Requirements
- This project uses [uv](https://docs.astral.sh/uv/) for lightning-fast dependency management.
- All dependencies are listed in `pyproject.toml`


## 🚀 Usage

### 1. Setup Environment
- Clone the repository.
- Install dependencies using `uv` by running `uv sync`.
- Point PyCharm to the local virtual environment.
- Activate Git hooks: Run `pre-commit install`.
- Install the assets:
    - run the script `./setup_remote_files.py`, this downloades a zip file with the
      necessary assets. Those assets are not in the repo because they are not source code.
    - unzip the file by running `unzip assets.zip`.
    - delete the zip file it is no longer needed.

### 2. Data Pre-processing
- Clean and prepare the raw data by running the pre-processing script `./data_pre_processing`
- This will create the pre processed dataset.
