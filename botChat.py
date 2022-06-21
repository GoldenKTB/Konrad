from transformers import pipeline, Conversation, AutoTokenizer,AutoModelForCausalLM, AutoModelForSequenceClassification
import torch
import random

def getResponse(msg, step):
    modelName = "microsoft/DialoGPT-medium"
    conversationalPipeline = pipeline("conversational", model=modelName) 
    conversation = Conversation()

    #There's ought to be a better way than this step==0, step==1, etc. But I'm running out of time.

    if step==0:
        greetings = ["Hello!", "Hey!", "What's up!", "Hi there!", "Hi!", "Sup!"]
        return greetings[random.randint(0, len(greetings)-1)] + " What's your name?"
    
    elif step==1:
        meetings = ["Nice to meet you!", "Good to see ya!", "It's great connecting with you!", "Pleased to meet you.", "Delighted to make your acquaintance."]
        return meetings[random.randint(0, len(meetings)-1)] + " How are you doing?"
    
    elif step==2:
        attitude = sentiment(msg)
        positive = ["That's good!", "Good to hear!", "Glad to hear that!", "Fantastic!", "Great!"]
        negative = ["Hmm...", "That's not so good.", "Oh.", "That's not great."]
        if attitude == "POSITIVE":
            return positive[random.randint(0, len(positive)-1)] + "Let's continue chatting for a bit.\nAnything on your mind?"
        else:
            return negative[random.randint(0, len(negative)-1)] + " What's on your mind?"  
    
    else:   
        ending = ["Bye!", "Goodbye!", "Adios!", "Take care.", "Farewell!", "See you later!"]
        if any([harm in msg for harm in ["kill myself", "disappear", "worthless", "dead inside", "no reason to live", "hopeless", "die"]]):
            return "If you're suicidal, please call 1-800-273-8255" + "\nIt's the National Suicide Prevention Lifeline." + "\nOr text HOME to 741741 for anonymous and free crisis counseling."

        elif any([end in msg for end in ["bye","goodbye", "see you later"]]):
            return ending[random.randint(0, len(ending)-1)]

        conversation.add_user_input(msg)
        response = str(conversationalPipeline([conversation], pad_token_id=50256))
        response = response.split("\n")
        return response[-2].split(" >> ")[-1]

def sentiment(msg):
    modelName = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)

    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = classifier(msg)
    return result[0]['label']




