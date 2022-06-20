from transformers import pipeline, Conversation
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-medium"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model_name2 = "distilbert-base-uncased-finetuned-sst-2-english"
model2 = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer2 = AutoTokenizer.from_pretrained(model_name)

#numQuestions = 10

def greedy(numQuestions):
    #greedy search: not very good
    for step in range(numQuestions):
        text = input("You >> ") #input
        #encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        #concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids

        #generate a bot response
        chat_history_ids = model.generate( #By default, model.generate() uses greedy search algorithm when no other parameters are set.
            bot_input_ids, 
            max_length = 1000, 
            pad_token_id=tokenizer.eos_token_id,
        )
        #print out the outputhph
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {output}")

#beam search: a little better, but still not very good
def beam(numQuestions):
    for step in range(numQuestions):
        text = input('You >> ')
        # encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
        # generate a bot response
        chat_history_ids = model.generate(
            #When setting num_beams to 3 in model.generate() method, then we're going to select 
            # three words at each time step and develop them to find the highest overall probability 
            # of the sequence, setting num_beams to 1 is the same as greedy search.
            bot_input_ids,
            max_length=1000,
            num_beams=3,
            early_stopping=True,
            pad_token_id=tokenizer.eos_token_id
        )
        #print the output
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {output}")

def randomSampling(numQuestions):
    #sampling: generating randomness for conversations
    for step in range(numQuestions):
        # take user input
        text = input(">> You:")
        # encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
        # generate a bot response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_k=0,
            pad_token_id=tokenizer.eos_token_id
        )
        #print the output
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {output}")
    #pretty good, but a little too random

#lower temperature:
# chatting 5 times with Top K sampling & tweaking temperature
def topKSampling(numQuestions):
    for step in range(numQuestions):
        # take user input
        text = input(">> You:")
        # encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
        # generate a bot response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_k=100,
            temperature=0.75,
            pad_token_id=tokenizer.eos_token_id
        )
        #print the output
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {output}")
    #Now, we set top_k to 100 to sample from the top 100 words sorted descendingly by probability. We also set temperature to 
    # 0.75 (default is 1.0) to give a higher chance of picking high probability words, setting the temperature to 0.0 is the 
    # same as greedy search; setting it to infinity is the same as completely random.

#nucleus sampling:
#Nucleus sampling or Top-p sampling chooses from the smallest possible words whose cumulative probability exceeds the parameter p we set.
def nucleusSampling(numQuestions):
    for step in range(numQuestions):
        # take user input
        text = input(">> You:")
        # encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
        # generate a bot response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=0,
            temperature=0.75,
            pad_token_id=tokenizer.eos_token_id
        )
        #print the output
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {output}")

#more than one response:
# chatting 5 times with nucleus & top-k sampling & tweaking temperature & multiple
# sentences
def multiple(numQuestions):
    for step in range(numQuestions):
        # take user input
        text = input(">> You:")
        # encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
        # generate a bot response
        chat_history_ids_list = model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=50,
            temperature=0.75,
            num_return_sequences=5,
            pad_token_id=tokenizer.eos_token_id
        )
        #print the outputs
        for i in range(len(chat_history_ids_list)):
            output = tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
            print(f"Bot {i}: {output}")
            choice_index = int(input("Choose the response you want for the next input: "))
            chat_history_ids = torch.unsqueeze(chat_history_ids_list[choice_index], dim=0)

#types: greedy(), beam(), randomSampling(), topKSampling(), nucleusSampling(), multiple()
def therapist():
    print("------------------")
    print("Welcome to the therapist. I will now I ask you some questions:")
    #ask questions, and use a bot to respond 
    questions = ['Do you have a good relationship with your parents?',
    'What do you see as being the biggest problem?',
    'How does this problem make you feel?',
    'What makes the problem better?',
    'What positive changes would you like to see happen in your life?',
    'In general, how would you describe your mood?',
    'What are you grateful for in your life?',
    ]
    for q in questions:
        print("Bot >> " + q)
        greedy(1)

    print("Thank you very much. Have a nice day!")
    print("------------------")
    return


print("Starting chatbot: ")



running = True
while running:
    print("Bot >> Hello! Can you tell me a bit about yourself? (Your name, where you are from, etc.)")
    foundName = False
    while not foundName:
        foundName = False
        response = input("You >> ")
        classifier = pipeline("ner", model = 'dbmdz/bert-large-cased-finetuned-conll03-english', tokenizer=AutoTokenizer.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english'))
        res = classifier(response)
        for i in res:
            if(i['entity'] == 'I-PER'):
                foundName = True
                print(f"Bot >> Nice to meet you, {i['word']}!")
                break
        if not foundName:
            print(" Bot >> Sorry, I didn't quite catch that. I have a hard time reading informal language. Can you please introduce yourself again?")

    #print(res)

    print("How are you doing?")
    response = input("You >> ")
    classifier = pipeline("sentiment-analysis" , model = model2, tokenizer= tokenizer2)
    res = classifier(response)
    #print(res)
    result = res[0]['label']
    #print(f"label: {result['label']}")
    if(result=="POSITIVE"):
        print("Bot >> That's great!")
    else:
        print("Bot >> That's not good")

        print("Bot >> Do you want to go see a therapist?")
        response = input("You >> ")

        if(response=="yes" or response=="yeah" or  response == "yea" or response=="ye" or response=="Yes"):
            therapist()

    nucleusSampling(10)

    #have a convo with user
    #still working on this part
    #gratefulness questions
    #therapist questions
   
    #askQuestions()


    
    running = False

print("Bot >> Alright, talk to you later. Bye!")
print("Chatbot shutting down...")