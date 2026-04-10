import streamlit as st
import pandas as pd
import os
import random
import streamlit.components.v1 as components

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
    :root {
        --primary-color: #58a6ff;
        --background-color: #0d1117;
        --secondary-background-color: #161b22;
        --text-color: #ffffff;
    }

    .stApp { background-color: #0d1117 !important; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d;}
    input, select, textarea, [data-baseweb="select"] { color: white !important; background-color: #0d1117 !important; }
    label, p, span { color: #ffffff !important; }

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
df_current = load_data()
menu = st.sidebar.radio("⚡ ĐIỀU KHIỂN", ["⚙️ Dashboard Quản lý", "💎 Flashcard", "📝 Kiểm tra"])

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
elif menu == "📝 Kiểm tra":
    st.title("📝 Kiểm tra trình độ")
    if len(df_current) < 4:
        st.warning("Cần tối thiểu 4 từ để tạo bài kiểm tra.")
    else:
        mode = st.radio("Chọn dạng kiểm tra:", 
                        ["Dạng 1 (Trắc nghiệm tập trung)", "Dạng 2 (Làm đâu biết đó)", "Dạng 3 (Thử thách viết từ)"], 
                        horizontal=True)
        
        if mode == "Dạng 1 (Trắc nghiệm tập trung)":
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
                for i, it in enumerate(st.session_state.ex_list):
                    st.markdown(f"**Câu {i+1}: {it['Từ']}** ({it['Loại']})")
                    st.session_state.ans[i] = st.radio("Chọn nghĩa đúng:", it['opts'], index=None, key=f"q_{i}", disabled=st.session_state.submitted_d1)
                    if st.session_state.submitted_d1:
                        if st.session_state.ans.get(i) == it['Nghĩa']: st.success(f"✨ Chính xác")
                        else: st.error(f"❌ Đáp án đúng: {it['Nghĩa']}")
                    st.divider()
                if st.form_submit_button("📤 NỘP BÀI"):
                    st.session_state.submitted_d1 = True
                    st.rerun()

        elif mode == "Dạng 2 (Làm đâu biết đó)":
            if 'q2' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                others = df_current[df_current['Nghĩa'] != target['Nghĩa']]['Nghĩa'].unique().tolist()
                opts = [target['Nghĩa']] + random.sample(others, min(len(others), 3))
                random.shuffle(opts)
                st.session_state.q2 = {'w':target['Từ'], 'ans':target['Nghĩa'], 'opts':opts, 'done':False, 'ipa':target['Phát âm'], 'type':target['Loại'], 'correct': False}
            
            q = st.session_state.q2
            st.info(f"Từ vựng: **{q['w']}** ({q['type']})")
            for opt in q['opts']:
                if st.button(opt, use_container_width=True, disabled=q['done']):
                    q['done'] = True
                    if opt == q['ans']: q['correct'] = True
                    st.rerun()
            if q['done']:
                if q['correct']: st.success("Chính xác! 🎉"); play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3"); st.balloons()
                else: st.error(f"Sai rồi! Đáp án là: **{q['ans']}**"); play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                if st.button("Câu tiếp theo ➡️"): del st.session_state.q2; st.rerun()

        else: # DẠNG 3 (WRITING)
            st.subheader("✍️ Thử thách ghi nhớ")
            if 'q3' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q3 = {'w': target['Từ'], 'ans': target['Nghĩa'], 'ipa': target['Phát âm'], 'type': target['Loại'], 'prep': target['Giới từ'], 'submitted': False, 'user_input': ""}
            
            q = st.session_state.q3
            st.info(f"Hãy viết từ tiếng Anh có nghĩa là: **{q['ans']}**")
            prep_hint = f" | Giới từ đi kèm: **{q['prep']}**" if q['prep'] else ""
            st.caption(f"Gợi ý: ({q['type']}) | {q['ipa']}{prep_hint}")
            
            # Key động giúp tự động xóa nội dung khi đổi câu hỏi
            user_word = st.text_input("Câu trả lời của bạn:", placeholder="Nhập từ...", key=f"input_{q['w']}", disabled=q['submitted']).strip()
            
            if not q['submitted'] and st.button("🔍 KIỂM TRA", use_container_width=True):
                if user_word:
                    q['user_input'] = user_word
                    q['submitted'] = True
                    st.rerun()
                else: st.warning("Bạn chưa nhập gì cả!")
            
            if q['submitted']:
                if q['user_input'].lower() == q['w'].lower():
                    st.success(f"Chính xác! ✨ Từ đúng là: **{q['w']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3"); st.balloons()
                else:
                    st.error(f"Sai rồi! Bạn nhập: '{q['user_input']}'. Đáp án đúng là: **{q['w']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                if st.button("Câu tiếp theo ➡️", use_container_width=True):
                    del st.session_state.q3
                    st.rerun()
