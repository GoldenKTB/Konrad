from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

history = []
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Starting chatbot: ")
running = True
while running:
    print("How are you doing?")
    response = input()
    classifier = pipeline("sentiment-analysis" , model = model, tokenizer= tokenizer)
    res = classifier(response)
    #print(res)
    result = res[0]['label']
    #print(f"label: {result['label']}")
    if(result=="POSITIVE"):
        print("That's great!")
    else:
        print("That's not so great")

    
    running = False

print("Chatbot shutting down...")