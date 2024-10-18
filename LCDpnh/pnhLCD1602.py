# GPIOEmulator/LCD1602.py
import pygame
import threading
import time

class LCD1602:
    def __init__(self, width=250, height=60, address=0x27):
        # Khởi tạo Pygame
        pygame.init()
        self.width = width
        self.height = height
        self.address = address
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LCD1602")
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.lines = ["", ""]  # 2 dòng
        self.backlight = True
        self.cursor_visible = False
        self.cursor_position = (0, 0)
        self.running = True  # Biến điều khiển vòng lặp

        self.clear()

    def clear(self):
        self.lines = ["", ""]
        self.display()

    def write_string(self, text):
        # Ghi chuỗi vào dòng đầu tiên nếu còn trống, còn không thì vào dòng thứ hai.
        if self.lines[0] == "":
            self.lines[0] = text[:16]  # Chỉ ghi tối đa 16 ký tự
        elif self.lines[1] == "":
            self.lines[1] = text[:16]  # Ghi vào dòng thứ hai nếu dòng đầu đã có nội dung
        self.display()

    def write_char(self, char):
        row, col = self.cursor_position
        if col < 16:
            self.lines[row] = self.lines[row][:col] + char + self.lines[row][col + 1:]
            self.cursor_position = (row, col + 1)
            self.display()

    def set_cursor(self, row, col):
        if row < 2 and col < 16:
            self.cursor_position = (row, col)

    def cursor_on(self):
        self.cursor_visible = True
        self.display()

    def cursor_off(self):
        self.cursor_visible = False
        self.display()

    def backlight_on(self):
        self.backlight = True
        self.display()

    def backlight_off(self):
        self.backlight = False
        self.display()

    def home(self):
        self.cursor_position = (0, 0)
        self.display()

    def display(self):
        self.screen.fill((0, 0, 0))  # Màu nền đen
        for i in range(2):
            text = self.lines[i]
            rendered_text = self.font.render(text, True, (0, 255, 0) if self.backlight else (50, 50, 50))
            # Đặt vị trí hiển thị cho dòng đầu tiên và dòng thứ hai
            if i == 0:
                self.screen.blit(rendered_text, (10, 2))  # Dòng đầu tiên sát với thanh tiêu đề
            else:
                self.screen.blit(rendered_text, (10, 30))  # Dòng thứ hai sát với dòng đầu

        if self.cursor_visible:
            cursor_x = 10 + self.cursor_position[1] * 15
            cursor_y = 2 if self.cursor_position[0] == 0 else 30
            pygame.draw.line(self.screen, (255, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 24), 2)

        pygame.display.flip()

    def run(self):
        while self.running:
            # Luôn luôn xử lý sự kiện Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return
            # Bạn có thể cập nhật hiển thị theo thời gian hoặc điều kiện ở đây
            self.display()
            time.sleep(0.1)  # Giảm tải CPU


    def close(self):
        self.running = False
        pygame.quit()
