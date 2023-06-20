##NEED TO ADD MEMORY TO THE CHAIN OF THOUGHT CHATBOTS## 

import openai
#insert prompts down here for different stages: 
chainOfThoughtPrompt = " Answer : Let’s work this out in a step by step way to be sure we have the right answer"
reflexionPrompt = "You are a researcher tasked with investigating the the 3 response options provided. List the flaws and faulty logic of each answer option. Let's work this out in a step by step way to be sure we have all the errors: "
deraPrompt = " You are a resolver tasked with 1) finding which of the X answer options the researcher thought was best 2) improving that answer and 4) Printing the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer: "

def openAIGPTcall(user_content, prompt=None): 
    openai.api_key = "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"
   
    messages = [{"role": "user", "content": user_content}]
    if prompt:
        messages.insert(0, {"role":"system", "content": prompt})

    completion  = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply_content = completion.choices[0].message.content
    message_history = message_history + reply_content

    return reply_content  # Returning the reply_content from the function

def chainOfThought():
    combinedOutput = ""
    user_input = input(">: ")   # Asking for user outside the loop
    for i in range(3):

        reply_content = openAIGPTcall(user_input, "Question :" + chainOfThoughtPrompt)  # Calling the function and getting the reply content
        combinedOutput += reply_content + "\n"  # Adding reply_content to combinedOutput

    return combinedOutput  # Printing combinedOutput after all iterations

def reflexionProcess(): 
    return openAIGPTcall(chainOfThought(), reflexionPrompt)

def deraProcess():
    return openAIGPTcall(reflexionProcess(), deraPrompt)

def SmartGPT(): 
    return deraProcess()


   





