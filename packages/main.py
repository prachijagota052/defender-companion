import flet as ft
import threading
import time
from ..core.db import fetch_unspoken_user_alerts, mark_user_alert_spoken

# Mouth movement toggle
is_talking = False 

def main(page: ft.Page):
    global is_talking
    
    # --- UI SETTINGS ---
    page.window_width = 400
    page.window_height = 250
    page.window_frameless = True
    page.window_always_on_top = True
    page.bgcolor = ft.colors.TRANSPARENT

    # --- UI ELEMENTS ---
    # Assets are pulled from the root assets folder
    avatar = ft.Image(src="assets/avatar_neutral.png", width=150, height=150)
    status_msg = ft.Text("Guardian Active", color="blue", weight="bold")

    # --- ANIMATION THREAD ---
    def lip_sync():
        while True:
            if is_talking:
                avatar.src = "assets/avatar_talk.png" if avatar.src == "assets/avatar_neutral.png" else "assets/avatar_neutral.png"
                avatar.update()
                time.sleep(0.15)
            else:
                avatar.src = "assets/avatar_neutral.png"
                avatar.update()
                time.sleep(0.5)

    # --- DATABASE MONITOR THREAD ---
    def monitor_db():
        global is_talking
        while True:
            alerts = fetch_unspoken_user_alerts(limit=1)
            if alerts:
                status_msg.value = f"🚨 {alerts[0].title}"
                status_msg.color = "red"
                page.update()

                is_talking = True
                time.sleep(5) # Matches the average length of a Hindi alert
                is_talking = False

                mark_user_alert_spoken(alerts[0].id)
                status_msg.value = "Guardian Active"
                status_msg.color = "blue"
                page.update()
            time.sleep(2)

    # Start threads
    threading.Thread(target=lip_sync, daemon=True).start()
    threading.Thread(target=monitor_db, daemon=True).start()

    # --- LAYOUT ---
    page.add(
        ft.Container(
            content=ft.Column([
                avatar, 
                status_msg,
                ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda _: page.window_close())
            ], horizontal_alignment="center"),
            padding=20, bgcolor="white", border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color="black26")
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
