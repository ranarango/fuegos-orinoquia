# -----------------------------------------------------------------------
# Author: Marcelo Villa-Piñeros
#
# Purpose: Determines whether there is an interannual trend amongst
# burned area values for each window. The trend is determined by running
# the Mann-Kendall trend test on the yearly median burned area values.
# -----------------------------------------------------------------------
import os

import pandas as pd
import pymannkendall as mk

from src.utils.constants import REGIONS


if __name__ == "__main__":

    # Project's root
    os.chdir("../..")

    output_folder = "results/csv"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df = pd.DataFrame(
        columns=[
            "window",
            "trend",
            "has_trend",
            "p_value",
            "z",
            "tau",
            "s",
            "variance",
            "slope",
            "intercept",
        ]
    )

    for region in REGIONS:

        series_filepath = f"results/xlsx/{region['name']}/fire_series.xlsx"
        monthly_series = pd.read_excel(series_filepath, sheet_name="Monthly")

        # Make sure the time column in the monthly series is interpreted.
        # as datetime.
        monthly_series["time"] = pd.to_datetime(monthly_series["time"])
        monthly_series = monthly_series.query("time.dt.month in (1, 2, 3)")

        # Compute the median year-wise.
        yearly_medians = monthly_series.resample("Y", on="time").median()

        # Run Mann-Kendall trend test on the medians.
        mk_trend_test_result = mk.original_test(yearly_medians, alpha=0.05)

        df.loc[len(df)] = [region["name"]] + list(mk_trend_test_result)

    save_to = os.path.join(output_folder, "burned_area_interannual_season_trend.csv")
    df.to_csv(save_to, index=False)
