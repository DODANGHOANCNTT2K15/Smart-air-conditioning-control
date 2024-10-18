# def voice_control():
    # Khởi tạo Recognizer
    # recognizer = sr.Recognizer()

    # # Sử dụng microphone làm nguồn âm thanh
    # with sr.Microphone() as source:
    #     print("Vui lòng nói gì đó...")
    #     speak_vietnamese("Vui lòng nói gì đó...")

    #     # Điều chỉnh tiếng ồn xung quanh để tối ưu kết quả nhận diện
    #     recognizer.adjust_for_ambient_noise(source, duration=1)

    #     # Nghe âm thanh từ microphone
    #     audio = recognizer.listen(source)

    #     try:
    #         # Nhận diện giọng nói và chuyển đổi thành văn bản (Ngôn ngữ: tiếng Việt)
    #         text = recognizer.recognize_google(audio, language="vi-VN")
    #         print("Bạn vừa nói: " + text)
    #         speak_vietnamese(f"Bạn vừa nói: {text}")

    #         # Kiểm tra xem người dùng có nói "tăng nhiệt độ" không
    #         if "tăng nhiệt độ" in text.lower():
    #             config.temperature += 1
    #             response = f"Nhiệt độ đã được tăng lên: {config.temperature}"
    #             print(response)
    #             speak_vietnamese(response)
    #         elif "giảm nhiệt độ" in text.lower():
    #             config.temperature -= 1
    #             response = f"Nhiệt độ đã được giảm xuống: {config.temperature}"
    #             print(response)
    #             speak_vietnamese(response)
    #         else:
    #             # Sử dụng regex để tìm số (ví dụ: "25 độ")
    #             match = re.search(r"(\d+)\s*độ", text)
    #             time.sleep(0.4)
    #             if match:
    #                 new_temp = int(match.group(1))
    #                 config.temperature = new_temp
    #                 response = f"Nhiệt độ đã được đặt thành: {config.temperature}"
    #                 print(response)
    #                 speak_vietnamese(response)
    #             else:
    #                 print("Không có lệnh thay đổi nhiệt độ.")
    #                 speak_vietnamese("Không có lệnh thay đổi nhiệt độ.")

    #     except sr.UnknownValueError:
    #         print("Xin lỗi, tôi không thể nhận diện được giọng nói.")
    #         speak_vietnamese("Xin lỗi, tôi không thể nhận diện được giọng nói.")
    #     except sr.RequestError as e:
    #         print(f"Yêu cầu không thành công; {e}")
    #         speak_vietnamese(f"Yêu cầu không thành công; {e}")


import speech_recognition as sr
import re
import time
import config
import os
from gtts import gTTS

def voice_control():
    # Khởi tạo Recognizer
    recognizer = sr.Recognizer()

    # Sử dụng microphone làm nguồn âm thanh
    with sr.Microphone() as source:
        print("Vui lòng nói gì đó...")

        # Điều chỉnh tiếng ồn xung quanh để tối ưu kết quả nhận diện
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Nghe âm thanh từ microphone
        audio = recognizer.listen(source)

        try:
            # Nhận diện giọng nói và chuyển đổi thành văn bản (Ngôn ngữ: tiếng Việt)
            text = recognizer.recognize_google(audio, language="vi-VN")
            print("Bạn vừa nói: " + text)

            # Kiểm tra xem người dùng có nói "tăng nhiệt độ" không
            if "tăng nhiệt độ" in text.lower():
                config.temperature += 1
                print(f"Nhiệt độ đã được tăng lên: {config.temperature}")
            elif "giảm nhiệt độ" in text.lower():
                config.temperature -= 1
                print(f"Nhiệt độ đã được giảm xuống: {config.temperature}")
            else:
                # Sử dụng regex để tìm số (ví dụ: "25 độ")
                match = re.search(r"(\d+)\s*độ", text)
                time.sleep(0.4)
                if match:
                    new_temp = int(match.group(1))
                    config.temperature = new_temp
                    print(f"Nhiệt độ đã được đặt thành: {config.temperature}")
                else:
                    print("Không có lệnh thay đổi nhiệt độ.")

        except sr.UnknownValueError:
            print("Xin lỗi, tôi không thể nhận diện được giọng nói.")
        except sr.RequestError as e:
            print(f"Yêu cầu không thành công; {e}")


def speak_vietnamese(text):
    tts = gTTS(text=text, lang='vi')
    
    tts.save("temp_audio.mp3")
    
    if os.name == 'posix': 
        os.system("mpg321 temp_audio.mp3")  
    else:  
        os.system("start temp_audio.mp3")