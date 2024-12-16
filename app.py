import streamlit as st
import pandas as pd
import random




# CSVファイルの読み込み
file_path = "leap_word_list.csv"
data = pd.read_csv(file_path, encoding="utf-8-sig")
word_list = data.to_dict("records")

# 範囲でフィルタリングする関数
def filter_words_by_range(start, end):
    return [word for word in word_list if start <= word["number"] <= end]

# 問題の出題
def generate_question(filtered_words):
    question = random.choice(filtered_words)
    choices = random.sample(filtered_words, 3) + [question]  # 正解+不正解3つ
    random.shuffle(choices)
    return question, [c["meaning"] for c in choices]

# サイドバーで範囲指定
st.sidebar.header("範囲を指定")
start_range = st.sidebar.number_input("開始番号", min_value=1, value=1)
end_range = st.sidebar.number_input("終了番号", min_value=1, value=len(word_list))

# フィルタリング
filtered_word_list = filter_words_by_range(start_range, end_range)

# 初期化部分で、セッションステートの初期値を設定
if "show_next" not in st.session_state:
    st.session_state.show_next = False
if "result" not in st.session_state:
    st.session_state.result = ""
if "question" not in st.session_state:
    st.session_state.question, st.session_state.choices = generate_question(filtered_word_list)

# 問題表示部分
st.write(f"問題: {st.session_state.question}")
choices = st.session_state.choices

# 選択肢を表示
user_answer = st.radio("選択肢から選んでください", choices, key="user_answer")

# 解答ボタン
if st.button("解答"):
    if user_answer == st.session_state.question["answer"]:
        st.session_state.result = "正解！"
    else:
        st.session_state.result = f"不正解。正しい答えは: {st.session_state.question['answer']}"
    st.session_state.show_next = True  # 次に進むボタンを表示可能に

# 結果表示
st.write(st.session_state.result)

# 次に進むボタン
if st.session_state.show_next:
    if st.button("次に進む", key="next_question"):
        # 新しい問題を生成
        st.session_state.question, st.session_state.choices = generate_question(filtered_word_list)
        # 結果をリセット
        st.session_state.result = ""
        # 次に進むボタンの状態をリセット
        st.session_state.show_next = False
        # ページの再レンダリングを明示的に実行
        st.experimental_rerun()
