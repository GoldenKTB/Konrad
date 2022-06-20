from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

response = ""

history = []
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Starting chatbot: ")
running = True
while running:
    response = input("How are you doing?\n\n")
    classifier = pipeline("sentiment-analysis" , model = model, tokenizer= tokenizer)
    res = classifier(response)
    #print(res)
    result = res[0]['label']
    #print(f"label: {result['label']}")
    if(result=="POSITIVE"):
        print("\nThat's great!")
        response = "\nThat's great!"
    else:
        print("\nThat's not so great")
        response = "\nThat's not so great"

    
    running = False

print("Chatbot shutting down...")