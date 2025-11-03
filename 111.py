import tkinter as tk
import random

# 配置
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 60
TOTAL_NOTES = 300       # 总共创建多少个便签
MAX_CONCURRENT =  300   # 同时最多存在多少个便签
NOTE_LIFETIME_MS = 9000 # 每个便签存活时间（毫秒）
CREATE_INTERVAL_MS = 100  # 创建间隔（毫秒）

TIPS = [
    '好好吃饭', '注意休息', '开开心心', '身体倍棒', '多吃水果',
    '早睡早起', '少玩手机', '多喝水', '注意防晒', '有心事吗',
    '顺顺利利', '心想事成', '万事如意', '身体健康', '工作顺利', '学业有成'
]

BACKGROUND_COLORS = [
    '#FFCCCC', '#CCFFCC', '#CCCCFF', '#FFFFCC', '#CCFFFF', '#B91CB9'
]

def rand_pos(root):
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = random.randint(0, max(0, screen_w - WINDOW_WIDTH))
    y = random.randint(0, max(0, screen_h - WINDOW_HEIGHT))
    return x, y

def create_note(root):
    tip = random.choice(TIPS)
    bg = random.choice(BACKGROUND_COLORS)

    top = tk.Toplevel(root)
    top.overrideredirect(False)     # True 可去掉标题栏，这里保留便于手动关闭
    top.attributes('-topmost', True)

    x, y = rand_pos(root)
    top.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    lbl = tk.Label(
        top, text=tip, bg=bg,
        font=('微软雅黑', 16), width=30, height=3
    )
    lbl.pack(fill='both', expand=True)

    # 自动销毁
    top.after(NOTE_LIFETIME_MS, top.destroy)
    return top

def main():
    root = tk.Tk()
    root.title("worm tip (single-threaded)")
    root.geometry("0x0+0+0")  # 可以把主窗口缩到极小/移到角落

    active = {"count": 0, "created": 0}

    def schedule_create():
        # 控制最大并发与总数量
        if active["created"] >= TOTAL_NOTES:
            return
        if active["count"] < MAX_CONCURRENT:
            win = create_note(root)
            active["count"] += 1
            active["created"] += 1
            # 当窗口销毁时，计数-1
            win.bind("<Destroy>", lambda e: active.__setitem__("count", max(0, active["count"] - 1)))
        root.after(CREATE_INTERVAL_MS, schedule_create)

    root.after(0, schedule_create)

    # 提供一个快捷键一次性关闭所有子窗口
    def close_all(event=None):
        for w in root.winfo_children():
            if isinstance(w, tk.Toplevel):
                w.destroy()

    root.bind("<Escape>", close_all)
    root.mainloop()

if __name__ == "__main__":
    main()

import cv2
print(cv2.__version__)

