import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components
import time
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components
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
    [data-testid="stSidebar"] {
        background-color: rgba(22, 27, 34, 0.7) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(88, 166, 255, 0.2);
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
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    .word-title { color: #58a6ff; font-size: 1.3em; font-weight: bold; }
    .word-type { background: #238636; color: white; padding: 1px 8px; border-radius: 4px; font-size: 0.7em; text-transform: uppercase; width: fit-content; }
    .word-ipa { color: #8b949e; font-style: italic; font-size: 0.9em; }
    .word-meaning { color: #c9d1d9; font-size: 1em; margin-top: 8px; }
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
            submitted = st.form_submit_button("LƯU LÊN GOOGLE SHEETS")
            
            if submitted and w and m:
                # Sửa lỗi: Đảm bảo tên cột khớp 100% với Sheets
                new_row = pd.DataFrame([{"Từ": w, "Nghĩa": m, "Loại": t, "Phát âm": p, "Giới từ": pr}])
                df_updated = pd.concat([df_current, new_row], ignore_index=True)
                save_to_gsheets(df_updated)
                st.success(f"Đã lưu từ '{w}' lên Cloud thành công!")
                time.sleep(1)
                st.rerun()

    with tab2:
        txt = st.text_area("Định dạng: Từ, Nghĩa, Loại, Phát âm, Giới từ", placeholder="Depend, Phụ thuộc, v, /dɪˈpend/, on")
        if st.button("🚀 NẠP HÀNG LOẠT"):
            if txt:
                new_items = [l.split(',') for l in txt.strip().split('\n') if ',' in l]
                if new_items:
                    new_df = pd.DataFrame(new_items, columns=["Từ", "Nghĩa", "Loại", "Phát âm", "Giới từ"])
                    save_to_gsheets(pd.concat([df_current, new_df], ignore_index=True))
                    st.rerun()

    st.subheader(f"📋 Danh sách ({len(df_current)} từ)")
    if not df_current.empty:
        cols = st.columns(4)
        for idx, row in df_current.iterrows():
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="vocab-card">
                        <div class="word-title">{row['Từ']}</div>
                        <div class="word-type">{row['Loại']}</div>
                        <div class="word-ipa">{row['Phát âm']}</div>
                        <div class="word-meaning">{row['Nghĩa']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Xoá {row['Từ']}", key=f"del_{idx}", use_container_width=True):
                    save_to_gsheets(df_current.drop(idx))
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
                
        # --- DẠNG 6: CHỌN TỪ (NGHĨA -> TỪ) ---
        elif mode == "Dạng 6 (Chọn từ)":
            if 'q6' not in st.session_state:
                # Lấy 1 từ làm đáp án đúng
                target = df_current.sample(n=1).iloc[0]
                # Lấy các từ khác làm phương án nhiễu (dựa trên cột 'Từ')
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
                    'correct': False
                }
            
            q = st.session_state.q6
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; border-left: 5px solid #a29bfe; margin-bottom: 20px;">
                    <h3 style="color: #a29bfe; margin: 0;">Nghĩa của từ: {q['meaning']}</h3>
                    <p style="color: #ffffff; margin: 5px 0 0 0; opacity: 0.9;">Gợi ý: <b>{q['type']}</b> | IPA: <i>{q['ipa']}</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Hiển thị các từ tiếng Anh để người dùng chọn
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    if st.button(opt, key=f"btn6_{opt}_{i}", use_container_width=True, disabled=q['done']):
                        q['done'] = True
                        if opt == q['ans_word']: 
                            q['correct'] = True
                        st.rerun()
            
            if q['done']:
                if q['correct']: 
                    st.success(f"Chính xác! **{q['ans_word']}** là đáp án đúng. 🎉")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                else: 
                    st.error(f"Sai rồi! Từ đúng phải là: **{q['ans_word']}**")
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                
                if st.button("Câu tiếp theo ➡️"): 
                    del st.session_state.q6
                    st.rerun()
GA_ID = "G-Y736MTG61T" 

def inject_ga():
    ga_code = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{GA_ID}');
        </script>
    """
    # Dòng này giúp nhúng mã Google vào app mà không hiện ra giao diện
    components.html(ga_code, height=0)

# Gọi hàm này để nó luôn chạy ngầm
inject_ga()
