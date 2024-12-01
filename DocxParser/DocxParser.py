"""
Project Name: pythonProject
File Name: DocxParser.py
Date Created: 11/4/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/4/2024
"""

import re
from fileinput import filename
from tkinter import filedialog
from typing import List, TextIO
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename

from Questions.QuestionTemplates import (
    BaseQuestion,
    MultipleChoiceQuestion,
    MultiSelectionQuestion,
    WrittenAnswerQuestion,
    ShortAnswerQuestion,
    MatchingQuestion,
    TrueFalseQuestion,
    OrderingQuestion,
)


class DocxParser:
    def __init__(self, currentDocPath):
        self.currentDocPath = currentDocPath
        self.listFullOfNewlineChars: list[str] = None
        self.text: str = None
        self.parsedQuestions: list[str] = None

    def ParseBasisDocxIntoText(self) -> str:
        with ZipFile(self.currentDocPath, "r") as docx:
            # Extract the document.xml which contains the text content
            with docx.open("word/document.xml") as document_xml:
                # Parse the XML content
                tree = ET.parse(document_xml)
                root = tree.getroot()

                # Define the namespace for the Word XML schema
                namespace = {
                    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                }

                # Extract paragraphs (<w:p>) from the document
                paragraphs = root.findall(".//w:p", namespaces=namespace)

                # Extract and concatenate text within each paragraph
                all_text = []
                for paragraph in paragraphs:
                    paragraph_text = []

                    # Iterate through each run (<w:r>) within the paragraph
                    for run in paragraph.findall(".//w:r", namespaces=namespace):
                        # Find all text elements (<w:t>) within the run
                        text_elements = run.findall(".//w:t", namespaces=namespace)
                        for t in text_elements:
                            if t.text:
                                paragraph_text.append(t.text)

                    # Join the text in the current paragraph
                    if paragraph_text:
                        all_text.append("".join(paragraph_text))
                    else:
                        # If the paragraph is empty, add an empty line
                        all_text.append("")

                # Join all paragraphs with a newline to maintain logical separation
                text = "\n".join(all_text)

        self.text = text
        # print(text)
        return text

    def CountEntriesWithAsterisks(self, questionData):
        numberOfAsterisks = 0
        for entries in questionData:
            if "*" in entries:
                numberOfAsterisks += 1

        if numberOfAsterisks < 2:
            return False
        else:
            return True

    def label_question_type(self, question_data):
        # Extract the first element of the list for identification
        first_element = question_data[0].strip().lower()

        # Define the criteria for each type of question

        if "bl" in first_element or "blank" in first_element:
            return "Short Answer"
        elif "match" in first_element:
            return "Matching"
        elif "order" in first_element:
            return "Ordering"
        elif len(question_data) == 1:
            return "Written Response"

        elif "tf" in first_element or (
                "true" in question_data[1].lower() or "false" in question_data[1].lower()
        ):
            return "True or False"

        elif "mc" in first_element or not self.CountEntriesWithAsterisks(question_data):
            return "Multiple Choice"
        elif "ma" in first_element or self.CountEntriesWithAsterisks(question_data):
            return "MultSelection"
        else:
            return "Unknown"

    def ParseTextIntoQuestions(self):

        self.listFullOfNewlineChars = self.text.split("\n\n")
        print(self.listFullOfNewlineChars)
        self.parsedQuestions = [
            bulkText.split("\n") for bulkText in self.listFullOfNewlineChars
        ]
        self.parsedQuestions = [
            [self.label_question_type(questions), questions]
            for questions in self.parsedQuestions
        ]

    def clean_option_text(self, option_text):
        # Match one letter (upper or lower case), followed by a punctuation mark and a space
        option_text = option_text.replace("*", "", 1).strip()
        return re.sub(r"^\*?[a-zA-Z][.)\-]\s", "", option_text)

    def create_question_object(self, question_data: List) -> BaseQuestion:
        # Extract the type of question and the question list from the data
        question_type = question_data[0]
        question_list = question_data[1]
        # print(f")))){question_data}(((((((")
        if question_list[0].lower().strip() in ["mc", "ma", "bl", "tf"]:
            del question_list[0]
        # print(f"***{question_list}***")

        # Determine which type of question to instantiate
        if question_type == "Multiple Choice":
            return MultipleChoiceQuestion(
                QuestionText=question_list[0],
                ListOfOptions=[
                    self.clean_option_text(opt) for opt in question_list[1:]
                ],
                ListOfPointsPerOption=[
                    100 if opt.startswith("*") else 0 for opt in question_list[1:]
                ],
                Points=100,
            )
        elif question_type == "MultSelection":
            return MultiSelectionQuestion(
                QuestionText=question_list[0],
                OptionText=[self.clean_option_text(opt) for opt in question_list[1:]],
                PointsPerAnswer=[
                    100 if opt.startswith("*") else 0 for opt in question_list[1:]
                ],
                Points=100,
            )
        elif question_type == "Written Response":
            return WrittenAnswerQuestion(QuestionText=question_list[0])
        elif question_type == "Short Answer":
            return ShortAnswerQuestion(
                QuestionText=(
                    question_list[0]
                    if question_list[0][0:6].lower() != "blank "
                    else question_list[0][6:]
                ),
                Answers=[
                    self.clean_option_text(opt[0:].strip()) for opt in question_list[1:]
                ],
                PointsPerAnswer=[100] * len(question_list[1:]),
                Points=100,
            )
        elif question_type == "Matching":
            return MatchingQuestion(
                QuestionText=(
                    question_list[0]
                    if question_list[0][0:6].lower() != "match "
                    else question_list[0][6:]
                ),
                ListOfChoiceNumbers=[
                    str(idx + 1) for idx in range(len(question_list[1:]))
                ],
                ListOfChoiceText=[
                    opt.split(" / ")[0].strip()[3:] for opt in question_list[1:]
                ],
                ListOfMatchNumbers=[
                    str(idx + 1) for idx in range(len(question_list[1:]))
                ],
                ListOfMatchingText=[
                    opt.split(" / ")[1].strip() for opt in question_list[1:]
                ],
            )
        elif question_type == "Ordering":
            return OrderingQuestion(
                QuestionText=(
                    question_list[0]
                    if question_list[0][0:6].lower() != "order "
                    else question_list[0][6:]
                ),
                ListOfItems=[item.strip() for item in question_list[1:]],
            )
        elif question_type == "True or False":
            true_points = 100 if question_list[1].lower() == "true" else 0
            false_points = 100 if question_list[1].lower() == "false" else 0
            return TrueFalseQuestion(
                QuestionText=question_list[0],
                TruePoints=true_points,
                FalsePoints=false_points,
            )
        else:
            raise ValueError("Unknown question type.")

    def SaveToFile(self, questions, saveFileName=None, saveFolderPath=None):
        """
        Saves the current quiz to a D2l Friendly quiz CSV format
        """
        # ask user for a filepath to use to create a save file (CSV)
        if saveFileName is None or saveFolderPath is None:
            file_path = filedialog.asksaveasfilename(
                initialdir=".\\QuizzesToBeUploaded",
                defaultextension=".csv",
                filetypes=[
                    ("CSV Files", "*.csv"),
                    ("Text Files", "*.txt"),
                    ("All files", "*.*"),
                ],
            )
        else:
            file_path = saveFolderPath + "/" + saveFileName

        # if filepath is empty, we cannot save. Return control to the user.
        print(f"THIS IS FILE PATH {file_path}")
        if file_path == "":
            return

        # open filepath and create file (if non-existent) for saving the CSV
        with open(file_path, "w") as file:
            # saved the data to a CSV
            self.__SaveQuestionsToCSVFile(file, questions)

    def __SaveQuestionsToCSVFile(self, file: TextIO, questions):
        """
        exports the currently loaded quiz questions into the currently opened file

        :param file: a file object containing the filepath the user wants to use
        """
        for question in questions:
            # Write question CSV form to the file
            file.write(question.CreateQuestionCSVRepresentation())

            # serves new lines in this CSV file
            file.write(",,,,\n,,,,\n")
