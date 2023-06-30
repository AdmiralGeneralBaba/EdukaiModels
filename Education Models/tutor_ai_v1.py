from openai_calls import OpenAI
from smart_gpt_v1 import SmartGPTV1
import re


class TutorAIV1:
    def __init__(self):
        self.chat_history = []
        self.gpt_initialise = OpenAI()
        self.SmartGPT = SmartGPTV1()
    def get_difficulty(self, request):
        difficultyDeterminePrompt = """Based on the user's prompt, determine it's difficulty in answering. return ONLY one of the three, based on how hard it is to answer: 
                                    "EASY", "MEDUIM", "HARD" """ 
        
        return self.gpt_initialise.open_ai_gpt_call(request, difficultyDeterminePrompt)
    def get_responseGpt3(self, request):
        gpt3Prompt = ""
        return self.gpt_initialise.open_ai_gpt_call(request, gpt3Prompt)
    def get_responseGpt4(self, request) : 
        gpt4Prompt = ""
        return self.gpt_initialise.open_ai_gpt4_call(request, gpt4Prompt)
    def get_smartResponseGpt4(self, request) : 
        SmartGPTPrompt = ""
        return self.SmartGPT.smart_gpt(request)
    def tutor_ai_initialise(self): 
        while True:  # start an infinite loop
            current_request = input("\nPlease enter your request (or type 'quit' to exit): ")
            
            
            # If user types 'quit', break the loop
            if current_request.lower() == 'quit':
                break

            difficulty = self.get_difficulty(current_request)
            print(difficulty)
            if re.match(r'^EASY', difficulty):
                print("This is an EASY question")
                print(self.get_responseGpt3(current_request))
            elif re.match(r'^MEDIUM', difficulty): 
                print("This is a MEDIUM question")
                print("GPT answer here")
                print(self.get_responseGpt3(current_request))
            elif re.match(r'^HARD', difficulty): 
                print("This is a HARD question")
                print("SmartGPT response here") 
                print(self.get_responseGpt3(current_request))
            else:
                print("Error in difficulty determination.")
                continue  # Skip to the next iteration