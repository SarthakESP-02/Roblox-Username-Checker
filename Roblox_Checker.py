import requests
import re
import tkinter as tk
import time
import threading

class RayfieldInspiredChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sniper Hub")
        self.root.geometry("800x600")
        self.root.configure(bg="#14181D")

        # Left Sidebar (Rayfield tabs)
        self.sidebar = tk.Frame(self.root, bg="#0F1216", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Sniper Hub", font=("Helvetica", 16, "bold"), fg="#7289DA", bg="#0F1216").pack(pady=30)

        self.tabs = {}
        tab_names = ["Home", "Username Checker", "Settings"]
        for name in tab_names:
            btn = tk.Button(self.sidebar, text=name, font=("Helvetica", 12), fg="white", bg="#0F1216", relief="flat", anchor="w", padx=30, command=lambda n=name: self.switch_tab(n))
            btn.pack(fill="x", pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1E2228"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#0F1216"))
            self.tabs[name] = btn

        # Main content frame
        self.content = tk.Frame(self.root, bg="#14181D")
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Create frames for each tab
        self.frames = {}
        for name in tab_names:
            frame = tk.Frame(self.content, bg="#14181D")
            self.frames[name] = frame

        # Home Tab
        home = self.frames["Home"]
        tk.Label(home, text="Welcome to Sniper Hub", font=("Helvetica", 28, "bold"), fg="#7289DA", bg="#14181D").pack(pady=100)
        tk.Label(home, text="Select a tab on the left", font=("Helvetica", 14), fg="#99AAB5", bg="#14181D").pack()

        # Username Checker Tab
        checker = self.frames["Username Checker"]
        tk.Label(checker, text="Roblox Username Sniper", font=("Helvetica", 24, "bold"), fg="#7289DA", bg="#14181D").pack(pady=40)

        self.entry = tk.Entry(checker, width=40, font=("Helvetica", 14), justify="center", bg="#23272A", fg="white", insertbackground="white")
        self.entry.pack(pady=20, ipady=12)
        self.entry.insert(0, "Enter username...")

        self.check_button = tk.Button(checker, text="SNIPE", font=("Helvetica", 16, "bold"), fg="white", bg="#7289DA", relief="flat", command=self.start_check)
        self.check_button.pack(pady=30, ipadx=40, ipady=15)
        self.check_button.bind("<Enter>", lambda e: self.check_button.config(bg="#5B6EB8"))
        self.check_button.bind("<Leave>", lambda e: self.check_button.config(bg="#7289DA"))

        self.spinner = tk.Label(checker, text="", font=("Helvetica", 24), fg="#7289DA", bg="#14181D")
        self.spinner.pack(pady=20)

        self.result = tk.Label(checker, text="", font=("Helvetica", 16), fg="white", bg="#14181D", wraplength=500)
        self.result.pack(pady=40)

        # Settings Tab (placeholder)
        settings = self.frames["Settings"]
        tk.Label(settings, text="Settings (Coming Soon)", font=("Helvetica", 20), fg="#7289DA", bg="#14181D").pack(pady=100)

        # Start on Username Checker tab
        self.switch_tab("Username Checker")

    def switch_tab(self, tab_name):
        # Highlight selected tab
        for name, btn in self.tabs.items():
            if name == tab_name:
                btn.config(bg="#7289DA", fg="white")
            else:
                btn.config(bg="#0F1216", fg="white")
        
        # Show selected frame
        for name, frame in self.frames.items():
            if name == tab_name:
                frame.pack(expand=True, fill="both")
            else:
                frame.pack_forget()

    def animate_loading(self):
        dots = ["   ", ".  ", ".. ", "..."]
        for i in range(25):
            if not self.checking:
                break
            self.spinner.config(text="Sniping" + dots[i % 4])
            time.sleep(0.3)
            self.root.update()

    def check_username(self, username):
        if not username.isalnum() or len(username) < 3 or len(username) > 20:
            return "Invalid username"

        url = f"https://www.roblox.com/users/profile?username={username}"
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            if response.status_code == 404 or (response.status_code == 200 and "/users/" not in response.url):
                return f"'{username}' is AVAILABLE!\nClaim it NOW!"
            elif response.status_code == 200 and re.search(r"/users/\d+/profile", response.url):
                user_id = re.search(r"/users/(\d+)/profile", response.url).group(1)
                return f"'{username}' is TAKEN\nUser ID: {user_id}"
            else:
                return "Unknown — try again"
        except:
            return "Network error"

    def start_check(self):
        username = self.entry.get().strip()
        if not username or "..." in username:
            self.result.config(text="Enter a username", fg="#FF5555")
            return

        self.checking = True
        self.result.config(text="")
        threading.Thread(target=self.animate_loading, daemon=True).start()
        threading.Thread(target=self.perform_check, args=(username,), daemon=True).start()

    def perform_check(self, username):
        result = self.check_username(username)
        time.sleep(1)
        self.checking = False
        self.spinner.config(text="")
        self.result.config(text=result, fg="#50FA7B" if "AVAILABLE" in result else "#FF5555")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RayfieldInspiredChecker()
    app.run()