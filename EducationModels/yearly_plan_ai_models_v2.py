from openai_calls import OpenAI 
from info_extraction_v1 import InfoExtractorV1
from info_extraction_v1 import SentenceIdentifier
import re

class YearlyPlanCreatorV2() : 
    def yearly_plan_facts_per_lesson(pdf_path) : 
        infoExtract = InfoExtractorV1()
        sentenceSplitter = SentenceIdentifier()
        rawFacts = infoExtract.info_extractor(pdf_path)
        sentences = []
     
        # Initialize list and character counter
        my_list = []
        total_characters = 0
        # Initialize variables
        lessons = []
        current_lesson = ""
        char_limit = 1500
        
        # Split the lesson_text into sentences using the sentence_splitter function
        for i in range(len(rawFacts)):
            sentences.extend(sentenceSplitter.split_into_sentences(rawFacts[i]))



        # Loop through sentences
        for sentence in sentences:
            # If adding the next sentence doesn't exceed the char_limit, add the sentence to the current lesson
            if len(current_lesson + sentence) <= char_limit:
                current_lesson += sentence
            # If it does, append the current lesson to lessons and start a new lesson
            else:
                lessons.append(current_lesson)
                current_lesson = sentence

        # Append the last lesson if it's non-empty
        if current_lesson:
            lessons.append(current_lesson)
        print(rawFacts)
        return lessons
    def yearly_plan_homework_creator(lessons, schoolType) :
        homeworkContent = [] 
        homeworkPrompt = f"""Pretend you are a teacher for a {schoolType}. Based on the following raw facts, create a homework plan for students to compelete.
                             Remember to only test based on the information provided: """
        gptAgent = OpenAI()
        for i in range(len(lessons)) : 
            homeworkContent.append(gptAgent.open_ai_gpt_call(lessons[i], homeworkPrompt))

path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\HoI_IV_Strategy_Guide.pdf"
schoolType = "High School"
lessons = YearlyPlanCreatorV2.yearly_plan_facts_per_lesson(path)
homework = YearlyPlanCreatorV2.yearly_plan_homework_creator(lessons, schoolType)

# Loop through each lesson and print it out with its number and length
for i, lesson in enumerate(lessons, start=1):
    print(f"Lesson {i} ({len(lesson)} characters):\n{lesson}\n")
# print(lessons)



print(homework)