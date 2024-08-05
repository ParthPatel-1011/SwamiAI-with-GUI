import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
import os
import cohere
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, font

api_key = 'UJL4zSrYc5ztTq6LrY7aFW5M1VttDvCTXzILUYmq'  # Set your Cohere API key here
chatStr = ""
last_response = ""
stop_speaking = False
font_size = 12  # Default font size

def chat(query):
    global chatStr, api_key
    if not api_key:
        return "API key is not set. Please set the API key."
    co = cohere.Client(api_key)
    chatStr += f"User: {query}\n"
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=chatStr,
        max_tokens=200
    )
    response_text = response.generations[0].text.strip()
    chatStr += f"Swami: {response_text}\n"
    return response_text

def ai(prompt):
    global api_key
    if not api_key:
        return "API key is not set. Please set the API key."
    co = cohere.Client(api_key)
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=200
    )
    response_text = response.generations[0].text.strip()
    if not os.path.exists("cohere Files"):
        os.mkdir("cohere Files")
    with open(f"cohere Files/{''.join(prompt.split('ai')[1:]).strip()}.txt", "w") as f:
        f.write(f"cohere response for prompt: {prompt}\n************************\n{response_text}")
    return response_text

def say(text):
    global stop_speaking
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    if stop_speaking:
        engine.stop()
        stop_speaking = False

def tackCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        loading_text.set("Listening...")
        root.update_idletasks()
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            return query
        except Exception:
            return "Some Error Occurred. Sorry from Swami"

def process_query(query):
    response_text = ""
    sites = [["YouTube", "https://www.youtube.com"], ["Google", "https://www.google.com"], ["Chat GPT", "https://chatgpt.com/"]]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} ...")
            webbrowser.open(site[1])
            response_text = f"Opened {site[0]}"
            return response_text

    if "open music".lower() in query.lower():
        musicpath = "C:/Users/Patel Parth/Downloads/Unstoppable - Dino James  Ft Avengers  Dipan Patel.mp3"
        os.startfile(musicpath)
        response_text = "Opened Music"
    elif "the time".lower() in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        response_text = f"Sir, the time is {hour} hours and {minute} minutes"
        say(response_text)
    elif "using AI".lower() in query.lower():
        response_text = ai(prompt=query)
    elif "let's talk".lower() in query.lower():
        say("Sure, Why Not?")
        response_text = "Sure, Why Not?"
    else:
        application = [["VS code", "C:/Users/Patel Parth/Desktop/Visual Studio Code.lnk"], ["file explorer", "C:/Users/Patel Parth/Desktop/File Explorer.lnk"]]
        for app in application:
            if f"Open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]} sir...")
                os.startfile(app[1])
                response_text = f"Opened {app[0]}"
                return response_text
        if "Swami shutdown".lower() in query.lower():
            say("Ok. Bye-bye, see you soon...")
            response_text = "Shutdown"
            exit(0)
    return response_text

def on_enter_pressed(event):
    global last_response
    query = user_input.get()
    user_input.delete(0, tk.END)
    output_text.insert(tk.END, f"User: {query}\n", "user")
    loading_text.set("Generating response...")
    root.update_idletasks()
    try:
        response_text = process_query(query)
        if not response_text:
            response_text = chat(query)
        output_text.insert(tk.END, f"Swami: {response_text}\n", "swami")
        last_response = response_text
        loading_text.set("")
    except Exception as e:
        loading_text.set("Generation failed")
        messagebox.showerror("Error", "Response generation failed. Please try again.")
    root.update_idletasks()

def on_lets_talk():
    global last_response
    say("Sure, I'd be happy to chat with you! Is there anything in particular you'd like to talk about?")
    loading_text.set("Listening...")
    root.update_idletasks()
    while True:
        query = tackCommand()
        if "bye".lower() in query.lower():
            say("Bye! It was nice chatting with you.")
            loading_text.set("")
            break
        output_text.insert(tk.END, f"User: {query}\n", "user")
        loading_text.set("Generating response...")
        root.update_idletasks()
        response_text = chat(query)
        output_text.insert(tk.END, f"Swami: {response_text}\n", "swami")
        loading_text.set("")
        say(response_text)
        last_response = response_text

