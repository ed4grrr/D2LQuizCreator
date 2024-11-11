"""
Project Name: pythonProject
File Name: AddQuestionWindow.py
Date Created: 11/2/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/2/2024

*** Created with the help of ChatGPT and a heavy amount of my own tinkering
"""

import tkinter as tk
from tkinter import ttk, messagebox

from GUI.AddEditOptionWindow import AddEditOptionWindow


class AddQuestionWindow:
    def __init__(
        self, root, ReturnValueAcceptingFunction, listbox=None, listBoxDict=None
    ):
        self.generalAdvancedRadioButton = None
        self.generalQuestionFieldsFrame = None
        self.submitQuestionButton = None
        self.isSpecificAdvancedCheckBox = None
        self.tree = None
        self.specificQuestionFieldsFrame = None
        self.listbox = listbox
        self.listBoxDict = listBoxDict
        self.questionTypeComboBox = None
        self.root = tk.Toplevel(root)
        self.isBothListBoxAndListDict = (
            True if (listBoxDict is not None) and (listbox is not None) else False
        )

        # used to determine if editing or adding a question
        if not self.isBothListBoxAndListDict:
            self.root.title("Add New Question")
        else:
            self.root.title("Edit New Question")

        # gets the return value from this window and returns it to maingui to be parsed
        self.ReturnValueAcceptingFunction = (
            ReturnValueAcceptingFunction  # Callback to notify the main screen
        )

        # bool variable linked to special advance radio button
        self.isShowingSpecificAdvancedFeatures = tk.BooleanVar(value=False)

        # bool variable linked to general advance radio button
        self.isShowingGeneralAdvancedFeatures = tk.BooleanVar(value=False)

        self.VALIDATION_FUNCTIONS = {
            # "Short Answer": self.validate_short_answer,
            "True or False": self.__ValidateTrueOrFalse,
            # Add other QuestionTypes and their validation functions as needed for advanced features
        }

        # the two following dicts are used to create the necessary general fields
        self.advancedGeneralFields = [
            ("Title", "str"),
            ("QuestionText", "str"),
            ("Points", "int"),
            ("Difficulty", "int"),
            ("ID", "str"),
            ("ImagePath", "str"),
            ("Scoring", "str"),
            ("Hint", "str"),
            ("QuestionFeedback", "str"),
        ]
        self.minimumGeneralFields = [("QuestionText", "str")]

        # used to create and parse fields within this window's treeview
        self.QuestionTypeFields = {
            "Short Answer": {"PointsPerAnswer": [], "Answers": []},
            "Written Response": {},
            "Matching": {
                "ListOfMatchNumbers": [],
                "ListOfMatchingText": [],
                "ListOfChoiceNumbers": [],
                "ListOfChoiceText": [],
            },
            "Multiple Choice": {"ListOfPointsPerOption": [], "ListOfOptions": []},
            "True or False": {},
            "MultiSelection": {"PointsPerAnswer": [], "OptionText": []},
            "Ordering": {"ListOfItems": []},
        }

        # General Properties Section
        self.InitializeGeneralFields()

        # Define restricted fields and their properties
        self.RESTRICTED_FIELDS = {
            "Short Answer": {
                "CharMinimumLength": {"type": "spinbox", "min": 1, "max": 199},
                "CharMaximumLength": {"type": "spinbox", "min": 2, "max": 200},
            },
            "True or False": {
                "TruePoints": {
                    "type": "combobox",
                    "values": [0, 100],
                    "linked_field": "FalsePoints",
                },
                "FalsePoints": {
                    "type": "combobox",
                    "values": [0, 100],
                    "linked_field": "TruePoints",
                },
            },
        }

        self.GeneralQuestionTypeFieldsNames = {
            "Short Answer": [("Answers", "list[int]")],
            "Written Response": [],
            "Matching": [("ListOfMatches", "list[str]")],
            "Multiple Choice": [("ListOfOptions", "list[str]")],
            "True or False": [("TruePoints", "int"), ("FalsePoints", "int")],
            "MultiSelection": [("Options", "list[str]")],
            "Ordering": [("ListOfItems", "list[str]")],
        }

        self.AdvancedQuestionTypeFieldsNames = {
            "Short Answer": [
                ("Answers", "list[str]"),
                ("PointsPerAnswer", "list[int]"),
                ("RegExsForAnswers", "list[str]"),
                ("CharMinimumLength", "int"),
                ("CharMaximumLength", "int"),
            ],
            "Written Response": [("InitialText", "str"), ("AnswerKey", "str")],
            "Matching": [
                ("ListOfMatchNumbers", "list[str]"),
                ("ListOfMatchingText", "list[str]"),
                ("ListOfChoiceNumbers", "list[str]"),
                ("ListOfChoiceText", "list[str]"),
            ],
            "Multiple Choice": [
                ("ListOfOptions", "list[str]"),
                ("ListOfPointsPerOption", "list[int]"),
                ("ListOfFeedBack", "list[str]"),
            ],
            "True or False": [
                ("TruePoints", "int"),
                ("FalsePoints", "int"),
                ("TrueFeedback", "str"),
                ("FalseFeedback", "str"),
            ],
            "MultiSelection": [
                ("PointsPerAnswer", "list[int]"),
                ("OptionText", "list[str]"),
                ("OptionFeedback", "list[str]"),
            ],
            "Ordering": [
                ("ListOfItems", "list[str]"),
                ("ListOfIsHTML", "list[str]"),
                ("ListOfFeedback", "list[str]"),
            ],
        }

        # General and specific question Fields to be parsed
        self.generalQuestionFields = {}
        self.specificQuestionFields = {}

        # especially necessary if editing a question
        self.UpdateGeneralQuestionFields()

        self.InitializeSpecificQuestionFields()

    def InitializeSpecificQuestionFields(self):
        # Specific Question Properties Frame
        self.specificQuestionFieldsFrame = tk.LabelFrame(
            self.root, text="Specific Question Properties", padx=10, pady=10
        )
        self.specificQuestionFieldsFrame.pack(
            fill="both", expand=True, padx=10, pady=10
        )
        self.tree = None
        # Initialize specific properties with default type
        self.UpdateSpecificQuestionFields()
        # Initialize Advanced fields checkbox
        self.isSpecificAdvancedCheckBox = tk.Checkbutton(
            self.root,
            text="Show Specific Question Advanced Fields",
            variable=self.isShowingSpecificAdvancedFeatures,
            command=self.UpdateSpecificQuestionFields,
        )
        # currently disabled as these features are not yet implemented
        self.isSpecificAdvancedCheckBox.config(state="disabled")
        self.isSpecificAdvancedCheckBox.pack(pady=5)

        # Submit Button
        self.submitQuestionButton = tk.Button(
            self.root, text="Add Question", command=self.SubmitQuestion
        )
        self.submitQuestionButton.pack(pady=10)

    def InitializeGeneralFields(self):

        # create frame to organize general fields
        self.generalQuestionFieldsFrame = tk.LabelFrame(
            self.root, text="General Properties", padx=10, pady=10
        )
        self.generalQuestionFieldsFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # create radio button to toggle advanced fields
        self.generalAdvancedRadioButton = tk.Checkbutton(
            self.root,
            text="Show General Questions Advanced Fields",
            variable=self.isShowingGeneralAdvancedFeatures,
            command=self.UpdateGeneralQuestionFields,
        )
        # currently not implement, so disabled
        self.generalAdvancedRadioButton.config(state="disabled")
        self.generalAdvancedRadioButton.pack()

    def __CreateGeneralFields(self):
        # Create frame for general fields to live in
        tk.Label(self.generalQuestionFieldsFrame, text="Question Type:").grid(
            row=0, column=0, sticky="w"
        )

        self.__CreateQuestionTypeComboBox()

        self.__CreateGeneralFieldEntries()

    def __CreateGeneralFieldEntries(self):

        # add combox to list of all general fields
        self.generalQuestionFields["QuestionType"] = self.questionTypeComboBox

        fieldsToUse = (
            self.minimumGeneralFields
            if not self.isShowingGeneralAdvancedFeatures.get()
            else self.advancedGeneralFields
        )

        # this method dynamically creates fields from the following given arguments
        self.__CreateEntryFieldsFromArgs(
            fieldsToUse,
            self.generalQuestionFieldsFrame,
            self.isBothListBoxAndListDict,
            self.listBoxDict,
            self.generalQuestionFields,
        )

    def __CreateEntryFieldsFromArgs(
        self,
        fieldsToUse,
        frameToUse,
        isEditingQuestion,
        listBoxDict,
        listOfLabelsAndEntryObjects,
    ):
        for idx, (label, _) in enumerate(fieldsToUse, start=1):
            tk.Label(frameToUse, text=f"{label}:").grid(row=idx, column=0, sticky="w")
            entry = tk.Entry(frameToUse, width=50)
            if isEditingQuestion:
                entry.insert(0, listBoxDict[label])

            entry.grid(row=idx, column=1, sticky="w")
            listOfLabelsAndEntryObjects[label] = entry

    def __CreateQuestionTypeComboBox(self):
        # Create Combo box by hand for fun.
        # used to select question type
        questionTypes = [
            "Short Answer",
            "Written Response",
            "Matching",
            "Multiple Choice",
            "True or False",
            "MultiSelection",
            "Ordering",
        ]
        self.questionTypeComboBox = ttk.Combobox(
            self.generalQuestionFieldsFrame,
            values=questionTypes,
            width=23,
            state="readonly",
        )
        self.questionTypeComboBox.grid(row=0, column=1, sticky="w")

        # Use this to make sure the combobox updates when selected
        self.questionTypeComboBox.bind(
            "<<ComboboxSelected>>", self.UpdateSpecificQuestionFields
        )

        # if editing question, grab its question type and set the combobox to that setting and lock the combobox
        # , otherwise just start at default question type
        if self.isBothListBoxAndListDict:

            self.questionTypeComboBox.current(
                questionTypes.index(self.listBoxDict["QuestionType"])
            )
            self.questionTypeComboBox.state(["disabled"])
        else:
            self.questionTypeComboBox.current(0)

    def UpdateSpecificQuestionFields(self, event=None):
        """
        Updates the specific fields based on the selected question type and resizes the frame dynamically.
        """

        if self.isShowingSpecificAdvancedFeatures.get():
            self.generalAdvancedRadioButton.config(
                text="Hide Specific Question Type Advanced Fields"
            )
        else:
            self.generalAdvancedRadioButton.config(
                text="Show Specific Question Type Advanced Fields"
            )

        # get question type to determine what fields to show
        question_type = self.questionTypeComboBox.get()

        # Hide all fields in the specific frame before updating
        self.ClearSpecificQuestionFields()

        # Show only the fields relevant to the selected question type
        self.CreateSpecificQuestionFields(question_type)

        # Dynamically resize the specific frame to fit the newly displayed widgets
        self.specificQuestionFieldsFrame.update_idletasks()
        self.specificQuestionFieldsFrame.pack(
            fill="both", expand=True, padx=10, pady=10
        )

    def UpdateGeneralQuestionFields(self, event=None):
        """
        Updates the general fields based on the selected question type and resizes the frame dynamically.
        """

        if self.isShowingGeneralAdvancedFeatures.get():
            self.generalAdvancedRadioButton.config(
                text="Hide General Question Advanced Fields"
            )

        else:
            self.generalAdvancedRadioButton.config(
                text="Show General Question Advanced Fields"
            )

        # Hide all fields in the specific frame before updating
        self.ClearGeneralQuestionFields()

        # Show only the fields relevant to the selected question type
        self.__CreateGeneralFields()

        # Dynamically resize the specific frame to fit the newly displayed widgets
        self.generalQuestionFieldsFrame.update_idletasks()
        self.generalQuestionFieldsFrame.pack(fill="both", expand=True, padx=10, pady=10)

    def ClearSpecificQuestionFields(self):
        self.specificQuestionFields.clear()
        # Clear existing specific fields
        for widget in self.specificQuestionFieldsFrame.winfo_children():
            widget.destroy()

    def ClearGeneralQuestionFields(self):
        self.generalQuestionFields.clear()
        # Clear existing general fields
        for widget in self.generalQuestionFieldsFrame.winfo_children():
            widget.destroy()

    def __SyncComboBoxFields(self, updated_field, linked_field):
        """Synchronize values for TruePoints and FalsePoints"""
        updated_value = int(self.specificQuestionFields[updated_field].get())
        linked_value = 100 if updated_value == 0 else 0
        self.specificQuestionFields[linked_field].set(linked_value)
        self.root.update_idletasks()

    def __ValidateShortAnswerChars(self):
        """Validate that MaxChars > MinChars for Short Answer"""
        min_chars = int(self.specificQuestionFields["CharMinimumLength"].get())
        max_chars = int(self.specificQuestionFields["CharMaximumLength"].get())

        if max_chars <= min_chars:
            messagebox.showerror(
                "Input Error",
                "Maximum Characters must be greater than Minimum Characters.",
                parent=self.root,
            )
            self.specificQuestionFields["CharMaximumLength"].delete(0, "end")
            self.specificQuestionFields["CharMaximumLength"].insert(0, min_chars + 1)

    def CreateSpecificQuestionFields(self, question_type):
        specific_fields = self.getSpecificFieldsByQuestionType(question_type)

        for idx, (label, field_type) in enumerate(specific_fields):

            # Create Label for specified field
            tk.Label(self.specificQuestionFieldsFrame, text=f"{label}:").grid(
                row=idx, column=0, sticky="w"
            )

            # Check if the field has restrictions
            if (
                question_type in self.RESTRICTED_FIELDS
                and label in self.RESTRICTED_FIELDS[question_type]
            ):
                restriction = self.RESTRICTED_FIELDS[question_type][label]

                # Handle spinbox fields
                if restriction["type"] == "spinbox":
                    self.__CreateAndUpdateSpinBox(idx, label, restriction)

                # Handle combobox fields
                elif restriction["type"] == "combobox":
                    self.__CreateAndUpdateComboBox(idx, label, restriction)

            # Default Entry fields for unrestricted fields
            elif field_type == "str" or field_type == "int":
                self.__CreateAndUpdateEntry(idx, label)

            # TreeView (list fields)
            elif field_type == "list[str]" or field_type == "list[int]":
                self.__CreateTreeView(idx, label, question_type)

                self.__CreateTreeviewManagementButtons(idx, label)

    def __CreateTreeView(self, idx, label, question_type):
        # Create a Treeview widget
        columns = list(self.QuestionTypeFields[question_type].keys())

        self.tree = ttk.Treeview(
            self.specificQuestionFieldsFrame, columns=columns, show="headings"
        )

        # fill in values if editing a selected question
        if self.isBothListBoxAndListDict:
            fields = []
            for fieldName in self.QuestionTypeFields[
                self.generalQuestionFields["QuestionType"].get()
            ].keys():
                fields.append(fieldName)

            # zip values together to be displayed as a single row, as question objects store row values separately
            for element in zip(*[self.listBoxDict[field] for field in fields]):
                self.tree.insert("", "end", values=tuple(element))

        # Set a fixed width or adjust dynamically
        self.tree.grid(row=idx, column=1, sticky="w")

        # Set up each column with a heading
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Store Treeview in dictionary for later access
        self.specificQuestionFields[label] = self.tree

    def __CreateTreeviewManagementButtons(self, idx, label):
        # Add, Edit, Delete buttons for managing treeview entries
        button_frame = tk.Frame(self.specificQuestionFieldsFrame)
        button_frame.grid(row=idx, column=2, sticky="w")
        add_button = tk.Button(
            button_frame,
            text="Add",
            # this is a bit of a cheat that allows for something that calls for a method
            # identifier and not a method call, BUT you need a method call to give specific
            # arguments. Anonymous functions FTW. This can be seen in all button widgets
            command=lambda: self.openAddWindow(
                tk.Toplevel(self.root),
                self.questionTypeComboBox.get(),
                label,
                self.tree,
            ),
        )
        add_button.pack(side=tk.TOP, fill=tk.X, pady=1)
        edit_button = tk.Button(
            button_frame,
            text="Edit",
            command=lambda: self.openEditWindow(
                tk.Toplevel(self.root),
                self.questionTypeComboBox.get(),
                label,
                self.tree,
            ),
        )
        edit_button.pack(side=tk.TOP, fill=tk.X, pady=1)
        delete_button = tk.Button(
            button_frame,
            text="Delete",
            command=lambda l=self.tree: self.deleteSelectedRow(),
        )
        delete_button.pack(side=tk.TOP, fill=tk.X, pady=1)

    def __CreateAndUpdateEntry(self, idx, label):
        entry = tk.Entry(self.specificQuestionFieldsFrame, width=50)

        # if editing a question, insert the existing value
        if self.isBothListBoxAndListDict:
            entry.insert(0, self.listBoxDict[label])
        entry.grid(row=idx, column=1, sticky="w", padx=5, pady=2)

        # store for later iteration
        self.specificQuestionFields[label] = entry

    def __CreateAndUpdateComboBox(self, idx, label, restriction):
        combobox = ttk.Combobox(
            self.specificQuestionFieldsFrame,
            values=restriction["values"],
            state="readonly",
            width=10,
        )
        combobox.grid(row=idx, column=1, sticky="w", padx=5, pady=2)
        # Bind the linked field for True/False
        if "linked_field" in restriction:
            combobox.bind(
                "<<ComboboxSelected>>",
                lambda event, field=label: self.__SyncComboBoxFields(
                    field, restriction["linked_field"]
                ),
            )

        # set up option if editing existing question, otherwise just use default option
        if self.isBothListBoxAndListDict:
            combobox.set(self.listBoxDict[label])
        else:
            combobox.set(restriction["values"][0])  # Default to the first value
        self.specificQuestionFields[label] = combobox

    def __CreateAndUpdateSpinBox(self, idx, label, restriction):
        spinbox = tk.Spinbox(
            self.specificQuestionFieldsFrame,
            from_=restriction["min"],
            to=restriction["max"],
            width=5,
            command=self.__ValidateShortAnswerChars,
        )
        spinbox.grid(row=idx, column=1, sticky="w", padx=5, pady=2)

        # set up option if editing existing question, otherwise just use default option
        if self.isBothListBoxAndListDict:
            spinbox.delete(0, "end")
            spinbox.insert(0, self.listBoxDict[label])
        self.specificQuestionFields[label] = spinbox

    def openAddWindow(self, root, comboBox, label, tree):
        AddEditOptionWindow(root, comboBox, label, tree, False)

    def openEditWindow(
        self,
        root,
        comboBox,
        label,
        tree,
    ):

        # do not allow program to open edit window if user has not selected an option in the treeview
        if self.tree.selection() != ():
            currentIndex = self.tree.index(self.tree.selection()[0]) + 1
            # ^^^ convert to match index as matches are 1-indexed
            # hence the plus 1 to retrieving the index.
            AddEditOptionWindow(
                root, comboBox, label, tree, True, currentIndex=currentIndex
            )
        else:
            messagebox.showerror(
                "No Option Selected!",
                "Please select an options before pressing this button",
                parent=self.root,
            )

    def deleteSelectedRow(self):
        """Delete the selected row from the Treeview after confirmation"""
        selected_items = self.tree.selection()

        # make sure user has selected an item before trying to delete nothing
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select an item to delete.", parent=self.root
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete the selected entry?",
            parent=self.root,
        )
        if confirm:
            for item in selected_items:
                self.tree.delete(item)

    def getSpecificFieldsByQuestionType(self, question_type):
        # Define question-specific fields

        QuestionTypeFields = None
        if self.isShowingSpecificAdvancedFeatures.get():
            # advanced fields for the power user
            QuestionTypeFields = self.AdvancedQuestionTypeFieldsNames
        else:
            # bare minimum fields for most users
            QuestionTypeFields = self.GeneralQuestionTypeFieldsNames

        return QuestionTypeFields[question_type]

    def SubmitQuestion(self):
        # Gather general field values

        general_data = self.ParseGeneralDataEntries()

        specific_data = self.ParseSpecificDataEntries(general_data)

        # Validate specific fields using the corresponding function
        question_type = general_data["QuestionType"]

        # Validate inputs, exit method to prevent parsing if invalid input.
        if not self.__ValidateInputs(question_type, general_data, specific_data):
            return

        self.ReturnParsedInputAndDie(general_data, specific_data)

    def __ValidateInputs(self, question_type, general_data, specific_data):

        # if restricted field, check to see if value is in range
        if question_type in self.VALIDATION_FUNCTIONS:
            is_valid, error_message = self.VALIDATION_FUNCTIONS[question_type](
                specific_data
            )
            if not is_valid:
                messagebox.showerror(
                    "Validation Error", error_message, parent=self.root
                )
                return False

        # check to see if bare minimum general question fields are filled
        if not general_data["QuestionType"] or not general_data["QuestionText"]:
            messagebox.showerror(
                "Input Error",
                f"Please fill in all required general fields.\n QuestionType:"
                f"{general_data["QuestionType"] if general_data["QuestionType"] else "None Selected"}\n"
                f"QuestionText:"
                f"{general_data["QuestionText"] if general_data["QuestionText"] else "None Entered"}",
                parent=self.root,
            )
            return False

        # check bare minimum specific question fields are filled.
        if not self.CheckRequiredFields(
            specific_data,
            self.QuestionTypeFields[general_data["QuestionType"]],
            general_data["QuestionType"],
        ):
            return False
        return True

    def ReturnParsedInputAndDie(self, general_data, specific_data):
        # no need for the window now, so kill it.
        question_data = {**general_data, **specific_data}
        self.ReturnValueAcceptingFunction(question_data)
        self.root.destroy()

    def ParseGeneralDataEntries(self):
        general_data = {}
        for key, field in self.generalQuestionFields.items():
            general_data[key] = field.get() if field.get() != "" else None
        general_data["QuestionType"] = self.questionTypeComboBox.get()
        return general_data

    def ParseSpecificDataEntries(self, general_data):
        # Specific field values
        specific_data = {}
        for key, field in self.specificQuestionFields.items():
            if key in general_data:
                continue  # Skip general fields
            if isinstance(field, tk.Entry):  # get single entry fields
                specific_data[key] = (
                    field.get() if field.get() != "" else None
                )  # use None to utilize question class coding
            elif isinstance(
                field, ttk.Treeview
            ):  # get the current options users have created

                self.ParseTreeview(general_data, specific_data)

        return specific_data

    def ParseTreeview(self, general_data, specific_data):
        questionSpecificFields = self.QuestionTypeFields[
            general_data["QuestionType"]
        ].keys()

        for row_id in self.tree.get_children():
            row_values = self.tree.item(row_id, "values")
            for keys, values in zip(
                questionSpecificFields, row_values
            ):  # the list and row values here SHOULD be in the
                #  same order if setup properly

                try:
                    specific_data[keys].append(values)
                except:
                    specific_data[keys] = [values]

    questionTypeAndRequiredParameterList = {
        "Written Response": None,
        "Short Answer": ["Answers", "CharMinimumLength", "CharMaximumLength"],
        "Multiple Choice": ["ListOfOptions"],
        "MultiSelection": ["Options"],
        "Matching": ["ListOfMatches"],
        "Ordering": ["ListOfItems"],
        "True or False": ["TruePoints", "FalsePoints"],
    }

    questionsNeedingCSVCounting = [
        "Short Answer",
        "Multiple Choice",
        "MultiSelection" "Matching",
    ]

    def __ValidateShortAnswer(self, data):
        min_chars = int(data.get("CharMinimumLength", 0))
        max_chars = int(data.get("CharMaximumLength", 0))

        if min_chars < 1:
            return False, "Minimum Characters must be at least 1."
        if max_chars > 200:
            return False, "Maximum Characters cannot exceed 200."
        if max_chars <= min_chars:
            return False, "Maximum Characters must be greater than Minimum Characters."
        return True, None

    def __ValidateTrueOrFalse(self, data):
        true_points = int(data.get("TruePoints", 0))
        false_points = int(data.get("FalsePoints", 0))

        if true_points not in [0, 100] or false_points not in [0, 100]:
            return False, "TruePoints and FalsePoints must be either 0 or 100."
        if true_points == false_points:
            return False, "TruePoints and FalsePoints must be different."
        return True, None

    # first draft of this method created by ChatGPT 4o at 1035 pm EDS 11/2/24

    def CheckRequiredFields(self, data, required_keys, QuestionType):
        """
        Checks if the required keys in a dictionary have non-empty values.

        :param QuestionType: str - containing the QuestionType
        :param data: dict - The dictionary containing data to check.
        :param required_keys: list - List of keys that are required.
        :return: bool - True if all required keys are present and non-empty, False otherwise.
        """
        if required_keys is None:
            return True

        missing_fields = AddQuestionWindow.DetermineMissingGeneralKeys(
            data, required_keys
        )

        if missing_fields:
            # Join missing fields into a message and display the error message
            messagebox.showerror(
                "General Question Data Input Error",
                f"Please fill in all required general fields:\n"
                + "\n".join(missing_fields),
                parent=self.root,
            )
            return False

        return True

    @staticmethod
    def DetermineSpecificMissingKeys(QuestionType, data):
        csv_length_mismatch = []
        # Check if CSV list fields have matching lengths
        if QuestionType in AddQuestionWindow.questionsNeedingCSVCounting:
            fields_group = AddQuestionWindow.questionTypeAndRequiredParameterList[
                QuestionType
            ]

            # This code makes sure that questions requiring a zip function
            # on the various input fields. This assures that the user is
            # inputting the correct number of arguments to prevent malformed
            # questions
            lengths = [len(data[key]) for key in fields_group]

            if len(set(lengths)) > 1:  # Check if all lengths are equal
                csv_length_mismatch.append(", ".join(fields_group))
        return csv_length_mismatch

    @staticmethod
    def DetermineMissingGeneralKeys(data, required_keys):
        missing_fields = []
        for key in required_keys:
            if not data.get(key):
                # Append a message indicating if the field is missing or empty
                missing_fields.append(
                    f"{key}: {'None Selected' if data.get(key) is None else 'None Entered'}"
                )
        return missing_fields

    # todo Currently, there is no logic that specifically checks to see if you left out a value in question specific
    #    fields. This needs to be changed with the following method.

    @staticmethod
    def DetermineMissingSpecificKeys(self, data, requiredKeys):
        raise NotImplemented
