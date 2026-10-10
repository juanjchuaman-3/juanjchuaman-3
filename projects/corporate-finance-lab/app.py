"""Corporate Finance Lab dashboard. Run: streamlit run app.py"""
import numpy as np
import pandas as pd
import streamlit as st
from model import Assumptions, dcf, sensitivity
from portfolio import demo_returns, metrics, min_variance_weights

st.set_page_config(page_title="Corporate Finance Lab",page_icon="📊",layout="wide")
st.title("Corporate Finance & Portfolio Analytics Lab")
st.caption("Synthetic teaching case • USD millions • Not investment advice")
tab1,tab2=st.tabs(["3 statements + DCF","Portfolio risk"])
with tab1:
    st.sidebar.header("Financial drivers")
    a=Assumptions(
        sales_growth=st.sidebar.slider("Sales growth",-0.10,0.20,.06,.005),
        cogs_pct=st.sidebar.slider("COGS / sales",.30,.80,.60,.01),
        opex_pct=st.sidebar.slider("OPEX / sales",.05,.35,.18,.01),
        capex_pct=st.sidebar.slider("CAPEX / sales",.01,.15,.05,.005),
        wacc=st.sidebar.slider("WACC",.06,.20,.105,.005),
        terminal_growth=st.sidebar.slider("Terminal growth",.00,.05,.03,.005))
    v=dcf(a)
    for col,label,key in zip(st.columns(4),
            ["Enterprise value","Equity value","Value per share","PV terminal / EV"],
            ["enterprise_value","equity_value","equity_per_share","terminal_weight"]):
        col.metric(label,f"{v[key]:.1%}" if key=="terminal_weight" else f"{v[key]:,.2f}")
    forecast=pd.DataFrame(v["forecast"]).set_index("year")
    st.subheader("P&L and FCFF")
    st.dataframe(forecast[["revenue","cogs","opex","da","ebit","net_income","fcff"]].T, use_container_width=True)
    st.line_chart(forecast[["revenue","ebit","fcff"]])
    st.subheader("Balance sheet checks")
    st.dataframe(forecast[["cash","ar","inventory","ppe","assets","ap","debt","equity","balance_check"]].T, use_container_width=True)
    grid=pd.DataFrame(sensitivity(a,[.085,.095,.105,.115,.125],[.02,.025,.03,.035,.04]))
    st.subheader("Equity value sensitivity (USD mm)")
    st.dataframe(grid.pivot(index="wacc",columns="g",values="equity_value"),use_container_width=True)
    st.download_button("Export projections (CSV)",forecast.to_csv().encode(),"forecast.csv","text/csv")
with tab2:
    st.subheader("Portfolio analytics • Synthetic returns")
    names,r=demo_returns()
    eq=np.repeat(1/len(names),len(names))
    mv=min_variance_weights(r)
    comparison=pd.DataFrame([{"Portfolio":name,**metrics(r,w)} for name,w in
       [("Equal weight",eq),("Minimum variance",mv)]])
    st.dataframe(comparison,use_container_width=True)
    st.bar_chart(pd.DataFrame({"Asset":names,"Equal weight":eq,"Minimum variance":mv}).set_index("Asset"))
    st.caption("In-sample estimates; historical VaR and CVaR are 1-day measures, not guarantees.")
