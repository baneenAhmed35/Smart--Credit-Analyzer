import wbgapi as wb
import pandas as pd

def load_macro_data():

    indicators = {
        "GDP": "NY.GDP.MKTP.CD",
        "Inflation": "FP.CPI.TOTL.ZG",
        "Credit": "FS.AST.PRVT.GD.ZS"
    }

    countries = ["SAU","USA","GBR"]

    macro_df = wb.data.DataFrame(
        list(indicators.values()),
        economy=countries,
        time=range(2015,2024)
    )

    macro_df = macro_df.reset_index()
    macro_df.columns = ["Country","Year","GDP","Inflation","Credit"]
    macro_df = macro_df.dropna()

    return macro_df

