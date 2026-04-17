import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components
import time
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Hieu's English Hub", page_icon="🧩", layout="wide")
# --- HỆ THỐNG BẢO MẬT (LOGIN) ---
def check_password():
    """Trả về True nếu mật khẩu đúng, ngược lại hiện ô nhập mật khẩu."""
    def password_entered():
        # Kiểm tra mật khẩu (Bạn có thể đổi 'hieu123' thành mật khẩu bạn muốn)
        if st.session_state["password"] == "hieu123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Xóa mật khẩu khỏi session để bảo mật
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Lần đầu truy cập: Hiện ô nhập mật khẩu
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h1 style='color: #58a6ff;'>🔒 Hieu's Hub Security</h1>
                <p style='color: white;'>Vui lòng nhập mật khẩu để truy cập hệ thống.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Mật khẩu:", type="password", on_change=password_entered, key="password")
            if "password_correct" in st.session_state and not st.session_state["password_correct"]:
                st.error("❌ Mật khẩu sai rồi Hiếu ơi!")
        return False
    else:
        return st.session_state["password_correct"]

# CHẶN TOÀN BỘ APP NẾU CHƯA ĐĂNG NHẬP
if not check_password():
    st.stop()  # Dừng mọi logic phía dưới nếu chưa đúng mật khẩu
    
@st.cache_data(ttl=600) 
def load_data(sheet_url):
    if not sheet_url:
        return pd.DataFrame()
    try:
        # Chuyển đổi link thường thành link export CSV
        if "/edit" in sheet_url:
            base_url = sheet_url.split("/edit")[0]
            csv_url = base_url + "/export?format=csv"
            if "gid=" in sheet_url:
                gid = sheet_url.split("gid=")[1].split("&")[0]
                csv_url += f"&gid={gid}"
        else:
            csv_url = sheet_url
            
        df = pd.read_csv(csv_url)
        df = df.fillna("")
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame()
def save_to_gsheets(new_row_dict):
    """Hàm xử lý lưu dữ liệu lên Google Sheets"""
    try:
        # 1. Khởi tạo kết nối (Sử dụng cấu hình trong .streamlit/secrets.toml)
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # 2. Đọc dữ liệu hiện tại từ Sheets để lấy cấu hình DataFrame
        # Lưu ý: target_url phải là link Sheets gốc (không phải link export CSV)
        existing_data = conn.read(spreadsheet=target_url)
        
        # 3. Thêm dòng mới vào DataFrame hiện tại
        new_row_df = pd.DataFrame([new_row_dict])
        updated_df = pd.concat([existing_data, new_row_df], ignore_index=True)
        
        # 4. Ghi đè toàn bộ DataFrame đã cập nhật lên lại Google Sheets
        conn.update(spreadsheet=target_url, data=updated_df)
        return True
    except Exception as e:
        st.error(f"Lỗi hệ thống khi lưu: {e}")
        return False

# --- LOGIC THỜI GIAN ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

def get_study_time():
    duration_seconds = int(time.time() - st.session_state.start_time)
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    return f"{minutes}p {seconds}s"

def play_sound(url):
    components.html(f'<audio autoplay style="display:none"><source src="{url}" type="audio/mp3"></audio>', height=0)

