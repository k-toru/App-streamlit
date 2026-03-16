import streamlit as st
import numpy as np
from fractions import Fraction

st.title("3次正方行列の逆行列を掃き出し法で求める")

st.write("## 行列 A の入力")
st.write("3×3 行列 A を入力してください（3行、各行を空白で区切る）:")
matrix_input = st.text_area(
    "行列 A を入力",
    value="1 2 3\n4 5 6\n7 8 10",
    height=100
)

def matrix_to_latex(matrix):
    """行列をLaTeX形式に変換"""
    rows = []
    for row in matrix:
        row_str = " & ".join([str(Fraction(val).limit_denominator(1000)) for val in row])
        rows.append(row_str)
    
    latex_str = r"\left(\begin{array}{ccc}" + "\n"
    latex_str += " \\\\ ".join(rows)
    latex_str += r" \end{array}\right)"
    return latex_str

def augmented_matrix_to_latex(aug_matrix):
    """拡大行列をLaTeX形式に変換"""
    rows = []
    for row in aug_matrix:
        row_str = " & ".join([str(Fraction(val).limit_denominator(1000)) for val in row])
        rows.append(row_str)
    
    latex_str = r"\left(\begin{array}{cccccc}" + "\n"
    latex_str += " \\\\ ".join(rows)
    latex_str += r" \end{array}\right)"
    return latex_str

def parse_fraction(value_str):
    """文字列を分数または小数に変換"""
    try:
        return float(Fraction(value_str))
    except:
        return None

try:
    rows = matrix_input.strip().split('\n')
    matrix = [list(map(float, row.split())) for row in rows]
    
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        st.error("エラー: 3×3 の行列が必要です。")
    else:
        A = np.array(matrix, dtype=float)
        
        # セッション状態の初期化
        if 'aug_matrix' not in st.session_state:
            I = np.eye(3)
            st.session_state.aug_matrix = np.hstack([A, I])
            st.session_state.history = []
        
        # 初期状態を履歴に追加
        if len(st.session_state.history) == 0:
            st.session_state.history.append(("初期状態 [A|I]", st.session_state.aug_matrix.copy()))
        
        st.write("### 現在の拡大行列 [A|I]")
        st.latex(augmented_matrix_to_latex(st.session_state.aug_matrix))
        
        st.write("---")
        st.write("## 行操作を選択")
        
        operation = st.radio(
            "操作を選択してください",
            ["ある行に他の行の何倍か加える", "ある行を何倍かする", "2つの行を入れ替える"]
        )
        
        if operation == "ある行に他の行の何倍か加える":
            st.write("### R_i ← R_i + k × R_j")
            st.write("（k は数値、分数（1/3など）、小数で入力可能）")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                target_row = st.selectbox("対象の行 i", [1, 2, 3], key="add_target") - 1
            
            with col2:
                source_row = st.selectbox("加える行 j", [1, 2, 3], key="add_source") - 1
            
            with col3:
                k_input = st.text_input("倍数 k（例: 1/3, 2, 0.5）", value="1", key="add_k")
            
            if st.button("実行"):
                k = parse_fraction(k_input)
                if k is None:
                    st.error("エラー: 倍数 k を正しく入力してください")
                else:
                    st.session_state.aug_matrix[target_row] = st.session_state.aug_matrix[target_row] + k * st.session_state.aug_matrix[source_row]
                    description = f"R{target_row + 1} ← R{target_row + 1} + {Fraction(k).limit_denominator(100)} × R{source_row + 1}"
                    st.session_state.history.append((description, st.session_state.aug_matrix.copy()))
                    st.rerun()
        
        elif operation == "ある行を何倍かする":
            st.write("### R_i ← k × R_i")
            st.write("（k は数値、分数（1/3など）、小数で入力可能）")
            col1, col2 = st.columns(2)
            
            with col1:
                target_row = st.selectbox("対象の行 i", [1, 2, 3], key="mul_target") - 1
            
            with col2:
                k_input = st.text_input("倍数 k（例: 1/3, 2, 0.5）", value="1", key="mul_k")
            
            if st.button("実行"):
                k = parse_fraction(k_input)
                if k is None:
                    st.error("エラー: 倍数 k を正しく入力してください")
                else:
                    st.session_state.aug_matrix[target_row] = k * st.session_state.aug_matrix[target_row]
                    description = f"R{target_row + 1} ← {Fraction(k).limit_denominator(100)} × R{target_row + 1}"
                    st.session_state.history.append((description, st.session_state.aug_matrix.copy()))
                    st.rerun()
        
        elif operation == "2つの行を入れ替える":
            st.write("### R_i ↔ R_j")
            col1, col2 = st.columns(2)
            
            with col1:
                row1 = st.selectbox("入れ替える行 i", [1, 2, 3], key="swap_row1") - 1
            
            with col2:
                row2 = st.selectbox("入れ替える行 j", [1, 2, 3], key="swap_row2") - 1
            
            if st.button("実行"):
                st.session_state.aug_matrix[[row1, row2]] = st.session_state.aug_matrix[[row2, row1]]
                description = f"R{row1 + 1} ↔ R{row2 + 1}"
                st.session_state.history.append((description, st.session_state.aug_matrix.copy()))
                st.rerun()
        
        # リセット・Undoボタン
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("直前の操作を取り消す（Undo）"):
                if len(st.session_state.history) > 1:
                    st.session_state.history.pop()
                    st.session_state.aug_matrix = st.session_state.history[-1][1].copy()
                    st.rerun()
                else:
                    st.warning("取り消す操作がありません")
        
        with col2:
            if st.button("全てリセット"):
                I = np.eye(3)
                st.session_state.aug_matrix = np.hstack([A, I])
                st.session_state.history = [("初期状態 [A|I]", st.session_state.aug_matrix.copy())]
                st.rerun()
        
        # 操作履歴を表示
        st.write("---")
        st.write("## 操作履歴")
        
        if len(st.session_state.history) > 1:
            with st.expander("操作履歴を表示（クリックで展開）", expanded=True):
                for i, (description, mat) in enumerate(st.session_state.history):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.write(f"**ステップ {i}**")
                        st.write(description)
                    
                    with col2:
                        st.latex(augmented_matrix_to_latex(mat))
        else:
            st.write("操作はまだ実行されていません。")
        
        # 逆行列の確認
        st.write("---")
        st.write("## 逆行列の確認")
        if st.button("現在の右側行列を逆行列として抽出"):
            try:
                A_inv_candidate = st.session_state.aug_matrix[:, 3:]
                
                st.write("### 抽出された逆行列 A⁻¹")
                st.latex(matrix_to_latex(A_inv_candidate))
                
                # 検証: A * A_inv_candidate == I
                product = np.dot(A, A_inv_candidate)
                identity = np.eye(3)
                
                if np.allclose(product, identity, atol=1e-6):
                    st.success("この行列は A の逆行列です。")
                else:
                    st.error("不正解：この行列は A の逆行列ではありません。")
                    st.write("A × A⁻¹:")
                    st.latex(matrix_to_latex(product))
            except Exception as e:
                st.error(f"エラー: {e}")

except ValueError:
    st.error("エラー: 入力形式が正しくありません。数値を空白で区切って入力してください。")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")