"""
Project Name: pythonProject
File Name: DocxParser.py
Date Created: 11/4/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/4/2024
"""
from fileinput import filename
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename


class DocxParser:
    def __init__(self, startingDirectory):
        self.currentDocPath = askopenfilename(initialdir=startingDirectory,
                                              defaultextension=".docx",
                                              filetypes=[("Word Documents", "*.docx"), ("All files", "*.*")])
        self.listFullOfNewlineChars: list[str] = None
        self.text: str = None
        self.parsedQuestions: list[str] = None

    def ParseBasisDocxIntoText(self) -> str:
        with ZipFile(self.currentDocPath, 'r') as docx:
            # Extract the document.xml which contains the text content
            with docx.open('word/document.xml') as document_xml:
                # Parse the XML content
                tree = ET.parse(document_xml)
                root = tree.getroot()

                # Define the namespace for the Word XML schema
                namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

                # Extract text elements, these are typically in 'w:t' (text) tags
                paragraphs = root.findall('.//w:t', namespaces=namespace)
                text = '\n'.join(paragraph.text for paragraph in paragraphs if paragraph.text)
        self.text = text
        print(text)
        return text

    def ParseTextIntoQuestions(self):
        self.listFullOfNewlineChars = self.text.split(
            "\n*************************************************************************************\n")
        self.parsedQuestions = [bulkText.split('\n') for bulkText in self.listFullOfNewlineChars]
