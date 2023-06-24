import PyPDF2
import os
import openai
import re


class AiOfficalModels :
    class OpenAI : 
        def __init__(self):
            openai.api_key = os.getenv('OPENAI_API_KEY') 
        def open_ai_gpt_call(self, user_content, prompt=None): 
                messages = [{"role": "user", "content": user_content}]
                if prompt:
                    messages.insert(0, {"role":"system", "content": prompt})

                completion  = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                reply_content = completion.choices[0].message.content

                return reply_content  # Returning the reply_content from the function7

class GeneralAiModels : 
    class SmartGPTV1 : 
        chain_of_thought_prompt = " Answer : Let’s work this out in a step by step way to be sure we have the right answer"
        reflexion_prompt = "You are a researcher tasked with investigating the the 3 response options provided. List the flaws and faulty logic of each answer option. Let's work this out in a step by step way to be sure we have all the errors: "
        dera_prompt = " You are a resolver tasked with 1) finding which of the X answer options the researcher thought was best 2) improving that answer and 4) Printing the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer: "
        
        gptAgent = AiOfficalModels.OpenAI

        def chain_of_thought(self):
            combined_output = ""
            user_input = input(">: ")   # Asking for user outside the loop
            for i in range(3):
                reply_content = self.gptAgent.open_ai_gpt_call(user_input, "Question :" + self.chain_of_thought_prompt)  # Calling the function and getting the reply content
                combined_output += reply_content + "\n"  # Adding reply_content to combinedOutput

            return combined_output  # Printing combinedOutput after all iterations

        def reflexion_process(self): 
            return self.gptAgent.open_ai_gpt_call(self.chain_of_thought(), self.reflexion_prompt)

        def dera_process(self):
            return self.gptAgent.open_ai_gpt_call(self.reflexion_process(), self.dera_prompt)

        def smart_gpt(self): 
            return self.gptAgent.dera_process()
    class InfoExtractorV1 : 
        
        def __init__(self):
           self.gptAgent = AiOfficalModels.OpenAI()
           
        def chunker(self, path) :
            pdfFileObj = open(path, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)  # Use PdfReader instead of PdfFileReader
            num_pages = len(pdfReader.pages)  # Use len(pdfReader.pages) instead of pdfReader.numPages

            pages = len(pdfReader.pages)

            chunks = []
            current_chunk = []

            for i in range(pages):
                pageObj = pdfReader.pages[i]
                text = pageObj.extract_text()
                words = text.split()
                for word in words:
                    current_chunk.append(word)
                    if len(current_chunk) >= 2500:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = []

            # Add the last chunk if it's not empty and has fewer than 3000 words
            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks
        
        def chunkerStringArray(self, string_array):
            chunks = []
            current_chunk = []

            for word in string_array:
                # Check if adding this word would make the chunk longer than 3000 characters
                if len(' '.join(current_chunk + [word])) > 3000:
                    # If so, add the current chunk to the list of chunks and start a new chunk
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []

                # Add the word to the current chunk
                current_chunk.append(word)

            # Add the last chunk if it's not empty
            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks

       
        # Reads a pdf, inputs them into chunks into GPT-3.5, then returns the raw facts from the file. 
        def info_extractor(self, textbook_path): 
            listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."

            rawFacts = []
            textbookChuncked = self.chunker(textbook_path)    
            for i in range(len(textbookChuncked)) : 
                rawFacts.append(self.gptAgent.open_ai_gpt_call(textbookChuncked[i], listPrompt))  # Changed here

            return rawFacts
    class SentenceIdentifier : 
        def split_into_sentences(self, text: str) -> list[str]:
            alphabets= "([A-Za-z])"
            prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
            suffixes = "(Inc|Ltd|Jr|Sr|Co)"
            starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
            acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
            websites = "[.](com|net|org|io|gov|edu|me)"
            digits = "([0-9])"
            multiple_dots = r'\.{2,}'

            """
            Split the text into sentences.

            If the text contains substrings "<prd>" or "<stop>", they would lead 
            to incorrect splitting because they are used as markers for splitting.

            :param text: text to be split into sentences
            :type text: str

            :return: list of sentences
            :rtype: list[str]
            """
            text = " " + text + "  "
            text = text.replace("\n"," ")
            text = re.sub(prefixes,"\\1<prd>",text)
            text = re.sub(websites,"<prd>\\1",text)
            text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
            text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
            if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
            text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
            text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
            text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
            text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
            text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
            text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
            text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
            if "”" in text: text = text.replace(".”","”.")
            if "\"" in text: text = text.replace(".\"","\".")
            if "!" in text: text = text.replace("!\"","\"!")
            if "?" in text: text = text.replace("?\"","\"?")
            text = text.replace(".",".<stop>")
            text = text.replace("?","?<stop>")
            text = text.replace("!","!<stop>")
            text = text.replace("<prd>",".")
            sentences = text.split("<stop>")
            sentences = [s.strip() for s in sentences]
            if sentences and not sentences[-1]: sentences = sentences[:-1]
            return sentences

