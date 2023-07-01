from EducationModels.aqa_english_language_paper_1 import aqa_english_language_paper_1_generator
from EducationModels.flashcard_model_v1 import FlashcardModelV1
from EducationModels.smart_gpt_v1 import SmartGPTV1
from EducationModels.tutor_ai_v1 import TutorAIV1
from EducationModels.yearly_plan_ai_models_v1 import YearlyPlanCreatorV1



class EducationModels : 
    AQAEnglishLanguagePaper1 = aqa_english_language_paper_1_generator # Assuming that paper_1_generator is a class
    flashcardModel = FlashcardModelV1()
    smartGpt = SmartGPTV1()
    tutorAi = TutorAIV1()
    yearlyPlanCreator = YearlyPlanCreatorV1()


    