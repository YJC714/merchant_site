import streamlit as st
import pandas as pd
import datetime

# ====================== 頁面設定 ======================
st.set_page_config(
    page_title="商家後台：點數兌換紀錄清單",
    
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== 初始化：商家紀錄 ======================
# 模擬商家名稱
MERCHANT_NAME = "健康生活藥局 - 永和店"

if "redeemed" not in st.session_state:
    # 模擬兌換紀錄，包含老闆想看的欄位：時間、店家、點數、使用者ID
    st.session_state.redeemed = [
        {"時間": "2025-12-02 11:20:05", "店家": MERCHANT_NAME, "點數": 80, "使用者ID": "USER12345"},
        {"時間": "2025-12-02 10:45:30", "店家": MERCHANT_NAME, "點數": 150, "使用者ID": "USER98765"},
        {"時間": "2025-12-01 15:45:40", "店家": MERCHANT_NAME, "點數": 60, "使用者ID": "USER1002"},
        {"時間": "2025-12-01 10:30:15", "店家": MERCHANT_NAME, "點數": 100, "使用者ID": "USER1001"},
        {"時間": "2025-12-01 09:10:05", "店家": "其他商家", "點數": 50, "使用者ID": "USER1003"}, # 模擬其他商家的紀錄
    ]
    
# ====================== 介面開始：交易清單區域 ======================
st.header("📋 點數兌換紀錄清單")
st.subheader(f"目前顯示商家：**{MERCHANT_NAME}**", divider="blue")


df_redeemed = pd.DataFrame(st.session_state.redeemed)

# 篩選出本店的交易紀錄，並依時間倒序排列
df_merchant_records = df_redeemed[
    df_redeemed['店家'] == MERCHANT_NAME
].sort_values("時間", ascending=False)


if df_merchant_records.empty:
    st.info("本店目前尚未有任何點數兌換紀錄。")
else:
    # 顯示總核銷點數 (Metrics)
    total_points = df_merchant_records['點數'].sum()
    st.metric(
        "本店歷史總核銷點數",
        f"{total_points:,} 點",
        delta=f"總筆數: {len(df_merchant_records)} 筆"
    )
    
    # 顯示老闆要求的欄位：使用者ID、點數、時間
    st.dataframe(
        df_merchant_records[["時間", "使用者ID", "點數"]], 
        use_container_width=True, 
        hide_index=True,
        column_order=("時間", "使用者ID", "點數"),
        column_config={
            "時間": st.column_config.DatetimeColumn("交易時間", format="YYYY-MM-DD HH:mm:ss"),
            "使用者ID": "使用者ID (兌換者)",
            "點數": st.column_config.NumberColumn("兌換點數", format="%d 點")
        }
    )

