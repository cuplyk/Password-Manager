from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_entry.delete(0, END)  # delete the content of the entry
    letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]  # list comprehension
    symbols = [chr(i) for i in range(33, 48)] + [chr(i) for i in range(58, 65)] + [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 127)]
    numbers = [str(i) for i in range(10)]
    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))] + [random.choice(symbols) for _ in range(random.randint(2, 4))] + [random.choice(numbers) for _ in range(random.randint(2, 4))]
    random.shuffle(password_list)  # shuffle the list to mix the characters and symbols in a random order
    password = "".join(password_list)
    password_entry.insert(0, password)  # insert the password in the entry
    pyperclip.copy(password)  # copy the password to the clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    # Get the values from the entry widgets
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if the user has entered a website and a password
    if not website or not password:
        messagebox.showinfo(title="Oops", message=f"Please make sure you haven't left any fields empty.")
        return

    # Create a dictionary with the website as the key and the email and password as the values
    new_data = {website: {"email": email, "password": password}}

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    # Clear the entry widgets
    website_entry.delete(0, END)
    password_entry.delete(0, END)


def search_data_from_json():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
        return
    # Get the website from the entry widget
    website = website_entry.get()
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Error", message=f"No data found for {website}.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)  # adding padding to the window

# Set up colors
BG_COLOR = "#FF7F4F#"  # light grey
BTN_COLOR = "#e2725b"  # blue
FG_COLOR = "white"  # white

FONT = ("Arial", 10, "bold")

# Add logo image
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=0, row=0, columnspan=3, pady=20)

# Labels
website_label = Label(text="Website:", fg=BTN_COLOR, font=FONT)
website_label.grid(row=1, column=0, sticky="E")
email_label = Label(text="Email/Username:", fg=BTN_COLOR, font=FONT)
email_label.grid(column=0, row=2, sticky="E")
password_label = Label(text="Password:", fg=BTN_COLOR, font=FONT)
password_label.grid(column=0, row=3, sticky="E")

# Entries
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1)
website_entry.focus()  # focus on the entry when the window opens
email_entry = Entry(width=30)
email_entry.grid(column=1, row=2)
email_entry.insert(0, "example@mail.ru")  # insert a default value in the entry
password_entry = Entry(width=30, show="*")
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=10, bg=BTN_COLOR, fg=FG_COLOR, font=FONT, command=search_data_from_json)
search_button.grid(column=2, row=1, padx=(10, 0), sticky="W")
generate_password_button = Button(text="Generate Password", bg=BTN_COLOR, fg=FG_COLOR, font=FONT, command=generate_password)
generate_password_button.grid(column=2, row=3, padx=(10, 0), sticky="W")
add_button = Button(text="Add", width=30, bg=BTN_COLOR, fg=FG_COLOR, font=FONT, command=save_data)
add_button.grid(column=1, row=4, columnspan=2, pady=(10, 0), sticky="EW")

# Set column and row weights
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(4, weight=1)

window.mainloop()
