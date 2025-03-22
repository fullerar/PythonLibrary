# GottaGoFast
# Author: Andrew Fuller
# Description: A speed reader script

import tkinter as tk  # For displaying text in GUI
import os
import argparse

# Globals
is_paused = False  # Pause toggle
current_index = 0  # Track current word index


# Function to load and process the file
# Function to load and process the file
def load_file(file_path):
    if not os.path.exists(file_path):
        error_label.config(text=f"Error: The file '{file_path}' does not exist.\nPlease restart with a valid file path.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            words = content.split()
            return words
    except Exception as e:
        error_label.config(text=f"Error: {e}\nPlease restart with a valid file path.")
        return []


# Function to highlight the middle letter of each word
def highlight_middle_letter(word):
    if len(word) == 1:  # If it's a single letter word
        # Wrap the single letter with spaces to allow centering
        before_middle = " "
        middle_letter = word
        after_middle = " "
    else:
        middle_index = len(word) // 2
        before_middle = word[:middle_index]
        middle_letter = word[middle_index]
        after_middle = word[middle_index + 1:]

    return before_middle, middle_letter, after_middle


# Function to display the next word on the GUI
def display_next_word(index):
    global current_index, is_paused

    if is_paused:
        return  # Do nothing if paused

    if index < len(words):
        word = words[index]
        before, middle, after = highlight_middle_letter(word)

        # Clear previous text in the Text widget
        text_widget.delete(1.0, tk.END)

        # Insert the before part and middle part (in red)
        text_widget.insert(tk.END, before, "center")
        text_widget.insert(tk.END, middle, "red")  # Apply the "red" tag to middle letter
        text_widget.insert(tk.END, after, "center")

        # Use the slider value directly for the delay
        delay = speed_slider.get()  # Directly use the slider value as the delay

        # After the time specified by the slider, show the next word
        current_index = index + 1
        root.after(delay, display_next_word, current_index)


# tied to the slider bar
def update_speed():
    delay = speed_slider.get()
    root.after(delay, display_next_word, 0)


# Function to toggle pause/resume
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if not is_paused:
        display_next_word(current_index)  # Resume from the current word index


# Function to restart
def restart():
    global is_paused
    display_next_word(0)
    is_paused = True


# Command-line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Speed reading tool.")
    parser.add_argument("file", metavar="FILE", type=str, help="Path to the text file")
    args = parser.parse_args()

    # If no file path is passed, show error and return None
    if not args.file:
        error_label.config(text="Error: You must provide a file path/name to read.\nPlease restart with the correct argument.")
        return None
    return args.file


# Initialize GUI window
root = tk.Tk()
root.title("Speed Reading Tool")

# Add a Text widget for displaying words
text_widget = tk.Text(root, height=2, width=20, font=("Helvetica", 36), wrap=tk.WORD)
text_widget.pack()

# Define the red color tag for highlighting
text_widget.tag_configure("red", foreground="red")

# Create a tag to center text
text_widget.tag_configure("center", justify="center")

# Add an error label at the top of the window
error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red")
error_label.pack()

pause_button = tk.Button(root, text="Pause/Resume", command=toggle_pause)
pause_button.pack()

restart_button = tk.Button(root, text="Restart", command=restart)
restart_button.pack()

# Speed adjustment slider
speed_slider = tk.Scale(root, from_=10, to_=1000, orient="horizontal", label="Speed (ms)")
speed_slider.set(500)  # Default speed
speed_slider.pack()

# Parse the file path argument
file_path = parse_arguments()

# Load words from file
words = load_file(file_path)

# Start reading the file after 1 second
if words:
    root.after(1000, display_next_word, 0)

# Run the GUI
root.mainloop()
