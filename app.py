from tkinter import *
from pipe1 import response

darkBackgroundColor = "#0f0e52"
lightBackgroundColor = "#4d6fa1"
fontColor = "#ffe380"

class chatApp:
    def __init__(self):
        self.window = Tk()
        self.setUp()

    def run(self):
        self.window.mainloop()
    
    def setUp(self):
        self.window.title("Friendly Chatbot")
        self.window.configure(background=darkBackgroundColor, width=420, height=420)
        self.window.resizable(width=False, height=False)

        top = Label(self.window, text="Welcome!", font=("Ariel", 20, "bold"), fg=fontColor, bg=darkBackgroundColor, pady=5)
        top.place(relwidth=1)

        self.text = Text(self.window, width=20, height=2, fg=fontColor, bg=lightBackgroundColor, font=("Ariel", 14), border=5)
        self.text.place(relwidth=1, relheight=0.75, rely=0.11)
        self.text.configure(cursor="arrow", state="disabled")

        scrollbar = Scrollbar(self.text)
        scrollbar.place(relx=0.96, relheight=1)
        scrollbar.configure(command=self.text.yview)

        bottom = Label(self.window, bg=darkBackgroundColor, height=80)
        bottom.place(relwidth=1, rely=0.86)

        self.messageBox = Entry(bottom)
        self.messageBox.place(relwidth=0.95, relheight=0.035, relx=0.025, rely=0.005)
        self.messageBox.focus()
        self.messageBox.bind("<Return>", self.enterPressed)

    def enterPressed(self, event):
        msg = self.messageBox.get()
        self.insertMessage(msg, "You")

    def insertMessage(self, msg, sender):
        if not msg:
            return
        
        self.messageBox.delete(0, "end")

        msgPerson = f"{sender}: {msg}\n"
        self.text.configure(cursor="arrow", state="normal")
        self.text.insert("end", msgPerson)
        self.text.configure(cursor="arrow", state="disabled")

        msgBot = f"Bot: {response}\n"
        self.text.configure(cursor="arrow", state="normal")
        self.text.insert("end", msgBot)
        self.text.configure(cursor="arrow", state="disabled")

        self.text.see("end")



if __name__ == "__main__":
    app = chatApp()
    app.run()