import flet as ft
import threading
import time
from ..audio_i18n.i18n import t

# State management
is_talking = False 
current_lang = "en"

def main(page: ft.Page):
    global is_talking, current_lang
    
    page.window_width = 900
    page.window_height = 500
    page.bgcolor = "white"
    page.title = "Defender Companion - Enterprise Security"

    # Asset Logic (Handling interchanged images)
    neutral_img = "assets/avatar_talk.png"    
    talking_img = "assets/avatar_neutral.png" 

    # --- UI COMPONENTS ---
    avatar = ft.Image(src=neutral_img, width=200, height=200)
    
    # Text Elements (Linked to JSON keys: title_default, why_default, explain_default, steps_prefix)
    status_header = ft.Text(t("title_default", lang=current_lang), size=28, weight="bold", color="blue")
    why_box = ft.Text("System scanning...", size=15)
    explain_box = ft.Text("", size=14, italic=True, color="grey700")
    steps_label = ft.Text("", size=13, weight="bold", color="red")
    measures_list = ft.Text("", size=13)

    # --- THE LANGUAGE & UPDATE LOGIC ---
    def update_ui_text():
        """Helper to refresh all localized strings"""
        status_header.value = t("title_default", lang=current_lang)
        why_box.value = t("why_default", lang=current_lang)
        explain_box.value = t("explain_default", lang=current_lang)
        steps_label.value = t("steps_prefix", lang=current_lang)
        measures_list.value = "• Isolate Device\n• Run Full Malware Scan"
        page.update()

    def lang_changed(e):
        global current_lang
        current_lang = lang_dropdown.value
        update_ui_text()

    # Dropdown Fix: Create first, then assign on_change to avoid version crashes
    lang_dropdown = ft.Dropdown(
        width=150,
        label="Language",
        options=[
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("hi", "Hindi"),
            ft.dropdown.Option("mr", "Marathi"),
        ]
    )
    lang_dropdown.on_change = lang_changed 
    lang_dropdown.value = "en"

    # --- VOICE & LIP SYNC ENGINE ---
    def lip_sync():
        while True:
            if is_talking:
                avatar.src = talking_img if avatar.src == neutral_img else neutral_img
                avatar.update()
                time.sleep(0.18)
            else:
                if avatar.src != neutral_img:
                    avatar.src = neutral_img
                    avatar.update()
                time.sleep(0.5)

    def simulate_threat():
        """Measures to take when a threat is found"""
        global is_talking
        time.sleep(3) # Wait 3 seconds after startup
        
        # 1. Update UI to Threat State using localized JSON data
        status_header.color = "red"
        update_ui_text()
        
        # 2. Trigger Lip Sync (Connect your voice engine 'say()' here)
        is_talking = True
        time.sleep(7) # Duration of the voice alert
        is_talking = False
        page.update()

    # Start Threads
    threading.Thread(target=lip_sync, daemon=True).start()
    threading.Thread(target=simulate_threat, daemon=True).start()

    # --- FINAL LAYOUT ---
    page.add(
        ft.Container(
            padding=30,
            content=ft.Column([
                ft.Row([
                    lang_dropdown, 
                    # Fixed IconButton: using explicit icon name string
                    ft.IconButton(icon="close", on_click=lambda _: page.window_close())
                ], alignment="spaceBetween"),
                ft.Row([
                    avatar,
                    ft.Column([
                        status_header,
                        ft.Container(
                            content=ft.Column([
                                why_box, 
                                explain_box, 
                                ft.Divider(color="grey300"), 
                                steps_label,
                                measures_list
                            ], spacing=10),
                            padding=20, bgcolor="#f8f9fa", border_radius=15, border=ft.border.all(1, "#dee2e6")
                        )
                    ], expand=True, spacing=20)
                ], alignment="start", vertical_alignment="top")
            ])
        )
    )

if __name__ == "__main__":
    ft.app(target=main)