import streamlit as st, pandas as pd
import features.func_stream as fs

st.set_page_config(layout="wide")
st.title("Analyse your Portfolio")

col1, col2 = st.columns(2)
with col1:
    pdf_file= st.file_uploader(label="Upload the Detailed CAS from CAMS", type=["pdf"], max_upload_size= 10)
    option = st.selectbox("Interval",("Daily","Weekly","Monthly","Quarterly", "Yearly"), index=0)
with col2:
    pdf_pass = st.text_input(label= "Enter Password (If encrypted)", type= "password")
   
if st.button(label = "Extract"):
    if pdf_file is not None:
        df= fs.get_data(pdf=pdf_file, password= pdf_pass, opt=option)
        tab1, tab2, tab3= st.tabs(["All", "Folio-Wise", "Performance"])
        with tab1:
            st.header("Portfolio Overview")
            fund_grouped_data= fs.get_grouped_data(df,by = ["Fund Name"])
            col3, col4, col5 = st.columns(3)
            total_cv, delta_cv, total_gain, delta_gain, cost_value, perc= fs.metrics(fund_grouped_data)
            col3.metric(label= "Current Valuation", value= total_cv, delta= delta_cv, format="%,d")
            col4.metric(label= "Total Gain",value= total_gain , delta= delta_gain, format="%,d")
            date= df["Date"].unique()[0]
            col5.metric(label= "Latest NAV Date",value= pd.to_datetime(date).strftime("%B %d, %Y"))
            fund_grouped_data= fund_grouped_data.sort_values(by="Gain %", ascending= False)
            st.write(fund_grouped_data)
            st.metric(label= "Total Cost Value", value= cost_value, format="%,d")

        with tab2:
            st.header("Grouped by Folio")
            for folio, folio_data in df.groupby("Folio", sort= False):
                total_cv, delta_cv, total_gain, delta_gain, cost_value, perc= fs.metrics(folio_data)
                col1, col2, col3, col4 = st.columns(4)
                col1.subheader(folio)
                col2.metric(label= "Current Valuation", value=total_cv, delta= delta_cv, format="%,d")
                col3.metric(label="Total Gain", value= total_gain, delta= delta_gain, format="%,d")
                col4.metric(label= "Folio %", value= perc)
                folio_data["All-Portfolio %"]= ((folio_data["Current Value"]/sum(folio_data["Current Value"]))*100).round(2)
                st.dataframe(folio_data.drop(columns=["Date", "Folio"]).sort_values(by="Gain %", ascending= False).set_index("Fund Name"))
                st.metric(label= "Total Cost Value", value= cost_value, format="%,d")
                st.divider()

    else:
        st.warning("Please attach a PDF file first before clicking the button.")