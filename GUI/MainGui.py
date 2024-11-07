import tkinter as tk
from tkinter import messagebox, Menu, filedialog
from Questions.QuestionFactory import QuestionFactory
from GUI.AddQuestionWindow import AddQuestionWindow


class QuestionManagerApp:
    def __init__(self, root):

        self.questionFactory = QuestionFactory()

        self.root = root
        self.root.title("Question Manager")
        self.questions = []  # List to hold question data dictionaries

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.fileMenu = Menu(self.menubar)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        self.fileMenu.add_command(label="Save", command=self.__doBoth)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        # Listbox to display questions
        self.question_listbox = tk.Listbox(root, width=100, height=15)
        self.question_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons to add and delete questions
        self.add_button = tk.Button(root, text="Add Question", command=self.open_add_question_window)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Delete Question", command=self.delete_selected_question)
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def onExit(self):
        self.root.quit()

    def __PrintListBoxToConsole(self):
        for entry in self.questions:
            print(entry)

    def __doBoth(self):
        self.__PrintListBoxToConsole()
        self.SaveToFile()

    def SaveToFile(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All files", "*.*")]
        )
        with open(file_path, "a") as file:
            for question in self.questions:
                print(question.CreateQuestionCSVRepresentation())
                file.write(question.CreateQuestionCSVRepresentation())
                file.write(",,,,\n,,,,\n")

    def open_add_question_window(self):
        # Opens the Add Question window and passes the callback to add questions
        AddQuestionWindow(self.root, self.add_question_to_list)

    def add_question_to_list(self, question_data):
        """
        Adds a question entry to the list of questions and displays it in the Listbox.
        """

        questionString = ""
        for key, value in question_data.items():
            questionString += f"{key}={value},"

        # Append the Basic Question Object to the questions list
        questionType = question_data["QuestionType"]
        del question_data["QuestionType"]
        questionToAdd = self.questionFactory.CreateNewQuestionObject(questionType, **question_data)
        self.questions.append(questionToAdd)

        # Display a brief summary of the question in the Listbox
        question_summary = f"{questionToAdd}"
        self.question_listbox.insert(tk.END, question_summary)

    def delete_selected_question(self):
        """
        Deletes the selected question from the list and the Listbox.
        """
        selected_index = self.question_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a question to delete.")
            return

        # Remove the question from both the Listbox and the questions list
        index = selected_index[0]
        del self.questions[index]
        self.question_listbox.delete(index)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionManagerApp(root)
    root.mainloop()
