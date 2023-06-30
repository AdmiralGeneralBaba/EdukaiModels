import PyPDF2
import re
import random
from openai_calls import OpenAI




class Paper1 : 
    class SourceExtractor : 
        def get_pdf_content(self, pdf_file):
            sourceTextRaw = ""
            with open(pdf_file, 'rb') as pdf_file_obj:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
                numpages =  pdf_reader.getNumPages()

                random_number = random.randint(5, numpages - 5)
                
                for i in range(random_number-1, random_number+1) : 
                    page_obj = pdf_reader.getPage(i)
                    sourceTextRaw = sourceTextRaw + page_obj.extract_text()
            
            return sourceTextRaw
        def start_and_end_lines(self, content) : 
            regexExpression = r'"(.*?)"'
            sourceExtractionPrompt = ""
            gptAgent = OpenAI
            beginningAndEndingLines = gptAgent.open_ai_gpt_call(content, sourceExtractionPrompt) #Calls GPT-3.5, creates the first and last line of the content extracted
            beginningAndEndingLines  = beginningAndEndingLines.replace("\n", " ") # Takes away any line breaks
            beginningAndEndingLines = re.findall(regexExpression, beginningAndEndingLines) #Seperates the result into two strings. [0] = start, [1] = last.
            return beginningAndEndingLines
        def extract_subsection(self, text, start_sentence, end_sentence):
            start_index = text.find(start_sentence)
            end_index = text.find(end_sentence)

            if start_index == -1 or end_index == -1:
                return "Start or end sentence not found in the text."
            
            # Adjust the indices to include the end sentence
            end_index += len(end_sentence)

            # Extract the subsection
            subsection = text[start_index:end_index]

            return subsection
        def source_extraction(self, pdf_file):
            if isinstance(pdf_file, str) : 
                content = pdf_file
            else : 
                content = self.get_pdf_content(pdf_file)
            startAndEndLines = self.start_and_end_lines(content)
            sourceExtract = self.extract_subsection(content, startAndEndLines[0], startAndEndLines[1])

    class Question1 : 
        def character_selection(self, sourceExtract) : 
            quesOnePrompt = ""
            gptAgent = OpenAI
            significantCharcter = gptAgent.open_ai_gpt_call(sourceExtract, quesOnePrompt)
            quesOneStringStructure = f"List four things about {significantCharcter} from this part of the source."
            
            return quesOneStringStructure
        def setting_selection(self, sourceExtract) : 
            return 
        def final_model(self, sourceExtract, choice) : 
            if choice == 0 : 
                question = self.characterSelection(sourceExtract)
                return question
            else : 
                question = self.settingSelection(sourceExtract)
                return question
    class Question2 :  
        def subsection_source(self, sourceExtract) : 
            subsectionPrompt = f"""Based on this extract, find an interesting section, then output the first and last sentence of this subsection EXCLUSIVELY, 
                                  with a comma between the two sentences. MAKE SURE the two quotes are BOTH in speech marks. Here is the extract: {sourceExtract}  """
            gptAgent = OpenAI
            twoStrings = gptAgent.open_ai_gpt_call(sourceExtract, subsectionPrompt)
            source_extractor_instance = Paper1.SourceExtractor()
            subsection = source_extractor_instance.extract_subsection(sourceExtract, twoStrings[0], twoStrings[1])

            return subsection
        def question_maker(self,subsectionExtract) : 
            questionMakerPrompt = f"""using the following extract : 

                                    {subsectionExtract}

                                    recreate the following question structure for a GCSE english paper, in relation to the input extract provided, so that you create a question like the one below in your output, ONLY include your output of the recreation of the question structure given. Here is an example of such question: 

                                    How does the writer use language here to describe Ugwu’s impression of the city?
                                    You could include the writer’s choice of:
                                    • words and phrases
                                    • language features and techniques
                                    • sentence forms.

                                    How does the writer use language here to describe the garden?
                                    You could include the writer’s choice of:
                                    • words and phrases
                                    • language features and techniques
                                    • sentence forms. """

            gptAgent = OpenAI
            question = gptAgent.open_ai_gpt4_call(subsectionExtract, questionMakerPrompt)
            return question
        def combined_model(self, sourceExtract) : 
            subsectionSource = self.subsection_source(sourceExtract)
            question = self.question_maker(subsectionSource)
            return question, subsectionSource
    class Question3 : 
        def descriptor(self, titleOfBook, bookType, pageNumber) : 


            