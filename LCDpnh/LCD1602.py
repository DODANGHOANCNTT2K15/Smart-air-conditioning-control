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
        pygame.display.set_caption("LCD1602 Emulator")
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.lines = [" " * 16, " " * 16]  # 2 dòng, mỗi dòng 16 ký tự
        self.backlight = True
        self.cursor_visible = False
        self.cursor_position = (0, 0)
        self.running = True  # Biến điều khiển vòng lặp

        self.display()

    def clear(self):
        self.lines = [" " * 16, " " * 16]
        self.display()

    def write_string(self, text, line=0):
        if line not in [0, 1]:
            raise ValueError("LCD1602 chỉ hỗ trợ 2 dòng.")
        # Cắt chuỗi thành tối đa 16 ký tự và căn chỉnh trái
        self.lines[line] = text.ljust(16)[:16]
        self.display()

    def write_char(self, char):
        row, col = self.cursor_position
        if col < 16 and row < 2:
            line = self.lines[row]
            self.lines[row] = line[:col] + char + line[col + 1:]
            self.cursor_position = (row, col + 1)
            self.display()

    def set_cursor(self, row, col):
        if row < 2 and col < 16:
            self.cursor_position = (row, col)
            self.display()

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
        for i, line in enumerate(self.lines):
            rendered_text = self.font.render(line, True, (0, 255, 0) if self.backlight else (50, 50, 50))
            # Đặt vị trí hiển thị cho dòng đầu tiên và dòng thứ hai
            y_position = 2 if i == 0 else 30
            self.screen.blit(rendered_text, (10, y_position))

        if self.cursor_visible:
            cursor_x = 10 + self.cursor_position[1] * 15
            cursor_y = 2 if self.cursor_position[0] == 0 else 30
            pygame.draw.line(self.screen, (255, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 24), 2)

        pygame.display.flip()

    def run(self):
        # Vòng lặp sự kiện Pygame
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return
            self.display_content()
            time.sleep(0.1)  # Giảm tải CPU

    def close(self):
        self.running = False
        # Thêm một sự kiện Pygame QUIT để đảm bảo vòng lặp sẽ nhận và thoát
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        pygame.quit()

