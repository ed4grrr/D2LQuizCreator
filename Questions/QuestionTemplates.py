# None of this project would be possible without the resources found here
# https://jenniferlynnwagner.com/d2l-question-import.html -> D2L Quiz CSV format
# Thank you so much. Without your help, I would have never created this project.


from dataclasses import dataclass


class BaseQuestion:
    # *********************REQUIRED/OPTIONAL GENERAL QUESTION STRINGS**********************************

    # REQUIRED STRINGS
    QUESTIONTYPELINE = "NewQuestion,{QuestionType},,,"
    # WHEN GENERATING CSV STRING, ID WOULD BE ADDED
    TITLELINE = "Title,{Title},,,"
    QUESTIONTEXTLINE = "QuestionText,{QuestionText},,,"
    POINTSLINE = "Points,{Points},,,"
    DIFFICULTYlINE = "Difficulty,{Difficulty},,,"
    # WHEN GENERATING CSV STRING, IMAGE WOULD BE ADDED

    # MINUS THE WHITESPACE, THIS IS WHERE THE OTHER QUESTION SPECIFIC STRINGS WOULD BE ADDED

    # FINALLY, THIS IS WHERE HINT AND FEEDBACK WOULD GO, IF PROVIDED.

    # OPTIONAL STRINGS
    IDLINE = "ID,{ID},,,"
    IMAGELINE = "Image,{ImagePath},,,"
    HINTLINE = "Hint,{Hint},,,"
    FEEDBACKLINE = "Feedback,{Feedback},,,"
    SCORINGlINE = "Scoring,{Scoring},,,"

    # UTILITY STRINGS
    NEWLINEREGULAR = "\n"
    NEWLINECSV = """,,,, 
    ,,,,
    """

    def __init__(self,
                 QuestionType: str,
                 QuestionText: str,
                 Title: str = None,
                 Points: int = None,
                 Difficulty: int = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None):
        self.QuestionType = QuestionType
        self.ID = ID
        self.Title = Title
        self.QuestionText = QuestionText
        self.Points = Points
        self.Difficulty = Difficulty
        self.ImagePath = ImagePath
        self.Scoring = Scoring
        self.Hint = Hint
        self.QuestionFeedback = QuestionFeedback
        self.CSVRepresentation = ""
        self.mandatoryFields = []

    def CreateQuestionCSVRepresentation(self):
        raise NotImplemented

    def CreateMinimumQuestionCSVRepresentation(self):
        return self.QUESTIONTYPELINE.format(QuestionType=self.QuestionType) + "\n" + self.CreateQuestionSpecificText()

    def CreateQuestionSpecificText(self):
        raise NotImplemented

    def CreateGeneralQuestionText(self, questionSpecificString: str):
        returnableQuestionString = ""

        # Generic Question Set-up

        # Minimum Mandatory for Questions to Function
        returnableQuestionString += BaseQuestion.QUESTIONTYPELINE.format(
            QuestionType=self.QuestionType) + "\n"

        if self.ID is not None:
            returnableQuestionString += BaseQuestion.IDLINE.format(ID=self.ID) + "\n"

        if self.Title is not None:
            returnableQuestionString += BaseQuestion.TITLELINE.format(Title=self.Title) + "\n"

        # Minimum Mandatory for Questions to Function
        returnableQuestionString += BaseQuestion.QUESTIONTEXTLINE.format(QuestionText=self.QuestionText) + "\n"

        if self.Points is not None:
            returnableQuestionString += BaseQuestion.POINTSLINE.format(Points=self.Points) + "\n"

        if self.Difficulty is not None:
            returnableQuestionString += BaseQuestion.DIFFICULTYlINE.format(Difficulty=self.Difficulty) + "\n"

        if self.ImagePath is not None:
            returnableQuestionString += BaseQuestion.IMAGELINE.format(ImagePath=self.ImagePath) + "\n"

        if self.Scoring is not None:
            returnableQuestionString += BaseQuestion.SCORINGlINE.format(Scoring=self.Scoring) + "\n"

        # Specialized Question Set-up

        returnableQuestionString += questionSpecificString

        # Back to Generic setup
        if self.Hint is not None:
            returnableQuestionString += BaseQuestion.HINTLINE.format(Hint=self.Hint) + "\n"
        if self.QuestionFeedback is not None:
            returnableQuestionString += BaseQuestion.FEEDBACKLINE.format(Feedback=self.QuestionFeedback) + "\n"

        return returnableQuestionString


