"""
Project Name: D2LQuizCreator
File Name: TESTINGONLY.py
Date Created: 11/23/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/23/2024
"""

from tkinter.filedialog import askopenfilename

from DocxParser import DocxParser

if __name__ == "__main__":

    docParser = DocxParser(
        askopenfilename(
            initialdir="DocxQuizzesToBeMade",
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All files", "*.*")],
        )
    )

    docParser.ParseBasisDocxIntoText()
    docParser.ParseTextIntoQuestions()
    questionObjects = []
    for questions in docParser.parsedQuestions:
        questionObjects.append(docParser.create_question_object(questions))
    docParser.SaveToFile(questionObjects)
