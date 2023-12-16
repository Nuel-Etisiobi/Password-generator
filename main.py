from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import string
import json


# --------------------------- SEARCH FOR SAVED DATA -------------------------#

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as file:
            # Read json file
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="error", message="No data file found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            password_entry.insert(0, password)
            messagebox.showinfo(title=website, message=f"Email: {email}, \nPassword: {password}")
        else:
            messagebox.showerror(title="error", message="Such website does not exist")
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation

    nr_letters = random.randint(5, 8)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for l in range(nr_letters)]
    password_symbol = [random.choice(symbols) for s in range(nr_symbols)]
    password_number = [random.choice(numbers) for n in range(nr_numbers)]

    pass_char = password_number + password_symbol + password_letter

    random.shuffle(pass_char)

    password = "".join(pass_char)

    password_entry.insert(0, password)

    # automatically copy the details inside the password entry
    pyperclip.copy(password_entry.get())

# ---------------------------- SAVE PASSWORD ------------------------------- #


def write_json(value):
    with open("data.json", mode="w") as file:
        json.dump(value, file, indent=4)


def save_data():
    website_data = website_entry.get()
    email_data = email_entry.get()
    pass_data = password_entry.get()
    new_data = {
            website_data: {
                "email": email_data,
                "password": pass_data,
            }
    }

    if len(website_data) == 0 or len(pass_data) == 0:
        messagebox.showerror(title="Error", message="The website or password can't be empty")

    else:
        # add message boxes
        # messagebox.showinfo(title="Title", message="message")

        # CONFIRM IF THE DATA IS CORRECT
        # is_ok = messagebox.askokcancel(title=website_data, message=f"These are the details for {website_data}: \nemail: {email_data} \npassword: {pass_data}")

        # if is_ok:
        try:
            with open("data.json", mode="r") as file:
                # Read json file
                data = json.load(file)  # this data is in a python dict format
        except FileNotFoundError:
            write_json(new_data)
        else:
            # update json file
            data.update(new_data)

            write_json(data)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
# win = window.minsize(width=500, height=500)
window.config(padx=50, pady=60)

canvas = Canvas(width=207, height=250)
logo = PhotoImage(file="logo.png")
canvas.create_image(104, 125, image=logo)
canvas.grid(row=1, column=2)

# Website label and entry
website_label = Label(text="Website:")
website_label.focus()
website_label.grid(row=2, column=1)

website_entry = Entry(width=35)
website_entry.grid(row=2, column=2)

# Search button
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=2, column=3)

# user_name label and entry
email_label = Label(text="Email/Username:")
email_label.grid(row=3, column=1)

email_entry = Entry(width=55)
email_entry.insert(0, 'etibaba16@gmail.com')
email_entry.grid(row=3, column=2, columnspan=2)

# Password label and entry
password_label = Label(text="Password:")
password_label.grid(row=4, column=1)

password_entry = Entry(width=35)
password_entry.grid(row=4, column=2)

# Generate button
generatepassword_button = Button(text="Generate Password", command=generate_password)
generatepassword_button.grid(row=4, column=3)

# Add button
add_button = Button(text="Add", width=24, command=save_data)
add_button.grid(row=5, column=2)


window.mainloop()
