import streamlit as st
import pandas as pd
import os
import random
import streamlit.components.v1 as components
import time
from datetime import datetime

# Khởi tạo thời gian bắt đầu nếu chưa có
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

def get_study_time():
    # Tính số giây đã trôi qua
    duration_seconds = int(time.time() - st.session_state.start_time)
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    return f"{minutes}p {seconds}s"
# 1. Cấu hình trang
st.set_page_config(page_title="Hieu's English Hub", page_icon="🧩", layout="wide")

def play_sound(url):
    components.html(
        f"""
        <audio autoplay style="display:none">
            <source src="{url}" type="audio/mp3">
        </audio>
        """,
        height=0,
    )

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    /* Làm đẹp Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(22, 27, 34, 0.7) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(88, 166, 255, 0.2);
    }

    /* Đổi màu tiêu đề và icon trong Sidebar */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] .st-emotion-cache-17l2puu {
        color: #58a6ff !important;
        font-weight: bold;
    }

    /* Hiệu ứng cho các lựa chọn Radio Button */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 5px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        border-color: #58a6ff;
        background: rgba(88, 166, 255, 0.1);
        transform: translateX(5px);
    }
    :root {
        --primary-color: #58a6ff;
        --background-color: #0d1117;
        --secondary-background-color: #161b22;
        --text-color: #ffffff;
    }

    .stApp {
        background-image: url("https://autopro8.mediacdn.vn/2021/6/9/192512984102214077220020009018985261205554951n-16231958391591109567842.jpeg") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    .vocab-card {
        background: rgba(28, 33, 40, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(88, 166, 255, 0.2) !important;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        animation: slideUp 0.4s ease-out forwards;
    }
    
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .vocab-card:hover { 
        border-color: #58a6ff !important; 
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.3) !important;
    }

    .word-title { color: #58a6ff; font-size: 1.4em; font-weight: bold; margin-bottom: 2px; }
    .word-type { background: #238636; color: white; padding: 2px 10px; border-radius: 6px; font-size: 0.75em; width: fit-content; margin: 5px 0; text-transform: uppercase; font-weight: bold; }
    .word-ipa { color: #8b949e; font-style: italic; font-size: 0.95em; }
    .word-prep { color: #ff7b72; font-weight: bold; font-size: 0.9em; margin-top: 5px; }
    .word-meaning { color: #c9d1d9; font-size: 1.1em; margin-top: 12px; font-weight: 500; }

    .del-btn button { background-color: transparent !important; border: 1px solid #f85149 !important; color: #f85149 !important; border-radius: 8px !important; font-size: 0.8em !important; transition: all 0.2s ease; }
    .del-btn button:hover { background-color: #f85149 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)


# --- LOGIC DỮ LIỆU ---
DB_FILE = 'vocabulary_pro.txt'

def load_data():
    words, meanings, types, ipas, preps = [], [], [], [], []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    try:
                        parts = line.split(',')
                        # Hỗ trợ cả file cũ (4 cột) và file mới (5 cột)
                        if len(parts) >= 5:
                            words.append(parts[0].strip())
                            meanings.append(parts[1].strip())
                            types.append(parts[2].strip())
                            ipas.append(parts[3].strip())
                            preps.append(parts[4].strip())
                        elif len(parts) == 4:
                            words.append(parts[0].strip())
                            meanings.append(parts[1].strip())
                            types.append(parts[2].strip())
                            ipas.append(parts[3].strip())
                            preps.append("") 
                    except: continue
    df = pd.DataFrame({'Từ': words, 'Nghĩa': meanings, 'Loại': types, 'Phát âm': ipas, 'Giới từ': preps})
    return df.sort_values(by='Từ').reset_index(drop=True)

def save_all(df):
    df_sorted = df.sort_values(by='Từ')
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        for _, row in df_sorted.iterrows():
            f.write(f"{row['Từ']},{row['Nghĩa']},{row['Loại']},{row['Phát âm']},{row['Giới từ']}\n")

# --- GIAO DIỆN ---
# --- 1. Load dữ liệu trước ---
df_current = load_data()

# --- SIDEBAR CẢI TIẾN (PHIÊN BẢN HOÀN THIỆN) ---
# --- SIDEBAR CẢI TIẾN (PHIÊN BẢN HOÀN THIỆN) ---
with st.sidebar:
    # 1. Ảnh đại diện và Tiêu đề
    st.markdown(f"""
        <div style="text-align: center; padding: 10px 0;">
            <img src="https://cdn-icons-png.flaticon.com/512/3898/3898082.png" width="80">
            <h1 style='color: #58a6ff; margin-top: 10px;'>Hieu's Hub</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Menu chính
    menu = st.radio(
        "⚡ ĐIỀU KHIỂN", 
        ["⚙️ Dashboard Quản lý", "💎 Flashcard", "📝 Kiểm tra"],
        key="main_navigation"
    )
    
    st.divider() 
    
    # 3. Nút bấm Trợ lý AI (Gemini)
    st.markdown("### 🤖 Trợ lý AI")
    st.markdown(f"""
        <a href="https://gemini.google.com/app" target="_blank" style="text-decoration: none;">
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                background: linear-gradient(135deg, #4285F4, #1D5BBF);
                color: white;
                border-radius: 12px;
                cursor: pointer;
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s ease;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(66, 133, 244, 0.4)';" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)';" >
                <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530437e922919e517.svg" 
                     width="25" height="25">
                <span>Gemini AI Assistant</span>
                <span style="margin-left: auto; font-size: 0.8em; opacity: 0.8;">🚀</span>
            </div>
        </a>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 4. BỘ ĐẾM THỜI GIAN ---
    st.markdown("### ⏱️ Thời gian học")
    study_time = get_study_time()
    
    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #00ffcc;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
        ">
            <span style="color: #8b949e; font-size: 0.9em;">Phiên học hiện tại</span><br>
            <span style="color: #00ffcc; font-size: 1.8em; font-weight: bold; font-family: 'Courier New', Courier, monospace;">
                {study_time}
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Update Time 🔄", use_container_width=True):
        st.rerun()
    
    st.divider()
    
    # 5. Thống kê & Quote
    st.markdown("### 📊 Thống kê")
    total_words = len(df_current)
    st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(88, 166, 255, 0.2); text-align: center;">
            <p style="margin: 0; color: #8b949e; font-size: 0.9em;">Từ vựng đã nạp</p>
            <h2 style="margin: 0; color: #58a6ff;">{total_words}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    quotes = [
        "Knowledge is power. 🚀",
        "Keep moving forward. 🔥",
        "Practice makes perfect. ✨",
        "Don't stop until you're proud. 🏆"
    ]
    st.markdown(f"<p style='text-align: center; color: #8b949e; font-style: italic; font-size: 0.9em;'>\"{random.choice(quotes)}\"</p>", unsafe_allow_html=True)

# --- 1. DASHBOARD QUẢN LÝ ---
if menu == "⚙️ Dashboard Quản lý":
    st.title("⚙️ Quản lý Từ vựng")
    tab1, tab2 = st.tabs(["✨ Thêm từ đơn", "📦 Thêm hàng loạt"])
    
    with tab1:
        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([2, 3, 1, 2, 1.5])
            w = c1.text_input("Từ (Word)")
            m = c2.text_input("Nghĩa (Meaning)")
            t = c3.selectbox("Loại", ["n", "v", "adj", "adv", "phr"])
            p = c4.text_input("Phát âm (IPA)")
            pr = c5.text_input("Giới từ (Prep)", placeholder="on, in...")
            
            if st.button("LƯU TỪ VỰNG", use_container_width=True):
                if w and m:
                    if w.lower() in df_current['Từ'].str.lower().values:
                        st.warning("Từ này đã có!")
                    else:
                        new_row = pd.DataFrame({'Từ':[w], 'Nghĩa':[m], 'Loại':[t], 'Phát âm':[p], 'Giới từ':[pr]})
                        save_all(pd.concat([df_current, new_row]))
                        st.rerun()

    with tab2:
        st.info("Định dạng: **Từ, Nghĩa, Loại, Phát âm, Giới từ**")
        txt = st.text_area("Mỗi từ một dòng", height=150, placeholder="Depend, Phụ thuộc, v, /dɪˈpend/, on")
        if st.button("🚀 XÁC NHẬN NẠP LOẠT"):
            if txt:
                lines = txt.strip().split('\n')
                new_list = []
                for l in lines:
                    try:
                        parts = l.split(',')
                        if len(parts) >= 5:
                            new_list.append({'Từ': parts[0].strip(), 'Nghĩa': parts[1].strip(), 'Loại': parts[2].strip(), 'Phát âm': parts[3].strip(), 'Giới từ': parts[4].strip()})
                    except: continue
                if new_list:
                    save_all(pd.concat([df_current, pd.DataFrame(new_list)]))
                    st.rerun()

    st.subheader(f"📋 Danh sách ({len(df_current)} từ)")
    if not df_current.empty:
        cols = st.columns(4)
        for idx, row in df_current.iterrows():
            with cols[idx % 4]:
                prep_display = f'<div class="word-prep">Prep: {row["Giới từ"]}</div>' if row['Giới từ'] else ""
                st.markdown(f"""
                    <div class="vocab-card">
                        <div>
                            <div class="word-title">{row['Từ']}</div>
                            <div class="word-type">{row['Loại']}</div>
                            <div class="word-ipa">{row['Phát âm']}</div>
                            {prep_display}
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
        
        prep_info = f"<p style='color:#ff7b72; font-weight:bold;'>Prep: {row['Giới từ']}</p>" if row['Giới từ'] else ""
        display = f"<h1>{row['Từ']}</h1><p class='word-ipa'>{row['Phát âm']}</p><p>({row['Loại']})</p>{prep_info}" if not st.session_state.flip else f"<h1 style='color:#58a6ff'>{row['Nghĩa']}</h1>"
        
        st.markdown(f"<div style='background:#1c2128; border:2px solid #30363d; border-radius:20px; height:350px; display:flex; align-items:center; justify-content:center; flex-direction:column; text-align:center;'>{display}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("🔄 LẬT THẺ", use_container_width=True):
            st.session_state.flip = not st.session_state.flip
            st.rerun()
        if c2.button("TIẾP THEO ➡️", use_container_width=True):
            st.session_state.idx += 1
            st.session_state.flip = False
            st.rerun()

# --- 3. KIỂM TRA ---
# --- 3. KIỂM TRA ---
# --- 3. KIỂM TRA ---
# --- 3. KIỂM TRA (CẬP NHẬT 5 DẠNG) ---
# --- 3. KIỂM TRA (CẬP NHẬT ĐẦY ĐỦ THÔNG TIN ĐỀ BÀI) ---
# --- 3. KIỂM TRA (BẢN FULL FIX LỖI & ĐỔI MÀU) ---
elif menu == "📝 Kiểm tra":
    st.title("📝 Kiểm tra trình độ")
    if len(df_current) < 4:
        st.warning("Cần tối thiểu 4 từ để tạo bài kiểm tra.")
    else:
        mode = st.radio("Chọn dạng kiểm tra:", 
                        ["Dạng 1 (Trắc nghiệm)", "Dạng 2 (Làm đâu biết đó)", "Dạng 3 (Viết từ)", "Dạng 4 (Loại từ)", "Dạng 5 (Giới từ)"], 
                        horizontal=True)
        
        # --- DẠNG 1: TRẮC NGHIỆM TỔNG HỢP ---
        if mode == "Dạng 1 (Trắc nghiệm)":
            num = st.slider("Số lượng câu hỏi:", 5, 50, 10)
            if st.button("🔄 TẠO ĐỀ MỚI") or 'ex_list' not in st.session_state:
                st.session_state.ex_list = df_current.sample(n=min(len(df_current), num)).to_dict('records')
                for it in st.session_state.ex_list:
                    others = df_current[df_current['Nghĩa'] != it['Nghĩa']]['Nghĩa'].unique().tolist()
                    opts = [it['Nghĩa']] + random.sample(others, min(len(others), 3))
                    random.shuffle(opts)
                    it['opts'] = opts
                st.session_state.ans = {}
                st.session_state.submitted_d1 = False

            with st.form("exam_form"):
                score = 0
                for i, it in enumerate(st.session_state.ex_list):
                    prep_info = f" + {it['Giới từ']}" if it['Giới từ'] else ""
                    st.markdown(f"**Câu {i+1}: {it['Từ']}{prep_info}**")
                    st.caption(f"Loại: {it['Loại']} | IPA: {it['Phát âm']}")
                    
                    st.session_state.ans[i] = st.radio(f"Chọn nghĩa:", it['opts'], index=None, key=f"q1_{i}", disabled=st.session_state.submitted_d1)
                    
                    if st.session_state.submitted_d1:
                        if st.session_state.ans.get(i) == it['Nghĩa']:
                            st.success("✨ Đúng"); score += 1
                        else: st.error(f"❌ Đáp án: {it['Nghĩa']}")
                    st.divider()
                
                if st.form_submit_button("📤 NỘP BÀI"):
                    st.session_state.submitted_d1 = True
                    st.rerun()

            if st.session_state.submitted_d1:
                total_q = len(st.session_state.ex_list)
                st.markdown(f"### 📊 Kết quả: `{score}/{total_q}` câu đúng ({(score/total_q)*100:.0f}%)")
                if score == total_q: st.balloons()

        # --- DẠNG 2: LÀM ĐÂU BIẾT ĐÓ ---
        elif mode == "Dạng 2 (Làm đâu biết đó)":
            if 'q2' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                others = df_current[df_current['Nghĩa'] != target['Nghĩa']]['Nghĩa'].unique().tolist()
                opts = [target['Nghĩa']] + random.sample(others, min(len(others), 3))
                random.shuffle(opts)
                st.session_state.q2 = {'w':target['Từ'], 'ans':target['Nghĩa'], 'opts':opts, 'done':False, 'ipa':target['Phát âm'], 'type':target['Loại'], 'prep':target['Giới từ'], 'correct': False}
            
            q = st.session_state.q2
            prep_info = f" + {q['prep']}" if q['prep'] else ""
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; border-left: 5px solid #fffd75; margin-bottom: 20px;">
                    <h3 style="color: #fffd75; margin: 0;">Từ vựng: {q['w']}{prep_info}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Loại: <b>{q['type']}</b> | IPA: <i>{q['ipa']}</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            for opt in q['opts']:
                if st.button(opt, key=f"btn2_{opt}", use_container_width=True, disabled=q['done']):
                    q['done'] = True
                    if opt == q['ans']: q['correct'] = True
                    st.rerun()
            
            if q['done']:
                if q['correct']: 
                    st.success("Chính xác! 🎉"); play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else: 
                    st.error(f"Sai rồi! Đáp án là: {q['ans']}"); play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                if st.button("Câu tiếp theo ➡️"): del st.session_state.q2; st.rerun()

        # --- DẠNG 3: VIẾT TỪ ---
        elif mode == "Dạng 3 (Viết từ)":
            if 'q3' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q3 = {'w': target['Từ'], 'ans': target['Nghĩa'], 'ipa': target['Phát âm'], 'type': target['Loại'], 'prep': target['Giới từ'], 'submitted': False, 'user_input': ""}
            
            q = st.session_state.q3
            prep_hint = f"Cấu trúc: + {q['prep']}" if q['prep'] else "Không giới từ"
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 20px;">
                    <h3 style="color: #00ffcc; margin: 0;">Nghĩa: {q['ans']}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Gợi ý: {q['type']} | {q['ipa']} | {prep_hint}</p>
                </div>
            """, unsafe_allow_html=True)
            
            user_word = st.text_input("Nhập từ tiếng Anh:", key=f"input3_{q['w']}", disabled=q['submitted']).strip()
            if not q['submitted'] and st.button("🔍 KIỂM TRA", use_container_width=True):
                q['user_input'] = user_word
                q['submitted'] = True
                st.rerun()
            
            if q['submitted']:
                if q['user_input'].lower() == q['w'].lower():
                    st.success("✨ Chính xác!"); play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else:
                    st.error(f"❌ Đáp án đúng là: {q['w']}"); play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                if st.button("Câu tiếp theo ➡️"): del st.session_state.q3; st.rerun()

        # --- DẠNG 4: LOẠI TỪ ---
        elif mode == "Dạng 4 (Loại từ)":
            if 'q4' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q4 = {'w': target['Từ'], 'ans': target['Loại'], 'meaning': target['Nghĩa'], 'ipa': target['Phát âm'], 'prep': target['Giới từ'], 'done': False, 'user_choice': None}
            
            q = st.session_state.q4
            prep_info = f" + {q['prep']}" if q['prep'] else ""
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; border-left: 5px solid #ffa500; margin-bottom: 20px;">
                    <h3 style="color: #ffa500; margin: 0;">Từ vựng: {q['w']}{prep_info}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Nghĩa: {q['meaning']} | IPA: {q['ipa']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            btns = st.columns(5)
            types = ["n", "v", "adj", "adv", "phr"]
            for idx, t in enumerate(types):
                if btns[idx].button(t.upper(), key=f"btn4_{t}", use_container_width=True, disabled=q['done']):
                    q['user_choice'] = t
                    q['done'] = True
                    st.rerun()
            
            if q['done']:
                if q['user_choice'] == q['ans']:
                    st.success(f"Đúng! {q['w']} là {q['ans']}"); play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else:
                    st.error(f"Sai! Đáp án: {q['ans']}"); play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                if st.button("Câu tiếp theo ➡️"): del st.session_state.q4; st.rerun()

        # --- DẠNG 5: GIỚI TỪ ---
        elif mode == "Dạng 5 (Giới từ)":
            if 'q5' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q5 = {'w': target['Từ'], 'meaning': target['Nghĩa'], 'ipa': target['Phát âm'], 'type': target['Loại'], 'ans': target['Giới từ'].strip().lower() if target['Giới từ'] else "none", 'done': False, 'user_choice': None}
            
            q = st.session_state.q5
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; border-left: 5px solid #ff7b72; margin-bottom: 20px;">
                    <h3 style="color: #ff7b72; margin: 0;">Cấu trúc của từ: {q['w']}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Nghĩa: {q['meaning']} | Loại: {q['type']} | IPA: {q['ipa']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            prep_options = ["none", "to", "from", "of", "with", "in", "on", "at", "for", "about", "be"]
            if q['ans'] not in prep_options: prep_options.append(q['ans'])
            
            cols = st.columns(4)
            for i, p_opt in enumerate(prep_options):
                with cols[i % 4]:
                    if st.button(p_opt.upper(), key=f"btn5_{p_opt}", use_container_width=True, disabled=q['done']):
                        q['done'] = True
                        q['user_choice'] = p_opt
                        st.rerun()
            
            if q['done']:
                if q['user_choice'] == q['ans']:
                    st.success(f"Đúng! Kết quả: {q['w']} {q['ans'] if q['ans'] != 'none' else ''}"); play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else:
                    st.error(f"Sai! Giới từ đúng: {q['ans'].upper()}")
                if st.button("Câu tiếp theo ➡️"): del st.session_state.q5; st.rerun()
