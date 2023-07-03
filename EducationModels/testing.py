import PyPDF2
import random
import re
from openai_calls import OpenAI

def get_pdf_content(pdf_file):
        contentGrammerFixerPrompt = """On the following raw PDF text, remove any grammtical errors or spacing, but KEEP THE CONTENT EXACTLY THE SAME. 
                                       PDF text : """
        sourceTextRaw = ""
        with open(pdf_file, 'rb') as pdf_file_obj:
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            numpages =  len(pdf_reader.pages)

            random_number = random.randint(5, numpages - 5)
            
            for i in range(random_number-1, random_number+1) : 
                page_obj = pdf_reader.pages[i]
                sourceTextRaw = sourceTextRaw + page_obj.extract_text()
        sourceTextRaw  = sourceTextRaw.replace("\n", " ") # Takes away any line breaks
        sourceTextRaw = OpenAI.open_ai_gpt_call(sourceTextRaw, contentGrammerFixerPrompt)
        return sourceTextRaw, random_number, numpages

def start_and_end_lines(content) : 
    regexExpression = r'"(.*?)"'
    sourceExtractionPrompt = """Based on this extract, find an interesting section, then output the first and last sentence of this subsection EXCLUSIVELY, 
                                with a comma between the two sentences. MAKE SURE the two quotes are BOTH in speech marks. Here is the extract:"""
       
    gptAgent = OpenAI()
    beginningAndEndingLines = gptAgent.open_ai_gpt_call(content, sourceExtractionPrompt) #Calls GPT-3.5, creates the first and last line of the content extracted
    beginningAndEndingLines  = beginningAndEndingLines.replace("\n", " ") # Takes away any line breaks
    beginningAndEndingLines = re.findall(regexExpression, beginningAndEndingLines) #Seperates the result into two strings. [0] = start, [1] = last.
    return beginningAndEndingLines

def extract_subsection(text, start_sentence, end_sentence):
            start_index = text.find(start_sentence)
            end_index = text.find(end_sentence)

            if start_index == -1 or end_index == -1:
                return "Start or end sentence not found in the text."
            
            # Adjust the indices to include the end sentence
            end_index += len(end_sentence)

            # Extract the subsection
            subsection = text[start_index:end_index]

            return subsection



path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."
questionPrompt = "Write a me a tailored question for the following raw fact for a flashcard."
school = "Primary School"
choice = 0


content = get_pdf_content(path)
# startAndEnd = start_and_end_lines(content[0])
# subsectionExtracted = extract_subsection(content[0], startAndEnd[0], startAndEnd[1])

print(content)
# print(startAndEnd)
# print(subsectionExtracted)