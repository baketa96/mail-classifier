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

known_bank_names = ["DNB", "Nordea", "Danske Bank", "Swedbank"]

def spacy_tokenizer(text):
    tokens = nlp(text)
    return [token.lemma_.lower() for token in tokens if not token.is_punct and not token.is_stop]

#loaded_pipeline = joblib.load("/Users/aleksandar.bajceta/src/mail-classifier/classification_model.joblib")


def predict(pipeline, text):
    return pipeline.predict(text)



def get_data(text):
    doc = nlp(text)
    bank_name = ""
    product = ""    
    for token in doc.ents:
        if (token.label_ == "ORG" and token.text in  known_bank_names):
            bank_name = token.text
        
        if (token.label_ == "WORK_OF_ART" and "Service" in token.text):
            product = token.text
        
    return InitialData(bank_name, product)

