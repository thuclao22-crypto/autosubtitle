import sys
import os
import cv2
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QLabel, QSlider, QComboBox, QFrame, 
                             QScrollArea, QColorDialog, QFontComboBox, QSpinBox,
                             QButtonGroup, QApplication, QFileDialog, QLineEdit, 
                             QGridLayout, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView) 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtGui import QImage, QPixmap
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoSubtitle Pro - Professional Edition V2.1 Fixed")
        self.setMinimumSize(1400, 950)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Đổi layout chính thành Vertical để chứa Top Bar
        self.container_layout = QVBoxLayout(central_widget)

        # --- PHẦN MỚI: NHẬP DỮ LIỆU ĐẦU VÀO & ĐẦU RA ---
        io_frame = QFrame()
        io_layout = QGridLayout(io_frame)
        
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("Chọn file video hoặc thư mục...")
        io_layout.addWidget(QLabel("Nguồn đầu vào:"), 0, 0)
        io_layout.addWidget(self.input_path_edit, 0, 1)
        
        btn_input_file = QPushButton("Chọn 1 Video"); btn_input_file.clicked.connect(self.select_input_file)
        btn_input_folder = QPushButton("Chọn Folder"); btn_input_folder.clicked.connect(self.select_input_folder)
        io_layout.addWidget(btn_input_file, 0, 2)
        io_layout.addWidget(btn_input_folder, 0, 3)

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Chọn thư mục lưu kết quả...")
        io_layout.addWidget(QLabel("Nơi lưu video:"), 1, 0)
        io_layout.addWidget(self.output_path_edit, 1, 1)
        
        btn_output = QPushButton("Chọn nơi lưu"); btn_output.clicked.connect(self.select_output_folder)
        io_layout.addWidget(btn_output, 1, 2)
        
        self.container_layout.addWidget(io_frame)

        # Tạo layout ngang cho phần nội dung chính bên dưới
        main_layout = QHBoxLayout()
        self.container_layout.addLayout(main_layout)
        
        # --- KHỐI 1: SIDEBAR ĐIỀU KHIỂN ---
        sidebar_scroll = QScrollArea()
        sidebar_scroll.setFixedWidth(460)
        sidebar_scroll.setWidgetResizable(True)
        sidebar_scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        self.sidebar_layout = QVBoxLayout(container)
        
        # A. BỘ XỬ LÝ DIỆN MẠO
        self.add_section_title("A. BỘ XỬ LÝ DIỆN MẠO (STYLING ENGINE)")
        
        self.sidebar_layout.addWidget(QLabel("Phông chữ (.ttf, .otf):"))
        self.font_combo = QFontComboBox()
        self.sidebar_layout.addWidget(self.font_combo)
        
        size_layout = QHBoxLayout()
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 500); self.font_size_spin.setValue(50)
        size_layout.addWidget(QLabel("Kích thước (px):"))
        size_layout.addWidget(self.font_size_spin)
        self.sidebar_layout.addLayout(size_layout)

        self.sidebar_layout.addWidget(QLabel("Màu sắc chính (Primary Color):"))
        color_action_layout = QHBoxLayout()
        self.color_preview = QFrame()
        self.color_preview.setFixedSize(60, 30)
        self.color_preview.setStyleSheet("background-color: #FFFF00; border: 1px solid #555; border-radius: 4px;")
        self.btn_pick_color = QPushButton("Mở bảng màu chuyên sâu")
        self.btn_pick_color.clicked.connect(self.open_advanced_color_dialog)
        color_action_layout.addWidget(self.color_preview)
        color_action_layout.addWidget(self.btn_pick_color)
        self.sidebar_layout.addLayout(color_action_layout)

        self.sidebar_layout.addWidget(QLabel("Viền chữ (Stroke):"))
        self.stroke_combo = QComboBox()
        self.stroke_combo.addItems(["Đen", "Trắng", "Vàng", "Đỏ", "Xanh dương", "Xanh lá", "Hồng", "Tím", "Cam", "Xám/Bạc"])
        self.sidebar_layout.addWidget(self.stroke_combo)

        self.sidebar_layout.addWidget(QLabel("Kiểu Đổ Bóng (Shadow):"))
        self.shadow_combo = QComboBox()
        self.shadow_combo.addItems(["Không", "Shadow đen nhẹ", "Shadow đậm", "Shadow mềm", "Shadow màu + Glow", "Shadow rất nhẹ", "Shadow dày lệch mạnh"])
        self.sidebar_layout.addWidget(self.shadow_combo)

        self.sidebar_layout.addWidget(QLabel("Nền chữ (Background/Box):"))
        self.box_combo = QComboBox()
        self.box_combo.addItems(["Không", "Box đen mờ", "Box đỏ/xanh", "Box neon", "Box trắng mờ", "Box bo góc mềm", "Highlight vàng"])
        self.sidebar_layout.addWidget(self.box_combo)
        
        # --- BỔ SUNG CẤU HÌNH NGÔN NGỮ ---
        # --- 1. ĐỔI TÊN THÀNH CẤU HÌNH NGÔN NGỮ ---
        self.add_section_title("CẤU HÌNH NGÔN NGỮ")
        
        # --- 2. THÊM LỰA CHỌN NGÔN NGỮ 1 ---
        self.sidebar_layout.addWidget(QLabel("Ngôn ngữ 1 (Gốc):"))
        self.lang1_combo = QComboBox()
        self.lang1_combo.addItems(["Tự động nhận diện", "Tiếng Việt", "Tiếng Anh", "Tiếng Đức", "Tiếng Nhật", "Tiếng Hàn", "Tiếng Trung"])
        self.sidebar_layout.addWidget(self.lang1_combo)

        # --- 3. Ô TICK VÀ NGÔN NGỮ 2 ---
        self.check_bilingual = QCheckBox("Kích hoạt phụ đề song ngữ")
        self.check_bilingual.setStyleSheet("font-weight: bold; color: white;")
        # Kết nối sự kiện để ẩn/hiện ngôn ngữ 2
        self.check_bilingual.toggled.connect(self.toggle_bilingual_options)
        self.sidebar_layout.addWidget(self.check_bilingual)

        # Container chứa các tùy chọn ngôn ngữ 2 (để ẩn/hiện)
        self.bilingual_container = QWidget()
        self.bilingual_vbox = QVBoxLayout(self.bilingual_container)
        self.bilingual_vbox.setContentsMargins(0, 5, 0, 5)

        self.bilingual_vbox.addWidget(QLabel("Ngôn ngữ 2 (Phụ):"))
        self.lang2_combo = QComboBox()
        self.lang2_combo.addItems(["Tiếng Anh", "Tiếng Việt", "Tiếng Đức", "Tiếng Nhật", "Tiếng Hàn", "Tiếng Trung"])
        self.bilingual_vbox.addWidget(self.lang2_combo)
        
        self.sidebar_layout.addWidget(self.bilingual_container)
        self.bilingual_container.setVisible(False) # Mặc định ẩn khi chưa tick

        # --- 4. TỶ LỆ SIZE CÓ HIỆN PHẦN TRĂM ---
        percent_layout = QHBoxLayout()
        self.label_percent = QLabel("Tỷ lệ size ngôn ngữ phụ: 80%")
        percent_layout.addWidget(self.label_percent)
        
        self.sub_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.sub_size_slider.setRange(40, 100)
        self.sub_size_slider.setValue(80)
        # Kết nối sự kiện để cập nhật con số phần trăm khi kéo
        self.sub_size_slider.valueChanged.connect(self.update_percent_label)
        
        self.sidebar_layout.addLayout(percent_layout)
        self.sidebar_layout.addWidget(self.sub_size_slider)

        # B. ĐỊNH VỊ & CĂN CHỈNH
        self.add_section_title("B. ĐỊNH VỊ & CĂN CHỈNH")
        
        self.sidebar_layout.addWidget(QLabel("Căn chỉnh lề (Alignment):"))
        align_btn_layout = QHBoxLayout()
        
        # Sửa lỗi: QButtonGroup phải nằm trong QtWidgets
        self.alignment_group = QButtonGroup(self)
        
        self.btn_align_left = QPushButton("Trái")
        self.btn_align_center = QPushButton("Giữa")
        self.btn_align_right = QPushButton("Phải")
        
        button_style = """
            QPushButton {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:checked {
                background-color: #3498db;
                color: white;
                border: 1px solid #2980b9;
                font-weight: bold;
            }
        """
        
        for btn in [self.btn_align_left, self.btn_align_center, self.btn_align_right]:
            btn.setCheckable(True)
            btn.setStyleSheet(button_style)
            self.alignment_group.addButton(btn)
            align_btn_layout.addWidget(btn)
        
        self.btn_align_center.setChecked(True)
        self.sidebar_layout.addLayout(align_btn_layout)

        self.sidebar_layout.addWidget(QLabel("Vị trí có sẵn (Quick Presets):"))
        self.pos_combo = QComboBox()
        self.pos_combo.addItems([
            "Top Left", "Top Center", "Top Right",
            "Center Left", "Center", "Center Right",
            "Bottom Left", "Bottom Center", "Bottom Right",
            "Upper Third Left", "Upper Third Center", "Upper Third Right",
            "Lower Third Left", "Lower Third Center", "Lower Third Right"
        ])
        self.sidebar_layout.addWidget(self.pos_combo)

        # C. BỘ TẠO HIỆU ỨNG (ANIMATION)
        self.add_section_title("C. BỘ TẠO HIỆU ỨNG (ANIMATION)")
        
        self.sidebar_layout.addWidget(QLabel("Hiệu ứng VÀO (In):"))
        self.anim_in = QComboBox()
        self.anim_in.addItems(["Không có", "Ném ra", "Điền chữ", "Rõ dần", "Hội tụ", "Lóe tự nhiên", "Sóng rơi", "Mầm hề hước", "Cánh bướm bay", "Làn gió nhẹ", "Máy đánh chữ retro", "Ánh sao", "Bắn hàng", "Mở bánh hành", "Thỏ con nhảy", "Cụm sao", "Làn khói trôi", "Vuốt để nhập", "Mực nước", "Cơn mưa tim", "Lung linh đưa", "Phóng bụp", "Loại xuất hiện trước", "Hé lộ tuần tự", "Dải lễ hội", "Quét từ đỉnh", "Ngọn nến sinh tử"])
        self.sidebar_layout.addWidget(self.anim_in)

        self.sidebar_layout.addWidget(QLabel("Hiệu ứng RA (Out):"))
        self.anim_out = QComboBox()
        self.anim_out.addItems(["Không có", "Chia nổ", "Quét lên", "Làm mờ", "Mờ dần", "Rơi trượt", "Kết mại", "Hoa anh đào", "Thổi lên", "Ném lại", "Thoái tốc", "Biến thành cát", "Gõ con trỏ", "Xoắn ốc trên", "Rơi dần", "Biến không", "Vuốt để xóa", "Trượt trái", "Đóng ngang", "Cuộn trái/phải", "Lửa cuộn", "Thổi mắt", "Bụi tan ra", "Súng cao su", "Phóng to", "Bụi sao mất"])
        self.sidebar_layout.addWidget(self.anim_out)
        
        # Thêm dưới phần Hiệu ứng RA (Out)
        self.sidebar_layout.addWidget(QLabel("Thời gian hiệu ứng (Automation):"))
        self.effect_dur_label = QLabel("0.5s")
        self.effect_dur_slider = QSlider(Qt.Orientation.Horizontal)
        self.effect_dur_slider.setRange(1, 30) # 0.1s đến 3.0s
        self.effect_dur_slider.setValue(5) # Mặc định 0.5s
        
        # Hiển thị con số khi kéo
        self.effect_dur_slider.valueChanged.connect(lambda v: self.effect_dur_label.setText(f"{v/10}s"))
        
        eff_layout = QHBoxLayout()
        eff_layout.addWidget(self.effect_dur_slider)
        eff_layout.addWidget(self.effect_dur_label)
        self.sidebar_layout.addLayout(eff_layout)

        self.sidebar_layout.addStretch()
        sidebar_scroll.setWidget(container)

        # --- KHỐI 2: PREVIEW & TIMELINE ---
        preview_container = QWidget()
        right_layout = QVBoxLayout(preview_container)

        self.video_preview = QLabel("MÀN HÌNH TRÌNH PHÁT")
        self.video_preview.setStyleSheet("background-color: black; border: 2px solid #333; color: white;")
        self.video_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.video_preview, 5)
        
        # --- PHẦN MỚI: LỰA CHỌN TỶ LỆ KHUNG HÌNH ---
        ratio_frame = QFrame()
        ratio_layout = QVBoxLayout(ratio_frame)
        ratio_layout.addWidget(QLabel("<b>LỰA CHỌN TỶ LỆ KHUNG HÌNH:</b>"))
        
        grid = QGridLayout()
        ratios = [
            ("16:9 YouTube, PC, TV", 0, 0), ("9:16 TikTok, Shorts", 0, 1), ("1:1 Instagram", 0, 2),
            ("4:3 Retro", 1, 0), ("2.35:1 Phim điện ảnh", 1, 1), ("1.85:1 Phim chuẩn", 1, 2),
            ("2:1 Netflix style", 2, 0), ("3:4 Ảnh dọc", 2, 1), ("5.8-inch Mobile preview", 2, 2),
            ("Custom Tùy chỉnh", 3, 1)
        ]
        
        self.ratio_group = QButtonGroup(self)
        for text, r, c in ratios:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton:checked { background-color: #27ae60; color: white; font-weight: bold; }")
            self.ratio_group.addButton(btn)
            grid.addWidget(btn, r, c)
            
        ratio_layout.addLayout(grid)
        right_layout.addWidget(ratio_frame)

        # Thay thế khung đen cũ bằng Slider tua giả lập
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setRange(0, 1000)
        self.timeline_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #222; height: 10px; border-radius: 5px; }
            QSlider::handle:horizontal { background: #e67e22; width: 18px; margin: -5px 0; border-radius: 9px; }
        """)
        right_layout.addWidget(self.timeline_slider) # Đặt vào khoảng trống giữa tỷ lệ khung hình và bảng SRT

        # --- BỔ SUNG BẢNG DUYỆT PHỤ ĐỀ ---
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        self.subtitle_table = QTableWidget()
        self.subtitle_table.setColumnCount(3)
        self.subtitle_table.setHorizontalHeaderLabels(["Bắt đầu", "Kết thúc", "Nội dung"])
        self.subtitle_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.subtitle_table.setFixedHeight(200)
        self.subtitle_table.setStyleSheet("background-color: #333; color: white;")
        
        # Thêm bảng vào layout trước nút Export
        right_layout.insertWidget(3, self.subtitle_table)
        
        self.btn_export = QPushButton("XUẤT VIDEO HOÀN CHỈNH")
        self.btn_export.clicked.connect(self.handle_export_process)
        self.btn_export.setFixedHeight(50)
        self.btn_export.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold;")
        right_layout.addWidget(self.btn_export)

        main_layout.addWidget(sidebar_scroll)
        main_layout.addWidget(preview_container)

    def add_section_title(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #3498db; margin-top: 15px; font-size: 13px; border-bottom: 1px solid #ddd; padding-bottom: 5px;")
        self.sidebar_layout.addWidget(label)

    def select_input_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Chọn Video", "", "Video Files (*.mp4 *.avi *.mkv)")
        if file: 
            self.input_path_edit.setText(file)
            # THÊM DÒNG NÀY ĐỂ HIỆN VIDEO:
            self.update_video_preview(file)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn Thư mục Video")
        if folder: 
            self.input_path_edit.setText(folder)
            # Tìm video đầu tiên trong folder để làm chuẩn hiển thị
            import os
            files = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.avi', '.mkv'))]
            if files:
                first_video = os.path.join(folder, files[0])
                self.update_video_preview(first_video)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn Nơi lưu")
        if folder: self.output_path_edit.setText(folder)
    
    def open_advanced_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color.name()
            self.color_preview.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #555; border-radius: 4px;")
            
    def select_srt2_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Chọn file phụ đề thứ 2", "", "Subtitle Files (*.srt)")
        if file: self.srt2_path_edit.setText(file)        
        
    def handle_export_process(self):
        """
        Hàm xử lý xuất video nâng cấp: 
        1. Tự động nhận diện File đơn lẻ hoặc Thư mục (Folder).
        2. Quy trình 2 giai đoạn: Quét tạo SRT -> Duyệt/Sửa trên bảng -> Render thành phẩm.
        """
        import os
        input_path = self.input_path_edit.text().strip()
        output_base = self.output_path_edit.text().strip()

        if not input_path or not os.path.exists(input_path):
            print("Lỗi: Đường dẫn đầu vào không hợp lệ hoặc không tồn tại!")
            return

        # --- GIAI ĐOẠN 1: KIỂM TRA VÀ TẠO PHỤ ĐỀ (QUÉT) ---
        if self.subtitle_table.rowCount() == 0:
            print("--- Bắt đầu Giai đoạn 1: Quét dữ liệu âm thanh ---")
            
            # Trường hợp là THƯ MỤC
            if os.path.isdir(input_path):
                video_extensions = ('.mp4', '.mkv', '.avi', '.mov')
                video_files = [os.path.join(input_path, f) for f in os.listdir(input_path) 
                               if f.lower().endswith(video_extensions)]
                
                if not video_files:
                    print("Không tìm thấy file video nào trong thư mục!")
                    return
                
                print(f"Phát hiện Folder: Đang quét video đầu tiên trong danh sách {len(video_files)} file...")
                # Đối với Folder, bước quét ban đầu sẽ lấy file đầu tiên để người dùng xem mẫu trên bảng
                self.process_scanning_flow(video_files[0])
            
            # Trường hợp là FILE đơn lẻ
            else:
                self.process_scanning_flow(input_path)
            
            print("--- Đã quét xong! Vui lòng duyệt nội dung trên bảng trước khi nhấn 'XUẤT VIDEO' lần nữa. ---")
            return # Dừng lại để người dùng sửa bảng

        # --- GIAI ĐOẠN 2: RENDER VIDEO (KHI BẢNG ĐÃ CÓ DỮ LIỆU) ---
        print("--- Bắt đầu Giai đoạn 2: Render video thành phẩm ---")
        
        # Thu thập cấu hình Style từ giao diện
        style_config = {
            "font_size": self.font_size_spin.value(),
            "font_color": self.current_color.name() if hasattr(self, 'current_color') else "yellow",
            "font_path": self.font_combo.currentFont().family(),
            "position": self.pos_combo.currentText(),
            "box_type": self.box_combo.currentText(),
            "box_opacity": self.opacity_slider.value() if hasattr(self, 'opacity_slider') else 128,
            "sub_size_ratio": self.sub_size_slider.value(),
            "is_bilingual": self.check_bilingual.isChecked(),
            "target_lang": self.lang2_combo.currentText()
        }

        if os.path.isdir(input_path):
            # Xử lý hàng loạt cho cả Folder
            video_files = [os.path.join(input_path, f) for f in os.listdir(input_path) 
                           if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]
            
            for v_path in video_files:
                filename = os.path.basename(v_path)
                # Tự động tạo tên file output: subbed_tenvideo.mp4
                current_output = os.path.join(output_base, f"subbed_{filename}")
                print(f"\n>>> Đang Render: {filename}")
                self.run_final_render_flow(v_path, current_output, style_config)
            
            print("\n--- CHÚC MỪNG: ĐÃ XỬ LÝ XONG TOÀN BỘ FOLDER! ---")
        else:
            # Xử lý cho 1 file đơn lẻ
            self.run_final_render_flow(input_path, output_base, style_config)

    def process_single_video_logic(self, video_path, output_path):
        """Hàm chứa toàn bộ logic xử lý từ Quét đến Render cho 1 video"""
        try:
            source_lang = self.lang1_combo.currentText()
            target_lang = self.lang2_combo.currentText()
            is_bilingual = self.check_bilingual.isChecked()

            # 1. Khởi tạo Module 1 và Quét (Nếu bảng trống hoặc đang chạy folder)
            from core.module_1_audio import TranscriptionModule
            transcriber = TranscriptionModule()
            
            # Lấy dữ liệu trực tiếp từ Module 1 (trả về 3 giá trị như bạn đã sửa)
            srt_file, lang, srt_list = transcriber.transcribe(video_path, selected_lang=source_lang)
            
            # Hiển thị lên bảng (để người dùng theo dõi tiến trình)
            self.display_srt_to_table(srt_list)

            # 2. Cấu hình Style
            style_config = {
                "font_size": self.font_size_spin.value(),
                "font_color": self.current_color.name() if hasattr(self, 'current_color') else "yellow",
                "font_path": self.font_combo.currentFont().family(),
                "position": self.pos_combo.currentText(),
                "box_type": self.box_combo.currentText(),
                "sub_size_ratio": self.sub_size_slider.value(),
                "is_bilingual": is_bilingual,
                "effect_duration": self.effect_dur_slider.value() / 10,
                "target_lang": target_lang
            }

            # 3. Chạy Module 2 (Render)
            self.run_automation_process(video_path, source_lang, target_lang, is_bilingual, style_config, output_path)
            
        except Exception as e:
            print(f"Lỗi khi xử lý file {video_path}: {str(e)}")
    
    def process_scanning_flow(self, video_path):
        """Hỗ trợ quét video và đổ dữ liệu lên bảng"""
        try:
            from core.module_1_audio import TranscriptionModule
            transcriber = TranscriptionModule()
            source_lang = self.lang1_combo.currentText()
            
            # Nhận 3 tham số từ Module 1 bạn đã nâng cấp
            srt_path, lang, srt_list = transcriber.transcribe(video_path, selected_lang=source_lang)
            self.display_srt_to_table(srt_list)
        except Exception as e:
            print(f"Lỗi khi quét video: {e}")

    def run_final_render_flow(self, video_path, output_path, style_config):
        """Hỗ trợ gọi Module 2 để render"""
        try:
            source_lang = self.lang1_combo.currentText()
            target_lang = self.lang2_combo.currentText()
            is_bilingual = self.check_bilingual.isChecked()
            
            self.run_automation_process(
                video_path, source_lang, target_lang, 
                is_bilingual, style_config, output_path
            )
        except Exception as e:
            print(f"Lỗi khi render {video_path}: {e}")
            
    def run_automation_process(self, video_path, src_lang, tar_lang, is_bi, style, output, srt2_manual):
        try:
            # BƯỚC 1: Lấy dữ liệu từ bảng Duyệt phụ đề (Đã được duyệt/sửa)
            srt_data1 = self.get_srt_from_table()
            
            if not srt_data1:
                # Nếu bảng trống, chạy Module 1 để tạo SRT mới
                from core.module_1_audio import TranscriptionModule
                transcriber = TranscriptionModule()
                srt_data1, detected_lang = transcriber.transcribe(video_path, selected_lang=src_lang)
                self.display_srt_to_table(srt_data1) # Đổ lên bảng để xem trước
                return # Dừng lại để người dùng duyệt chữ

            # BƯỚC 2: Xử lý song ngữ tự động
            srt_data2 = None
            from core.module_2_render import RenderingModule
            renderer = RenderingModule()

            if is_bi:
                if srt2_manual:
                    srt_data2 = self.parse_srt_file(srt2_manual)
                else:
                    # Tự động dịch dựa trên nội dung đã duyệt trên bảng
                    srt_data2 = renderer.auto_translate_srt(srt_data1, tar_lang)

            # BƯỚC 3: Render thành phẩm
            renderer.render_video(video_path, srt_data1, style, output, srt_data2=srt_data2)
            
        except Exception as e:
            print(f"Lỗi hệ thống: {str(e)}")
    
    def parse_srt_file(self, file_path):
        """Đọc file .srt và chuyển thành danh sách để Module 2 hiểu được"""
        import re
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex đơn giản để tách mốc thời gian và văn bản
        pattern = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\n$|$)', re.DOTALL)
        matches = pattern.findall(content)
        
        return [{'start': m[0], 'end': m[1], 'text': m[2].replace('\n', ' ')} for m in matches]     
    
    def toggle_bilingual_options(self, checked):
        """Ẩn hoặc hiện tùy chọn ngôn ngữ 2 dựa trên ô tick"""
        self.bilingual_container.setVisible(checked)

    def update_percent_label(self, value):
        """Cập nhật văn bản hiển thị phần trăm khi kéo slider"""
        self.label_percent.setText(f"Tỷ lệ size ngôn ngữ phụ: {value}%")   
        
    def display_srt_to_table(self, srt_data):
        """Đưa dữ liệu từ Module 1 lên bảng để duyệt"""
        self.subtitle_table.setRowCount(len(srt_data))
        for i, item in enumerate(srt_data):
            self.subtitle_table.setItem(i, 0, QTableWidgetItem(item.get('start', '')))
            self.subtitle_table.setItem(i, 1, QTableWidgetItem(item.get('end', '')))
            self.subtitle_table.setItem(i, 2, QTableWidgetItem(item.get('text', '')))

    def get_srt_from_table(self):
        """Lấy dữ liệu đã sửa từ bảng để đưa vào render"""
        updated_srt = []
        for i in range(self.subtitle_table.rowCount()):
            updated_srt.append({
                'start': self.subtitle_table.item(i, 0).text(),
                'end': self.subtitle_table.item(i, 1).text(),
                'text': self.subtitle_table.item(i, 2).text()
            })
        return updated_srt    
    
    def update_video_preview(self, video_path):
        """Trích xuất ảnh từ video để hiện lên màn hình phát"""
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            qt_img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.video_preview.setPixmap(pixmap.scaled(self.video_preview.size(), 
                                         Qt.AspectRatioMode.KeepAspectRatio))
        cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())