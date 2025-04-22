import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import time

# 30-second length sentences
sentences = [
    "Programming requires patience, creativity, and a problem-solving mindset.",
    "Python is widely used in data science, web development, and automation.",
    "Focus on accuracy before speed while improving your typing skills.",
    "Learning to code is a valuable skill that opens up many career opportunities.",
    "Practice typing daily to build speed and reduce errors effectively."
]

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.state("zoomed")  # Maximized window

        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.text_to_type = tk.StringVar()
        self.start_time = None
        self.direction = 1
        self.remaining_time = 30  # 30 seconds

        # Load and resize background image
        self.bg_image = Image.open("WhatsApp Image 2025-04-20 at 21.36-Photoroom.jpg")
        self.bg_image = self.bg_image.resize((self.screen_width, self.screen_height))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas and set background
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.image_obj = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.animate_image()

        # Center X
        center_x = self.screen_width // 2

        # Style for rounded buttons using ttk
        style = ttk.Style()
        style.theme_use('default')  # Ensure base theme
        style.configure("Rounded.TButton",
                        font=("Arial", 16),
                        padding=10,
                        foreground="white",
                        background="#5B5F97",
                        borderwidth=0)
        style.map("Rounded.TButton",
                  background=[("active", "#4E5481")],
                  foreground=[("disabled", "#d9d9d9")])

        # Timer label
        self.timer_label = tk.Label(root, text="Time: 30s", font=("Arial", 20), bg="#f2f2f2", fg="red")

        self.heading = tk.Label(root, text="Typing Speed Tester", font=("Merriweather", 24, "bold"), bg="#f2f2f2")
        self.sentence_display = tk.Label(root, textvariable=self.text_to_type, font=("Arial", 18), wraplength=900, bg="#f2f2f2", fg="#333")
        self.result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f2f2f2", fg="green")
        self.text_entry = tk.Text(root, height=5, font=("Arial", 16), wrap="word", state="disabled", bg="#D4C2FC", fg="black")

        self.start_button = ttk.Button(root, text="Start Test", command=self.start_test, style="Rounded.TButton")
        self.submit_button = ttk.Button(root, text="Submit", command=self.calculate_result, style="Rounded.TButton")
        self.submit_button.state(["disabled"])

        # Placing all widgets centered
        self.canvas.create_window(center_x, 50, window=self.heading)
        self.canvas.create_window(center_x, 110, window=self.timer_label)
        self.canvas.create_window(center_x, 160, window=self.sentence_display)
        self.canvas.create_window(center_x, 220, window=self.result_label)
        self.canvas.create_window(center_x, 300, window=self.text_entry, width=900, height=130)
        self.canvas.create_window(center_x - 100, 460, window=self.start_button)
        self.canvas.create_window(center_x + 100, 460, window=self.submit_button)

        # Bind Enter key to submit
        self.root.bind("<Return>", lambda event: self.submit_button.invoke())

    def animate_image(self):
        self.canvas.move(self.image_obj, self.direction, 0)
        current_coords = self.canvas.coords(self.image_obj)
        if current_coords[0] <= -10 or current_coords[0] >= 10:
            self.direction *= -1
        self.root.after(50, self.animate_image)

    def start_test(self):
        sentence = random.choice(sentences)
        self.text_to_type.set(sentence)
        self.text_entry.config(state="normal")
        self.text_entry.delete("1.0", tk.END)
        self.text_entry.focus()
        self.start_time = time.time()
        self.result_label.config(text="")
        self.submit_button.state(["!disabled"])
        self.remaining_time = 30
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.remaining_time}s")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.calculate_result()

    def calculate_result(self):
        if self.start_time is None:
            return

        end_time = time.time()
        total_time = end_time - self.start_time
        typed_text = self.text_entry.get("1.0", tk.END).strip()
        original_text = self.text_to_type.get()

        words_typed = typed_text.split()
        wpm = (len(words_typed) / total_time) * 60 if total_time > 0 else 0

        original_words = original_text.split()
        correct_words = sum(1 for i, word in enumerate(words_typed) if i < len(original_words) and word == original_words[i])
        accuracy = (correct_words / len(original_words)) * 100 if original_words else 0

        result = f"Time Taken: {total_time:.2f} sec | WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%"
        self.result_label.config(text=result)
        self.submit_button.state(["disabled"])
        self.text_entry.config(state="disabled")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTester(root)
    root.mainloop()
