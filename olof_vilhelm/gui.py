import tkinter as tk
from entity_relations_model import *


class Gui:
    MODE_BOTH = "both"
    MODE_ACTIVE = "both"
    MODE_PASSIVE = "passive"

    def __init__(self, entities, relations):
        if not all(isinstance(e, Entity) for e in entities):
            TypeError("Argument 'entities' must be a list of", type(Entity), "objects.")
        elif not all(isinstance(r, Relation) for r in relations):
            TypeError("Argument 'relations' must be a list of", type(Relation), "objects.")

        self.root = tk.Tk()
        self.root.title("Gui")
        self.root.geometry("1500x1100")
        #self.container = tk.PanedWindow(orient=tk.HORIZONTAL)
        self.left_panel = tk.Frame(self.root)
        #self.left_panel = tk.Frame(self.container)

        self.mode = Gui.MODE_BOTH
        relation_types = set()
        for relation in relations:
            relation_types.add(relation.word)
            relation_types.add(relation.inverse_word)
        relation_types = list(relation_types)

        self.entities = sorted(RelationalSet(entities).list())
        self.relations = relations
        self.filtered_relations = list()

        self.top_selected_i = -1
        self.relation_type_selected = tk.StringVar()
        self.relation_type_selected.set(relation_types[0])
        self.bottom_selected_i = -1

        self.big_font = ("Helvetica", 18)
        self.top_scrollbar = tk.Scrollbar(self.left_panel, orient=tk.VERTICAL)
        self.top_listbox = tk.Listbox(self.left_panel, yscrollcommand=self.top_scrollbar.set, font=self.big_font, exportselection=False)
        self.relations_menu = tk.OptionMenu(self.left_panel, self.relation_type_selected, *tuple(relation_types))
        self.bottom_scrollbar = tk.Scrollbar(self.left_panel, orient=tk.VERTICAL)
        self.bottom_listbox = tk.Listbox(self.left_panel, yscrollcommand=self.bottom_scrollbar.set, font=self.big_font, exportselection=False)

        self.textbox = tk.Text(self.root, font=self.big_font)
        #self.textbox = tk.Text(self.container, font=self.big_font)
        self.textbox.insert(tk.END, "The protein interaction text will appear here")

        self.__style_gui_()
        self.__setup_triggers()
        self.__init_top_entities()
        self.root.mainloop()

    def __style_gui_(self):
        self.top_listbox.grid(row=0, column=0, sticky="nswe")
        self.top_scrollbar.grid(row=0, column=1, sticky="nswe")
        self.top_scrollbar.config(command=self.top_listbox.yview)

        self.relations_menu.grid(row=1, sticky="nswe", pady=(10, 10))
        self.relations_menu.config(font=self.big_font)
        self.relations_menu.config()

        self.bottom_listbox.grid(row=2, column=0, sticky="nswe")
        self.bottom_scrollbar.grid(row=2, column=1, sticky="nswe")
        self.bottom_scrollbar.config(command=self.bottom_listbox.yview)

        self.left_panel.grid(row=0, column=0, sticky="nswe")
        self.left_panel.grid_rowconfigure(0, weight=2, uniform="left_panel")
        #self.left_panel.grid_rowconfigure(1, weight=1, uniform="left_panel")
        self.left_panel.grid_rowconfigure(2, weight=2, uniform="left_panel")
        self.left_panel.grid_columnconfigure(0, weight=1)

        self.textbox.grid(row=0, column=1, sticky="nswe")
        self.textbox.config(state=tk.DISABLED, wrap=tk.WORD)

        #self.container.insert(0, self.left_panel, weight=1)
        #self.container.insert(1, self.textbox, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)


    def __setup_triggers(self):
        def on_select_top_item(event):
            self.top_selected_i = self.top_listbox.index(tk.ACTIVE)
            self.__update_relations_menu()

        def on_select_relation(*args):
            self.__update_bottom_listbox()

        def on_select_bottom_item(event):
            self.bottom_selected_i = self.bottom_listbox.index(tk.ACTIVE)
            self.update_text_view()

        def on_window_resize(event):
            self.__update_container_children_width()

        self.top_listbox.bind("<Double-Button-1>", on_select_top_item)
        self.bottom_listbox.bind("<Double-Button-1>", on_select_bottom_item)
        self.root.bind("<Configure>", on_window_resize)
        self.relation_type_selected.trace("w", on_select_relation)
        # TODO on_resize_window
        # TODO manage text longer than textbox

    def __init_top_entities(self):
        self.top_listbox.delete(0, tk.END)

        for i in range(len(self.entities)):
            nr_relations = str(len(self.entities[i].active_relations) + len(self.entities[i].passive_relations))
            item = "[" + nr_relations + "] " + self.entities[i].name
            self.top_listbox.insert(i, item)

    def __update_relations_menu(self):
        active_relations = self.entities[self.top_selected_i].active_relations
        passive_relations = self.entities[self.top_selected_i].passive_relations
        relation_types = set(relation.word for relation in active_relations)
        relation_types |= set(relation.inverse_word for relation in passive_relations)
        relation_types = list(relation_types)
        self.relation_type_selected.set(relation_types[0])

        self.relations_menu['menu'].delete(0, tk.END)
        for relation in relation_types:
            self.relations_menu['menu'].add_command(label=relation, command=tk._setit(self.relation_type_selected, relation))

    def __update_bottom_listbox(self):
        self.bottom_listbox.delete(0, tk.END)

        entity = self.entities[self.top_selected_i]
        self.filtered_relations = list(filter(lambda r: r.word == self.relation_type_selected.get(), entity.active_relations))
        self.filtered_relations += list(filter(lambda r: r.inverse_word == self.relation_type_selected.get(), entity.passive_relations))
        for i in range(len(self.filtered_relations)):
            rel = self.filtered_relations[i]
            other_entity = rel.to_entity if rel.from_entity == entity else rel.from_entity
            self.bottom_listbox.insert(i, other_entity.name)

    def __update_container_children_width(self):
        # TODO
        # print("Window size updated")
        pass

    def update_text_view(self):
        relation = self.filtered_relations[self.bottom_selected_i]
        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, relation.source.identifier + "\n\n")
        self.textbox.mark_set("abstract", tk.INSERT)
        self.textbox.mark_gravity("abstract", tk.LEFT)
        self.textbox.insert(tk.END, relation.source.text + "\n\n")

        nr_other_relations = str(len(relation.source.relations) - 1)
        self.textbox.insert(tk.END, "Abstract contains " + nr_other_relations + " other detected relations.")

        # Mark text
        for s_i, e_i in relation.indices(Relation.FROM):
            self.textbox.tag_add("entityfrom", "abstract+" + str(s_i) + "chars", "abstract+" + str(e_i) + "chars")

        for s_i, e_i in relation.indices(Relation.TO):
            self.textbox.tag_add("entityto", "abstract+" + str(s_i) + "chars", "abstract+" + str(e_i) + "chars")

        for s_i, e_i in relation.indices(Relation.RELATION):
            self.textbox.tag_add("relation", "abstract+" + str(s_i) + "chars", "abstract+" + str(e_i) + "chars")

        self.textbox.tag_config("entityfrom", background="orange")
        self.textbox.tag_config("entityto", background="yellow")
        self.textbox.tag_config("relation", background="cyan")

        self.textbox.config(state=tk.DISABLED)