# *************************QUESTION SPECIFIC STRINGS***********************

@dataclass
class ShortAnswerQuestion(BaseQuestion):
    INPUTBOXLIMITSLINE = "InputBox,{Minimum},{Maximum},,"
    ANSWERLINE = "Answer,{Points},{Answer},{RegEx},"

    def __init__(self,

                 QuestionText: str,

                 Answers: list[str],

                 PointsPerAnswer: list[int],
                 Points: int = None,
                 Difficulty: int = None,
                 Title: str = None,
                 RegExsForAnswers: list[str] = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 CharMinimumLength: int = 3,
                 CharMaximumLength: int = 40,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("SA", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.CharMinimumLength = CharMinimumLength
        self.CharMaximumLength = CharMaximumLength
        self.RegExsForAnswers = RegExsForAnswers
        # print(Answers)
        # print(PointsPerAnswer)
        self.Answers = Answers
        self.PointsPerAnswer = PointsPerAnswer
        self.mandatoryFields.append("Answers")
        self.mandatoryFields.append("PointsPerAnswer")

    def CreateQuestionSpecificText(self):
        returnableString = ""

        # if the user provided RegExs for the answers
        if self.RegExsForAnswers is not None:
            print("\n\nREGEX\n\n\n")
            print(zip(self.Answers, self.PointsPerAnswer))
            print("\n\n\n\n\n")
            for Points, Answer, currRegEx in zip(self.Answers, self.PointsPerAnswer, self.RegExsForAnswers):
                returnableString += ShortAnswerQuestion.ANSWERLINE.format(Points=Points, Answer=Answer,
                                                                          RegEx=currRegEx) + "\n"
        else:
            print("\n\nNoneRegex\n\n\n")
            print(zip(self.Answers, self.PointsPerAnswer))
            print("\n\n\n\n\n")
            for Points, Answer in zip(self.Answers, self.PointsPerAnswer):
                returnableString += ShortAnswerQuestion.ANSWERLINE.format(Points=Points, Answer=Answer,
                                                                          RegEx="") + "\n"
        return returnableString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


@dataclass
class WrittenAnswerQuestion(BaseQuestion):
    AnswerKey = "AnswerKey,{AnswerKey},,,"
    InitialText = "InitialText,{InitialText},,,"

    def __init__(self, Title: str,
                 QuestionText: str,
                 Points: int,
                 Difficulty: int,
                 InitialText: str,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 AnswerKey: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("WR", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.InitialText = InitialText
        self.AnswerKey = AnswerKey

    def CreateQuestionSpecificText(self):
        returnableQuestionString = ""
        returnableQuestionString += WrittenAnswerQuestion.InitialText.format(InitialText=self.InitialText) + "\n"
        returnableQuestionString += WrittenAnswerQuestion.AnswerKey.format(AnswerKey=self.AnswerKey) + "\n"
        return returnableQuestionString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


@dataclass
class MatchingQuestion(BaseQuestion):
    Choice = 'Choice, {ChoiceNumber}, {ChoiceText},,'
    Match = 'Match, {CorrectChoiceNumber}, {CorrectChoiceText}, ,'

    def __init__(self,
                 QuestionText: str,
                 ListOfMatchNumbers: list[str],
                 ListOfMatchingText: list[str],
                 ListOfChoiceNumbers: list[str],
                 ListOfChoiceText: list[str],
                 Title: str = None,
                 Points: int = None,
                 Difficulty: int = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("M", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.ListOfChoiceNumbers = ListOfChoiceNumbers
        self.ListOfChoiceText = ListOfChoiceText
        self.ListOfMatchNumbers = ListOfMatchNumbers
        self.ListOfMatchingText = ListOfMatchingText
        self.mandatoryFields.append("ListOfMatchingText")
        self.mandatoryFields.append("ListOfMatchNumbers")
        self.mandatoryFields.append("ListOfChoiceText")
        self.mandatoryFields.append("ListOfChoiceNumbers")

    def CreateQuestionSpecificText(self):

        returnableQuestionString = ""

        for choiceNumber, choiceText in zip(self.ListOfChoiceNumbers, self.ListOfChoiceText):
            returnableQuestionString += self.Choice.format(ChoiceNumber=choiceNumber, ChoiceText=choiceText) + "\n"

        for matchNumber, matchAnswer in zip(self.ListOfMatchNumbers, self.ListOfMatchingText):
            returnableQuestionString += self.Match.format(CorrectChoiceNumber=matchNumber,
                                                          CorrectChoiceText=matchAnswer) + "\n"

        return returnableQuestionString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


@dataclass
class MultipleChoiceQuestion(BaseQuestion):
    Option = "Option,{QuestionPoints},{OptionText},,{OptionFeedback}"

    def __init__(self,
                 QuestionText: str,
                 ListOfOptions: list[str],
                 ListOfPointsPerOption: list[str],
                 Points: int = None,
                 Difficulty: int = None,
                 Title: str = None,
                 ListOfFeedBack: list[str] = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("MC", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.ListOfFeedBack = ListOfFeedBack
        self.ListOfOptions = ListOfOptions
        self.ListOfPointsPerOption = ListOfPointsPerOption
        self.mandatoryFields.append("ListOfOptions")
        self.mandatoryFields.append("ListOfPointsPerOption")

    def CreateQuestionSpecificText(self):

        returnableQuestionString = ""

        if self.ListOfFeedBack is not None:
            for questionPoints, optionText, optionFeedback in zip(self.ListOfPointsPerOption, self.ListOfOptions,
                                                                  self.ListOfFeedBack):
                returnableQuestionString += self.Option.format(QuestionPoints=questionPoints, OptionText=optionText,
                                                               OptionFeedback=optionFeedback) + "\n"
        else:
            for questionPoints, optionText in zip(self.ListOfPointsPerOption, self.ListOfOptions):
                returnableQuestionString += self.Option.format(QuestionPoints=questionPoints, OptionText=optionText,
                                                               OptionFeedback="") + "\n"

        return returnableQuestionString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


@dataclass
class TrueFalseQuestion(BaseQuestion):
    TRUELINE = "TRUE,{TruePoints},{TrueFeedback}"
    FASLELINE = "FALSE,{FalsePoints},{FalseFeedback}"

    def __init__(self,
                 QuestionText: str,
                 TruePoints: int,
                 FalsePoints: int,
                 Title: str = None,
                 Points: int = None,
                 Difficulty: int = None,
                 TrueFeedback: str = None,
                 FalseFeedback: str = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("TF", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.TruePoints = TruePoints
        self.FalsePoints = FalsePoints
        self.FalseFeedback = FalseFeedback
        self.TrueFeedback = TrueFeedback
        self.mandatoryFields.append("TruePoints")
        self.mandatoryFields.append("FalsePoints")

    def CreateQuestionSpecificText(self):

        returnableQuestionString = ""

        if self.TrueFeedback is not None:
            returnableQuestionString += self.TRUELINE.format(TruePoints=self.TruePoints,
                                                             TrueFeedback=self.TrueFeedback) + "\n"
        else:
            returnableQuestionString += self.TRUELINE.format(TruePoints=self.TruePoints, TrueFeedback="") + "\n"

        if self.FalseFeedback is not None:
            returnableQuestionString += self.FASLELINE.format(FalsePoints=self.FalsePoints,
                                                              FalseFeedback=self.FalseFeedback) + "\n"
        else:
            returnableQuestionString += self.FASLELINE.format(FalsePoints=self.FalsePoints, FalseFeedback="") + "\n"

        return returnableQuestionString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


@dataclass
class MultiSelectionQuestion(BaseQuestion):
    MULTISELECTIONOPTIONLINE = """Option,{points},{OptionText},,{OptionFeedback}"""

    def __init__(self,
                 QuestionText: str,
                 PointsPerAnswer: list[int],
                 OptionText: list[str],
                 Points: int = None,
                 Difficulty: int = None,
                 Title: str = None,
                 OptionFeedback: list[str] = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("MS", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.OptionFeedback = OptionFeedback
        self.PointsPerAnswer = PointsPerAnswer
        self.OptionText = OptionText
        self.mandatoryFields.append("OptionText")
        self.mandatoryFields.append("PointsPerAnswer")

    def CreateQuestionSpecificText(self):

        returnableQuestionString = ""

        if self.OptionFeedback is not None:
            for points, OptionText, OptionFeedback in zip(self.PointsPerAnswer, self.OptionText, self.OptionFeedback):
                returnableQuestionString += self.MULTISELECTIONOPTIONLINE.format(points=points, OptionText=OptionText,
                                                                                 OptionFeedback=OptionFeedback) + "\n"
        else:
            for points, OptionText in zip(self.PointsPerAnswer, self.OptionText):
                returnableQuestionString += self.MULTISELECTIONOPTIONLINE.format(points=points, OptionText=OptionText,
                                                                                 OptionFeedback="") + "\n"

        return returnableQuestionString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


@dataclass
class OrderingQuestion(BaseQuestion):
    ORDERITEMLINE = """Item,{ItemText},{IsHTML},{OptionFeedback},"""

    def __init__(self,
                 QuestionText: str,
                 ListOfItems: list[str],
                 Title: str = None,
                 Points: int = None,
                 Difficulty: int = None,
                 ListOfIsHTML: list[bool] = None,
                 ListOfFeedback: list[str] = None,
                 ID: str = None,
                 ImagePath: str = None,
                 Scoring: str = None,
                 Hint: str = None,
                 QuestionFeedback: str = None
                 ):
        super().__init__("O", QuestionText, Title=Title, Points=Points, Difficulty=Difficulty, ID=ID,
                         ImagePath=ImagePath, Scoring=Scoring, Hint=Hint, QuestionFeedback=QuestionFeedback)
        self.ListOfIsHTML = ListOfIsHTML
        self.ListOfFeedback = ListOfFeedback
        self.ListOfItems = ListOfItems
        self.mandatoryFields.append("ListOfItems")

    def CreateQuestionSpecificText(self):

        returnableQuestionString = ""

        if self.ListOfFeedback is not None:
            for items, isHTML, feedback in zip(self.ListOfItems, self.ListOfIsHTML, self.ListOfFeedback):
                returnableQuestionString += self.ORDERITEMLINE.format(ItemText=items, IsHTML=isHTML,
                                                                      OptionFeedback=feedback) + "\n"
        elif self.ListOfIsHTML is not None:
            for items, isHTML in zip(self.ListOfItems, self.ListOfIsHTML):
                returnableQuestionString += self.ORDERITEMLINE.format(ItemText=items, IsHTML=isHTML,
                                                                      OptionFeedback="") + "\n"
        else:
            for items in self.ListOfItems:
                returnableQuestionString += self.ORDERITEMLINE.format(ItemText=items, IsHTML="",
                                                                      OptionFeedback="") + "\n"

        return returnableQuestionString

    def CreateQuestionCSVRepresentation(self):
        return self.CreateGeneralQuestionText(self.CreateQuestionSpecificText())

    def __str__(self):
        return self.CreateQuestionCSVRepresentation()


bulk_example_to_pull_from = """
"//(Note: The 'images' folder is assumed to be in the ""/content/<course path>/"" directory)",,,,
//Question Text is always a required field,,,,
// An ID will be generated using the (Course code)-(Question number) if an ID is not specified for a question,,,,
,,,,
"// Please ensure that the CSV file is saved as ""CSV UTF-8"" encoded to ensure that non-ASCII characters like à, ø, é and other are able to be correctly imported",,,,
,,,,
//WRITTEN RESPONSE QUESTION TYPE,,,,
//This sample question also shows how you can set a question caID for the question of format {Course Code}-{Question Number},,,,
NewQuestion,WR,,,
ID,CHEM110-234,,,
Title,This is a written response question,,,
QuestionText,This is the question text for WR1,,,
Points,1,,,
Difficulty,7,,,
Image,images/LA1.jpg,,,
InitialText,This is the initial text,,,
AnswerKey,This is the answer key text,,,
Hint,This is the hint text,,,
Feedback,This is the feedback text,,,
,,,,
,,,,
//SHORT ANSWER QUESTION TYPE,,,,
//Answers must include text in column3,,,,
NewQuestion,SA,,,
ID,CHEM110-235,,,
Title,This is a short answer question,,,
QuestionText,This is the question text for SA1,,,
Points,5,,,
Difficulty,2,,,
Image,images/SA1.jpg,,,
InputBox,3,40,,
Answer,100,This is the text for answer 1,regexp,
Answer,50,This is the text for answer 2,,
Hint,This is the hint text,,,
Feedback,This is the feedback text,,,
,,,,
//MATCHING QUESTION TYPE,,,,
//Choices and Matches must include text in column3,,,,
NewQuestion,M,,,
ID,CHEM110-236,,,
Title,This is a matching question,,,
QuestionText,This is the question text for M1,,,
Points,2,,,
Difficulty,2,,,
Image,images/mc1.jpg,,,
Scoring,EquallyWeighted,,,
Choice,1,This is choice 1 text,,
Choice,2,This is choice 2 text,,
Choice,3,This is choice 3 text,,
Match,3,This matches with choice 3,,
Match,1,This matches with choice 1,,
Match,2,This matches with choice 2,,
Hint,This is the hint text,,,
Feedback,This is the feedback text,,,
,,,,
//MULTIPLE CHOICE QUESTION TYPE,,,,
//Options must include text in column3,,,,
NewQuestion,MC,,,
ID,CHEM110-237,,,
Title,This is a multiple choice question,,,
QuestionText,This is the question text for MC1,,,
Points,1,,,
Difficulty,1,,,
Image,images/MC1.jpg,,,
Option,100,This is the correct answer,,This is feedback for option 1
Option,0,This is incorrect answer 1,,This is feedback for option 2
Option,0,This is incorrect answer 2,,This is feedback for option 3
Option,25,This is partially correct,,This is feedback for option 4
Hint,This is the hint text,,,
Feedback,This is the feedback text,,,
,,,,
,,,,
//TRUE / FALSE QUESTION TYPE,,,,
NewQuestion,TF,,,
ID,CHEM110-238,,,
Title,This is a True/False question,,,
QuestionText,This is the question text for TF1,,,
Points,1,,,
Difficulty,1,,,
Image,images/TF1.jpg,,,
TRUE,100,This is feedback for 'TRUE',,
FALSE,0,This is feedback for 'FALSE',,
Hint,This is the hint text,,,
Feedback,This is the feedback text,,,
,,,,
,,,,
//MULTISELECT QUESTION TYPE,,,,
//Options must include text in column3,,,,
NewQuestion,MS,,,
ID,CHEM110-239,,,
Title,This is a Multi-Select question,,,
QuestionText,This is the question text for MS1,,,
Points,10,,,
Difficulty,5,,,
Image,images/MS1.jpg,,,
Scoring,RightAnswers,,,
Option,1,This is option 1 text,,This is feedback for option 1
Option,0,This is option 2 text,,This is feedback for option 2
Option,1,This is option 3 text,,This is feedback for option 3
Hint,This is the hint text,,,
Feedback ,This is the feedback text,,,
,,,,
,,,,
//ORDERING QUESTION TYPE,,,,
//Items must include text in column2,,,,
NewQuestion,O,,,
ID,CHEM110-240,,,
Title,This is an ordering question,,,
QuestionText,This is the question text for O1,,,
Points,2,,,
Difficulty,2,,,
Scoring,RightMinusWrong,,,
Image,images/O1.jpg,,,
Item,This is the text for item 1,NOT HTML,This is feedback for option 1,
Item,This is the text for item 2,HTML,This is feedback for option 2,
Hint,This is the hint text,,,
Feedback,This is the feedback text,,,
"""
