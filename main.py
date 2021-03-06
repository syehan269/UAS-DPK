import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter.constants import DISABLED, END, NO
import random
import webbrowser
from tkinter.messagebox import *

from utils.date import Date
from utils.validation import Validation
from repository.note import Note
from config.config import Config


class Main:
    def __init__(self) -> None:
        self.config = Config()
        self.note = Note()
        self.date = Date()
        self.validation = Validation()

        self.view_item = self.note.get_data()
        self.init_root()

    """Initialize the app"""

    def init_app(self) -> None:
        self.configure_grid()
        self.create_list_container()
        self.create_bottom_button()

        self.tree.bind("<Button-3>", self.create_menu)

    """Components initiallization"""

    """Initialize the main window"""

    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.title(self.config.app_name)
        self.root.geometry(self.config.window_size)
        self.root.resizable(False, False)
        self.root.config(menu=self.create_menubar())

    """Configure the grid of the main window"""

    def configure_grid(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=6)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)

    """Create the container for button at the bottom"""

    def create_bottom_button(self) -> None:
        button_add_item = tk.Button(
            self.root, text='View Note', command=lambda: self.open_view_window(self.get_selected_item_id()))
        button_add_item.grid(column=0, row=1, sticky='EWN', padx=10, pady=5)

        button_add_item = tk.Button(
            self.root, text='Add New Note', command=self.open_create_window)
        button_add_item.grid(column=0, row=2, sticky='EWN', padx=10, pady=5)

        button_update_item = tk.Button(
            self.root, text='Update Note', command=lambda: self.open_update_window(self.get_selected_item_id()))
        button_update_item.grid(column=0, row=3, sticky='EWN', padx=10)

        button_delete_item = tk.Button(
            self.root, text='Delete Note', command=self.delete_item)
        button_delete_item.grid(column=0, row=4, sticky='EWN', padx=10)

    """Create the container for treeview"""

    def create_list_container(self) -> None:
        columns = ('id', 'no', 'title', 'date')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        self.tree.heading('id', text='ID.')
        self.tree.column('id', stretch=NO, width=10)
        self.tree.heading('no', text='No.')
        self.tree.column('no', stretch=NO, width=40, minwidth=20)
        self.tree.heading('title', text='Title')
        self.tree.column('title', stretch=NO, width=188, minwidth=100)
        self.tree.heading('date', text='Date')
        self.tree.column('date', stretch=NO, width=100, minwidth=30)

        self.tree['displaycolumns'] = ('no', 'title', 'date')

        self.load_item()

        self.tree.grid(column=0, row=0, sticky='NSEW',
                       padx=self.config.main_margin, pady=self.config.main_margin)

    """initialize the menu"""

    def create_menu(self, event) -> None:
        iid = self.tree.identify_row(event.y)

        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="View", command=lambda: self.open_view_window(
            self.get_selected_item_id()))

        menu.add_command(label="Update", command=lambda: self.open_update_window(
            self.get_selected_item_id()))

        menu.add_command(label="Delete", command=self.delete_item)

        if iid:
            self.tree.selection_set(iid)
            menu.tk_popup(event.x_root, event.y_root)
        else:
            menu.grab_release()

    """Initialize the menubar"""

    def create_menubar(self):
        menubar = tk.Menu(self.root)
        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="About", command=self.open_menu_about)

        menubar.add_cascade(label="Info", menu=info_menu)

        return menubar

    """Initialize the new windows"""

    """Open new window to create new note"""

    def open_create_window(self) -> None:
        create_window = Toplevel(self.root)
        create_window.title('Add New Note')
        create_window.geometry('330x500')
        create_window.resizable(False, False)

        create_window.columnconfigure(0, weight=1)
        create_window.rowconfigure(0, weight=0)
        create_window.rowconfigure(1, weight=0)
        create_window.rowconfigure(2, weight=0)
        create_window.rowconfigure(3, weight=2)
        create_window.rowconfigure(4, weight=0)

        """Label for title"""
        label_title = tk.Label(create_window, text='Title :')
        label_title.grid(
            column=0, row=0, padx=self.config.main_margin, pady=5, sticky='NW')

        """Input for title"""
        self.input_title = ttk.Entry(create_window, width=90)
        self.input_title.grid(
            column=0, row=1, padx=self.config.main_margin, pady=5, sticky='NWE')

        """Label for content"""
        label_content = tk.Label(create_window, text='Content :')
        label_content.grid(
            column=0, row=2, padx=self.config.main_margin, pady=5, sticky='NW')

        """Input for content"""
        self.input_content = tk.Text(create_window, width=90)
        self.input_content.grid(
            column=0, row=3, padx=self.config.main_margin, pady=5)

        """Button for submit"""
        button_create = tk.Button(create_window, text='Add Note', command=lambda: self.add_item(
            self.input_title.get(), self.input_content.get("1.0", 'end-1c')))
        button_create.grid(
            column=0, row=4, padx=self.config.main_margin, pady=5, sticky='NWE')

    """Open new window to update note"""

    def open_update_window(self, id) -> None:
        iid = self.tree.focus()

        if len(iid) > 0:
            update_window = Toplevel(self.root)
            update_window.title('Edit Note')
            update_window.geometry('330x500')
            update_window.resizable(False, False)

            update_window.columnconfigure(0, weight=1)
            update_window.rowconfigure(0, weight=0)
            update_window.rowconfigure(1, weight=0)
            update_window.rowconfigure(2, weight=0)
            update_window.rowconfigure(3, weight=2)
            update_window.rowconfigure(4, weight=0)

            note = self.get_item_by_id(id)

            """Label for title"""
            label_title = tk.Label(update_window, text='Title :')
            label_title.grid(
                column=0, row=0, padx=self.config.main_margin, pady=5, sticky='NW')

            """Input for title"""
            input_title = ttk.Entry(update_window, width=90)
            input_title.grid(
                column=0, row=1, padx=self.config.main_margin, pady=5, sticky='NWE')
            input_title.insert(END, note['title'])

            """Label for content"""
            label_content = tk.Label(update_window, text='Content :')
            label_content.grid(
                column=0, row=2, padx=self.config.main_margin, pady=5, sticky='NW')

            """Input for content"""
            input_content = tk.Text(update_window, width=90)
            input_content.grid(
                column=0, row=3, padx=self.config.main_margin, pady=5)
            input_content.insert(END, note['content'])

            """Button for submit"""
            button_create = tk.Button(update_window, text='Update Note', command=lambda: self.update_item(
                input_title.get(), input_content.get("1.0", 'end-1c')))
            button_create.grid(
                column=0, row=4, padx=self.config.main_margin, pady=5, sticky='NWE')

        else:
            print('No item is selected')

    """Open new window to update note"""

    def open_view_window(self, id) -> None:
        iid = self.tree.focus()

        if len(iid) > 0:
            update_window = Toplevel(self.root)
            update_window.title('View Note')
            update_window.geometry('330x500')
            update_window.resizable(False, False)

            update_window.columnconfigure(0, weight=1)
            update_window.rowconfigure(0, weight=0)
            update_window.rowconfigure(1, weight=0)
            update_window.rowconfigure(2, weight=0)

            note = self.get_item_by_id(id)

            """Input for title"""
            text_title = tk.Label(update_window, text=note['title'])
            text_title.grid(
                column=0, row=1, padx=self.config.main_margin, pady=5, sticky='NW')

            """Label for content"""
            separator = ttk.Separator(update_window)
            separator.grid(column=0, row=2, padx=15, pady=5, sticky='EW')

            """Input for content"""
            text_content = tk.Message(update_window, text=note['content'], width=300)
            text_content.grid(column=0, row=3, padx=self.config.main_margin, pady=5, sticky='NW')

        else:
            print('No item is selected')

    """Open new window of menu about"""

    def open_menu_about(self) -> None:
        about_window = tk.Toplevel(self.root)
        about_window.resizable(False, False)
        about_window.geometry('250x100')
        about_window.title('About')
        about_window.attributes('-toolwindow', True)

        about_window.columnconfigure(0, weight=1)
        about_window.rowconfigure(0, weight=1)
        about_window.rowconfigure(1, weight=1)
        about_window.rowconfigure(2, weight=1)
        about_window.rowconfigure(3, weight=1)

        author_label = tk.Label(
            about_window, text=f"Author: {self.config.author}")
        author_label.grid(column=0, row=0)

        info_label = tk.Label(about_window, text=f"Info: {self.config.info}")
        info_label.grid(column=0, row=1)

        nim_label = tk.Label(about_window, text=f"NIM: {self.config.nim}")
        nim_label.grid(column=0, row=2)

        repository_label = tk.Label(
            about_window, text="Link repository", fg='blue', cursor='hand2')
        repository_label.bind(
            '<Button-1>', lambda e: self.open_link(self.config.repository_link))
        repository_label.grid(column=0, row=3)

    """Listener function"""

    """Populate the treeview with data"""

    def load_item(self) -> None:
        self.tree.delete(*self.tree.get_children())

        for index, item in enumerate(self.view_item):
            column_values = (item['id'], index + 1,
                             item['title'], item['date'])

            self.tree.insert('', tk.END, values=column_values, iid=item['id'])

    """Add new item"""

    def add_item(self, title, content) -> None:
        validation = self.validation.validate([title, content])

        if validation:
            new_item = {
                'id': random.randint(100, 500),
                'title': title,
                'date': self.date.get_formatted_date(),
                'content': content
            }

            self.note.insert_data(new_item)
            self.load_item()

            """reset the field's value"""
            self.input_content.insert(END, '')
            self.input_title.insert(END, '')
        else:
            showwarning(title='Validation Failed',
                        message="There's empty field!")
            print('field(s) is empty!')

    """Get item"""

    def get_item_by_id(self, id) -> None:
        return self.note.get_data_by_id(id)

    """Update item"""

    def update_item(self, title, content) -> None:
        validation = self.validation.validate([title, content])

        if validation:
            updated_item = {
                'title': title,
                'content': content
            }

            self.note.update_data(self.get_selected_item_id(), updated_item)
            self.load_item()
        else:
            showwarning(title='Validation Failed',
                        message="There's empty field!")
            print('Field(s) is empty!')

    """Delete selected item"""

    def delete_item(self) -> None:
        iid = self.tree.focus()

        if len(iid) > 0:
            self.note.delete_data(self.get_selected_item_id())
            self.load_item()
        else:
            print('No item is selected')

    """Get the ID of the selected item of treeview"""

    def get_selected_item_id(self) -> str:
        selected_row = self.tree.focus()

        if len(selected_row) > 0:
            return self.tree.item(selected_row, 'values')[0]
        else:
            return False

    def open_link(self, link) -> None:
        webbrowser.open_new(link)
