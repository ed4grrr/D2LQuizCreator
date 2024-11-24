"""
Project Name: D2LQuizCreator
File Name: TESTINGONLY.py
Date Created: 11/23/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/23/2024
"""

from DocxParser import DocxParser

if __name__ == "__main__":
    docParser = DocxParser("DocxQuizzesToBeMade")

    docParser.ParseBasisDocxIntoText()
    docParser.ParseTextIntoQuestions()

    for questions in docParser.parsedQuestions:
        print(questions)
