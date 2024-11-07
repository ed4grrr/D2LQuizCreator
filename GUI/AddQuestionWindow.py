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


class AddQuestionWindow:
    def __init__(self, root, ReturnValueAcceptingFunction):
        self.questionTypeComboBox = None
        self.root = tk.Toplevel(root)
        self.root.title("Add New Question")
        self.ReturnValueAcceptingFunction = ReturnValueAcceptingFunction  # Callback to notify the main screen
        self.isShowingSpecificAdvancedFeatures = tk.BooleanVar(
            value=False)  # bool variable linked to special advance radio button
        self.isShowingGeneralAdvancedFeatures = tk.BooleanVar(
            value=False)  # bool variable linked to general advance radio button

        # General Properties Section
        self.generalQuestionFieldsFrame = tk.LabelFrame(self.root, text="General Properties", padx=10, pady=10)

        self.generalQuestionFieldsFrame.pack(fill="both", expand=True, padx=10, pady=10)
        self.generalAdvancedRadioButton = tk.Checkbutton(self.root, text="Show General Questions Advanced Fields",
                                                         variable=self.isShowingGeneralAdvancedFeatures,
                                                         command=self.UpdateGeneralQuestionFields)
        self.generalAdvancedRadioButton.config(state="disabled")
        self.generalAdvancedRadioButton.pack()

        # General Fields
        self.generalQuestionFields = {}
        self.specificQuestionFields = {}
        self.UpdateGeneralQuestionFields()

        # Specific Question Properties Frame
        self.specificQuestionFieldsFrame = tk.LabelFrame(self.root, text="Specific Question Properties", padx=10,
                                                         pady=10)
        self.specificQuestionFieldsFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize specific properties with default type
        self.UpdateSpecificQuestionFields()

        self.isSpecificAdvancedRadioButton = tk.Checkbutton(self.root, text="Show Specific Question Advanced Fields",
                                                            variable=self.isShowingSpecificAdvancedFeatures,
                                                            command=self.UpdateSpecificQuestionFields)
        self.isSpecificAdvancedRadioButton.config(state="disabled")
        self.isSpecificAdvancedRadioButton.pack(pady=5)

        # Submit Button
        self.submitQuestionButton = tk.Button(self.root, text="Add Question", command=self.SubmitQuestion)
        self.submitQuestionButton.pack(pady=10)

    def createGeneralFields(self):
        # Create frame for general fields to live in
        tk.Label(self.generalQuestionFieldsFrame, text="Question Type:").grid(row=0, column=0, sticky="w")

        # Create Combo box by hand for fun.
        # used to select question type
        self.questionTypeComboBox = ttk.Combobox(self.generalQuestionFieldsFrame, values=[
            "Short Answer", "Written Response", "Matching",
            "Multiple Choice", "True or False", "MultiSelection", "Ordering"
        ], width=23, state="readonly")
        self.questionTypeComboBox.grid(row=0, column=1, sticky="w")
        self.questionTypeComboBox.bind("<<ComboboxSelected>>", self.UpdateSpecificQuestionFields)
        self.questionTypeComboBox.current(0)
        self.generalQuestionFields["QuestionType"] = self.questionTypeComboBox

        advancedGeneralFields = [
            ("Title", "str"), ("QuestionText", "str"), ("Points", "int"),
            ("Difficulty", "int"), ("ID", "str"), ("ImagePath", "str"),
            ("Scoring", "str"), ("Hint", "str"), ("QuestionFeedback", "str")
        ]

        minimumGeneralFields = [("QuestionText", "str")]

        fieldsToUse = minimumGeneralFields if not self.isShowingGeneralAdvancedFeatures.get() else advancedGeneralFields

        for idx, (label, _) in enumerate(fieldsToUse, start=1):
            tk.Label(self.generalQuestionFieldsFrame, text=f"{label}:").grid(row=idx, column=0, sticky="w")
            entry = tk.Entry(self.generalQuestionFieldsFrame, width=50)
            entry.grid(row=idx, column=1, sticky="w")
            self.generalQuestionFields[label] = entry

    def UpdateSpecificQuestionFields(self, event=None):

        """
        Updates the specific fields based on the selected question type and resizes the frame dynamically.
        """

        if self.isShowingSpecificAdvancedFeatures.get():
            self.generalAdvancedRadioButton.config(text="Hide Specific Question Type Advanced Fields")
        else:
            self.generalAdvancedRadioButton.config(text="Show Specific Question Type Advanced Fields")

        question_type = self.questionTypeComboBox.get()

        # Hide all fields in the specific frame before updating
        self.ClearQuestionSpecificFields()

        # Show only the fields relevant to the selected question type
        self.CreateQuestionSpecificFields(question_type)

        # Dynamically resize the specific frame to fit the newly displayed widgets
        self.specificQuestionFieldsFrame.update_idletasks()
        self.specificQuestionFieldsFrame.pack(fill="both", expand=True, padx=10, pady=10)

    def UpdateGeneralQuestionFields(self, event=None):

        """
        Updates the general fields based on the selected question type and resizes the frame dynamically.
        """

        if self.isShowingGeneralAdvancedFeatures.get():
            self.generalAdvancedRadioButton.config(text="Hide General Question Advanced Fields")

        else:
            self.generalAdvancedRadioButton.config(text="Show General Question Advanced Fields")

        # Hide all fields in the specific frame before updating
        self.ClearQuestionGeneralFields()

        # Show only the fields relevant to the selected question type
        self.createGeneralFields()

        # Dynamically resize the specific frame to fit the newly displayed widgets
        self.generalQuestionFieldsFrame.update_idletasks()
        self.generalQuestionFieldsFrame.pack(fill="both", expand=True, padx=10, pady=10)

    def ClearQuestionSpecificFields(self):
        self.specificQuestionFields.clear()
        # Clear existing specific fields
        for widget in self.specificQuestionFieldsFrame.winfo_children():
            widget.destroy()

    def ClearQuestionGeneralFields(self):
        self.generalQuestionFields.clear()
        # Clear existing specific fields
        for widget in self.generalQuestionFieldsFrame.winfo_children():
            widget.destroy()

    def CreateQuestionSpecificFields(self, question_type):
        # Define fields based on question type
        specific_fields = self.getSpecificFieldsByQuestionType(question_type)
        # Create fields for each specific question property
        for idx, (label, field_type) in enumerate(specific_fields):
            tk.Label(self.specificQuestionFieldsFrame, text=f"{label}:").grid(row=idx, column=0, sticky="w")
            if field_type == "str" or field_type == "int":
                entry = tk.Entry(self.specificQuestionFieldsFrame, width=50)
                entry.grid(row=idx, column=1, sticky="w")
            elif field_type == "list[str]" or field_type == "list[int]":
                entry = tk.Text(self.specificQuestionFieldsFrame, height=2, width=50)
                entry.grid(row=idx, column=1, sticky="w")
            self.specificQuestionFields[label] = entry

    def getSpecificFieldsByQuestionType(self, question_type):
        # Define question-specific fields
        if self.isShowingSpecificAdvancedFeatures.get():
            # advanced fields for the power user
            QuestionTypeFields = {
                "Short Answer": [
                    ("Answers", "list[str]"), ("PointsPerAnswer", "list[int]"),
                    ("RegExsForAnswers", "list[str]"), ("CharMinimumLength", "int"),
                    ("CharMaximumLength", "int")
                ],
                "Written Response": [
                    ("InitialText", "str"), ("AnswerKey", "str")
                ],
                "Matching": [
                    ("ListOfMatchNumbers", "list[str]"), ("ListOfMatchingText", "list[str]"),
                    ("ListOfChoiceNumbers", "list[str]"),
                    ("ListOfChoiceText", "list[str]")
                ],
                "Multiple Choice": [
                    ("ListOfOptions", "list[str]"), ("ListOfPointsPerOption", "list[int]"),
                    ("ListOfFeedBack", "list[str]")
                ],
                "True or False": [
                    ("TruePoints", "int"), ("FalsePoints", "int"),
                    ("TrueFeedback", "str"), ("FalseFeedback", "str")
                ],
                "MultiSelection": [
                    ("PointsPerAnswer", "list[int]"), ("OptionText", "list[str]"), ("OptionFeedback", "list[str]")
                ],
                "Ordering": [
                    ("ListOfItems", "list[str]"), ("ListOfIsHTML", "list[str]"), ("ListOfFeedback", "list[str]")
                ]
            }
        else:
            # bare minimum fields for most users
            QuestionTypeFields = {
                "Short Answer": [
                    ("Answers", "list[str]"), ("PointsPerAnswer", "list[int]"),
                    ("CharMinimumLength", "int"), ("CharMaximumLength", "int")
                ],
                "Written Response": [
                    ("InitialText", "str"), ("AnswerKey", "str")
                ],
                "Matching": [
                    ("ListOfMatchNumbers", "list[str]"), ("ListOfMatchingText", "list[str]"),
                    ("ListOfChoiceNumbers", "list[str]"),
                    ("ListOfChoiceText", "list[str]")
                ],
                "Multiple Choice": [
                    ("ListOfOptions", "list[str]"), ("ListOfPointsPerOption", "list[int]")

                ],
                "True or False": [
                    ("TruePoints", "int"), ("FalsePoints", "int")
                ],
                "MultiSelection": [
                    ("PointsPerAnswer", "list[int]"), ("OptionText", "list[str]")
                ],
                "Ordering": [
                    ("ListOfItems", "list[str]")
                ]
            }

        return QuestionTypeFields[question_type]

    def SubmitQuestion(self):
        # Gather general field values

        general_data = self.ParseGeneralDataEntries()

        specific_data = self.ParseSpecificDataEntries(general_data)

        if not general_data["QuestionType"] or not general_data["QuestionText"]:
            messagebox.showerror("Input Error", f"Please fill in all required general fields.\n QuestionType:"
                                                f"{general_data["QuestionType"] if general_data["QuestionType"] else "None Selected"}\n"
                                                f"QuestionText:"
                                                f"{general_data["QuestionText"] if general_data["QuestionText"] else "None Entered"}")
            return
        if not self.CheckRequiredFields(specific_data,
                                        self.questionTypeAndRequiredParameterList[general_data['QuestionType']],
                                        general_data["QuestionType"]):
            return

        self.ReturnParsedInputAndDie(general_data, specific_data)

    def ReturnParsedInputAndDie(self, general_data, specific_data):
        question_data = {**general_data, **specific_data}
        self.ReturnValueAcceptingFunction(question_data)
        self.root.destroy()

    def ParseGeneralDataEntries(self):
        general_data = {}
        for key, field in self.generalQuestionFields.items():
            general_data[key] = field.get() if field.get() != "" else None
        general_data['QuestionType'] = self.questionTypeComboBox.get()
        return general_data

    def ParseSpecificDataEntries(self, general_data):
        # Specific field values
        specific_data = {}
        for key, field in self.specificQuestionFields.items():
            if key in general_data:
                continue  # Skip general fields
            if isinstance(field, tk.Entry):  # get single entry fields
                specific_data[
                    key] = field.get() if field.get() != "" else None  # use None to utilize question class coding
            elif isinstance(field, tk.Text):  # get multiple entry fields
                specific_data[key] = field.get("1.0", tk.END).strip().split(",") \
                    if field.get("1.0", tk.END).strip().split(",") != [
                    ""] else None  # use None to utilize question class coding

        return specific_data

    questionTypeAndRequiredParameterList = {
        "Written Response": None,
        "Short Answer": ["Answers", "PointsPerAnswer"],
        "Multiple Choice": ["ListOfOptions", "ListOfPointsPerOption"],
        "MultiSelection": ["PointsPerAnswer", "OptionText"],
        "Matching": ["ListOfMatchingText", "ListOfMatchNumbers", "ListOfChoiceText", "ListOfChoiceNumbers"],
        "Ordering": ["ListOfItems"],
        "True or False": ["TruePoints", "FalsePoints"],
    }

    questionsNeedingCSVCounting = [
        "Short Answer",
        "Multiple Choice",
        "MultiSelection"
        "Matching"
    ]

    # first draft of this method created by ChatGPT 4o at 1035 pm EDS 11/2/24
    @staticmethod
    def CheckRequiredFields(data, required_keys, QuestionType):
        """
        Checks if the required keys in a dictionary have non-empty values.

        :param QuestionType: str - containing the QuestionType
        :param data: dict - The dictionary containing data to check.
        :param required_keys: list - List of keys that are required.
        :return: bool - True if all required keys are present and non-empty, False otherwise.
        """
        if required_keys is None:
            return True

        missing_fields = AddQuestionWindow.DetermineMissingGeneralKeys(data, required_keys)

        csv_length_mismatch = AddQuestionWindow.DetermineSpecificMissingKeys(QuestionType, data)

        if missing_fields:
            # Join missing fields into a message and display the error message
            messagebox.showerror("General Question Data Input Error",
                                 f"Please fill in all required general fields:\n" + "\n".join(missing_fields))
            return False

        # Display an error if there are any CSV length mismatches
        if csv_length_mismatch:
            messagebox.showerror(
                "Question Specific Data Input Error",
                "The following fields must have an equal number of CSV entries:\n" + "\n".join(csv_length_mismatch)
            )
            return False

        return True

    @staticmethod
    def DetermineSpecificMissingKeys(QuestionType, data):
        csv_length_mismatch = []
        # Check if CSV list fields have matching lengths
        if QuestionType in AddQuestionWindow.questionsNeedingCSVCounting:
            fields_group = AddQuestionWindow.questionTypeAndRequiredParameterList[QuestionType]

            # This code makes sure that questions requiring a zip function
            # on the various input fields. This assures that the user is
            # inputting the correct number of arguments to prevent malformed
            # questions
            lengths = [len(data[key]) for key in fields_group]
            # print(f"currentLengths for {fields_group}: {lengths}")
            if len(set(lengths)) > 1:  # Check if all lengths are equal
                csv_length_mismatch.append(", ".join(fields_group))
        return csv_length_mismatch

    @staticmethod
    def DetermineMissingGeneralKeys(data, required_keys):
        missing_fields = []
        for key in required_keys:
            if not data.get(key):
                # Append a message indicating if the field is missing or empty
                missing_fields.append(f"{key}: {'None Selected' if data.get(key) is None else 'None Entered'}")
        return missing_fields

    # todo Currently, there is no logic that specifically checks to see if you left out a value in question specific
    #    fields. This needs to be changed with the following method.

    @staticmethod
    def DetermineMissingSpecificKeys(self, data, requiredKeys):
        raise NotImplemented
