import joblib
import spacy


class InitialData:
    def __init__(self, bank_name, product):
        self.bank_name = bank_name
        self.product = product
    
    def get_bank_name(self):
        return self.bank_name
    
    def get_product(self):
        return self.product

nlp = spacy.load('en_core_web_sm')

known_bank_names = ["DNB", "Nordea", "Danske Bank"]

def spacy_tokenizer(text):
    tokens = nlp(text)
    return [token.lemma_.lower() for token in tokens if not token.is_punct and not token.is_stop]

loaded_pipeline = joblib.load("/Users/aleksandar.bajceta/src/mail-classifier/classification_model.joblib")

new_texts = ["""	
Hello there,
DNB's Payment Initiation Service API is currently affected by the following incident:
ID: a7b65818-d0c8-4918-af13-28e15501e4a0
Reported at: May 21, 2023 - 21:33 GMT +02:00
We are currently experiencing technical issues. Our team is actively working to resolve these and hope to have them fixed soon.
You can check the API's current status on the status page.
Best regards,
The team at DNB Open Banking"""]

def predict(text):
    return loaded_pipeline.predict(text)



def get_data(text):
    doc = nlp(text)
    bank_name = ""
    product = ""    
    for token in doc.ents:
        if (token.label_ == "ORG" and token.text in  known_bank_names):
            bank_name = token.text
        
        if (token.label_ == "ORG" and "Service" in token.text):
            product = token.text
        
    return InitialData(bank_name, product)


print(predict(new_texts))

small_data = get_data(new_texts[0])

print(small_data.get_bank_name(), small_data.get_product())

