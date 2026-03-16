import customtkinter as ctk
from database.db import initialize_db

def main():
    #DB初期化（テーブル作成・初期データ投入）
    initialize_db()

    #ウィンドウ設定
    ctk.set_appearance_mode("system") #OS設定に合わせる
    ctk.set_default_color_theme("blue")

    #メインウィンドウ作成
    app = ctk.CTk()
    app.title("Job Tracker")
    app.geometry("1200x700")

    # 仮のラベル（後で消す）
    label = ctk.CTkLabel(app, text="Job Tracker 起動確認", font=ctk.CTkFont(size=20))
    label.pack(expand=True)

    app.mainloop()

if __name__ == "__main__":
    main()