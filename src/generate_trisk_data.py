import os
from rpy2 import robjects
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.vectors import ListVector
from typing import List, Dict

# Enable the conversion between Pandas DataFrame and R DataFrame
pandas2ri.activate()


def run_r_analysis(
    input_path: str,
    project_output_path: str,
    run_params: List[Dict],
    country_iso2: str = None,
    sector: str = None,
):
    """
    Runs the R analysis by calling the R function from the provided script.

    Parameters:
    - input_path (str): Path to the input directory for trisk analysis.
    - project_output_path (str): Path where output files will be saved.
    - run_params (list of dicts): List of run parameters.
    - country (str): Country ISO code.
    - sector (str): Sector to analyze.
    """

    # Get the current directory of this Python script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the R script
    r_script_path = os.path.join(current_directory, "country_specific_analysis.R")
    # Import the R script using the full path
    r.source(r_script_path)

    # Convert each dictionary in the list to an R ListVector
    run_params_r = ListVector(
        {str(i): ListVector(params) for i, params in enumerate(run_params)}
    )

    # Define the R function to run
    run_analysis_r = robjects.r["run_country_specific_analysis"]

    # Call the R function with parameters
    run_analysis_r(
        input_path=input_path,
        project_output_path=project_output_path,
        run_params=run_params_r,
        country_iso2=country_iso2,
        sector=sector,
    )


if __name__ == "__main__":
    # Define the paths
    input_path = os.path.join("workspace", "trisk_inputs_v2_legacy_countries")
    project_output_path = os.path.join("workspace", "trisk_outputs")

    # Define the parameters
    run_params = [
        {
            "scenario_geography": "Global",
            "baseline_scenario": "IPR2023_baseline",
            "shock_scenario": "IPR2023_FPS",
            "shock_year": 2030,
        },
        {
            "scenario_geography": "Europe",
            "baseline_scenario": "WEO2021_APS",
            "shock_scenario": "WEO2021_SDS",
            "shock_year": 2030,
        },
    ]

    country_iso2 = None
    sector = "Power"

    # Run the R analysis with the defined parameters
    run_r_analysis(input_path, project_output_path, run_params, country_iso2, sector)
