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
    /* 1. Thiết lập màu chủ đạo cho toàn bộ ứng dụng (Global Theme) */
    :root {
        --primary-color: #58a6ff;
        --background-color: #0d1117;
        --secondary-background-color: #161b22;
        --text-color: #ffffff;
    }

    /* 2. Ép nền tối cho toàn bộ trang và Sidebar */
    .stApp { 
        background-color: #0d1117 !important; 
        color: #ffffff !important; 
    }
    
    [data-testid="stSidebar"] { 
        background-color: #161b22 !important; 
        border-right: 1px solid #30363d;
    }

    /* 3. Sửa màu chữ cho các thành phần nhập liệu (Input, Selectbox) */
    input, select, textarea, [data-baseweb="select"] {
        color: white !important;
        background-color: #0d1117 !important;
    }
    
    label, p, span {
        color: #ffffff !important;
    }

    /* 4. Khối Card Từ vựng (Giữ phong cách Cyber của bạn) */
    .vocab-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .vocab-card:hover { 
        border-color: #58a6ff; 
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .word-title { color: #58a6ff; font-size: 1.4em; font-weight: bold; margin-bottom: 2px; }
    
    .word-type {
        background: #238636; 
        color: white; 
        padding: 2px 10px;
        border-radius: 6px; 
        font-size: 0.75em; 
        width: fit-content;
        margin: 5px 0;
        text-transform: uppercase;
        font-weight: bold;
    }
    
    .word-ipa { color: #8b949e; font-style: italic; font-size: 0.95em; }
    .word-meaning { color: #c9d1d9; font-size: 1.1em; margin-top: 12px; font-weight: 500; }

    /* 5. Nút Xóa (Phong cách Danger của GitHub) */
    .del-btn button {
        background-color: transparent !important;
        border: 1px solid #f85149 !important;
        color: #f85149 !important;
        border-radius: 8px !important;
        font-size: 0.8em !important;
    }
    
    .del-btn button:hover { 
        background-color: #f85149 !important; 
        color: white !important; 
        border-color: #f85149 !important;
    }

    /* 6. Tùy chỉnh các Tab (Thêm vào để đồng bộ màu tối) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
    }
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
    }
    /* Hiệu ứng trượt lên cho các Card từ vựng */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.vocab-card {
    animation: slideUp 0.4s ease-out forwards;
    background: rgba(28, 33, 40, 0.8) !important;
    backdrop-filter: blur(10px); /* Hiệu ứng kính mờ */
    border: 1px solid rgba(88, 166, 255, 0.2) !important;
}

/* Hiệu ứng phát sáng khi di chuột qua card */
.vocab-card:hover {
    border-color: #58a6ff !important;
    box-shadow: 0 0 20px rgba(88, 166, 255, 0.3) !important;
    transform: translateY(-8px) scale(1.02);
}

/* Làm đẹp nút Xóa */
.del-btn button {
    transition: all 0.2s ease;
}
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

# --- 3. KIỂM TRA (Full 3 Dạng) ---
elif menu == "📝 Kiểm tra":
    st.title("📝 Kiểm tra trình độ")
    if len(df_current) < 4:
        st.warning("Cần tối thiểu 4 từ để tạo bài kiểm tra.")
    else:
        # Thêm lựa chọn Dạng 3 vào Menu điều khiển
        mode = st.radio("Chọn dạng kiểm tra:", 
                        ["Dạng 1 (Nộp bài tập trung)", "Dạng 2 (Làm đâu biết đó)", "Dạng 3 (Thử thách viết từ)"], 
                        horizontal=True)
        
      # --- DẠNG 1 (NỘP BÀI TẬP TRUNG) ---
        if mode == "Dạng 1 (Nộp bài tập trung)":
            num = st.slider("Số lượng câu hỏi:", 5, 50, 10)
            
            # Khởi tạo đề thi
            if st.button("🔄 TẠO ĐỀ MỚI") or 'ex_list' not in st.session_state:
                st.session_state.ex_list = df_current.sample(n=min(len(df_current), num)).to_dict('records')
                for it in st.session_state.ex_list:
                    others = df_current[df_current['Nghĩa'] != it['Nghĩa']]['Nghĩa'].unique().tolist()
                    opts = [it['Nghĩa']] + random.sample(others, min(len(others), 3))
                    random.shuffle(opts)
                    it['opts'] = opts
                st.session_state.ans = {}
                st.session_state.submitted_d1 = False  # Reset trạng thái nộp bài

            with st.form("exam_form"):
                for i, it in enumerate(st.session_state.ex_list):
                    st.markdown(f"**Câu {i+1}: {it['Từ']}** ({it['Loại']}) - *{it['Phát âm']}*")
                    
                    # Radio chọn đáp án
                    st.session_state.ans[i] = st.radio(
                        "Chọn nghĩa đúng:", 
                        it['opts'], 
                        index=None, 
                        key=f"q_{i}",
                        disabled=st.session_state.get('submitted_d1', False) # Khóa input sau khi nộp
                    )
                    
                    # Logic hiển thị đáp án sau khi bấm NỘP BÀI
                    if st.session_state.get('submitted_d1', False):
                        user_choice = st.session_state.ans.get(i)
                        correct_ans = it['Nghĩa']
                        
                        if user_choice == correct_ans:
                            st.success(f"✨ Chính xác: {correct_ans}")
                        else:
                            st.error(f"❌ Sai rồi. Đáp án đúng là: **{correct_ans}**")
                    
                    st.divider()

                # Nút nộp bài
                submit_btn = st.form_submit_button("📤 NỘP BÀI")
                if submit_btn:
                    st.session_state.submitted_d1 = True
                    st.rerun() # Refresh để hiển thị các thông báo success/error phía trên

            # Hiển thị bảng điểm tổng quát sau khi nộp
            if st.session_state.get('submitted_d1', False):
                score = sum(1 for i, it in enumerate(st.session_state.ex_list) if st.session_state.ans.get(i) == it['Nghĩa'])
                total = len(st.session_state.ex_list)
                percent = (score / total) * 100
                
                st.metric(label="Kết quả chung", value=f"{score} / {total}", delta=f"{percent:.0f}%")
                
                if percent == 100:
                    st.balloons()
                elif percent >= 50: st.info("Khá tốt! Tiếp tục cố gắng nhé! 👍")
                else: st.error("Bạn cần ôn tập kỹ hơn rồi! 📚")

        # --- DẠNG 2 (LÀM ĐÂU BIẾT ĐÓ - TRẮC NGHIỆM) ---
        elif mode == "Dạng 2 (Làm đâu biết đó)":
            if 'q2' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                others = df_current[df_current['Nghĩa'] != target['Nghĩa']]['Nghĩa'].unique().tolist()
                opts = [target['Nghĩa']] + random.sample(others, min(len(others), 3))
                random.shuffle(opts)
                st.session_state.q2 = {
                    'w':target['Từ'], 'ans':target['Nghĩa'], 'opts':opts, 
                    'done':False, 'ipa':target['Phát âm'], 'type':target['Loại'],
                    'user_choice': None, 'correct': False
                }
            
            q = st.session_state.q2
            st.info(f"Từ vựng: **{q['w']}** ({q['type']}) - *{q['ipa']}*")
            for opt in q['opts']:
                if st.button(opt, use_container_width=True, disabled=q['done']):
                    q['done'] = True
                    q['user_choice'] = opt
                    if opt == q['ans']: q['correct'] = True
                    st.rerun()

            if q['done']:
                if q['correct']:
                    st.success(f"Chính xác! 🎉 Đáp án là: **{q['ans']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                    st.balloons()
                else:
                    st.error(f"Sai rồi! Đáp án đúng là: **{q['ans']}** 😟")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                
                if st.button("Câu tiếp theo ➡️"):
                    del st.session_state.q2
                    st.rerun()

      
       # --- DẠNG 3 (ĐIỀN TỪ TIẾNG ANH - WRITING) ---
      
        else:
            st.subheader("✍️ Thử thách ghi nhớ")
            
            # 1. Khởi tạo câu hỏi
            if 'q3' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q3 = {
                    'w': target['Từ'], 
                    'ans': target['Nghĩa'], 
                    'ipa': target['Phát âm'], 
                    'type': target['Loại'],
                    'submitted': False,  # Trạng thái đã kiểm tra hay chưa
                    'user_input': ""      # Lưu lại từ người dùng đã gõ
                }
            
            q = st.session_state.q3
            
            # 2. Giao diện hiển thị
            st.info(f"Hãy viết từ tiếng Anh có nghĩa là: **{q['ans']}**")
            st.caption(f"Gợi ý: Từ loại **({q['type']})** | Phát âm: *{q['ipa']}*")
            
            # 3. Ô nhập liệu
            # Lưu ý: Nếu đã submit thì disable ô nhập để chốt kết quả
            user_word = st.text_input(
                "Câu trả lời của bạn:", 
                placeholder="Nhập từ tại đây...", 
                key="input_write",
                disabled=q['submitted']
            ).strip()
      
             
            # 4. Nút bấm kiểm tra
            if not q['submitted']:
                if st.button("🔍 KIỂM TRA", use_container_width=True):
                    if user_word:
                        q['user_input'] = user_word
                        q['submitted'] = True
                        st.rerun() # Chạy lại để hiển thị kết quả dựa trên 'submitted' = True
                    else:
                        st.warning("Bạn chưa nhập gì cả!")
            
            # 5. Hiển thị kết quả sau khi bấm kiểm tra
            if q['submitted']:
                if q['user_input'].lower() == q['w'].lower():
                    st.success(f"Chính xác! ✨ Từ đúng là: **{q['w']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                    st.balloons()
                else:
                    st.error(f"Sai rồi! Bạn nhập: '{q['user_input']}'. Đáp án đúng là: **{q['w']}** 😟")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                # Nút chuyển câu tiếp theo
                if st.button("Câu tiếp theo ➡️", use_container_width=True):
                    del st.session_state.q3
                    st.rerun()
