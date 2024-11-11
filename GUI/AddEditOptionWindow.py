"""
Project Name: D2LQuizCreator
File Name: AddEditOptionWindow.py
Date Created: 11/7/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/7/2024
"""

from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


class AddEditOptionWindow:
    def __init__(
            self,
            root,
            comboBoxSelectedEntry,
            label,
            tree,
            existing_entry=None,
            currentIndex=None,
    ):
        """Opens a new window for adding or editing a treeview entry, with dynamic fields based on a supplied dictionary."""
        self.currentIndex = currentIndex
        self.existingEntry = existing_entry
        self.tree = tree
        field_structure = {
            "Short Answer": ["PointsPerThisAnswer", "Answer"],
            "Written Response": [],
            "Multiple Choice": ["PointsPerAnswer", "Option"],
            "Matching": ["MatchText", "ChoiceText"],
            "True or False": ["TruePoints", "FalsePoints"],
            "Ordering": ["Option"],
            "MultiSelection": ["PointsPerOption", "Option"],
        }

        restricted_points_fields = {
            "Short Answer": {"PointsPerThisAnswer": [0, 100]},
            "Multiple Choice": {"PointsPerAnswer": [0, 100]},
            "MultiSelection": {"PointsPerOption": [0, 1]},
        }

        self.root = root
        if not existing_entry:
            self.root.title("Add Question")
        else:
            self.root.title("Edit Question")

        self.root.title(f"{'Edit' if existing_entry else 'Add'} {label} Entry")
        self.fieldsFrame = tk.LabelFrame(
            self.root, text="General Properties", padx=10, pady=10
        )
        self.entry_widgets = {}
        self.questionType = comboBoxSelectedEntry

        matchingValueList = []
        if self.questionType == "Matching":
            for index in range(1, len(self.tree.item(self.tree.focus())["values"]), 2):
                matchingValueList.append(
                    [index, self.tree.item(self.tree.focus())["values"][index]]
                )

        self.__BuildOptionSpecificWidgets(
            comboBoxSelectedEntry,
            existing_entry,
            field_structure,
            restricted_points_fields,
        )

        self.fieldsFrame.grid()

        self.save_button = tk.Button(
            self.root,
            text="Save",
            command=lambda: self.saveEntryToTreeView(
                self.entry_widgets, isEditable=bool(existing_entry)
            ),
        )
        self.save_button.grid(row=len(field_structure), column=0, columnspan=2, pady=10)

    def __BuildOptionSpecificWidgets(
            self,
            comboBoxSelectedEntry,
            existing_entry,
            field_structure,
            restricted_points_fields,
    ):
        for idx, field_label in enumerate(field_structure[comboBoxSelectedEntry]):
            tk.Label(self.fieldsFrame, text=f"{field_label}:").grid(
                row=idx, column=0, sticky="w"
            )

            # Use Combobox for restricted fields, Entry otherwise
            if field_label in restricted_points_fields.get(self.questionType, {}):
                allowed_values = restricted_points_fields[self.questionType][
                    field_label
                ]
                widget = ttk.Combobox(
                    self.fieldsFrame, values=allowed_values, state="readonly", width=48
                )
                if existing_entry:
                    widget.set(self.tree.item(self.tree.focus())["values"][idx])
                else:
                    widget.set(
                        allowed_values[0]
                    )  # Set the default value to the first allowed value
            else:
                widget = tk.Entry(self.fieldsFrame, width=50)
                if existing_entry:
                    widget.insert(0, self.tree.item(self.tree.focus())["values"][idx])

            widget.grid(row=idx, column=1, padx=5, pady=2)
            self.entry_widgets[field_label] = widget

    def saveEntryToTreeView(self, entry_widgets, isEditable=None):
        """Save a new or edited entry to the Treeview"""
        values = []
        for field_label, widget in entry_widgets.items():
            if isinstance(widget, ttk.Combobox):
                values.append(widget.get())
            else:
                values.append(widget.get())

        if self.questionType == "Matching":
            values.insert(
                0,
                (
                    len(self.tree.get_children()) + 1
                    if not self.existingEntry
                    else self.currentIndex
                ),
            )
            values.insert(
                2,
                (
                    len(self.tree.get_children()) + 1
                    if not self.existingEntry
                    else self.currentIndex
                ),
            )

        if "" in values:
            messagebox.showerror(
                "Empty Values",
                "Please enter an appropriate value for ALL fields",
                parent=self.root,
            )
            return

        if isEditable:
            selected_item = self.tree.selection()[0]
            self.tree.item(selected_item, values=values)
        else:
            self.tree.insert("", "end", values=values)

        self.root.destroy()
