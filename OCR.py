import pyautogui
import pytesseract
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import tkinter as tk
from PIL import Image
import keyboard

class ScreenCaptureTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.root = tk.Tk()
        self.canvas = None
        self.rect = None
        
    def start_capture(self):
        # 設置全螢幕透明視窗
        self.root.attributes('-fullscreen', True, '-alpha', 0.3)
        self.root.configure(background='grey')
        
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 綁定滑鼠事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.root.mainloop()
        
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.current_x = event.x
        self.current_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y,
                                               self.current_x, self.current_y,
                                               outline='red')
        
    def on_release(self, event):
        # 獲取選擇區域的座標
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        # 截圖
        screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
        
        # 關閉視窗
        self.root.destroy()
        
        # 分析圖片
        self.analyze_image(screenshot)
        
    def analyze_image(self, image):
        # 轉換圖片格式
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # 嘗試 QR code 解析
        qr_results = decode(cv_image)
        if qr_results:
            print("檢測到 QR Code:")
            for qr in qr_results:
                print(qr.data.decode('utf-8'))
            return
            
        # 如果不是 QR code，嘗試 OCR
        text = pytesseract.image_to_string(image, lang='chi_tra+eng')
        if text.strip():
            print("檢測到文字:")
            print(text)
        else:
            print("未能識別任何文字或 QR Code")

def main():
    print("按下 'ctrl+alt+s' 開始截圖")
    keyboard.wait('ctrl+alt+s')
    tool = ScreenCaptureTool()
    tool.start_capture()

if __name__ == "__main__":
    main()
