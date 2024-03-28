from tkinter import *
from tkinter import messagebox
from random import shuffle,randint,choice
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()
    if email_data and password_data and website_data:
        data = {
            f"{website_data}":{
                "email":f"{email_data}",
                "password":f"{password_data}"
            }
        }
        try:
            with open("data.json","r") as file:
                data_dict = json.load(file)
                data_dict.update(data)
        except (FileNotFoundError,json.JSONDecodeError):
            data_dict = data
        finally:
            with open("data.json","w") as file:
                json.dump(data_dict,file,indent=4)

        website_entry.delete(0, END)
        password_entry.delete(0, END)


    elif not email_data or not password_data or not website_data:
        messagebox.showinfo(title="Oops",message="please enter all details")

# ---------------------------- SEARCH BUTTON SETUP ------------------------------- #
def search():
    website_data = website_entry.get()
    try:
        with open("data.json") as file:
            data = json.load(file)
        email_password = data[website_data]
        email = email_password["email"]
        password = email_password["password"]
        messagebox.showinfo(website_data, f"email: {email}\npassword: {password}")
    except (FileNotFoundError):
        messagebox.showerror("Error","There is no such data")
        website_entry.delete(0, END)
    except KeyError:
        messagebox.showerror("Error",f"There is no such data with {website_data} website")
        website_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()

window.minsize(width=200, height=200)
window.title("password manager")
window.config(padx=40, pady=40)

img = PhotoImage(file="logo.png")
canvas = Canvas()
canvas.config(width=200,height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)
label_website = Label(text="Website:")

def cl():
    website_entry.focus()
window.after(10,cl)
label_website.grid(column=0,row=1)
label_email = Label(text="Email/Username:")
label_email.grid(row=2,column=0)
label_password = Label(text="Password:")
label_password.grid(row=3,column=0)

website_entry = Entry(width=34)
website_entry.grid(row=1,column=1,columnspan=1)
email_entry = Entry(width=52)
email_entry.insert(0, YOUR_MAIL)
email_entry.grid(row=2,column=1,columnspan=2)
password_entry = Entry(width=34)
password_entry.grid(row=3,column=1,columnspan=1)

generate_password_button = Button(command=password_generator)
generate_password_button.config(text="Generate Password",width=14)
generate_password_button.grid(column=2,row=3)
password_add_button = Button(text="Add",width=44,command=save_data)
password_add_button.grid(row=4,column=1,columnspan=2)
search_button = Button(text='search',width=14,command=search)
search_button.grid(column=2,row=1)


window.mainloop()
