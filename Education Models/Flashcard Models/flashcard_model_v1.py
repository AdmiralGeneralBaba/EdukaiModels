


class FlashcardModelV1 : 
    def __init__(self):
        self.gptAgent = AiOfficalModels.OpenAI()
        self.InfoExtraction = GeneralAiModels.InfoExtractorV1()
        self.SentenceIdentifier = GeneralAiModels.SentenceIdentifier()
    def flashcard_intialise(self, infoExtractPrompt, questionPrompt, textbook_path):
        rawInfo = self.InfoExtraction.info_extractor(infoExtractPrompt, textbook_path) #creates the raw information
        answerArray = [sentence for chunk in rawInfo for sentence in self.SentenceIdentifier.split_into_sentences(chunk)]  # <-- change this line
        questionsArray = []

        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))   
        return questionsArray, answerArray
