import os
import PyPDF2
import spacy
import json

nlp = spacy.load("en_core_web_sm")

def search_pdf_files(input_text, folder_path):
    related_files = []

    input_text_tokens = nlp(input_text.lower())

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                # Iterate through each page of the PDF
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()

                    # Process the page text using spaCy
                    page_text_tokens = set(token.text.lower() for token in nlp(text))
                    
                    # Check if there's an intersection between input text tokens and page text tokens
                    if any(token.text in page_text_tokens for token in input_text_tokens):
                        # Find the sentence containing the input text
                        sentences = text.split('.')
                        matching_sentence = next((s.strip() for s in sentences if input_text.lower() in s.lower()), None)
                        if matching_sentence:
                            related_files.append({
                                "file_name": filename,
                                "page_number": page_num + 1,
                                "sentence": matching_sentence
                            })
                            break
    
    return related_files

# Example usage
input_text = "CSS"
folder_path = "C://Users//Prakhar Singh//Desktop//Prakhar//Sample Docs"
related_files = search_pdf_files(input_text, folder_path)
print(json.dumps(related_files, indent=4))
