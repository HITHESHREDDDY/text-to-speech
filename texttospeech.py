import pyttsx3 # type: ignore
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from PIL import Image, ImageTk # type: ignore
import threading

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Global variables
is_speaking = False
engine_thread = None

# Functions
def set_buttons_state(state):
    convert_button.config(state=state)
    stop_button.config(state='normal' if state == 'disabled' else 'disabled')
    save_button.config(state=state)
    reset_button.config(state=state)

def select_voice(selected_voice):
    voices = engine.getProperty('voices')
    for voice in voices:
        if selected_voice.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

def text_to_speech():
    global is_speaking, engine_thread
    text = text_input.get("1.0", tk.END).strip()
    if text:
        try:
            engine.setProperty('rate', speech_rate.get())
            select_voice(voice_var.get())
            is_speaking = True
            set_buttons_state('disabled')
            engine_thread = threading.Thread(target=run_speech, args=(text,))
            engine_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("Input Error", "Please enter some text!")

def run_speech(text):
    global is_speaking
    try:
        engine.say(text)
        engine.runAndWait()
    finally:
        is_speaking = False
        set_buttons_state('normal')

def stop_speech():
    global is_speaking
    if is_speaking:
        engine.stop()
        is_speaking = False
        set_buttons_state('normal')
        messagebox.showinfo("Stopped", "Speech has been stopped.")

def save_as_audio():
    text = text_input.get("1.0", tk.END).strip()
    if text:
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Audio Files", "*.wav")])
        if file_path:
            try:
                engine.setProperty('rate', speech_rate.get())
                select_voice(voice_var.get())
                engine.save_to_file(text, file_path)
                engine.runAndWait()
                messagebox.showinfo("Success", "Audio file saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("Input Error", "Please enter some text!")

def reset_text():
    text_input.delete("1.0", tk.END)

def show_help():
    help_message = (
        "Welcome to the Text-to-Speech App!\n\n"
        "1. Enter the text you want to convert to speech.\n"
        "2. Use the slider to adjust the speech rate.\n"
        "3. Select a voice (Male or Female).\n"
        "4. Click 'Convert to Speech' to hear the text.\n"
        "5. Click 'Stop' to stop the speech in progress.\n"
        "6. Click 'Save as Audio' to save the speech as a file.\n"
        "7. Use 'Reset' to clear the text box."
    )
    messagebox.showinfo("Help", help_message)

def open_main_app():
    start_page.destroy()

    main_app = tk.Tk()
    main_app.title("Text-to-Speech Converter")
    main_app.geometry("700x700")
    main_app.configure(bg="#F0E5CF")

    # Top Section with Image
    try:
        header_image = PhotoImage(file="header_image.png")  # Replace with your header image
        header_label = tk.Label(main_app, image=header_image, bg="#F0E5CF")
        header_label.image = header_image
        header_label.pack(pady=10)
    except Exception:
        pass

    # Title Label
    title_label = tk.Label(main_app, text="Text-to-Speech Converter", font=("Helvetica", 20, "bold"), bg="#F0E5CF", fg="#4E5166")
    title_label.pack(pady=10)

    # Instruction Label
    instruction_label = tk.Label(main_app, text="Enter the text you want to convert to speech:", font=("Helvetica", 12), bg="#F0E5CF", fg="#4E5166")
    instruction_label.pack(pady=5)

    # Text Input Frame
    text_frame = tk.Frame(main_app, bg="#F0E5CF")
    text_frame.pack(pady=10)

    global text_input
    text_input = tk.Text(text_frame, height=8, width=60, font=("Helvetica", 12), wrap="word", bg="#FFF8E7", fg="#4E5166")
    text_input.pack(side="left", fill="both", expand=True)

    text_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_input.yview)
    text_scrollbar.pack(side="right", fill="y")
    text_input.config(yscrollcommand=text_scrollbar.set)

    # Speech Rate Slider
    global speech_rate
    speech_rate = tk.Scale(main_app, from_=50, to=300, orient="horizontal", label="Speech Rate", font=("Helvetica", 10), bg="#F0E5CF", fg="#4E5166")
    speech_rate.set(150)
    speech_rate.pack(pady=10)

    # Voice Selection
    global voice_var
    voice_var = tk.StringVar(value="Male")
    voice_frame = tk.Frame(main_app, bg="#F0E5CF")
    voice_frame.pack(pady=5)
    voice_label = tk.Label(voice_frame, text="Select Voice:", font=("Helvetica", 12), bg="#F0E5CF", fg="#4E5166")
    voice_label.pack(side="left")
    voice_menu = tk.OptionMenu(voice_frame, voice_var, "Male", "Female")
    voice_menu.config(bg="#FFF8E7", fg="#4E5166", font=("Helvetica", 10))
    voice_menu.pack(side="left", padx=5)

    # Buttons
    global convert_button, stop_button, save_button, reset_button
    button_style = {"font": ("Helvetica", 12, "bold"), "fg": "white"}

    convert_button = tk.Button(main_app, text="Convert to Speech", bg="#4E5166", **button_style, command=text_to_speech)
    convert_button.pack(pady=10)

    stop_button = tk.Button(main_app, text="Stop", bg="#F05454", **button_style, command=stop_speech)
    stop_button.pack(pady=10)

    save_button = tk.Button(main_app, text="Save as Audio", bg="#6E85B2", **button_style, command=save_as_audio)
    save_button.pack(pady=10)

    reset_button = tk.Button(main_app, text="Reset", bg="#F05454", **button_style, command=reset_text)
    reset_button.pack(pady=10)

    help_button = tk.Button(main_app, text="Help", bg="#30475E", **button_style, command=show_help)
    help_button.pack(pady=10)

    main_app.mainloop()

# Start Page
start_page = tk.Tk()
start_page.title("Welcome")
start_page.geometry("700x700")
start_page.configure(bg="#4E5166")

# Welcome Image
try:
    img = Image.open(r"C:\Users\Hitesh Reddy\Desktop\New folder\sticker5.png")  # Replace with your image path
    img = img.resize((700, 400))
    welcome_image = ImageTk.PhotoImage(img)
    welcome_label = tk.Label(start_page, image=welcome_image, bg="#4E5166")
    welcome_label.image = welcome_image
    welcome_label.pack(pady=20)
except Exception as e:
    print(f"Error loading or resizing welcome image: {e}")

# Welcome Text
welcome_text = tk.Label(start_page, text="Welcome to the Text-to-Speech App", font=("Helvetica", 20, "bold"), bg="#4E5166", fg="white")
welcome_text.pack(pady=20)

# Start Button
start_button = tk.Button(start_page, text="Let's Start", font=("Helvetica", 14, "bold"), bg="#F05454", fg="white", command=open_main_app)
start_button.pack(pady=20)

start_page.mainloop()