# --- CSS CUSTOM (GIỮ NGUYÊN GIAO DIỆN CỦA HIẾU) ---
st.markdown("""
    <style>
    /* 1. NHẬP FONT CHỮ & NỀN APP */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(rgba(10, 12, 16, 0.9), rgba(10, 12, 16, 0.95)), 
                    url("https://wallpaperaccess.com/full/2454628.png") no-repeat center fixed;
        background-size: cover !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 2. SIDEBAR - CHẾ ĐỘ NÚT BẤM (KHÔNG CHẤM TRÒN) */
    [data-testid="stSidebar"] {
        background-color: rgba(13, 17, 23, 0.98) !important;
        border-right: 1px solid rgba(88, 166, 255, 0.1);
    }

    /* Ẩn triệt để radio mặc định */
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetSelectionMarker"],
    [data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {
        display: none !important;
    }

    /* Biến Label thành Card */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: rgba(33, 38, 45, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        justify-content: center !important;
        cursor: pointer !important;
    }

    /* Chữ trong Sidebar */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        color: #8b949e !important;
        letter-spacing: 1px;
    }

    /* Khi Sidebar được chọn hoặc Hover */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
    [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background: rgba(88, 166, 255, 0.1) !important;
        border: 1px solid #58a6ff !important;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.3) !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(88, 166, 255, 0.6) !important;
    }

    /* 3. WORD CARDS (KHUNG TỪ VỰNG) */
    .word-card {
        background: rgba(22, 27, 34, 0.7) !important;
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(88, 166, 255, 0.1);
        margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }

    .word-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }

    /* 4. HỆ THỐNG NÚT BẤM NEON BLUE (QUIZ) */
    div.stButton > button {
        background: rgba(13, 17, 23, 0.8) !important;
        color: #00d4ff !important;
        border: 1.5px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 8px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px;
        transition: all 0.2s ease !important;
        width: 100%;
        padding: 10px !important;
    }

    /* Hover nút */
    div.stButton > button:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 12px rgba(0, 212, 255, 0.4) !important;
        transform: scale(1.02);
    }

    /* TRẠNG THÁI ĐÃ CHỌN (PRIMARY) - GIỮ MÀU RỰC RỠ */
    div.stButton > button[kind="primary"] {
        background: #00d4ff !important;
        color: #0d1117 !important;
        border: 1.5px solid #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.8) !important;
        opacity: 1 !important;
    }

    /* Khi nộp bài xong bị khóa (Disabled) */
    div.stButton > button:disabled {
        cursor: not-allowed !important;
    }

    /* 5. THÔNG BÁO (SUCCESS/ERROR) */
    div[data-testid="stNotification"] {
        background: rgba(13, 17, 23, 0.9) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & CẤU HÌNH DỮ LIỆU ---
with st.sidebar:
    st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3898/3898082.png' width='80'><h1 style='color: #58a6ff;'>Hieu's Hub</h1></div>", unsafe_allow_html=True)
    
    st.markdown("### 🔗 Cấu hình Database")
    db_mode = st.radio("Nguồn từ vựng:", ["Mẫu của Hieu", "Sheets cá nhân"], label_visibility="collapsed")
    
    if db_mode == "Mẫu của Hieu":
        target_url = "https://docs.google.com/spreadsheets/d/1Cryecd2kF8cmpXGfhsKFenMT89XHhyaMJyx7wkeUxa4/edit#gid=1604492918"
    else:
        target_url = st.text_input("Dán link Sheets của bạn:", placeholder="https://docs.google.com/spreadsheets/d/...")
        st.caption("⚠️ Yêu cầu: Share -> Anyone with the link (Viewer)")

    # Nạp dữ liệu vào biến df_current
    df_current = load_data(target_url)

    if st.button("🔄 Cập nhật dữ liệu mới"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    menu = st.radio("⚡ ĐIỀU KHIỂN", ["⚙️ Dashboard Quản lý", "💎 Flashcard", "📝 Kiểm tra"], key="main_nav")
    
    st.divider()
    st.markdown(f"### ⏱️ Học được: `{get_study_time()}`")
    if st.button("Update Time 🔄"): st.rerun()
    
    st.divider()
    st.metric("Tổng số từ hiện tại", len(df_current))
# --- 1. DASHBOARD QUẢN LÝ ---
if menu == "⚙️ Dashboard Quản lý":
    st.title("⚙️ Quản lý Từ vựng Cloud")
    tab1, tab2 = st.tabs(["✨ Thêm từ đơn", "📦 Thêm hàng loạt"])
    
    with tab1:
        with st.form("add_form", clear_on_submit=True):
            c1, c2, c3, c4, c5 = st.columns([2, 3, 1, 2, 1.5])
            w = c1.text_input("Từ (Word)")
            m = c2.text_input("Nghĩa (Meaning)")
            t = c3.selectbox("Loại", ["n", "v", "adj", "adv", "phr"])
            p = c4.text_input("Phát âm (IPA)")
            pr = c5.text_input("Giới từ (Prep)")
            submitted = st.form_submit_button("LƯU LÊN GOOGLE SHEETS", use_container_width=True)
            
            if submitted:
                if w and m:  
                    new_entry = {
                        "Từ": w,
                        "Nghĩa": m,
                        "Loại": t,
                        "Phát âm": p,
                        "Giới từ": pr
                    }
                    
                    with st.spinner("Đang đồng bộ lên Cloud..."):
                        if save_to_gsheets(new_entry):
                            st.success(f"🚀 Đã thêm thành công từ: {w}")
                            st.cache_data.clear() 
                            time.sleep(1)
                            st.rerun()
                else:
                    st.warning("Hiếu ơi, điền thiếu Từ hoặc Nghĩa rồi kìa!")

    with tab2:
        txt = st.text_area("Định dạng: Từ, Nghĩa, Loại, Phát âm, Giới từ", placeholder="Depend, Phụ thuộc, v, /dɪˈpend/, on")
        if st.button("🚀 NẠP HÀNG LOẠT", use_container_width=True):
            if txt:
                try:
                    # Tách dòng và tách dấu phẩy
                    new_items = [[i.strip() for i in l.split(',')] for l in txt.strip().split('\n') if ',' in l]
                    if new_items:
                        new_df = pd.DataFrame(new_items, columns=["Từ", "Nghĩa", "Loại", "Phát âm", "Giới từ"])
                        final_df = pd.concat([df_current, new_df], ignore_index=True)
                        if save_to_gsheets(final_df):
                            st.success("🚀 Đã nạp hàng loạt thành công!")
                            st.cache_data.clear()
                            st.rerun()
                except Exception as e:
                    st.error(f"Định dạng nhập vào chưa đúng Hiếu ơi: {e}")

    st.divider()
    st.subheader(f"📋 Danh sách ({len(df_current)} từ)")
    
    if not df_current.empty:
        # Search đơn giản
        search = st.text_input("🔍 Tìm nhanh từ trong danh sách:", placeholder="Nhập từ cần tìm...")
        filtered_df = df_current[df_current['Từ'].str.contains(search, case=False)] if search else df_current
        
        cols = st.columns(4)
        for idx, row in filtered_df.iterrows():
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="word-card">
                        <div class="word-title">{row['Từ']}</div>
                        <div style="margin-bottom: 5px;">
                            <span class="type-badge">{row['Loại']}</span>
                            <span style="color: #8b949e; font-size: 0.8em;">{row['Phát âm']}</span>
                        </div>
                        <div class="word-meaning">{row['Nghĩa']}</div>
                        <div style="color: #58a6ff; font-size: 0.8em; margin-top: 5px;">{f"Prep: {row['Giới từ']}" if row['Giới từ'] else ""}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Xoá", key=f"del_{idx}", use_container_width=True):
                    # Tạo bản copy và xóa dòng
                    df_after_del = df_current.drop(idx)
                    if save_to_gsheets(df_after_del):
                        st.cache_data.clear()
                        st.rerun()
# --- 2. FLASHCARD ---
elif menu == "💎 Flashcard":
    st.title("💎 Thẻ ghi nhớ")
    if not df_current.empty:
        if 'idx' not in st.session_state: st.session_state.idx = 0
        if 'flip' not in st.session_state: st.session_state.flip = False
        row = df_current.iloc[st.session_state.idx % len(df_current)]
        
        display = f"<h1>{row['Từ']}</h1><p>{row['Phát âm']}</p>" if not st.session_state.flip else f"<h1 style='color:#58a6ff'>{row['Nghĩa']}</h1>"
        st.markdown(f"<div style='background:rgba(28,33,40,0.9); border:1px solid #58a6ff; border-radius:20px; height:350px; display:flex; align-items:center; justify-content:center; flex-direction:column; text-align:center;'>{display}</div>", unsafe_allow_html=True)
        
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
                ["Dạng 1 (Trắc nghiệm)", "Dạng 2 (Làm đâu biết đó)", "Dạng 3 (Viết từ)", "Dạng 4 (Loại từ)", "Dạng 5 (Giới từ)", "Dạng 6 (Chọn từ)"], 
                horizontal=True)
        
        # --- DẠNG 1: TRẮC NGHIỆM TỔNG HỢP ---
        # --- DẠNG 1: TRẮC NGHIỆM TỔNG HỢP (CẬP NHẬT ĐỦ THÔNG TIN) ---
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

            score = 0
            for i, it in enumerate(st.session_state.ex_list):
                prep_info = f" + {it['Giới từ']}" if it['Giới từ'] else ""
                
                # HIỂN THỊ ĐẦY ĐỦ: TỪ - LOẠI - PHÁT ÂM
                st.markdown(f"""
                    <div style="background: rgba(88, 166, 255, 0.1); padding: 12px; border-radius: 10px; border-left: 5px solid #58a6ff; margin-top: 20px;">
                        <span style="color: #8b949e; font-size: 0.9em;">Câu {i+1}:</span> 
                        <b style="font-size: 1.3em; color: #58a6ff; margin-left: 5px;">{it['Từ']}{prep_info}</b>
                        <div style="margin-top: 5px;">
                            <span style="background: #238636; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; text-transform: uppercase;">{it['Loại']}</span>
                            <span style="color: #8b949e; font-style: italic; font-size: 0.9em; margin-left: 10px;">{it['Phát âm']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(2)
                for idx, opt in enumerate(it['opts']):
                    with cols[idx % 2]:
                        button_key = f"q1_{i}_{idx}"
                        is_selected = (st.session_state.ans.get(i) == opt)
                        
                        if not st.session_state.submitted_d1:
                            if st.button(opt, key=button_key, use_container_width=True, type="primary" if is_selected else "secondary"):
                                st.session_state.ans[i] = opt
                                st.rerun() 
                        else:
                            # Trạng thái sau khi nộp bài
                            if opt == it['Nghĩa']:
                                st.success(f"✓ {opt}")
                            elif is_selected:
                                st.error(f"✗ {opt}")
                            else:
                                st.button(opt, key=button_key, use_container_width=True, disabled=True)

                if st.session_state.submitted_d1 and st.session_state.ans.get(i) == it['Nghĩa']:
                    score += 1
                st.divider()
            
            if not st.session_state.submitted_d1:
                if st.button("📤 NỘP BÀI & CHẤM ĐIỂM", use_container_width=True, type="primary"):
                    st.session_state.submitted_d1 = True
                    st.rerun()
            else:
                st.markdown(f"### 📊 Kết quả: `{score}/{len(st.session_state.ex_list)}` câu đúng")
                if st.button("Làm đề mới 🔄"):
                    del st.session_state.ex_list
                    st.rerun()

            if st.session_state.submitted_d1:
                total_q = len(st.session_state.ex_list)
                st.markdown(f"### 📊 Kết quả: `{score}/{total_q}` câu đúng ({(score/total_q)*100:.0f}%)")
                if score == total_q: st.balloons()

        # --- DẠNG 2: LÀM ĐÂU BIẾT ĐÓ ---
        # --- DẠNG 2: LÀM ĐÂU BIẾT ĐÓ (ANH -> VIỆT) ---
        elif mode == "Dạng 2 (Làm đâu biết đó)":
            if 'q2' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                others = df_current[df_current['Nghĩa'] != target['Nghĩa']]['Nghĩa'].unique().tolist()
                opts = [target['Nghĩa']] + random.sample(others, min(len(others), 3))
                random.shuffle(opts)
                # FIX 1: Thêm 'user_choice' và thống nhất tên biến 'ans'
                st.session_state.q2 = {
                    'w': target['Từ'], 
                    'ans': target['Nghĩa'], 
                    'opts': opts, 
                    'done': False, 
                    'ipa': target['Phát âm'], 
                    'type': target['Loại'], 
                    'prep': target['Giới từ'], 
                    'correct': False,
                    'user_choice': None # Cực kỳ quan trọng để đổi màu
                }
            
            q = st.session_state.q2
            prep_info = f" + {q['prep']}" if q['prep'] else ""
            st.markdown(f"""
                <div class="word-card" style="border-left: 5px solid #fffd75;">
                    <h3 style="color: #fffd75; margin: 0;">Từ vựng: {q['w']}{prep_info}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Loại: <b>{q['type']}</b> | IPA: <i>{q['ipa']}</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            # FIX 2: Khai báo cols để không bị lỗi NameError
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    # KIỂM TRA ĐỂ ĐỔI MÀU NEON
                    is_selected = (q.get('user_choice') == opt)
                    
                    if st.button(
                        opt, 
                        key=f"btn2_{opt}_{i}", 
                        use_container_width=True, 
                        disabled=q['done'],
                        type="primary" if is_selected else "secondary"
                    ):
                        q['user_choice'] = opt
                        q['done'] = True
                        # FIX 3: Sửa từ ans_vn thành ans cho khớp với bên trên
                        if opt == q['ans']: 
                            q['correct'] = True
                        st.rerun()
            
            if q['done']:
                if q['correct']: 
                    st.success("Chính xác! 🎉")
                else: 
                    st.error(f"Sai rồi! Đáp án là: {q['ans']}")
                
                # FIX LỖI DUPLICATE ID
                if st.button("Câu tiếp theo ➡️", key="next_q2_unique_btn"):
                    del st.session_state.q2
                    st.rerun()

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
        # --- DẠNG 4: LOẠI TỪ (NOUN, VERB, ADJ...) ---
        elif mode == "Dạng 4 (Loại từ)":
            if 'q4' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q4 = {
                    'w': target['Từ'], 
                    'ans': target['Loại'], 
                    'meaning': target['Nghĩa'], 
                    'ipa': target['Phát âm'], 
                    'prep': target['Giới từ'], 
                    'done': False, 
                    'user_choice': None # Lưu lựa chọn để đổi màu
                }
            
            q = st.session_state.q4
            prep_info = f" + {q['prep']}" if q['prep'] else ""
            
            # Hiển thị câu hỏi bằng Word Card
            st.markdown(f"""
                <div class="word-card" style="border-left: 5px solid #ffa500;">
                    <h3 style="color: #ffa500; margin: 0;">Từ vựng: {q['w']}{prep_info}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Nghĩa: {q['meaning']} | IPA: {q['ipa']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            btns = st.columns(5)
            types = ["n", "v", "adj", "adv", "phr"]
            
            for idx, t in enumerate(types):
                with btns[idx]:
                    # KIỂM TRA ĐỂ ĐỔI MÀU NEON
                    is_selected = (q.get('user_choice') == t)
                    
                    if st.button(
                        t.upper(), 
                        key=f"btn4_{t}", 
                        use_container_width=True, 
                        disabled=q['done'],
                        # Sáng đèn Neon nếu nút này được chọn
                        type="primary" if is_selected else "secondary"
                    ):
                        q['user_choice'] = t
                        q['done'] = True
                        st.rerun()
            
            if q['done']:
                if q['user_choice'] == q['ans']:
                    st.success(f"✨ Đúng! **{q['w']}** là **{q['ans']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else:
                    st.error(f"❌ Sai rồi! Đáp án đúng là: **{q['ans']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                
                # FIX LỖI DUPLICATE ID BẰNG KEY RIÊNG
                if st.button("Câu tiếp theo ➡️", key="next_q4_unique"): 
                    del st.session_state.q4
                    st.rerun()

        # --- DẠNG 5: GIỚI TỪ ---
        # --- DẠNG 5: KIỂM TRA GIỚI TỪ (PREPOSITIONS) ---
        elif mode == "Dạng 5 (Giới từ)":
            if 'q5' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                st.session_state.q5 = {
                    'w': target['Từ'], 
                    'meaning': target['Nghĩa'], 
                    'ipa': target['Phát âm'], 
                    'type': target['Loại'], 
                    # Chuẩn hóa giới từ về chữ thường
                    'ans': target['Giới từ'].strip().lower() if target['Giới từ'] else "none", 
                    'done': False, 
                    'user_choice': None # Lưu lựa chọn để đổi màu Neon
                }
            
            q = st.session_state.q5
            
            # Hiển thị câu hỏi bằng Card đẹp hơn
            st.markdown(f"""
                <div class="word-card" style="border-left: 5px solid #ff7b72;">
                    <h3 style="color: #ff7b72; margin: 0;">Cấu trúc của từ: {q['w']}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Nghĩa: {q['meaning']} | Loại: {q['type']} | IPA: {q['ipa']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            prep_options = ["none", "to", "from", "of", "with", "in", "on", "at", "for", "about", "be"]
            if q['ans'] not in prep_options: prep_options.append(q['ans'])
            
            cols = st.columns(4)
            for i, p_opt in enumerate(prep_options):
                with cols[i % 4]:
                    # KIỂM TRA ĐỂ ĐỔI MÀU NEON
                    is_selected = (q.get('user_choice') == p_opt)
                    
                    if st.button(
                        p_opt.upper(), 
                        key=f"btn5_{p_opt}_{i}", # Thêm index vào key để tránh trùng ID nếu có trùng tên
                        use_container_width=True, 
                        disabled=q['done'],
                        # Sáng đèn Neon nếu nút này được chọn
                        type="primary" if is_selected else "secondary"
                    ):
                        q['done'] = True
                        q['user_choice'] = p_opt
                        st.rerun()
            
            if q['done']:
                if q['user_choice'] == q['ans']:
                    st.success(f"✨ Đúng! Kết quả: **{q['w']} {q['ans'] if q['ans'] != 'none' else ''}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else:
                    st.error(f"❌ Sai rồi! Giới từ đúng phải là: **{q['ans'].upper()}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                
                # FIX LỖI DUPLICATE ID BẰNG KEY RIÊNG
                if st.button("Câu tiếp theo ➡️", key="next_q5_unique"): 
                    del st.session_state.q5
                    st.rerun()
                
        # --- DẠNG 6: CHỌN TỪ (NGHĨA -> TỪ) ---
        # --- DẠNG 6: CHỌN TỪ (NGHĨA -> TỪ) ---
        elif mode == "Dạng 6 (Chọn từ)":
            if 'q6' not in st.session_state:
                target = df_current.sample(n=1).iloc[0]
                others = df_current[df_current['Từ'] != target['Từ']]['Từ'].unique().tolist()
                opts = [target['Từ']] + random.sample(others, min(len(others), 3))
                random.shuffle(opts)
                
                st.session_state.q6 = {
                    'ans_word': target['Từ'], 
                    'meaning': target['Nghĩa'], 
                    'opts': opts, 
                    'done': False, 
                    'ipa': target['Phát âm'], 
                    'type': target['Loại'], 
                    'prep': target['Giới từ'], 
                    'user_choice': None # Thêm biến này để lưu lựa chọn
                }
            
            q = st.session_state.q6
            st.markdown(f'<div class="word-card"><h3>Nghĩa: {q["meaning"]}</h3></div>', unsafe_allow_html=True)
            
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    # KIỂM TRA ĐỂ ĐỔI MÀU NEON
                    is_selected = (q.get('user_choice') == opt)
                    
                    if st.button(
                        opt, 
                        key=f"btn6_{opt}_{i}", 
                        use_container_width=True, 
                        disabled=q['done'],
                        type="primary" if is_selected else "secondary" # Dòng này giúp sáng đèn Neon
                    ):
                        q['user_choice'] = opt
                        q['done'] = True
                        st.rerun()
            
            if q['done']:
                if q['user_choice'] == q['ans_word']:
                    st.success("Chính xác! 🎉")
                else:
                    st.error(f"Sai rồi! Đáp án là: {q['ans_word']}")
                
                # THÊM KEY RIÊNG BIỆT Ở ĐÂY ĐỂ FIX LỖI DUPLICATE ID
                if st.button("Câu tiếp theo ➡️", key="next_q6_btn"): 
                    del st.session_state.q6
                    st.rerun()
