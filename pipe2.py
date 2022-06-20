from transformers import pipeline, Conversation
from transformers import AutoTokenizer, AutoModelForSequenceClassification

history = []
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def askQuestions():
    conversational_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium") 


    conv = Conversation("Do you like the color yellow?")
    print(conversational_pipeline([conv], pad_token_id=50256))

    conv.add_user_input("Why do you think so?")
    print(conversational_pipeline([conv], pad_token_id=50256))

print("Starting chatbot: ")
running = True
while running:
    print("Hello! Can you tell me a bit about yourself? (Your name, where you are from, etc.)")
    foundName = False
    while not foundName:
        foundName = False
        response = input()
        classifier = pipeline("ner", model = 'dbmdz/bert-large-cased-finetuned-conll03-english', tokenizer=AutoTokenizer.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english'))
        res = classifier(response)
        for i in res:
            if(i['entity'] == 'I-PER'):
                foundName = True
                print(f"Nice to meet you, {i['word']}!")
                break
        if not foundName:
            print("Sorry, I didn't quite catch that. I have a hard time reading informal language. Can you please introduce yourself again?")

    #print(res)

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
        print("That's not good")

        print("What happened?")
        response = input()

        print("It's Ok. I'll cheer you up.")



    #have a convo with user
    #still working on this part
    #askQuestions()


    
    running = False

print("Alright, bye!")