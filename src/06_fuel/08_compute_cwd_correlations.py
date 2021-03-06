"""

"""

import os

import pandas as pd
from scipy.stats import pearsonr

from src.utils.constants import REGIONS, SAMPLING_PROPORTION, RANDOM_SEED

if __name__ == "__main__":

    # Project's root
    os.chdir("../..")

    spatial_corr = pd.DataFrame(columns=["region", "r", "p_value", "n"])
    temporal_corr = pd.DataFrame(columns=["region", "r", "p_value", "n"])

    output_folder = f"results/xlsx"
    save_to1 = os.path.join(output_folder, "burned_area_cwd_corr.xlsx")
    with pd.ExcelWriter(save_to1) as writer1:
        for region in REGIONS:
            region_name = region.get("name")
            output_folder = f"results/xlsx/{region_name}"
            save_to2 = os.path.join(output_folder, "burned_area_cwd_values.xlsx")
            with pd.ExcelWriter(save_to2) as writer2:
                # ---------- Spatial (grid) correlations ----------
                fn = f"results/csv/{region_name}/burned_area_and_cwd_samples.csv"
                df = pd.read_csv(fn)
                df = df.dropna()
                df = df[df["burned_area"] > 0]
                df = df.sample(
                    frac=SAMPLING_PROPORTION / df["year"].unique().size,
                    random_state=RANDOM_SEED
                )
                df.to_excel(writer2, sheet_name="Spatial", index=False)
                r, p_value = pearsonr(df["burned_area"], df["cwd"])
                spatial_corr.loc[len(spatial_corr)] = [region_name, r, p_value, len(df)]

                # ---------- Temporal (time series) correlations ----------
                fire_series_fn = f"results/xlsx/{region_name}/fire_series.xlsx"
                fire_series = pd.read_excel(fire_series_fn, sheet_name="Monthly")
                cwd_series_fn = f"results/xlsx/{region_name}/cwd_series.xlsx"
                cwd_series = pd.read_excel(cwd_series_fn, sheet_name="Monthly")
                series = pd.concat([fire_series["area"], cwd_series["cwd"]], axis=1)
                series.index = cwd_series.time
                series = series[series.index.month.isin([1, 2, 3])]
                series = series.resample("Y").sum()
                series.to_excel(writer2, sheet_name="Temporal", index=False)
                r, p_value = pearsonr(series["area"], series["cwd"])
                temporal_corr.loc[len(temporal_corr)] = [
                    region_name, r, p_value, len(series)
                ]

        spatial_corr.to_excel(writer1, sheet_name="Spatial", index=False)
        temporal_corr.to_excel(writer1, sheet_name="Temporal", index=False)