def on_say():
    global last_response
    query = tackCommand()
    output_text.insert(tk.END, f"User: {query}\n", "user")
    loading_text.set("Generating response...")
    root.update_idletasks()
    response_text = process_query(query)
    if not response_text:
        response_text = chat(query)
    output_text.insert(tk.END, f"Swami: {response_text}\n", "swami")
    loading_text.set("Swami AI speaking...")
    say(response_text)
    last_response = response_text

def on_speak():
    global last_response
    if last_response:
        say(last_response)
    else:
        say("Last Response Not Available")

def on_stop():
    global stop_speaking
    stop_speaking = True

def save_chat():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_text.get("1.0", tk.END))
        messagebox.showinfo("Saved", "Chat saved successfully!")

def adjust_button_positions():
    width = root.winfo_width()
    if width < 800:  # Define the threshold for small screens (e.g., 800 pixels)
        button_frame.grid(row=3, column=0, columnspan=7, pady=10, sticky="ew")
        for i, button in enumerate(button_frame.winfo_children()):
            button.grid(row=0, column=i, padx=5, pady=5)
    else:
        button_frame.grid(row=3, column=0, columnspan=7, pady=10, sticky="ew")
        for i, button in enumerate(button_frame.winfo_children()):
            button.grid(row=0, column=i, padx=5, pady=5, sticky="w")

def zoom_in():
    global font_size
    font_size += 2
    update_font_size()

def zoom_out():
    global font_size
    if font_size > 8:  # Set a minimum font size limit
        font_size -= 2
    update_font_size()

def update_font_size():
    new_font = font.Font(size=font_size)
    output_text.configure(font=new_font)
    font_size_label.config(text=f"-{font_size}-")

# Setup Tkinter GUI
root = tk.Tk()
root.title("Swami AI")

# Configure dark theme
root.configure(bg="#2E2E2E")

frame = tk.Frame(root, bg="#2E2E2E")
scrollbar = tk.Scrollbar(frame)
output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg="#1C1C1C", fg="#FFFFFF", insertbackground="#FFFFFF", selectbackground="#555555")
scrollbar.config(command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame.grid(row=0, column=0, columnspan=7, padx=10, pady=10, sticky="nsew")

user_input = tk.Entry(root, bg="#1C1C1C", fg="#FFFFFF", insertbackground="#FFFFFF")
user_input.grid(row=1, column=0, columnspan=7, padx=10, pady=10, sticky="ew")
user_input.bind("<Return>", on_enter_pressed)

loading_text = tk.StringVar()
loading_label = tk.Label(root, textvariable=loading_text, fg="cyan", bg="#2E2E2E")
loading_label.grid(row=2, column=0, columnspan=7, pady=10)

button_frame = tk.Frame(root, bg="#2E2E2E")
zoom_out_button = tk.Button(button_frame, text="-", command=zoom_out, bg="#F44336", fg="#FFFFFF", activebackground="#D32F2F")
zoom_out_button.grid(row=0, column=0, padx=5, pady=5)
font_size_label = tk.Label(button_frame, text=f"Font Size: {font_size}", fg="cyan", bg="#2E2E2E")
font_size_label.grid(row=0, column=1, padx=5, pady=5)
zoom_in_button = tk.Button(button_frame, text="+", command=zoom_in, bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049")
zoom_in_button.grid(row=0, column=2, padx=5, pady=5)
lets_talk_button = tk.Button(button_frame, text="Let's Talk", command=on_lets_talk, bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049")
lets_talk_button.grid(row=0, column=3, padx=5, pady=5)
say_button = tk.Button(button_frame, text="Say", command=on_say, bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049")
say_button.grid(row=0, column=4, padx=5, pady=5)
speak_button = tk.Button(button_frame, text="Speak", command=on_speak, bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049")
speak_button.grid(row=0, column=5, padx=5, pady=5)
stop_button = tk.Button(button_frame, text="Stop", command=on_stop, bg="#F44336", fg="#FFFFFF", activebackground="#D32F2F")
stop_button.grid(row=0, column=6, padx=5, pady=5)
save_button = tk.Button(button_frame, text="Save Chat", command=save_chat, bg="#2196F3", fg="#FFFFFF", activebackground="#1976D2")
save_button.grid(row=0, column=7, padx=5, pady=5)
button_frame.grid(row=4, column=0, columnspan=7, pady=10, sticky="ew")

# Configure text tags for different speakers
output_text.tag_config("user", foreground="cyan")
output_text.tag_config("swami", foreground="yellow")

# Make the grid cells expandable
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)

update_font_size()  # Apply the initial font size

root.mainloop()
