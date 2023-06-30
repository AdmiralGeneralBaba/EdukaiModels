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
        def descriptor(self, sourceExtract, titleOfBook, bookType, pageNumber, bookLength) :
            describeExtractPrompt = f"""
                                    , The book is {titleOfBook}, A {bookType}. This is an extract starting from page 
                                    {pageNumber} out of {bookLength}

                                    Create me a brief description of what this source is supposed to be. 
                                    Keep the language as simple as the given examples, you should also ALWAYS start with 
                                    'This text is from' then followed by where the extract is from. It should be very brief, 
                                    to the point, and simply stated. Here are some examples of what you should output; note, 
                                    this to help you with structuring your answer, but you don't need to say the exact words in the examples given. 
                                    DO NOT mention the author name or the book title: 

                                    (This text is from the opening of a novel. 
                                    This text is from the middle of a short story.
                                    This text is from the beginning of a novel. 
                                    This text is from the end of a novel.
                                    This text is from the middle of a novel .
                                    This text is from the opening of a novelle.
                                    This text is from the opening of a short story.) """
            gptAgent = OpenAI() 
            description = gptAgent.open_ai_gpt_call(sourceExtract, describeExtractPrompt)
            return description
        def final_model(self, description) : 
            questionString = f""" You now need to think about the whole of the source.
                                {description}
                                How has the writer structured the text to interest you as a reader?
                                You could write about:
                                • what the writer focuses your attention on at the beginning of the source
                                • how and why the writer changes this focus as the source develops
                                • any other structural features that interest you.
                                """ 
            return questionString
    class Question4 : 
        def focus_question(self, extract) : 
            question4PromptGPT4 = f"""
                                . Now with this extract in mind, 
                                Based on these three exam style questions, I want you to create a new once based on the extract I give you. 
                                Here are the example questions: 
                                ( Focus this part of your answer on the second part of the source, from line 25 to
                                the end.
                                A student said, ‘This part of the story, where Mr Fisher is marking homework,
                                shows Tibbet’s story is better than Mr Fisher expected, and his reaction is
                                extreme.’
                                To what extent do you agree?
                                In your response, you could:
                                • consider your own impressions of what Mr Fisher expected Tibbet’s
                                homework to be like
                                • evaluate how the writer conveys Mr Fisher’s reaction to what he discovers
                                • support your response with references to the text.

                                Focus this part of your answer on the second part of the source, from line 24 to the
                                end.
                                A student said, ‘I wasn’t at all surprised by the disappearance of the stranger child
                                at the end of the extract. The writer has left us in no doubt that she is just part of
                                Rosie’s imagination.’
                                To what extent do you agree?
                                In your response, you could:
                                • consider the disappearance of the stranger child
                                • evaluate how the writer presents the stranger child
                                • support your response with references to the text.

                                Focus this part of your answer on the second part of the source, from line 20 to the
                                end.
                                A student said, ‘From the moment he arrives at Master’s compound, the writer
                                portrays Ugwu’s feelings of pure excitement, but by the end it seems that he may
                                be very disappointed.’
                                To what extent do you agree?
                                In your response, you could:
                                • consider your own impressions of Ugwu’s feelings
                                • evaluate how the write(r describes Ugwu’s feelings by the end
                                • support your response with references to the text.) 

                                , and here is the extract. Note, instead of saying 'from line (number)' just output (from line (STARTING SENTENCE HERE))', for that sentence, DO NOT add anything else, 
                                just continue to the next section once the quote is made.
                                
                                """
            gptAgent = OpenAI()
            question4 = gptAgent.open_ai_gpt4_call(extract, question4PromptGPT4)
            return question4
    class Question5 : 
        def introduction(self) :
            introductionPrompt = "" #input prompt from google drive
            gptAgent = OpenAI()
            introduction = gptAgent.open_ai_gpt_call(prompt=introductionPrompt)
            return introduction
            #return introduction
        def write_a_whatever(self) : 
            writeAWhateverPrompt = "" #input prompt from google drive
            gptAgent = OpenAI()
            writeAWhatever = gptAgent.open_ai_gpt_call(prompt=writeAWhateverPrompt)
            #return writeAWhatever
        def describe(self) : 
            describePrompt = ""#input prompt from google drive
            gptAgent = OpenAI()
            describe = gptAgent.open_ai_gpt_call(prompt=describePrompt)
            #API call to dalle2, with describe as the input prompt.
            #return describe, + describeImage

        def final_model(self) : 
            #Combine all three into one return for ease of use


            