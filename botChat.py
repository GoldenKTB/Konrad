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
            return positive[random.randint(0, len(positive)-1)] + " Let's continue chatting for a bit. Anything on your mind?"
        else:
            return negative[random.randint(0, len(negative)-1)] + " What's on your mind?"  
    
    #RIGHT HERE
    else:    
        #This is basic and it works with the app.
        conversation.add_user_input(msg)
        response = str(conversationalPipeline([conversation], pad_token_id=50256))
        response = response.split("\n")
        return response[-2].split(" >> ")[-1]

        #This is the more complex response for bot thingy. The error is with chat_history_ids. 
        #On line 45, it keeps saying chat_history_ids is not defined yet. But when taken out and placed into a seperate file it works.
        #On another note, I did remove the for loop, and that could be another reason why. I didn't want to limit the user to like 5 messages only.
        #Also not quite done with this, as I want to add the ending goodbyes and stuff.

        # input_ids = tokenizer.encode(msg + tokenizer.eos_token, return_tensors="pt")
        # # concatenate new user input with chat history (if there is)

        # bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 3 else input_ids
        # # generate a bot response
        # chat_history_ids = model.generate(
        #     bot_input_ids,
        #     max_length=1000,
        #     do_sample=True,
        #     top_p=0.95,
        #     top_k=100,
        #     temperature=0.75,
        #     pad_token_id=tokenizer.eos_token_id
        # )
        # #print the output
        # output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        # return output


def sentiment(msg):
    modelName = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)

    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = classifier(msg)
    return result[0]['label']