class FlashcardModels : 
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

class yearlyPlanProcess : 
    class yearlyPlanCreator : 
        def split_string(self, s):
            # split the string, but keep the delimiter
            parts = re.split("(#_!LESSON \d<@~)", s)[1:]
            
            # group parts in pairs (a pair is a delimiter and the part after it)
            parts = [parts[i] + parts[i + 1] for i in range(0, len(parts), 2)]
            
            return parts
        def yearly_plan_facts_per_lesson(self, lessonNumber, path) : 
            chunkedFacts = []
            lessonPlansFacts = []
            lessonPlanFactsFinal = []
            gptAgent = AiOfficalModels.OpenAI()
            InfoExtractor = GeneralAiModels.InfoExtractorV1() # Creates a infoExtractor object
            rawTextbookFacts = InfoExtractor.info_extractor(path) # Extracts the raw facts from a PDF into a String array
            chunkedFacts = InfoExtractor.chunkerStringArray(rawTextbookFacts) #Splits a String array into chunks of less than 3000 characters

            lessonNumber = lessonNumber // len(chunkedFacts)

            factForLessonPrompt = f"""Based on these facts, I want you to section off them so that they are split up into {lessonNumber} lessons. 
                                    Don't change the facts; put them into {lessonNumber} chunks, with starting before them their lesson number, 
                                    and add these symbols before and after like so: #_!LESSON 1<@~, #_!LESSON 2<@~, and #_!LESSON 3<@~, up to lesson {lessonNumber} and have it be so that the information 
                                    is grouped in the most logical way. Make sure that ALL facts are inside the lessons, such that there are none
                                    left over. Do not change, or add anything about the facts; copy and paste them, into each respective lesson, from the
                                    list you have been given. Here are the facts: """
            for i in range(len(chunkedFacts)) : 
                lessonPlansFacts.append(gptAgent.open_ai_gpt_call(chunkedFacts[i], factForLessonPrompt))
                lessonPlanFactsFinal = self.split_string(lessonPlansFacts[i])
            return lessonPlanFactsFinal
        
        def yearly_plan_powerpoint_creator(self, lessonPlanFacts) :
            lessonPlans = []
            powerpointCreatorPrompt = """Make me a lesson plan based on the following raw facts. I want it to be in a powerpoint slide, such that for each slide, you input 
                                         [SLIDE {i}], and then have a space, with the powerpoint plan afterwards, with all of the information to be included in the powerpoint. 
                                         Here is the information to make into a powerpoint lesson; remember to use ONLY the information here, to ensure accuracy: """
            gptAgent = AiOfficalModels.OpenAI()
            for i in range(len(lessonPlanFacts)) : 
                lessonPlans.append(gptAgent.open_ai_gpt_call(lessonPlanFacts[i], powerpointCreatorPrompt))

            
            return lessonPlans
        def yearly_plan_final(self, lessonNumber, path) : 
            lessonPlanFacts = self.yearly_plan_facts_per_lesson(lessonNumber, path)
            finalLessonStructure = self.yearly_plan_powerpoint_creator(lessonPlanFacts)
            return finalLessonStructure
    
########################################################################  TESTING CODE ###########################################################


path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."
questionPrompt = "Write a me a tailored question for the following raw fact for a flashcard."

test = yearlyPlanProcess.yearlyPlanCreator()
output = test.yearly_plan_facts_per_lesson(5, path)
print(output[0])

