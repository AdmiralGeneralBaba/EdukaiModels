import PyPDF2
import openai

path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."

def chunker(path) :
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


def GPT3Call(user_content, prompt=None): 
    openai.api_key = "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"
   
    messages = [{"role": "user", "content": user_content}]
    if prompt:
        messages.insert(0, {"role":"system", "content": prompt})

    completion  = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply_content = completion.choices[0].message.content

    return reply_content  # Returning the reply_content from the function



def infoExtractor(inputPrompt, textbookPath) : 
    rawFacts = []
    textbookChuncked = chunker(textbookPath)    
    for i in range(len(textbookChuncked)) : 
        rawFacts.append(GPT3Call(textbookChuncked[i]))

    return rawFacts

print(infoExtractor(listPrompt, path))