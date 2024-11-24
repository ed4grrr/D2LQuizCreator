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
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename


class DocxParser:
    def __init__(self, startingDirectory):
        self.currentDocPath = askopenfilename(
            initialdir=startingDirectory,
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All files", "*.*")],
        )
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
        # print(self.listFullOfNewlineChars)
        self.parsedQuestions = [
            bulkText.split("\n") for bulkText in self.listFullOfNewlineChars
        ]
        self.parsedQuestions = [
            [self.label_question_type(questions), questions]
            for questions in self.parsedQuestions
        ]

    def ParseMultipleChoiceQuestion(self):
        pass
