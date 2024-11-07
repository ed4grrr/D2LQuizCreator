"""
Project Name: pythonProject
File Name: Questions.py
Date Created: 11/2/2024
Author: Edgar Wallace Bowlin III
Class: CSCI 1317 Introduction to Scripting Languages
Instructor: Edgar Wallace Bowlin III
Date Last Edited: 11/2/2024
"""
from typing import Type

from Questions.QuestionTemplates import *


class QuestionFactory:

    def __init__(self):
        self.QuestionTypes = {
            "Short Answer": "SA", "Written Response": "WR", "Matching": "M",
            "Multiple Choice": "MC", "True or False": "TF", "MultiSelection": "MS", "Ordering": "O"}

    @classmethod
    def DetermineQuestionClass(cls, questionType: str) -> Type[BaseQuestion]:
        match questionType:
            case "Short Answer":
                return ShortAnswerQuestion
            case "Written Response":
                return WrittenAnswerQuestion
            case "Matching":
                return MatchingQuestion
            case "Multiple Choice":
                return MultipleChoiceQuestion
            case "True or False":
                return TrueFalseQuestion
            case "MultiSelection":
                return MultiSelectionQuestion
            case "Ordering":
                return OrderingQuestion
            case _:
                raise NotImplemented

    @classmethod
    def CreateNewQuestionObject(cls, questionType: str, **kwargs):

        questionClass = cls.DetermineQuestionClass(questionType)

        return questionClass(**kwargs)
