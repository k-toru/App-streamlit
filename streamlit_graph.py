# streamlit_graph.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit でグラフ表示の例")

# ランダムデータを用意
df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"],
    index=pd.date_range("2026-01-01", periods=20)
)

st.write("## ラインチャート")
st.line_chart(df)

st.write("## バーチャート（同じデータ）")
st.bar_chart(df)

# Plotly など他のライブラリも使える
import plotly.express as px
fig = px.scatter(df.reset_index(), x="index", y=["A", "B", "C"],
                 title="Plotly 散布図")
st.write("## Plotly の例")
st.plotly_chart(fig)