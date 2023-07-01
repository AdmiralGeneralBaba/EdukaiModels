from openai_calls import OpenAI
from info_extraction_v1 import InfoExtractorV1
from info_extraction_v1 import SentenceIdentifier

class FlashcardModelV1 : 
    def __init__(self):
        self.gptAgent = OpenAI()
        self.InfoExtraction = InfoExtractorV1()
        self.SentenceIdentifier = SentenceIdentifier()
    def flashcard_intialise(self, textbook_path):
        questionPrompt = "Create me a tailored, short question for this raw fact to be used in a flashcard : "
        rawInfo = self.InfoExtraction.info_extractor(textbook_path) #creates the raw information
        answerArray = [sentence for chunk in rawInfo for sentence in self.SentenceIdentifier.split_into_sentences(chunk)]  # <-- change this line
        questionsArray = []

        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))   
        return questionsArray, answerArray
