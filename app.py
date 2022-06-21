from tkinter import *
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from botChat import getResponse

#colors
darkBackgroundColor = "#0f0e52"
lightBackgroundColor = "#4d6fa1"
fontColor = "#f0e7b6"

class chatApp:
    step = 0

    def __init__(self):
        self.window = Tk()
        self.setUp()
        

    def run(self):
        self.window.mainloop()
    
    def setUp(self):
        #window
        self.window.title("Friendly Chatbot")
        self.window.configure(background=darkBackgroundColor, width=520, height=600)
        self.window.resizable(width=False, height=False)

        #top
        top = Label(self.window, text="Welcome!💬", font=("Ariel", 20, "bold"), fg=fontColor, bg=darkBackgroundColor, pady=20)
        top.place(relwidth=1)
        
        #text area
        self.text = Text(self.window, width=20, height=2, fg=fontColor, bg=lightBackgroundColor, font=("Ariel", 13), border=5)
        self.text.place(relwidth=1, relheight=0.75, rely=0.11)
        self.text.configure(cursor="arrow", state="disabled")

        #scrollbar
        scrollbar = Scrollbar(self.text)
        scrollbar.place(relx=0.96, relheight=1)
        scrollbar.configure(command=self.text.yview)

        #bottom
        bottom = Label(self.window, bg=darkBackgroundColor, height=80)
        bottom.place(relwidth=1, rely=0.86)

        #text input box
        self.messageBox = Entry(bottom, font=("Ariel", 13))
        self.messageBox.place(relwidth=0.95, relheight=0.05, relx=0.025, rely=0.01)
        self.messageBox.focus()
        self.messageBox.bind("<Return>", self.enterPressed)

    def enterPressed(self, event):
        msg = self.messageBox.get()
        self.yourMessage(msg, "You")
        self.botResponse(getResponse(msg, self.step))
        self.step += 1

    def yourMessage(self, msg, sender):
        if not msg:
            return
        
        self.messageBox.delete(0, "end")

        msgPerson = f"{sender}: {msg}\n\n"
        self.text.configure(cursor="arrow", state="normal")
        self.text.insert("end", msgPerson)
        self.text.configure(cursor="arrow", state="disabled")
        self.text.see("end")

    def botResponse(self, botResponse):
        msgBot = f"Bot: {botResponse}\n\n"
        self.text.configure(cursor="arrow", state="normal")
        self.text.insert("end", msgBot)
        self.text.configure(cursor="arrow", state="disabled")
        self.text.see("end")

        text_object = gTTS(text=botResponse, lang="en", slow=False)
        text_object.save(f"botRecordings/response.mp3")
        audio = AudioSegment.from_mp3(f"botRecordings/response.mp3")
        play(audio)

if __name__ == "__main__":
    app = chatApp()
    app.run()