import tkinter as tk

root = tk.Tk()
root.title("Gui")
root.geometry("1500x1100")

textbox = tk.Text(root)
textbox.grid(row=0, column=2, sticky="nswe")
textbox.insert(tk.END, "LEEEefeeft")
textbox.config(state=tk.DISABLED)
label3 = tk.Label(root, text="input", bg="green")
label3.grid(row=0, column=3, sticky="nswe")


def hello(event):
    selected_index = listbox.curselection()[0]
    text = data[selected_index]["text"]
    importants = data[selected_index]["importants"]
    textbox.config(state=tk.NORMAL)

    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, text)
    for s_i, e_i in importants:
        textbox.tag_add("colorize", "1." + str(s_i), "1." + str(e_i))

    textbox.tag_config("colorize", background="yellow")
    textbox.config(state=tk.DISABLED)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
for i in range(100):
    string = "item nr " + str(i)
    listbox.insert(i, string)

listbox.grid(row=0, column=0, sticky="nswe")
listbox.bind("<Double-Button-1>", hello)
scrollbar.grid(row=0, column=1, sticky="nswe")
scrollbar.config(command=listbox.yview)

data = list()
for i in range(100):
    text = "This is the text of item nr " + str(i)
    this_s_i = text.find("This")
    this_e_i = this_s_i + len("This")
    text_s_i = text.find("text")
    text_e_i = text_s_i + len("text")
    nr_s_i = text.find(str(i))
    nr_e_i = nr_s_i + len(str(i))

    important = [(this_s_i, this_e_i), (text_s_i, text_e_i), (nr_s_i, nr_e_i)]
    data.append({
        "text": text,
        "importants": important
    })


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=3)
root.grid_columnconfigure(3, weight=1)

root.mainloop()