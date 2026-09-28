import os

import requests
import streamlit as st
from dotenv import load_dotenv

# 一定要是第一個 Streamlit 指令
st.set_page_config(
    page_title="音樂推薦系統",
    layout="wide",
)

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

st.title("🎵 音樂推薦系統")

# 建立兩個分頁
tab1, tab2 = st.tabs(
    [
        "探索所有歌曲",
        "推薦與歌曲清單",
    ]
)

# -----------------------------
# Tab 1：探索所有歌曲
# -----------------------------
with tab1:

    st.subheader("🎼 探索所有歌曲")

    st.write("請輸入您想查詢的歌曲範圍：")

    skip_input = st.number_input(
        "從第幾首開始 (Skip)：",
        min_value=0,
        value=0,
        step=1,
    )

    limit_input = st.number_input(
        "顯示多少首歌曲 (Limit)：",
        min_value=1,
        value=10,
        step=1,
    )


    if st.button(
        f"🎵 取得歌曲（跳過 {skip_input} 首，顯示 {limit_input} 首）"
    ):

        try:

            songs_response = requests.get(
                f"{FASTAPI_URL}/songs",
                params={
                    "skip": skip_input,
                    "limit": limit_input,
                },
            )


            if songs_response.status_code == 200:

                data = songs_response.json()

                st.success("成功取得歌曲！")


                if data:

                    st.write(
                        f"以下是從第 **{skip_input}** 首開始，共 **{limit_input}** 首歌曲："
                    )

                    cols = st.columns(5)


                    for idx, item in enumerate(data):

                        song = item["song"]
                        artist_name = item["artist_name"]

                        col = cols[idx % 5]


                        with col:

                            st.markdown(
                                f"""
                                <div style="
                                    border:1px solid #ddd;
                                    padding:16px;
                                    border-radius:12px;
                                    margin-bottom:12px;
                                    background-color:#f9f9f9;
                                    height:220px;
                                ">

                                <h4>
                                🎵 {song["song_title"]}
                                </h4>

                                <p>
                                👤 歌手：{artist_name}
                                </p>

                                <p>
                                ID：{song["song_id"]}
                                </p>

                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                else:

                    st.info("沒有找到歌曲資料")


            else:

                st.error(
                    f"取得歌曲失敗：{songs_response.text}"
                )


        except Exception as e:

            st.error(
                f"發生錯誤：{e}"
            )
# -----------------------------
# Tab 2：推薦與歌曲清單
# -----------------------------
with tab2:

    st.header("🎧 使用者推薦與歌曲瀏覽")

    user_ids = []

    try:

        user_list_resp = requests.get(
            f"{FASTAPI_URL}/users/",
            params={
                "skip": 0,
                "limit": 10,
            },
        )

        if user_list_resp.status_code == 200:
            user_ids = user_list_resp.json()[:10]

        else:
            st.warning(
                f"⚠️ 無法取得使用者列表，HTTP 狀態碼：{user_list_resp.status_code}"
            )


    except Exception as e:

        st.error(
            f"取得使用者列表錯誤：{e}"
        )


    if user_ids:

        selected_user = st.selectbox(
            "請選擇一位使用者來獲取推薦：",
            user_ids,
        )


        # 按鈕取得推薦歌曲
        if st.button("🎵 取得推薦歌曲"):


            try:

                rec_response = requests.get(
                    f"{FASTAPI_URL}/users/{selected_user}/recommendations",
                    params={
                        "limit": 10
                    },
                )


                if rec_response.status_code == 200:


                    data = rec_response.json()


                    if data:

                        st.success(
                            "成功取得推薦歌曲！"
                        )


                        st.write(
                            f"以下是為使用者 **{selected_user}** 推薦的歌曲："
                        )


                        cols = st.columns(5)


                        for idx, item in enumerate(data):

                            song = item["song"]

                            artist_name = item["artist_name"]


                            col = cols[idx % 5]


                            with col:


                                st.markdown(
                                    f"""
                                    <div style="
                                        border:1px solid #ddd;
                                        padding:16px;
                                        border-radius:12px;
                                        margin-bottom:12px;
                                        background-color:#f9f9f9;
                                        box-shadow:2px 2px 5px rgba(0,0,0,0.1);
                                    ">

                                    <h4 style="
                                        margin-bottom:4px;
                                        font-size:20px;
                                        color:#333;
                                    ">
                                    🎵 {song["song_title"]}
                                    </h4>


                                    <p style="
                                        margin:0;
                                        font-size:16px;
                                        color:#555;
                                    ">
                                    👤 歌手：{artist_name}
                                    </p>


                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )


                    else:

                        st.info(
                            f"目前沒有為使用者 {selected_user} 找到推薦歌曲。"
                        )


                else:

                    st.error(
                        f"推薦失敗：{rec_response.text}"
                    )


            except Exception as e:

                st.error(
                    f"取得推薦歌曲時發生錯誤：{e}"
                )


    else:

        st.info(
            "目前沒有可用使用者。"
        )