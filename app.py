import streamlit as st
import pandas as pd
import random

# 生徒専用のユーザー名とパスワード
AUTHORIZED_USER = {"username": "student", "password": "password123"}

# ログイン機能
def login():
    st.sidebar.header("ログイン")
    username = st.sidebar.text_input("ユーザー名")
    password = st.sidebar.text_input("パスワード", type="password")
    if st.sidebar.button("ログイン"):
        if username == AUTHORIZED_USER["username"] and password == AUTHORIZED_USER["password"]:
            st.session_state["logged_in"] = True
        else:
            st.sidebar.error("ユーザー名またはパスワードが間違っています。")

# セッション状態の初期化
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ログインしていない場合、ログイン画面を表示
if not st.session_state["logged_in"]:
    login()
    st.stop()

# ログイン後のアプリ本体
st.title("英単語テスト")
st.write("ログインしました！単語テストを始めましょう。")

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

# 初期化
if "question" not in st.session_state:
    st.session_state.question, st.session_state.choices = generate_question(filtered_word_list)
    st.session_state.result = ""  # 結果表示
    st.session_state.show_next = False

# 問題表示
st.write(f"**{st.session_state.question['word']}** の意味はどれ？")
user_answer = st.radio("選択肢", st.session_state.choices, key="user_answer")

# 回答ボタン
if st.button("回答する") and not st.session_state.show_next:
    correct_answer = st.session_state.question["meaning"]
    if user_answer == correct_answer:
        st.session_state.result = "正解！ 🎉"
    else:
        st.session_state.result = f"不正解… 正解は: {correct_answer}"
    st.session_state.show_next = True

# 結果表示
if st.session_state.result:
    st.write(st.session_state.result)

# 次に進むボタン
if st.session_state.show_next and st.button("次に進む"):
    st.session_state.question, st.session_state.choices = generate_question(filtered_word_list)
    st.session_state.result = ""  # 結果をリセット
    st.session_state.show_next = False







