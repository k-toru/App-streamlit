import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction

st.title("3次正方行列の逆行列計算")

st.write("## 3×3 行列 A を入力してください")

# 行列入力用のテキストエリア
st.write("行列を以下の形式で入力（3行、各行を空白で区切る）:")
matrix_input = st.text_area(
    "行列 A を入力",
    value="1 2 3\n4 5 6\n7 8 10",
    height=100
)

def matrix_to_latex(matrix, as_fraction=False):
    """行列をLaTeX形式に変換"""
    rows = []
    for row in matrix:
        if as_fraction:
            row_str = " & ".join([str(Fraction(val).limit_denominator(1000)) for val in row])
        else:
            row_str = " & ".join([str(Fraction(val).limit_denominator(1000)) for val in row])
        rows.append(row_str)
    
    latex_str = r"\begin{pmatrix}" + "\n"
    latex_str += " \\\\ ".join(rows)
    latex_str += r" \end{pmatrix}"
    return latex_str

try:
    # 入力をパース
    rows = matrix_input.strip().split('\n')
    A = np.array([list(map(float, row.split())) for row in rows])
    
    # 3×3 行列であることを確認
    if A.shape != (3, 3):
        st.error(f"エラー: 3×3 行列が必要です。入力は {A.shape} です。")
    else:
        st.write("### 入力された行列 A")
        st.latex(matrix_to_latex(A, as_fraction=True))
        
        # 行列式を計算
        det = np.linalg.det(A)
        st.write(f"**行列式 det(A) = {det:.6f}**")
        
        if abs(det) < 1e-10:
            st.error("エラー: 行列式がほぼ0のため、逆行列は存在しません。")
        else:
            # 逆行列を計算
            A_inv = np.linalg.inv(A)
            
            # 逆行列を分数で表示
            st.write("### 逆行列 A⁻¹")
            st.latex(matrix_to_latex(A_inv, as_fraction=True))

except ValueError:
    st.error("エラー: 入力形式が正しくありません。数値を空白で区切って入力してください。")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")