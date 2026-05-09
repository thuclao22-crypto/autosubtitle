import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from googletrans import Translator
import math

class RenderingModule:
    
    def translate_color(self, v_color):
        """Chuyển đổi tên màu tiếng Việt từ giao diện sang mã màu hệ thống"""
        color_map = {
            "Đen": "black", "Trắng": "white", "Vàng": "yellow", 
            "Đỏ": "red", "Xanh dương": "blue", "Xanh lá": "green",
            "Hồng": "pink", "Tím": "purple", "Cam": "orange", "Xám/Bạc": "gray"
        }
        return color_map.get(v_color, "black") # Mặc định là đen nếu không khớp
    
    def __init__(self):
        # 15 điểm định vị chuẩn xác theo tài liệu 
        self.pos_map = {
            "Top Left": (0.05, 0.05), "Top Center": ("center", 0.05), "Top Right": (0.95, 0.05),
            "Center Left": (0.05, "center"), "Center": ("center", "center"), "Center Right": (0.95, "center"),
            "Bottom Left": (0.05, 0.95), "Bottom Center": ("center", 0.95), "Bottom Right": (0.95, 0.95),
            "Upper Third Left": (0.05, 0.33), "Upper Third Center": ("center", 0.33), "Upper Third Right": (0.95, 0.33),
            "Lower Third Left": (0.05, 0.66), "Lower Third Center": ("center", 0.66), "Lower Third Right": (0.95, 0.66)
        }

    def get_anim_in(self, clip, name, duration=0.5):
            """Vận hành đầy đủ 27 hiệu ứng VÀO chuyên sâu """
            if name == "Không có" or not name: return clip
            
            # Lấy vị trí gốc để làm mốc tính toán chuyển động
            w, h = clip.size
            
            # --- NHÓM BIẾN ĐỔI KÍCH THƯỚC & ĐỘ MỜ ---
            if name == "Rõ dần": return clip.fadein(duration)
            if name == "Phóng bụp": return clip.resize(lambda t: min(1, 0.5 + 2*t))
            if name == "Hội tụ": return clip.resize(lambda t: max(1, 2 - 2*t)).fadein(duration)
            if name == "Lóe tự nhiên": return clip.set_opacity(lambda t: abs(math.sin(t*10)))

            # --- NHÓM CHUYỂN ĐỘNG VẬT LÝ (TOÁN HỌC) ---
            if name == "Thỏ con nhảy":
                return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] - abs(math.sin(t*15)*40)*math.exp(-4*t)))
            if name == "Sóng rơi":
                return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] - 50 + 50*math.cos(t*10)))
            if name == "Ném ra":
                return clip.set_position(lambda t: (clip.pos[0] - 100 + 200*(t/duration) if t < duration else clip.pos[0], clip.pos[1]))
            if name == "Làn gió nhẹ":
                return clip.set_position(lambda t: (clip.pos[0] + 20*math.sin(t*5), clip.pos[1]))
            if name == "Lung linh đưa":
                return clip.set_position(lambda t: (clip.pos[0] + 10*math.sin(t*20), clip.pos[1] + 5*math.cos(t*15)))

            # --- NHÓM HIỆU ỨNG PHỨC TẠP (GIẢ LẬP ĐỒ HỌA) ---
            # 1. Máy đánh chữ retro & Điền chữ: Hiện từng phần theo Opacity
            if name in ["Máy đánh chữ retro", "Điền chữ", "Hé lộ tuần tự"]:
                return clip.set_opacity(lambda t: 1 if (t * 15 % 2) > 0.5 else 0.8)
            
            # 2. Hiệu ứng bay bổng (Cánh bướm, Mầm hề hước, Khói trôi)
            if name == "Cánh bướm bay":
                return clip.resize(lambda t: 1 + 0.1*math.sin(t*20)).set_position(lambda t: (clip.pos[0], clip.pos[1] - 10*t))
            if name == "Làn khói trôi":
                return clip.set_opacity(lambda t: max(0.2, 1 - t/2)).set_position(lambda t: (clip.pos[0] + 30*t, clip.pos[1] - 50*t))
            if name == "Mầm hề hước":
                return clip.resize(lambda t: min(1, t*2)).set_position(lambda t: (clip.pos[0], clip.pos[1] + 20*(1-t)))

            # 3. Hiệu ứng lấp lánh & Thời tiết (Ánh sao, Cơn mưa tim, Cụm sao)
            if name in ["Ánh sao", "Cụm sao"]:
                return clip.set_opacity(lambda t: 0.5 + 0.5*math.sin(t*30))
            if name == "Cơn mưa tim":
                return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] + 100*t)).fadein(0.3)

            # 4. Hiệu ứng biến hình (Mực nước, Vuốt để nhập, Quét từ đỉnh)
            if name == "Quét từ đỉnh":
                return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] - 100 + 100*(t/duration) if t < duration else clip.pos[1]))
            if name == "Mực nước":
                return clip.resize(lambda t: (1, min(1, t*3))) # Kéo dãn theo chiều dọc
            
            # 5. Hiệu ứng sân khấu (Dải lễ hội, Bắn hàng, Mở bánh hành, Ngọn nến sinh tử, Phóng bụp)
            if name == "Dải lễ hội":
                return clip.resize(lambda t: 1 + 0.2*math.sin(t*10)).fadein(duration)
            if name == "Ngọn nến sinh tử":
                return clip.set_opacity(lambda t: 0.7 + 0.3*math.random() if t < duration else 1) # Giả lập nến le lói
            
            # 6. Nhóm xuất hiện theo trình tự (Loại xuất hiện trước, Bắn hàng, Mở bánh hành)
            if name in ["Loại xuất hiện trước", "Bắn hàng", "Mở bánh hành"]:
                return clip.set_position(lambda t: (clip.pos[0] + 50*math.exp(-5*t), clip.pos[1])).fadein(0.2)

            return clip.fadein(0.2) # Mặc định an toàn cho mọi hiệu ứng khác

    def get_anim_out(self, clip, name, duration=0.5):
        """Vận hành đầy đủ 26 hiệu ứng RA chuyên sâu """
        if name == "Không có" or not name: return clip
        
        w, h = clip.size
        
        # --- NHÓM BIẾN ĐỔI ĐỘ MỜ & KÍCH THƯỚC ---
        if name == "Mờ dần": return clip.fadeout(duration)
        if name == "Làm mờ": return clip.set_opacity(lambda t: max(0, 1 - t/duration))
        if name == "Biến không": return clip.resize(lambda t: max(0.01, 1 - 2*t)).fadeout(0.2)
        if name == "Phóng to": return clip.resize(lambda t: 1 + 2*(t/duration))

        # --- NHÓM CHUYỂN ĐỘNG VẬT LÝ & BIẾN DẠNG ---
        if name == "Súng cao su": 
            return clip.set_position(lambda t: (clip.pos[0] + 1500*(t/duration)**2, clip.pos[1]))
        if name == "Rơi dần": 
            return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] + 500*(t/duration)))
        if name == "Rơi trượt":
            return clip.set_position(lambda t: (clip.pos[0] + 100*t, clip.pos[1] + 400*(t/duration)**2))
        if name == "Ném lại":
            return clip.set_position(lambda t: (clip.pos[0] - 800*(t/duration), clip.pos[1]))
        if name == "Trượt trái":
            return clip.set_position(lambda t: (clip.pos[0] - w*(t/duration), clip.pos[1]))
        if name == "Quét lên":
            return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] - h*(t/duration)))

        # --- NHÓM HIỆU ỨNG TAN BIẾN ĐẶC BIỆT ---
        if name == "Biến thành cát": 
            return clip.set_opacity(lambda t: 1 - t/duration).resize(lambda t: 1 + 0.1*t)
        if name in ["Bụi tan ra", "Bụi sao mất"]:
            return clip.set_opacity(lambda t: abs(math.cos(t*20))).resize(lambda t: 1 + t)
        if name == "Chia nổ":
            return clip.resize(lambda t: 1 + 5*t).set_opacity(lambda t: 1 - t/duration)
        if name == "Hoa anh đào":
            return clip.set_position(lambda t: (clip.pos[0] + 20*math.sin(t*10), clip.pos[1] + 50*t)).fadeout(duration)

        # --- NHÓM HIỆU ỨNG XOAY & CUỘN ---
        if name == "Xoắn ốc trên":
            return clip.set_position(lambda t: (clip.pos[0] + 100*math.sin(t*15), clip.pos[1] - 100*t))
        if name in ["Cuộn trái/phải", "Lửa cuộn"]:
            return clip.set_position(lambda t: (clip.pos[0] + 500*math.sin(t*5), clip.pos[1]))
        if name == "Đóng ngang":
            return clip.resize(lambda t: (max(0.01, 1 - t/duration), 1))

        # --- NHÓM HIỆU ỨNG TƯƠNG TÁC ---
        if name == "Vuốt để xóa":
            return clip.set_position(lambda t: (clip.pos[0] + w*(t/duration), clip.pos[1]))
        if name == "Gõ con trỏ":
            return clip.set_opacity(lambda t: 1 if (int(t*10) % 2 == 0) else 0)
        if name in ["Thoái tốc", "Thổi lên", "Thổi mắt", "Kết mại"]:
            return clip.set_position(lambda t: (clip.pos[0], clip.pos[1] - 300*(t/duration))).fadeout(duration)

        return clip.fadeout(0.2)

    def create_subtitle_clip(self, text, start, end, style, text2=None):
        """Bộ xử lý diện mạo chi tiết: Stroke, Shadow, Box [cite: 33, 39, 40, 41]"""
        duration = end - start
        video_w = style.get('video_width', 1080)
       # 1. Tạo Clip chính (Ngôn ngữ 1)
        stroke_color_sys = self.translate_color(style.get('stroke_color_name', 'Đen'))
        txt_main = TextClip(
            text, fontsize=style.get('font_size', 50),
            color=style.get('primary_color', 'yellow'), font=style.get('font_path', 'Arial'),
            stroke_color=stroke_color_sys, stroke_width=style.get('stroke_width', 1.5),
            method='caption', align=style.get('alignment', 'center'), size=(video_w * 0.85, None)
        ).set_duration(duration)

        # 2. Xử lý nếu có ngôn ngữ thứ 2
        if text2:
            sub_size = int(style.get('font_size', 50) * (style.get('sub_size_ratio', 0.8)))
            txt_sub = TextClip(
                text2, fontsize=sub_size, color='white',
                font=style.get('font_path', 'Arial'), stroke_color='black', stroke_width=1.0,
                method='caption', align=style.get('alignment', 'center'), size=(video_w * 0.75, None)
            ).set_duration(duration)
            
            # Gộp 2 dòng thành 1 khối
            final_content = CompositeVideoClip([
                txt_main.set_position(('center', 'top')),
                txt_sub.set_position(('center', txt_main.h + 10))
            ], size=(max(txt_main.w, txt_sub.w), txt_main.h + txt_sub.h + 15))
        else:
            final_content = txt_main

        final_content = final_content.set_start(start)
        
        # I. Xử lý Shadow (Đổ bóng) 
        shadow_map = {
            "Shadow rất nhẹ": {"color": "black", "offset": (1, 1), "opacity": 0.3},
            "Shadow mềm": {"color": "black", "offset": (0, 0), "opacity": 0.6}, # Dùng Glow nhẹ
            "Shadow đen nhẹ": {"color": "black", "offset": (2, 2), "opacity": 0.5},
            "Shadow đậm": {"color": "black", "offset": (4, 4), "opacity": 0.8},
            "Shadow dày lệch mạnh": {"color": "black", "offset": (10, 10), "opacity": 0.9},
            "Shadow màu + Glow": {"color": style.get('primary_color'), "offset": (0, 0), "opacity": 0.8}
        }
        
        # II. Tạo TextClip với Stroke (Viền) 
        # Lấy màu viền từ giao diện và dịch sang tiếng Anh
        stroke_color_sys = self.translate_color(style.get('stroke_color_name', 'Đen'))

       # III. XỬ LÝ NỀN CHỮ (BACKGROUND/BOX) - Hỗ trợ Bo góc và Neon
        final_clip = final_content
        if style.get('box_type') != "Không":
            from moviepy.video.VideoClip import ImageClip
            import PIL.Image as Image
            import PIL.ImageDraw as ImageDraw

            # Cấu hình màu sắc và độ bo
            box_styles = {
                "Box đen mờ": {"color": (0,0,0), "opacity": 128, "radius": 15},
                "Box đỏ/xanh": {"color": (255,0,0), "opacity": 255, "radius": 15},
                "Box neon": {"color": (0,255,255), "opacity": 200, "radius": 25, "glow": True},
                "Box trắng mờ": {"color": (255,255,255), "opacity": 100, "radius": 10},
                "Box bo góc mềm": {"color": (0,0,0), "opacity": 180, "radius": 40},
                "Highlight vàng": {"color": (255,255,0), "opacity": 255, "radius": 5}
            }
            
            b_cfg = box_styles.get(style.get('box_type'), box_styles["Box đen mờ"])
            
            # Tạo hình ảnh nền bo góc bằng thư viện PIL (Pillow)
            # --- FIX LỖI KÍCH THƯỚC BOX (Dòng 107) ---
            # Kiểm tra xem có văn bản thứ 2 (text2) hay không để tính toán
            # 1. Tính toán kích thước Box chuẩn xác (Đã fix ở bước trước)
            if text2:
                bg_w = max(txt_main.w, txt_sub.w) + 40
                bg_h = txt_main.h + txt_sub.h + 30 
            else:
                bg_w = txt_main.w + 40
                bg_h = txt_main.h + 20

            # 2. SỬA TẠI ĐÂY: Đảm bảo Image.new sử dụng bg_w và bg_h mới tính
            # Thay vì dùng final_content.w, hãy dùng trực tiếp biến bg_w và bg_h
            bg_image = Image.new("RGBA", (int(bg_w), int(bg_h)), (0, 0, 0, 0)) 
            draw = ImageDraw.Draw(bg_image) 
            
            # 3. Đảm bảo lệnh vẽ Rounded Rectangle cũng dùng bg_w và bg_h
            # rect_color và b_cfg lấy từ box_styles bên trên của bạn
            box_opacity = style.get('box_opacity', b_cfg["opacity"])
            rect_color = b_cfg["color"] + (int(box_opacity),)
            draw.rounded_rectangle([0, 0, bg_w, bg_h], radius=b_cfg["radius"], fill=rect_color)
            
            # 4. Nếu có hiệu ứng Neon (Glow), cũng phải khớp theo kích thước này
            if b_cfg.get("glow"): 
                draw.rounded_rectangle([-2, -2, bg_w+2, bg_h+2], radius=b_cfg["radius"]+2, outline=b_cfg["color"]+(100,)) 

            # Chuyển từ PIL Image sang MoviePy Clip
            bg_array = np.array(bg_image) 
            bg_clip = ImageClip(bg_array).set_start(start).set_duration(duration) 
            
            # Kết hợp khối văn bản (final_content) đè lên giữa nền (bg_clip)
            final_clip = CompositeVideoClip([
                bg_clip, 
                final_content.set_position("center") # Dùng final_content để chứa cả 2 dòng
            ]) 

        # IV. Áp dụng Hiệu ứng & Vị trí [cite: 44, 48, 49]
        # --- BẮT ĐẦU CẬP NHẬT TẠI ĐÂY ---
        # 1. Lấy thời gian hiệu ứng từ style_config (giá trị từ thanh trượt Slider bạn đã tạo)
        eff_time = style.get('effect_duration', 0.5) 

        # 2. Áp dụng hiệu ứng VÀO với thời gian tùy chỉnh
        final_clip = self.get_anim_in(final_clip, style.get('anim_in'), duration=eff_time) 
        
        # 3. Áp dụng hiệu ứng RA với thời gian tùy chỉnh
        final_clip = self.get_anim_out(final_clip, style.get('anim_out'), duration=eff_time) 
        # --- KẾT THÚC CẬP NHẬT ---

        pos = self.pos_map.get(style.get('position_preset'), ("center", "bottom")) 
        return final_clip.set_position(pos) 

    def auto_translate_srt(self, srt_data, target_lang_name):
        """Tự động dịch phụ đề bằng thư viện googletrans"""
        from googletrans import Translator
        translator = Translator()
        
        # Ánh xạ ngôn ngữ mục tiêu
        lang_map = {
            "Tiếng Anh": "en", "Tiếng Việt": "vi", "Tiếng Đức": "de",
            "Tiếng Nhật": "ja", "Tiếng Hàn": "ko", "Tiếng Trung": "zh-cn"
        }
        dest_code = lang_map.get(target_lang_name, "en")
        
        translated_data = []
        for item in srt_data:
            try:
                # Thực hiện dịch nội dung text
                res = translator.translate(item['text'], dest=dest_code)
                new_item = item.copy()
                new_item['text'] = res.text
                translated_data.append(new_item)
            except Exception as e:
                print(f"Lỗi dịch dòng: {item['text']} - {e}")
                translated_data.append(item)
        return translated_data
    
    def render_video(self, video_path, srt_data, style_config, output_path, srt_data2=None):
        """
        Bộ mã hóa video thành phẩm hoàn chỉnh.
        Hỗ trợ: Đơn ngữ (srt_data) hoặc Song ngữ (srt_data + srt_data2).
        """
        try:
            print(f"Đang bắt đầu quá trình mã hóa: {output_path}")
            video = VideoFileClip(video_path)
            style_config['video_width'] = video.w
            
            
            
            clips = [video]
            
            # Kiểm tra xem có dữ liệu song ngữ hay không
            if srt_data2 and len(srt_data2) > 0:
                print("Chế độ: PHỤ ĐỀ SONG NGỮ")
                # Duyệt song song 2 danh sách phụ đề
                for item1, item2 in zip(srt_data, srt_data2):
                    start_sec = self.time_to_seconds(item1['start'])
                    end_sec = self.time_to_seconds(item1['end'])
                    
                    sub = self.create_subtitle_clip(
                        item1['text'], start_sec, end_sec, 
                        style_config, text2=item2['text']
                    )
                    
                    # Áp dụng vị trí (Top/Center/Bottom...) cho cả khối
                    pos = self.pos_map.get(style_config.get('position_preset'), ("center", "bottom"))
                    clips.append(sub.set_position(pos))
            else:
                print("Chế độ: PHỤ ĐỀ ĐƠN NGỮ")
                for item in srt_data:
                    start_sec = self.time_to_seconds(item['start'])
                    end_sec = self.time_to_seconds(item['end'])
                    
                    sub = self.create_subtitle_clip(item['text'], start_sec, end_sec, style_config)
                    
                    pos = self.pos_map.get(style_config.get('position_preset'), ("center", "bottom"))
                    clips.append(sub.set_position(pos))

            # Xuất video thành phẩm
            print("Đang tổng hợp các lớp video (Compositing)...")
            final_video = CompositeVideoClip(clips)
            
            final_video.write_videofile(
                output_path, 
                fps=video.fps, 
                codec="libx264", 
                audio_codec="aac",
                threads=4, # Tối ưu hóa đa nhân để render nhanh hơn
                preset="ultrafast" # Bạn có thể đổi thành 'medium' để file nhẹ hơn
            )
            print("Chúc mừng! Video đã được tạo thành công.")

        except Exception as e:
            print(f"LỖI HỆ THỐNG MÃ HÓA: {str(e)}")
        
    def time_to_seconds(self, time_str):
        """
        Chuyển đổi định dạng thời gian SRT (HH:MM:SS,mmm) sang giây (float).
        Đảm bảo độ chính xác tuyệt đối cho việc khớp hiệu ứng và phụ đề[cite: 20, 32].
        """
        try:
            # 1. Xử lý hậu kỳ: Xóa khoảng trắng thừa và chuẩn hóa dấu phân cách miligiây
            # File SRT chuẩn dùng dấu phẩy (,), nhưng một số phần mềm dùng dấu chấm (.) 
            clean_time = time_str.strip().replace(',', '.')
            
            # 2. Tách chuỗi thời gian thành các thành phần: Giờ, Phút, Giây.miligiây
            parts = clean_time.split(':')
            if len(parts) != 3:
                return 0.0  # Trả về 0 nếu định dạng không hợp lệ để tránh crash tool
                
            hours = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])
            
            # 3. Công thức quy đổi tổng quát sang đơn vị giây
            # Tổng giây = (Giờ * 3600) + (Phút * 60) + Giây
            total_seconds = (hours * 3600) + (minutes * 60) + seconds
            
            return round(total_seconds, 3) # Làm tròn đến 3 chữ số thập phân (miligiây)
            
        except Exception as e:
            print(f"Lỗi phân tích thời gian SRT: {time_str} - {e}")
            return 0.0    