def main():
    vowels = {"A", "E", "I", "O", "U", "Y"}
    voiced_consonants = {"L", "M", "N", "R", "V", "W", "Z"}
    consonants = {"B", "C", "D", "F", "G", "H", "J", "K", "P", "Q", "S", "T", "X"} | voiced_consonants
    alphabet = vowels | consonants
    test_entities = list(map(lambda n: Entity(n), alphabet))
    test_entities = RelationalSet(test_entities)
    test_sources = RelationalSet()

    def __relation(type, c_1, c_2):
        text = ""
        if type == "strong":
            e_1_is = (len(text), len(text) + len(c_1))
            text += c_1 +" is... something to "
            e_2_is = (len(text), len(text) + len(c_2))
            text += c_2 + ". What was it? I can't really remember hmm... It was something about a connection between two entites, it's on the tip of my tongue. Goddamn it how come i can't remember? Oh yes i do remember, I was just lying and writing alot so this text becomes superlong, anyways the word is \""
            r = "related"
            r_is = (len(text), len(text) + len(r))
            text += r + "\"."

        elif type == "weak":
            e_1_is = (len(text), len(text) + len(c_1))
            text += c_1 + " is "
            r = "not really related"
            r_is = (len(text), len(text) + len(r))
            text += r + " to "
            e_2_is = (len(text), len(text) + len(c_2))
            text += c_2 + ", as one is a vowel, but the other is a voiced consonant."

        else:
            e_1_is = (len(text), len(text) + len(c_1))
            text += c_1 + " and "
            e_2_is = (len(text), len(text) + len(c_2))
            text += c_2 + " are "
            r = "not related"
            r_is = (len(text), len(text) + len(r))
            text += r + "."

        return text, e_1_is, e_2_is, r, r_is

    test_relations = list()
    for i in range(len(test_entities)):
        for j in range(0, len(test_entities)):
            if i != j:
                e_1 = test_entities[i]
                e_2 = test_entities[j]
                e_set = {e_1.name, e_2.name}
                if e_set.issubset(vowels) or e_set.issubset(consonants):
                    text, e_1_is, e_2_is, r, r_is = __relation("strong", e_1.name, e_2.name)
                    src = Source(text, "test_data: " + e_1.name + " - " + e_2.name)
                    test_relations.append(Relation(src, r, r + " (INVERSE)", *r_is).from_(e_1, *e_1_is).to_(e_2, *e_2_is))
                    test_sources.add(src)
                else:
                    if e_set.issubset(vowels | voiced_consonants):
                        text, e_1_is, e_2_is, r, r_is = __relation("weak", e_1.name, e_2.name)
                        src = Source(text, "test_data: " + e_1.name + " - " + e_2.name)
                        test_relations.append(Relation(src, r, r + " (INVERSE)", *r_is).from_(e_1, *e_1_is).to_(e_2, *e_2_is))
                        test_sources.add(src)
                    text, e_1_is, e_2_is, r, r_is = __relation("none", e_1.name, e_2.name)
                    src = Source(text, "test_data: " + e_1.name + " - " + e_2.name)
                    test_relations.append(Relation(src, r, r + " (INVERSE)", *r_is).from_(e_1, *e_1_is).to_(e_2, *e_2_is))
                    test_sources.add(src)

    entity_a = Entity("A")
    entity_z = Entity("Z")
    strange_entity = Entity("STRANGE_ENTITY")
    multi_rel_src= Source("This is the single Source with multiple relations. A is related to STRANGE_ENTITY, and STRANGE_ENTITY is also related to Z.", "multirelation source")
    r1 = Relation(multi_rel_src, "related", "related (INVERSE)", 56, 64).from_(entity_a, 51, 52).to_(strange_entity, 67, 82)
    r2 = Relation(multi_rel_src, "related", "related (INVERSE)", 110, 118).from_(strange_entity, 87, 102).to_(entity_z, 121, 122)
    test_entities += entity_z, strange_entity, entity_z
    test_relations.append(r1)
    test_relations.append(r2)
    test_sources += multi_rel_src

    print("Starting gui...")

    Gui(test_entities, test_relations)


if __name__ == "__main__":
    main()
