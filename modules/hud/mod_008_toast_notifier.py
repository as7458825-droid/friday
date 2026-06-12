import tkinter as tk


def show_toast(title: str, message: str, duration_ms: int = 3000):
    try:
        from plyer import notification

        notification.notify(title=title, message=message, timeout=duration_ms // 1000)
    except ImportError:
        root = tk.Tk()
        root.title(title)
        root.attributes("-topmost", True)
        root.geometry(
            f"+{root.winfo_screenwidth() - 320}+{root.winfo_screenheight() - 120}"
        )
        lbl = tk.Label(root, text=message, wraplength=280, padx=20, pady=20)
        lbl.pack()
        root.after(duration_ms, root.destroy)
        root.mainloop()
