import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter.constants import NO
from typing import Container
from config.config import Config
from repository.note import Note
import random
from utils.date import Date

class Main:
    def __init__(self) -> None:
        self.config = Config()
        self.note = Note()
        self.date = Date()

        self.view_item = self.note.get_data()
        self.init_root()

    """Initialize the app"""
    def init_app(self) -> None:
        self.configure_grid()
        self.create_list_container()
        self.create_bottom_button()

    """Components initiallization"""

    """Initialize the main window"""
    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.title(self.config.app_name)
        self.root.geometry(self.config.window_size)
        self.root.resizable(False, False)

    """Configure the grid of the main window"""
    def configure_grid(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=6)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

    """Create the container for button at the bottom"""
    def create_bottom_button(self) -> None:
        button_add_item = tk.Button(
            self.root, text='Add New Item', command=self.open_create_window)
        button_add_item.grid(column=0, row=1, sticky='EWN', padx=10, pady=5)

        Button_delete_item = tk.Button(
            self.root, text='Delete Item', command=self.update_item)
        Button_delete_item.grid(column=0, row=2, sticky='EWN', padx=10)

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

    """Listener function"""

    """Populate the treeview with data"""
    def load_item(self) -> None:
        self.tree.delete(*self.tree.get_children())

        for index, item in enumerate(self.view_item):
            column_values = (item['id'], index + 1,
                             item['title'], item['date'])

            self.tree.insert('', tk.END, values=column_values, iid=item['id'])

    """Open new window to create new item"""
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
        label_title = tk.Label(create_window, text='Title')
        label_title.grid(
            column=0, row=0, padx=self.config.main_margin, pady=5, sticky='NW')

        """Input for title"""
        input_title = ttk.Entry(create_window, width=90)
        input_title.grid(
            column=0, row=1, padx=self.config.main_margin, pady=5, sticky='NWE')

        """Label for content"""
        label_content = tk.Label(create_window, text='Content')
        label_content.grid(
            column=0, row=2, padx=self.config.main_margin, pady=5, sticky='NW')

        """Input for content"""
        input_content = tk.Text(create_window, width=90)
        input_content.grid(
            column=0, row=3, padx=self.config.main_margin, pady=5)

        """Button for submit"""
        button_create = tk.Button(create_window, text='Add Note', command=lambda: self.add_item(
            input_title.get(), input_content.get("1.0", 'end-1c')))
        button_create.grid(
            column=0, row=4, padx=self.config.main_margin, pady=5, sticky='NWE')

    """Add new item"""
    def add_item(self, title, content) -> None:
        new_item = {
            'id': random.randint(100, 500),
            'title': title,
            'date': self.date.get_formatted_date(),
            'content': content
        }

        self.note.insert_data(new_item)
        self.load_item()

    """Delete selected item"""
    def delete_item(self) -> None:
        self.note.delete_data(self.get_selected_item_id())
        self.load_item()

    """Update item"""
    def update_item(self, title, content) -> None:
        updated_item = {
            'title': title,
            'content': content
        }

        self.note.update_data(self.get_selected_item_id(), updated_item)
        self.load_item()

    """Get the ID of the selected item of treeview"""
    def get_selected_item_id(self) -> str:
        selected_row = self.tree.focus()
        return self.tree.item(selected_row, 'values')[0]
