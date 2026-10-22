from features.amfi_navhistory import NAVFetcher
from features.pofo_data import MFdata
from features.config import URL, CACHE_DIR 
# from features.config_folio import FOLIO_DIR, FOLIO_MAP
import streamlit as st

def get_data(pdf, password, opt, folio_details: str| None =None):
    fetch= NAVFetcher(url= URL, cache_directory= CACHE_DIR)
    proc= MFdata(pdf_path= pdf, passw= password, fetcher= fetch)

    if opt == "1-D":
        df= proc.get_processed_folio_data(timeframe= "1-D", folio_details=folio_details)
    elif opt == "1-W":
        df= proc.get_processed_folio_data(timeframe= "1-W", folio_details=folio_details)
    elif opt == "1-M":
        df= proc.get_processed_folio_data(timeframe= "1-M", folio_details=folio_details)
    elif opt == "1-Q":
        df= proc.get_processed_folio_data(timeframe= "1-Q", folio_details=folio_details)
    elif opt == "1-Y":
        df= proc.get_processed_folio_data(timeframe= "1-Y", folio_details=folio_details)
    elif opt == "3-Y":
        df= proc.get_processed_folio_data(timeframe= "3-Y", folio_details=folio_details)
    elif opt == "5-Y":
        df= proc.get_processed_folio_data(timeframe= "5-Y", folio_details=folio_details)
    else:
        raise ValueError(
            "Invalid timeframe. Use 'Daily', 'Weekly', 'Monthly', 'Quarterly' or 'Yearly'"
        )

    return df

def metrics(data):
    value=  data["Current Value"].sum().round()
    value_delta= f"{((data['Total Gain'].sum())/data['Cost Value'].sum()):.2%}"
    gain= data["Total Gain"].sum().round()
    gain_delta= data["Gain"].sum().round(2)
    cost_value= data["Cost Value"].sum().round()
    perc= f"{(data["All-Portfolio %"].sum()/100):.0%}"

    return value, value_delta, gain, gain_delta, cost_value, perc

def get_grouped_data(data, by):
    agg_num_col={
        "All-Portfolio %": "mean",
        "Cost Value":"sum",
        "Current Value": "sum",
        "Total Gain %": "mean",
        "Total Gain": "sum",
        "Gain": "sum",
        "Gain %": "mean"
    }
    return data.groupby(by).agg(agg_num_col)


    