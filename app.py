import streamlit as st
import pandas as pd
import os
import random

# 1. Cấu hình trang
st.set_page_config(page_title="Hieu's English Hub", page_icon="🧩", layout="wide")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; }

    .vocab-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .vocab-card:hover { border-color: #58a6ff; transform: translateY(-5px); }

    .word-title { color: #58a6ff; font-size: 1.4em; font-weight: bold; }
    .word-type {
        background: #238636; color: white; padding: 2px 8px;
        border-radius: 5px; font-size: 0.8em; width: fit-content;
        margin: 5px 0;
    }
    .word-ipa { color: #8b949e; font-style: italic; font-size: 0.9em; }
    .word-meaning { color: #c9d1d9; font-size: 1.1em; margin-top: 10px; }

    .del-btn button {
        background-color: transparent !important;
        border: 1px solid #f85149 !important;
        color: #f85149 !important;
    }
    .del-btn button:hover { background-color: #f85149 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC DỮ LIỆU (Từ, Nghĩa, Loại, Phát âm) ---
DB_FILE = 'vocabulary_pro.txt'

def load_data():
    words, meanings, types, ipas = [], [], [], []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    try:
                        parts = line.split(',')
                        if len(parts) >= 4:
                            words.append(parts[0].strip())
                            meanings.append(parts[1].strip())
                            types.append(parts[2].strip())
                            ipas.append(parts[3].strip())
                    except: continue
    df = pd.DataFrame({'Từ': words, 'Nghĩa': meanings, 'Loại': types, 'Phát âm': ipas})
    return df.sort_values(by='Từ').reset_index(drop=True)

def save_all(df):
    df_sorted = df.sort_values(by='Từ')
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        for _, row in df_sorted.iterrows():
            f.write(f"{row['Từ']},{row['Nghĩa']},{row['Loại']},{row['Phát âm']}\n")

# --- GIAO DIỆN ---
df_current = load_data()
menu = st.sidebar.radio("⚡ ĐIỀU KHIỂN", ["⚙️ Dashboard Quản lý", "💎 Flashcard", "📝 Kiểm tra"])

# --- 1. DASHBOARD QUẢN LÝ ---
if menu == "⚙️ Dashboard Quản lý":
    st.title("⚙️ Quản lý Từ vựng")
    tab1, tab2 = st.tabs(["✨ Thêm từ đơn", "📦 Thêm hàng loạt"])
    
    with tab1:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 3, 2, 2])
            w = c1.text_input("Từ (Word)")
            m = c2.text_input("Nghĩa (Meaning)")
            t = c3.selectbox("Loại", ["n", "v", "adj", "adv", "phr"])
            p = c4.text_input("Phát âm (IPA)")
            if st.button("LƯU TỪ VỰNG", use_container_width=True):
                if w and m:
                    if w.lower() in df_current['Từ'].str.lower().values:
                        st.warning("Từ này đã có!")
                    else:
                        new_row = pd.DataFrame({'Từ':[w], 'Nghĩa':[m], 'Loại':[t], 'Phát âm':[p]})
                        save_all(pd.concat([df_current, new_row]))
                        st.rerun()

    with tab2:
        st.info("Định dạng: **Từ, Nghĩa, Loại, Phát âm**")
        txt = st.text_area("Mỗi từ một dòng", height=150, placeholder="Apple, Quả táo, n, /ˈæpl/")
        if st.button("🚀 XÁC NHẬN NẠP LOẠT"):
            if txt:
                lines = txt.strip().split('\n')
                new_list = []
                for l in lines:
                    try:
                        parts = l.split(',')
                        if len(parts) >= 4:
                            new_list.append({'Từ': parts[0].strip(), 'Nghĩa': parts[1].strip(), 'Loại': parts[2].strip(), 'Phát âm': parts[3].strip()})
                    except: continue
                if new_list:
                    save_all(pd.concat([df_current, pd.DataFrame(new_list)]))
                    st.rerun()

    st.subheader(f"📋 Danh sách ({len(df_current)} từ)")
    if not df_current.empty:
        cols = st.columns(4)
        for idx, row in df_current.iterrows():
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="vocab-card">
                        <div>
                            <div class="word-title">{row['Từ']}</div>
                            <div class="word-type">{row['Loại']}</div>
                            <div class="word-ipa">{row['Phát âm']}</div>
                            <div class="word-meaning">{row['Nghĩa']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="del-btn">', unsafe_allow_html=True)
                if st.button(f"Xoá {row['Từ']}", key=f"del_{idx}", use_container_width=True):
                    save_all(df_current.drop(idx))
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# --- 2. FLASHCARD ---
elif menu == "💎 Flashcard":
    st.title("💎 Thẻ ghi nhớ")
    if not df_current.empty:
        if 'idx' not in st.session_state: st.session_state.idx = 0
        if 'flip' not in st.session_state: st.session_state.flip = False
        row = df_current.iloc[st.session_state.idx % len(df_current)]
        
        display = f"<h1>{row['Từ']}</h1><p class='word-ipa'>{row['Phát âm']}</p><p>({row['Loại']})</p>" if not st.session_state.flip else f"<h1 style='color:#58a6ff'>{row['Nghĩa']}</h1>"
        st.markdown(f"<div style='background:#1c2128; border:2px solid #30363d; border-radius:20px; height:300px; display:flex; align-items:center; justify-content:center; flex-direction:column; text-align:center;'>{display}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("🔄 LẬT THẺ", use_container_width=True):
            st.session_state.flip = not st.session_state.flip
            st.rerun()
        if c2.button("TIẾP THEO ➡️", use_container_width=True):
            st.session_state.idx += 1
            st.session_state.flip = False
            st.rerun()

# --- 3. KIỂM TRA (Đã thêm Cảm xúc & Hiệu ứng) ---
elif menu == "📝 Kiểm tra":
    st.title("📝 Kiểm tra trình độ")
    if len(df_current) < 4:
        st.warning("Cần tối thiểu 4 từ để tạo bài kiểm tra.")
    else:
        mode = st.radio("Chọn dạng kiểm tra:", ["Dạng 1 (Nộp bài tập trung)", "Dạng 2 (Làm đâu biết đó)"], horizontal=True)
        
        # --- DẠNG 1 (NỘP BÀI TẬP TRUNG) ---
        if mode == "Dạng 1 (Nộp bài tập trung)":
            num = st.slider("Số lượng câu hỏi:", 5, 50, 10)
            if st.button("🔄 TẠO ĐỀ MỚI") or 'ex_list' not in st.session_state:
                st.session_state.ex_list = df_current.sample(n=min(len(df_current), num)).to_dict('records')
                for it in st.session_state.ex_list:
                    others = df_current[df_current['Nghĩa'] != it['Nghĩa']]['Nghĩa'].unique().tolist()
                    opts = [it['Nghĩa']] + random.sample(others, min(len(others), 3))
                    random.shuffle(opts)
                    it['opts'] = opts
                st.session_state.ans = {}

            with st.form("exam_form"):
                for i, it in enumerate(st.session_state.ex_list):
                    st.markdown(f"**Câu {i+1}: {it['Từ']}** ({it['Loại']}) - *{it['Phát âm']}*")
                    st.session_state.ans[i] = st.radio("Chọn nghĩa đúng:", it['opts'], index=None, key=f"q_{i}")
                    st.divider()
                if st.form_submit_button("📤 NỘP BÀI"):
                    score = sum(1 for i, it in enumerate(st.session_state.ex_list) if st.session_state.ans.get(i) == it['Nghĩa'])
                    total = len(st.session_state.ex_list)
                    percent = (score / total) * 100
                    
                    # Hiển thị điểm số cơ bản
                    st.metric(label="Kết quả của bạn", value=f"{score} / {total}", delta=f"{percent:.0f}%")
                    
                    # --- XỬ LÝ CẢM XÚC THEO TỪNG BẬC ĐẠT ĐƯỢC ---
                    if percent == 100:
                        st.success(f"Xuất sắc! Bạn đã đạt điểm tuyệt đối. Giao diện pháo hoa chào đón bạn! 🏆🎉🥳")
                        st.balloons() # Hiệu ứng pháo hoa
                    elif percent >= 80:
                        st.success(f"Tuyệt vời! Bạn nhớ từ rất tốt. Tiếp tục phát huy nhé! 💪🌟😊")
                    elif percent >= 50:
                        st.warning(f"Khá tốt! Bạn đã vượt qua mức trung bình. Cố gắng thêm chút nữa! 👍📖😐")
                    elif percent > 0:
                        st.error(f"Cố gắng lên! Bạn cần ôn tập thêm một chút. Đừng bỏ cuộc! 📚✍️😟")
                    else:
                        st.error(f"Hic! Bạn chưa trả lời đúng câu nào. Hãy xem lại Flashcard nhé! 😭📕")

        
        # --- DẠNG 2 (LÀM ĐÂU BIẾT ĐÓ) ---
        else:
            if 'q2' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                others = df_current[df_current['Nghĩa'] != target['Nghĩa']]['Nghĩa'].unique().tolist()
                opts = [target['Nghĩa']] + random.sample(others, min(len(others), 3))
                random.shuffle(opts)
                st.session_state.q2 = {
                    'w':target['Từ'], 
                    'ans':target['Nghĩa'], 
                    'opts':opts, 
                    'done':False, 
                    'ipa':target['Phát âm'], 
                    'type':target['Loại'],
                    'user_choice': None,
                    'correct': False # Lưu trạng thái đúng/sai
                }
            
            q = st.session_state.q2
            st.info(f"Từ vựng: **{q['w']}** ({q['type']}) - *{q['ipa']}*")
            for opt in q['opts']:
                if st.button(opt, use_container_width=True, disabled=q['done']):
                    q['done'] = True
                    q['user_choice'] = opt
                    if opt == q['ans']:
                        q['correct'] = True
                    st.rerun()

            if q['done']:
                # --- XỬ LÝ HIỆU ỨNG KHI ĐÚNG/SAI ---
                if q['correct']:
                    st.success(f"Chính xác! 🎉 Đáp án là: **{q['ans']}**")
                    st.balloons() # Hiệu ứng pháo hoa ngay lập tức khi đúng
                else:
                    st.error(f"Sai rồi! Lựa chọn của bạn: {q['user_choice']}. Đáp án đúng là: **{q['ans']}** 😟")
                
                if st.button("Câu tiếp theo ➡️"):
                    del st.session_state.q2
                    st.rerun()