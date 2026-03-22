# 🚀 Hieu's English Cyber Quiz App
Một ứng dụng học từ vựng tiếng Anh cá nhân được xây dựng bằng **Python** và **Streamlit**, thiết kế riêng để tối ưu hóa việc học tập và quản lý dữ liệu cá nhân.

---

## 💡 Tại sao dự án này ra đời?
Hiện nay, hầu hết các nền tảng học từ vựng phổ biến (như Quizlet) đã bắt đầu thu phí hoặc giới hạn tính năng của người dùng miễn phí. Là một sinh viên chuyên ngành **An toàn thông tin (Network Information Security)**, mình quyết định tự xây dựng công cụ riêng. 

**Mục tiêu:** - Tự do quản lý dữ liệu (không phụ thuộc vào bên thứ ba).
- Hoàn toàn miễn phí và không giới hạn số lượng từ vựng.
- Thực hành kỹ năng lập trình Python và triển khai ứng dụng thực tế (Deployment).

---

## ✨ Tính năng nổi bật
* **Modern Cyber Dashboard:** Giao diện Dark Mode với hiệu ứng Neon sống động, lấy cảm hứng từ các hệ thống giám sát an ninh mạng.
* **Quản lý thông minh:** * Thêm từ vựng đơn lẻ hoặc nạp hàng loạt (Bulk Add) qua văn bản thô.
    * Tự động sắp xếp danh sách theo thứ tự A-Z.
    * Kiểm tra trạng thái từ vựng (Đã tồn tại/Chưa có) để tránh trùng lặp.
* **Hệ thống Flashcard:** Luyện trí nhớ hiệu quả với tính năng lật thẻ (Flip card).
* **Đấu trường kiểm tra (Exam Mode):**
    * **Dạng 1:** Làm bài tập tổng hợp (tùy chọn 20 - 50 câu), nộp bài và tính điểm tự động.
    * **Dạng 2:** Phản hồi tức thì (Làm câu nào biết kết quả câu đó).

---

## 🛠 Công nghệ sử dụng
* **Ngôn ngữ:** Python 3.x
* **Framework:** [Streamlit](https://streamlit.io/) (Xây dựng giao diện Web nhanh chóng).
* **Xử lý dữ liệu:** Pandas Library.
* **Lưu trữ:** Local Database (Flat file `.txt`) - Đảm bảo tính nhẹ gọn và dễ di chuyển.

---

## 📸 Giao diện ứng dụng
<img width="1920" height="950" alt="image" src="https://github.com/user-attachments/assets/6d277fcf-82c9-4bbd-a072-a98dd9f6d4ef" />

---

## 🛠 Cài đặt và Chạy thử (Local)
Nếu bạn muốn chạy thử ứng dụng này trên máy cá nhân:

1. **Clone dự án:**
   ```bash
   git clone [https://github.com/Hieuse22082005/Hieu-English-Quiz-App.git](https://github.com/Hieuse22082005/Hieu-English-Quiz-App.git)

2. **Cài Đặt Thư Viện**

```bash
pip install -r requirements.txt

3. **Khởi chạy:**
```bash
streamlit run app.py
