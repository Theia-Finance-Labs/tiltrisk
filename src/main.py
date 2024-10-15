import os
from .generate_trisk_data import run_r_analysis
from load_data import load_trisk_data

if __name__ == "__main__":
    # Define the paths
    input_path = os.path.join("data", "trisk_inputs_v2_legacy_countries")
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
    # Run the R analysis with the defined parameters
    run_r_analysis(input_path, project_output_path, run_params)

    npv_df, pd_df, params_df, trajectories_df = load_trisk_data(
        source=project_output_path
    )

    # ...
