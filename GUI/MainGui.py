import json
import tkinter as tk
from tkinter import messagebox, Menu, filedialog
from typing import TextIO
from GUI.AddQuestionWindow import AddQuestionWindow
from Questions.QuestionFactory import QuestionFactory


class QuestionManagerApp:
    """
    The Main Screen Class for this program
    """

    def __init__(self, root: tk.Tk):
        """
        initializes the main screen for this program

        :param root: the TK object used to run tkinter guis
        """
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&initialize variables for later use&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

        # ***********************************Used for Editing Questions ***********************************************
        # this is used to pass the currently edited question's listbox index IF it needs to be replaced.
        self.editQuestionListboxIndex = None
        # this is used to pass the currently edited question's list index IF it needs to be replaced.
        self.editQuestionListIndex = None
        # *************************************************************************************************************

        # *******************************GUI Widgets ******************************************************************
        # These buttons are used to interact with the elements found in the questionListBox
        self.deleteButton = None
        self.editButton = None
        self.addButton = None
        self.QuestionID = tk.StringVar()
        # The listbox widget containing current existing questions.
        self.questionListbox = None

        # The file menu that contains the various commands expected. Load/Save/Export in this case
        self.fileMenu = None
        self.menubar = None
        # dict that links together the question listbox entries, Question objects, a dict containing {questionListBoxEntry :
        # [questionDataDict : Question object ]}. This allows for easier loading/saving/editing of question objects and the
        # corresponding entries in the instance variables questionDataDict, questions, self.questionListbox
        self.questionDataDict = {}

        self.questions = []  # List to hold Question objects

        self.questionFactory = QuestionFactory()  # used to create Question Objects

        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

        # Time to actually make the widgets for this window
        self.__InitializeMainWindow(root)

    def __InitializeMainWindow(self, root: tk.Tk):
        """
        Initializes all main menu widgets and stores them for later use

        :param root: the Tk object and TCL interpreter being used currently
        """
        # basic tkinter window config
        self.root = root
        self.root.title("Question Manager")

        # Methods to set up the required widgets
        self.__CreateMenu()
        self.__AddListBoxAndButtons(root)

    def __AddListBoxAndButtons(self, root: tk.Tk):
        """
        Creates the necessary buttons to interact with the main screen.

        :param root: the Tk object and TCL interpreter being used currently
        """
        # Listbox to display questions
        self.questionListbox = tk.Listbox(root, width=100, height=15)
        self.questionListbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(root, text="Question ID:", anchor="w").pack(side=tk.LEFT, padx=5)
        self.question_id_entry = tk.Entry(root, width=20, textvariable=self.QuestionID)
        self.question_id_entry.pack(side=tk.LEFT, padx=5)

        # Buttons to add, edit, and delete questions
        self.addButton = tk.Button(
            root, text="Add Question", command=self.__OpenAddQuestionWindow
        )
        self.addButton.pack(side=tk.LEFT, padx=10, pady=10)
        self.editButton = tk.Button(
            root, text="Edit Question", command=self.__OpenEditQuestionWindow
        )
        self.editButton.pack(side=tk.LEFT, padx=10, pady=10)
        self.deleteButton = tk.Button(
            root, text="Delete Question", command=self.__DeleteSelectedQuestion
        )
        self.deleteButton.pack(side=tk.RIGHT, padx=10, pady=10)
        self.editQuestionListboxIndex = 0

    def __CreateMenu(self):
        """
        Creates the menu at the top of the window that traditionally hold File, Edit, etc.
        """
        # create menu bar to hold menus
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # create new menu within menubar
        self.fileMenu = Menu(self.menubar)

        # config the new above menu
        self.fileMenu.add_command(
            label="Export To D2L-Friendly Quiz CSV", command=self.__SaveToFile
        )
        self.fileMenu.add_command(
            label="Save In-Progress Quiz", command=self.__SaveToDQIP
        )
        self.fileMenu.add_command(label="Load", command=self.__LoadFromDQIP)

        # add fileMenu to the existing menubar
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

    def __ClearQuiz(self):
        """
        Clears the current quiz.
        """
        # These three things are vital to resetting the quiz, especially when using loading new quiz in-progress files
        self.questionDataDict.clear()
        self.questions.clear()
        self.questionListbox.delete(0, tk.END)
        self.question_id_entry.delete(0, tk.END)

    def __LoadFromDQIP(self):
        """
        Load a DQIP file into the program to begin editing a quiz
        """
        # If quiz is unsaved, then warn user before loading file
        if self.questionListbox.size() != 0 and not messagebox.askokcancel(
                "Unsaved Quiz",
                "You have an unsaved Quiz. Continuing will wipe all current"
                " progress. Continue?",
        ):
            return

        # get the user to choose the file path for file to be loaded
        file_path = filedialog.askopenfilename(
            defaultextension=".dqip",
            filetypes=[("D2L Quiz In-Progress Files", "*.dqip"), ("All files", "*.*")],
        )

        # if no file is selected, no need to wipe and load GUI, so just return
        if file_path == "":
            return

        # Clear the quiz fields.
        self.__ClearQuiz()

        # open chosen file and load as JSON
        with open(file_path, "r") as file:
            JSONData = json.loads(file.read())

        # load values from JSON into the appropriate fields.
        self.__InsertLoadedValuesIntoQuiz(JSONData)

    def __InsertLoadedValuesIntoQuiz(self, JSONData: dict):
        """
        inserts the values in the loaded DQIP file into the appropriate fields for editing

        :param JSONData: the parsed JSON Data to be read
        """
        # loop through each value found in the JSON. The keys are simple integers and are not necessary for loading the
        # quiz.

        # ################ THE BELOW CODE IS A TEMPORARY< HACKY WAY TO ADD QUESTION ID################################
        values = JSONData["1"]["QuestionData"]
        self.question_id_entry.insert(
            0, (f"{values["ID"]}" if "ID" in values.keys() else "")
        )
        ##################### PLEASE REPLACE THE ABOVE CODE IN ADVANCED SETTINGS REFACTOR###########################
        for values in JSONData.values():
            # add question summary here to display to the user in the listbox
            self.questionListbox.insert(tk.END, values["QuestionSummary"])

            # create a question object from the QuestionData to be used when making the CSV file
            temp = self.questionFactory.CreateNewQuestionObjectFromJSON(
                values["QuestionData"]
            )

            # append the question object to the list of objects to be saved in the CSV export option
            self.questions.append(temp)

            # add an entry to the questionDataDict to serve as a link between all windows
            self.questionDataDict[values["QuestionSummary"]] = [
                values["QuestionData"],
                temp,
            ]

    def __SaveToDQIP(self):
        """
        Saves the currently loaded quiz to a file for later editing or exporting.
        """
        # create a dict to store questions to be saved
        questionsToSave = {}

        # get all savable questions
        self.__CollectAllSavableQuestions(questionsToSave)

        # get the filepath the user wants to use to save this current quiz
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dqip",
            filetypes=[("D2L Quiz In-Progress Files", "*.dqip"), ("All files", "*.*")],
        )

        # if filepath is empty, we cannot save. Return control to the user.
        if file_path == "":
            return

        # convert the dict to be saved into a JSON string
        savable = json.dumps(questionsToSave)

        # Open file that hold this quiz's data
        with open(file_path, "w") as file:
            file.write(savable)

    def __CollectAllSavableQuestions(self, questionsToSave: dict):
        """
        gathers all the questions and various metadata to be saved to a DQIP file

        :param questionsToSave: the dictionary to be filled with the question data
        """
        # adds all questions to a dict to be saved to the DQIP file
        for index, key in enumerate(self.questionListbox.get(0, tk.END), 1):
            ##############################HACKY WAY TO ADD ID TO QUESTIONS##############################################
            # TODO fix this hacky mess
            questionsToSave[index]["Question"].ID = self.QuestionID.get()
            questionsToSave[index]["QuestionData"]["ID"] = self.QuestionID.get()

            ##############################Refactor when adding advanced fields are added ###############################
            questionsToSave[index] = {
                "QuestionSummary": key,
                "QuestionData": self.questionDataDict[key][0],
                "Question": self.questionFactory.toDict(self.questionDataDict[key][1]),
            }

    def __SaveToFile(self):
        """
        Saves the current quiz to a D2l Friendly quiz CSV format
        """
        # ask user for a filepath to use to create a save file (CSV)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        # if filepath is empty, we cannot save. Return control to the user.
        if file_path == "":
            return

        # open filepath and create file (if non-existent) for saving the CSV
        with open(file_path, "w") as file:
            # saved the data to a CSV
            self.__SaveQuestionsToCSVFile(file)

    def __SaveQuestionsToCSVFile(self, file: TextIO):
        """
        exports the currently loaded quiz questions into the currently opened file

        :param file: a file object containing the filepath the user wants to use
        """
        for question in self.questions:
            # Write question CSV form to the file
            file.write(question.CreateQuestionCSVRepresentation())

            # serves new lines in this CSV file
            file.write(",,,,\n,,,,\n")

    def __onExit(self):
        """
        Exits programs
        """
        self.root.quit()

    def __OpenAddQuestionWindow(self):
        """
        Opens the add question window
        """
        # Opens the Add Question window and passes the callback to add questions
        AddQuestionWindow(self.root, self.__AddQuestion)

    def __OpenEditQuestionWindow(self):
        """
        Opens the edit question window
        """
        # first, make sure user has a question selected
        if self.questionListbox.curselection() != ():

            # initialize quiz for question editing
            questionData = self.__InitializeEditQuestionMode()

            # send data to be worked on by the AddQuestionWindow
            AddQuestionWindow(
                self.root,
                self.__EditQuestion,
                self.questionListbox,
                questionData,
            )
        else:
            messagebox.showerror(
                "No Question Selected",
                "Please select a question before pressing the edit button.",
            )

    def __InitializeEditQuestionMode(self):
        """
        use to prep the program to re-add the edited question in the appropriate data structures

        this is used to make sure that the question edited is re-added at the index it was selected from in the various
        data structures used in this file. This keeps track of the index
        :return: the dict storing the question data of the chosen question
        """

        # store the currently selected listbox element's index so that the newly edited question can be stored in the
        # same listbox location
        self.editQuestionListboxIndex = self.questionListbox.curselection()[0]
        # get the index of the specific question in the question list. this is used to assure the edited question appears
        # in the correct position (its previous position) in the CSV export format.
        questionIndex = [
            element
            for element in self.questions
            if element.CreateQuestionCSVRepresentation()
               == self.questionListbox.get(self.editQuestionListboxIndex)
        ]
        # store the above question's index in the question list and store for proper storage of edited question
        self.editQuestionListIndex = self.questions.index(questionIndex[0])
        # get the chosen question's data
        questionData = self.questionDataDict[self.questionListbox.get(tk.ACTIVE)][0]
        return questionData

    def __AddQuestion(self, question_data: dict):
        """
        Adds a question entry to the list of questions and displays it in the Listbox.
        """

        questionToAdd, questionType, question_summary = (
            self.__PrepForAddingOrEditingQuestion(question_data)
        )

        # store question object in question list
        self.questions.append(questionToAdd)

        # link question string to data dict to return to AddQuestionWindow when editing that question.
        self.questionDataDict[question_summary] = [question_data, questionToAdd]

        # insert string representation into the listbox for visual user feedback
        self.questionListbox.insert(tk.END, question_summary)

    def __PrepForAddingOrEditingQuestion(self, question_data: dict):
        """
        prepare the program to add/edit a question

        This method does the bookkeeping necessary to succesfully add and edit questions, while adding them to the
        appropriate tracking data structures.


        :param question_data: the dict holding the chosen question's data, if editing a question
        :return: a question object, a string containing the question type, and a question data dict for that question.
        """
        # create a string representation of the current question
        questionString = ""

        for key, value in question_data.items():
            questionString += f"{key}={value},"
        # Append the Basic Question Object to the questions list
        questionType = question_data["QuestionType"]

        # Not needed for creating a question (at least not in the dict)
        del question_data["QuestionType"]
        # create question object
        questionToAdd = self.questionFactory.CreateNewQuestionObject(
            questionType, **question_data
        )

        # Display a brief summary of the question in the Listbox
        question_summary = f"{questionToAdd}"

        # This is needed further down the chain so add it back
        # is there a better way? sure. Do I care at this second? no.
        question_data["QuestionType"] = questionType

        return questionToAdd, questionType, question_summary

    def __EditQuestion(self, question_data: dict):
        """
        Adds a question entry to the list of questions and displays it in the Listbox.
        """

        # Generate data needed to edit quiz
        questionToAdd, questionType, question_summary = (
            self.__PrepForAddingOrEditingQuestion(question_data)
        )

        # remove the selected question's old form from program
        self.__DeleteSelectedQuestion(specificIndex=self.editQuestionListboxIndex)

        # link question string to data dict to return to AddQuestionWindow when editing that question.
        self.questionDataDict[question_summary] = [question_data, questionToAdd]

        # insert new question object in old one's place
        self.questions.insert(self.editQuestionListIndex, questionToAdd)

        # insert edited question string into old question's string place
        self.questionListbox.insert(self.editQuestionListboxIndex, question_summary)

    def __DeleteSelectedQuestion(self, specificIndex: int = None):
        """
        Deletes the selected question from the list and the Listbox.
        """

        # used to differentiate between method callers. The user must have a selected question to use this via the delete
        # function. The program, however, can simply send it an index to delete.
        # This is handy as handling where exactly to put edited questions can be unwieldy with the current implementation
        if not specificIndex and specificIndex != 0:
            selected_index = self.questionListbox.curselection()[0]
        else:
            selected_index = specificIndex

        # nothing is selected, or the program did not send an index. Give a warning message and move on.
        if selected_index == () and specificIndex is None:
            messagebox.showwarning(
                "Selection Error",
                f"Please select a question to delete. index {selected_index} ",
            )
            return

        # delete the selected question from the important collections
        del self.questions[selected_index]
        del self.questionDataDict[self.questionListbox.get(selected_index)]
        self.questionListbox.delete(selected_index)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionManagerApp(root)
    root.mainloop()
