import tkinter as tk


class Gui:

    def __init__(self, list_data, text_data, relations):
        self.root = tk.Tk()
        self.root.title("Gui")
        self.root.geometry("1500x1100")

        self.top_selected = None
        self.relation_selected = tk.StringVar()
        self.relation_selected.set(relations[0])
        self.bottom_selected = None
        self.list_data = list_data
        self.text_data = text_data

        self.left_panel = tk.Frame(self.root)

        self.big_font = ("Helvetica", 20)
        self.top_scrollbar = tk.Scrollbar(self.left_panel, orient=tk.VERTICAL)
        self.top_listbox = tk.Listbox(self.left_panel, yscrollcommand=self.top_scrollbar.set, font=self.big_font, exportselection=False)
        self.middle = tk.OptionMenu(self.left_panel, self.relation_selected, *tuple(relations))
        self.bottom_scrollbar = tk.Scrollbar(self.left_panel, orient=tk.VERTICAL)
        self.bottom_listbox = tk.Listbox(self.left_panel, yscrollcommand=self.bottom_scrollbar.set, font=self.big_font, exportselection=False)

        self.textbox = tk.Text(self.root, font=self.big_font)
        self.textbox.insert(tk.END, "The protein interaction text will appear here")

        self.__style_gui_()
        self.__setup_triggers()
        self.__add_list_data(list_data)
        self.root.mainloop()

    def __style_gui_(self):
        self.top_listbox.grid(row=0, column=0, sticky="nswe")
        self.top_scrollbar.grid(row=0, column=1, sticky="nswe")
        self.top_scrollbar.config(command=self.top_listbox.yview)

        self.middle.grid(row=1, sticky="nswe")
        self.middle.config(font=self.big_font)

        self.bottom_listbox.grid(row=2, column=0, sticky="nswe")
        self.bottom_scrollbar.grid(row=2, column=1, sticky="nswe")
        self.bottom_scrollbar.config(command=self.bottom_listbox.yview)

        self.left_panel.grid(row=0, column=0, sticky="nswe")
        self.left_panel.grid_rowconfigure(0, weight=2, uniform="left_panel")
        self.left_panel.grid_rowconfigure(1, weight=1, uniform="left_panel")
        self.left_panel.grid_rowconfigure(2, weight=2, uniform="left_panel")
        self.left_panel.grid_columnconfigure(0, weight=1)

        self.textbox.grid(row=0, column=1, sticky="nswe")
        self.textbox.config(state=tk.DISABLED, wrap=tk.WORD)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1, uniform="root")
        self.root.columnconfigure(1, weight=2, uniform="root")

    def __setup_triggers(self):
        def update_selected_top_item(event):
            self.top_selected = self.top_listbox.get(tk.ACTIVE)
            self.__update_bottom_listbox()

        def update_selected_relation(*args):

            self.__update_bottom_listbox()

        def update_selected_bottom_item(event):
            self.bottom_selected = self.bottom_listbox.get(tk.ACTIVE)
            self.update_text_view()

        self.top_listbox.bind("<Double-Button-1>", update_selected_top_item)
        self.bottom_listbox.bind("<Double-Button-1>", update_selected_bottom_item)
        self.relation_selected.trace("w", update_selected_relation)
        # TODO on_resize_window
        # TODO manage text longer than textbox

    def __add_list_data(self, data):
        self.data = data
        self.top_listbox.delete(0, tk.END)
        list_items = list(data.keys())
        for i in range(len(list_items)):
            item = list_items[i]
            self.top_listbox.insert(i, item)

    def __update_bottom_listbox(self):
        self.bottom_listbox.delete(0, tk.END)
        bottom_items = self.list_data[self.top_selected][self.relation_selected.get()]
        print(bottom_items)
        for i in range(len(bottom_items)):
            self.bottom_listbox.insert(i, bottom_items[i])

    def update_text_view(self):
        text = self.text_data[self.top_selected][self.bottom_selected]["text"]
        entities = self.text_data[self.top_selected][self.bottom_selected]["entities"]
        relations = self.text_data[self.top_selected][self.bottom_selected]["relations"]

        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, text)

        # Mark text
        for s_i, e_i in entities:
            self.textbox.tag_add("entity", "1.0+" + str(s_i) + "chars", "1.0+" + str(e_i) + "chars")

        for s_i, e_i in relations:
            self.textbox.tag_add("relation", "1.0+" + str(s_i) + "chars", "1.0+" + str(e_i) + "chars")

        self.textbox.tag_config("entity", background="cyan")
        self.textbox.tag_config("relation", background="yellow")

        self.textbox.config(state=tk.DISABLED)


def main():
    vowels = ["A", "E", "I", "O", "U", "Y"]
    consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N ", "P", "Q", "R", "S", "T", "V", "W", "X", "Z"]
    alphabet = (vowels + consonants)
    alphabet.sort()

    test_relations = ["related", "not related"]
    test_list_data = dict()
    test_text_data = dict()
    for i in range(len(alphabet)):
        c_1 = alphabet[i]
        test_list_data[c_1] = dict()
        test_list_data[c_1][test_relations[0]] = list()
        test_list_data[c_1][test_relations[1]] = list()

        test_text_data[c_1] = dict()
        for j in range(len(alphabet)):
            if i != j:
                c_2 = alphabet[j]
                if c_1 in vowels and c_2 in vowels:
                    curr_relation = test_relations[0]
                    text = c_1 + " is... something to " + c_2 + ". What was it? I can't really remember hmm... It was something about a connection between two entites, it's on the tip of my tongue. Goddamn it how come i can't remember? Oh yes i do remember, I was just lying and writing alot so this text becomes superlong, anyways the word is \"related\"."
                elif c_1 in consonants and c_2 in consonants:
                    curr_relation = test_relations[0]
                    text = c_1 + " is related to " + c_2 + ", as both are consonants."
                else:
                    curr_relation = test_relations[1]
                    text = c_1 + " and " + c_2 + " are not related."

                test_list_data[c_1][curr_relation].append(c_2)

                relation_s = text.find(curr_relation)
                relation_e = relation_s + len(curr_relation)
                entity_1_s = text.find(c_1)
                entity_1_e = entity_1_s + len(c_1)
                entity_2_s = text.find(c_2)
                entity_2_e = entity_2_s + len(c_2)

                entities_i = [(entity_1_s, entity_1_e), (entity_2_s, entity_2_e)]
                relations_i = [(relation_s, relation_e)]
                value = {"text": text, "entities": entities_i, "relations":relations_i}
                test_text_data[c_1][c_2] = value

    print ("Starting gui...")
    gui = Gui(test_list_data, test_text_data, test_relations)


if __name__ == "__main__":
    main()
