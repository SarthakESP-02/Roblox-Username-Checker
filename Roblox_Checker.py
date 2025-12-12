import requests
import re
import tkinter as tk
from tkinter import ttk
import time
import threading

class RobloxUsernameChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Roblox Username Checker")
        self.root.geometry("500x600")
        self.root.configure(bg="#0F1923")
        self.root.resizable(False, False)

        # Title
        title = tk.Label(self.root, text="Roblox Username Checker", font=("Helvetica", 24, "bold"), fg="#00D4FF", bg="#0F1923")
        title.pack(pady=40)

        # Subtitle
        subtitle = tk.Label(self.root, text="Check if your dream username is available", font=("Helvetica", 12), fg="#99AAB5", bg="#0F1923")
        subtitle.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#0F1923")
        input_frame.pack(pady=30)

        self.entry = tk.Entry(input_frame, width=40, font=("Helvetica", 14), justify="center", relief="flat", bg="#1E2A38", fg="white", insertbackground="white")
        self.entry.pack(pady=10, ipady=12)
        self.entry.insert(0, "Enter username...")
        self.entry.bind("<FocusIn>", lambda e: self.entry.delete(0, tk.END) if self.entry.get() == "Enter username..." else None)

        # Button with hover animation
        self.check_button = tk.Button(input_frame, text="Check Availability", font=("Helvetica", 14, "bold"), fg="white", bg="#00D4FF", relief="flat", cursor="hand2", command=self.start_check)
        self.check_button.pack(pady=20, ipadx=20, ipady=10)
        self.check_button.bind("<Enter>", lambda e: self.check_button.config(bg="#00B0D4"))
        self.check_button.bind("<Leave>", lambda e: self.check_button.config(bg="#00D4FF"))

        # Loading spinner
        self.spinner = ttk.Label(self.root, text="", font=("Helvetica", 20), fg="#00D4FF", bg="#0F1923")
        self.spinner.pack(pady=20)

        # Result area
        self.result = tk.Label(self.root, text="", font=("Helvetica", 14), fg="white", bg="#0F1923", wraplength=450, justify="center")
        self.result.pack(pady=30, expand=True)

        # Footer
        footer = tk.Label(self.root, text="Made with ❤️ using Python", font=("Helvetica", 10), fg="#555", bg="#0F1923")
        footer.pack(side="bottom", pady=20)

    def animate_loading(self):
        dots = ["   ", ".  ", ".. ", "..."]
        for i in range(20):
            if not self.checking:
                break
            self.spinner.config(text="Checking" + dots[i % 4])
            time.sleep(0.3)
            self.root.update()

    def check_username(self, username):
        if not username.isalnum() or len(username) < 3 or len(username) > 20:
            return "❌ Invalid username (3-20 letters/numbers only)"

        url = f"https://www.roblox.com/users/profile?username={username}"
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            if response.status_code == 404 or (response.status_code == 200 and "/users/" not in response.url):
                return f"✅ '{username}' is AVAILABLE!\nGo claim it now!"
            elif response.status_code == 200 and re.search(r"/users/\d+/profile", response.url):
                user_id = re.search(r"/users/(\d+)/profile", response.url).group(1)
                return f"❌ '{username}' is TAKEN\nUser ID: {user_id}"
            else:
                return "⚠️ Unknown response — try again"
        except:
            return "⚠️ Network error — check internet"

    def start_check(self):
        username = self.entry.get().strip()
        if not username or username == "Enter username...":
            self.result.config(text="Please enter a username", fg="#FF6B6B")
            return

        self.checking = True
        self.result.config(text="")
        threading.Thread(target=self.animate_loading, daemon=True).start()
        threading.Thread(target=self.perform_check, args=(username,), daemon=True).start()

    def perform_check(self, username):
        result = self.check_username(username)
        time.sleep(1)  # Let animation finish
        self.checking = False
        self.spinner.config(text="")
        self.result.config(text=result, fg="#00FF00" if "AVAILABLE" in result else "#FF6B6B")

    def run(self):
        self.root.mainloop()

# Run the app
if __name__ == "__main__":
    app = RobloxUsernameChecker()
    app.run()
