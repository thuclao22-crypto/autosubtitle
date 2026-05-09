import whisper
import os
from whisper.utils import get_writer

class TranscriptionModule:
    def __init__(self, model_size="base"):
        """
        Khởi tạo Module 1 với mô hình Whisper.
        Model 'base' cân bằng giữa tốc độ và độ chính xác.
        """
        # Sử dụng mô hình AI để xử lý giọng nói thành chữ [cite: 18]
        self.model = whisper.load_model(model_size)

    def format_time(self, seconds):
        """Chuyển đổi giây (float) sang định dạng SRT: HH:MM:SS,mmm"""
        import math
        ms = int((seconds - math.floor(seconds)) * 1000)
        s = int(math.floor(seconds))
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    
    def transcribe(self, video_path, output_dir="outputs", selected_lang="Tự động nhận diện"):
        """
        Quy trình vận hành chi tiết: Tách âm -> Nhận diện ngôn ngữ chọn sẵn -> Xuất SRT
        """
        # 1. Ánh xạ ngôn ngữ từ giao diện sang mã Whisper (Nâng cấp quan trọng)
        lang_map = {
            "Tiếng Việt": "vi",
            "Tiếng Anh": "en",
            "Tiếng Đức": "de",
            "Tiếng Nhật": "ja",
            "Tiếng Hàn": "ko",
            "Tiếng Trung": "zh",
            "Tự động nhận diện": None
        }
        whisper_lang = lang_map.get(selected_lang)

        # 2. Khởi tạo thư mục đầu ra nếu chưa có
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"--- Đang bắt đầu xử lý: {video_path} ---")
        if whisper_lang:
            print(f"--- Chế độ: Ép ngôn ngữ '{selected_lang}' để tăng độ chính xác ---")
        else:
            print(f"--- Chế độ: Tự động nhận diện ngôn ngữ (LID) ---")

        # 3. Thực hiện nhận diện với tham số language đã nâng cấp
        # Thêm language=whisper_lang để ép Whisper chạy đúng model ngôn ngữ
        result = self.model.transcribe(
            video_path, 
            verbose=False, 
            fp16=False,
            language=whisper_lang 
        )

        # 4. Tiêu chuẩn chống lỗi font và xuất file SRT
        video_filename = os.path.basename(video_path).split('.')[0]
        writer = get_writer("srt", output_dir)

        # 5. Thiết lập các tùy chọn kiểm soát độ dài câu (Hậu xử lý văn bản)
        options = {
            "max_line_width": 30, # Kiểm soát độ dài câu để tránh tràn khung hình ở Module 2
            "max_line_count": 1,
            "highlight_words": False
        }

        # 6. Ghi file SRT dự phòng
        writer(result, video_path, options)
        srt_path = os.path.join(output_dir, f"{video_filename}.srt")
        
        # --- ĐOẠN CODE MỚI THÊM VÀO TỪ ĐÂY ---
        
        # 7. Tạo danh sách phụ đề trực tiếp từ kết quả của Whisper trong bộ nhớ RAM
        formatted_srt_list = []
        for segment in result['segments']:
            formatted_srt_list.append({
                'start': self.format_time(segment['start']), 
                'end': self.format_time(segment['end']),
                'text': segment['text'].strip()
            })

        print(f"--- Hoàn thành! Đã trích xuất {len(formatted_srt_list)} câu phụ đề ---")

        # TRẢ VỀ CẢ 3 THỨ: Đường dẫn file, Ngôn ngữ, và DANH SÁCH DỮ LIỆU ĐÃ ĐỊNH DẠNG
        return srt_path, result.get('language'), formatted_srt_list

# Đoạn code kiểm tra nhanh (Test)
if __name__ == "__main__":
    # Lưu ý: Thay 'test_video.mp4' bằng 1 file video thật của bạn để thử nghiệm
    # transcriber = TranscriptionModule()
    # transcriber.transcribe("path_to_your_video.mp4")
    pass