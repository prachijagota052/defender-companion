import flet as ft
import threading
import time
from packages.core.db import get_latest_user_alert

def main(page: ft.Page):
    page.window_width = 800
    page.window_height = 500
    page.title = "Defender Companion"
    page.window_always_on_top = True
    page.bgcolor = "#FFFFFF"

    # UI Components
    status_title = ft.Text("System Secure", size=26, weight="bold", color="blue")
    why_text = ft.Text("", size=16)
    explain_box = ft.Text("", size=14, italic=True, color="grey700")
    steps_list = ft.Column()

    def update_ui(alert):
        if alert:
            status_title.value = alert.title
            status_title.color = "red"
            why_text.value = f"Reason: {alert.why_blocked}"
            explain_box.value = alert.explanation
            steps_list.controls = [ft.Text(f"• {s}") for s in alert.recommended_steps]
            page.update()

    # --- THE ICON FIX IS HERE ---
    page.add(
        ft.Container(
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text("🛡️ SECURITY ALERT", weight="bold"),
                    # Use icons.CLOSE_ROUNDED or icons.CLOSE
                    ft.IconButton(
                        icon=ft.icons.CLOSE, 
                        on_click=lambda _: page.window_close()
                    )
                ], alignment="spaceBetween"),
                status_title,
                why_text,
                ft.Container(explain_box, padding=10, bgcolor="#f5f5f5", border_radius=10),
                steps_list
            ])
        )
    )

    def monitor():
        last_id = None
        while True:
            try:
                alert = get_latest_user_alert()
                if alert and alert.id != last_id:
                    last_id = alert.id
                    update_ui(alert)
            except Exception as e:
                print(f"UI Monitor Error: {e}")
            time.sleep(1)

    threading.Thread(target=monitor, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)