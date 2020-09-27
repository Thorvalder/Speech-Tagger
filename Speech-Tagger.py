

#Importing modules
import speech_recognition as sr
import tkinter as tk
from tkinter import StringVar
from tkinter import filedialog
from tkinter import *
import os


def main():
    BUTTON_FONT = ("Calibre",45,"bold")
    HELP_FONT = ("Verdana",20)
    LABEL_FONT = ("Verdana",14,"bold")



    #creating main class
    class ultimate(tk.Tk):

        def __init__(self,*args,**kwargs):
            
            tk.Tk.__init__(self,*args,**kwargs)
            container = tk.Frame(self)

            container.pack(side = "top", fill = "both", expand = True)

            container.grid_rowconfigure(0,weight = 1)
            container.grid_columnconfigure(0,weight = 1)

            self.frames = {}


            for F in (StartPage,Translate,HelpPage):
                
                frame = F(container,self)

                self.frames[F] = frame

                frame.grid(row = 0, column = 0, sticky = "nesw")

            self.show_frame(StartPage)

        def show_frame(self, cont):

            frame = self.frames[cont]
            frame.tkraise()

    class StartPage(tk.Frame):

        def __init__(self,parent,controller):

            tk.Frame.__init__(self,parent, bg = "#e2f9ff")

            gotoTranslate = tk.Button(self,text = "Tag Audio",fg = "#191a1a", font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: controller.show_frame(Translate))
            gotoTranslate.pack(padx= 20, pady=70)


            gotoHelpPage = tk.Button(self,text = "Help",fg = "#191a1a", font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: controller.show_frame(HelpPage))
            gotoHelpPage.pack(padx= 20, pady=70)

            gotoQuit=tk.Button(self,text = "Quit",fg = "#191a1a",font = BUTTON_FONT,cursor = "hand2",
                              command = self.leave)
            gotoQuit.pack(padx= 20, pady=70)

        def leave(self):
            app.destroy()
            raise SystemExit

    class Translate(tk.Frame):
        
        def __init__(self,parent,controller):

            global filename
            global vartext
            global selected
            global vartext2
            selected = 'None'
            
            vartext = StringVar()
            vartext.set("No file/folder selected")
            vartext2 = StringVar()
            vartext2.set("No file has been tagged")

            tk.Frame.__init__(self,parent, bg = "#e2f9ff")

            gotoStartPage = tk.Button(self,text = "Main Menu",fg = "#191a1a", font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: controller.show_frame(StartPage))
            gotoStartPage.pack(padx= 20, pady=20)

            gotoQuit=tk.Button(self,text = "Quit",fg = "#191a1a",font = BUTTON_FONT,cursor = "hand2",
                              command = self.leave)
            gotoQuit.pack()
            gotoQuit.place(relx=0.5, rely=0.91, anchor=CENTER)

            selectAudio = tk.Button(self,text = "Select File",fg = "#191a1a",font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: self.fileSelect())
            selectAudio.pack(side = LEFT)
            selectAudio.place(relx = 0.2,rely = 0.3,anchor = CENTER)

            selectAudio2 = tk.Button(self,text = "Select Folder",fg = "#191a1a",font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: self.folderSelect())
            selectAudio2.pack()
            selectAudio2.place(relx = 0.5,rely = 0.3,anchor = CENTER)

            tagAudio = tk.Button(self,text = "Tag Audio",fg = "#191a1a",font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: self.tagger())
            tagAudio.pack(side = RIGHT)
            tagAudio.place(relx = 0.8,rely = 0.3,anchor = CENTER)

            filenameLabel = tk.Label(self,bg = "#e2f9ff",fg = "#191a1a",textvariable = vartext, font = LABEL_FONT, relief=FLAT)
            filenameLabel.pack()
            filenameLabel.place(relx = 0.5, rely = 0.5,anchor = CENTER)

            taggedLabel = tk.Label(self,bg = "#e2f9ff",fg = "#191a1a",textvariable = vartext2, font = LABEL_FONT, relief=FLAT)
            taggedLabel.pack()
            taggedLabel.place(relx = 0.5, rely = 0.7,anchor = CENTER)
            

        def leave(self):
            app.destroy()
            raise SystemExit

        def fileSelect(self):
            global filename
            global vartext
            global selected
            
            selected = 'File'
            
            filename = filedialog.askopenfilename()
            temp = filename.split("/")
            temp = temp[len(temp )-1]
            vartext.set("Chosen file: " + temp)

        def folderSelect(self):
            global filename
            global vartext
            global selected
            
            selected = 'Folder'
            
            filename = filedialog.askdirectory()
            vartext.set("Chosen folder: " + filename)
            

        def tagger(self):
            global filename
            global selected
            global vartext2
            
            tagged = False
            
            if selected == 'File':
                file = filename.split("/")
                directory = "/".join(file[:len(file)-1])
                file = file[len(file)-1]
                try:
                    r = sr.Recognizer()
                    audioclip = sr.AudioFile(filename)
                    with audioclip as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.record(source)
                        
                    translated = r.recognize_google(audio).split()
                    
                    tagged = True
                except:
                    print("failed using google algorithm")

                if tagged == False:
                    try:
                        AUDIO_FILE = filename
                        # use the audio file as the audio source
                        r = sr.Recognizer()
                        with sr.AudioFile(AUDIO_FILE) as source:
                            r.adjust_for_ambient_noise(source,1)
                            audio = r.record(source)  # read the entire audio file

                        # recognize speech using Houndify
                        HOUNDIFY_CLIENT_ID = "auQy_gK6S3dfX-DPgl2vDA=="  # Houndify client IDs are Base64-encoded strings
                        HOUNDIFY_CLIENT_KEY = "-gt2j8AMFMTDHcgdQHiMF-cMAVF4sCVwSGYMgF6VCSurt7InOhj_vZEG1zSplmzGwPfOH8dVI-kiQSC8H9XGzw=="  # Houndify client keys are Base64-encoded strings
                        try:
                            translated = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY).split()
                        except sr.UnknownValueError:
                            print("Houndify could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results from Houndify service; {0}".format(e))
                        tagged = True
                    except:
                        print("Failed to translate")
                if tagged == True:
                    connectives = ['here','next','eye','now','since','soon','then','when','while','also','even','indeed','moreover','anyway','but','elsewhere','however','instead','in','other','rather','though','yet','anyway','besides']
                    pronouns = ['i','he','she','we','you','her','him','them','yous','those','that','this','they']
                    profanity = ['anal','anus','arse','ass','ballsack','balls','bastard','bitch','bloody','blowjob','bollock','bollok','boner','boob','bugger','buttplug','clitoris','cock','coon','crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','fudgepacker','flange','goddamn','hell','homo','jerk','jizz','knobend','labia','muff','nigger','penis','piss','prick','pube','pussy','queer','scrotum','sex','shit','slut','smegma','spunk','tit','tosser','turd','twat','vagina','wank','whore']


                    if translated == []:
                        translated = 'NOT FOUND'
                    else:
                        for i in range(len(translated)-1):
                            translated[i] = translated[i].lower()
                            if translated[i] in profanity:
                                del translated[i]
                            elif translated[i] in connectives:
                                del translated[i]
                            elif translated[i] in pronouns:
                                del translated[i]

                    nfile = file.replace('.wav','') + ' TAGS '+ str(translated)+ '.wav'
                    vartext2.set(file + " successfully tagged")
                    print(directory)
                    print(file)
                    old_file = os.path.join(directory, file)
                    new_file = os.path.join(directory, nfile)
                    os.rename(old_file, new_file)
                        

                        
            elif selected == 'Folder':
                directory = filename
                
                for file in os.listdir(filename):
                    tagged = False
                    
                    try:
                        r = sr.Recognizer()
                        #print(filename +"/"+ file)
                        audioclip = sr.AudioFile(filename +"/"+ file)
                        with audioclip as source:
                            r.adjust_for_ambient_noise(source)
                            audio = r.record(source)
                            
                        translated = r.recognize_google(audio).split()
                        
                        tagged = True
                    except:
                        print("failed using google algorithm")
                    if tagged == False:
                        try:
                            AUDIO_FILE = filename +"/"+ file
                            # use the audio file as the audio source
                            r = sr.Recognizer()
                            with sr.AudioFile(AUDIO_FILE) as source:
                                r.adjust_for_ambient_noise(source,1)
                                audio = r.record(source)  # read the entire audio file

                            # recognize speech using Houndify
                            HOUNDIFY_CLIENT_ID = "auQy_gK6S3dfX-DPgl2vDA=="  # Houndify client IDs are Base64-encoded strings
                            HOUNDIFY_CLIENT_KEY = "-gt2j8AMFMTDHcgdQHiMF-cMAVF4sCVwSGYMgF6VCSurt7InOhj_vZEG1zSplmzGwPfOH8dVI-kiQSC8H9XGzw=="  # Houndify client keys are Base64-encoded strings
                            try:
                                translated = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY).split()
                            except sr.UnknownValueError:
                                print("Houndify could not understand audio")
                            except sr.RequestError as e:
                                print("Could not request results from Houndify service; {0}".format(e))
                            tagged = True
                        except:
                            print("Failed to translate")
                    if tagged == True:
                        connectives = ['here','next','eye','now','since','soon','then','when','while','also','even','indeed','moreover','anyway','but','elsewhere','however','instead','in','other','rather','though','yet','anyway','besides']
                        pronouns = ['i','he','she','we','you','her','him','them','yous','those','that','this','they']
                        profanity = ['anal','anus','arse','ass','ballsack','balls','bastard','bitch','bloody','blowjob','bollock','bollok','boner','boob','bugger','buttplug','clitoris','cock','coon','crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','fudgepacker','flange','goddamn','hell','homo','jerk','jizz','knobend','labia','muff','nigger','penis','piss','prick','pube','pussy','queer','scrotum','sex','shit','slut','smegma','spunk','tit','tosser','turd','twat','vagina','wank','whore']
                        

                        if translated == []:
                            translated = 'NOT FOUND'
                        else:
                            for i in range(len(translated)-1):
                                translated[i] = translated[i].lower()
                                if translated[i] in profanity:
                                    del translated[i]
                                elif translated[i] in connectives:
                                    del translated[i]
                                elif translated[i] in pronouns:
                                    del translated[i]

                        nfile = file.replace('.wav','') + ' TAGS '+ str(translated)+ '.wav'
        
                        vartext2.set(file + " successfully tagged")
                        old_file = os.path.join(directory, file)
                        new_file = os.path.join(directory, nfile)
                        os.rename(old_file, new_file)
                        
                    if tagged == True:
                        vartext2.set("Appropriate files have been successfully tagged")
                



    class HelpPage(tk.Frame):
        
        def __init__(self,parent,controller):

            tk.Frame.__init__(self,parent, bg = "#e2f9ff")

            instructions = ("There are two options for this audio clip tagger. Audio clips can be tagged individually" + "\n" +
                            "where the user will manually select the file to be tagged using the file explorer. This " + "\n" +
                            "option is selected by clicking the 'Select File' button on the translation page. Audio  " + "\n" +
                            "clips can also be tagged by folder which requires the user to manually select the folder" + "\n" +
                            "in which the audio files are located. This option is selected by clicking the 'Select Folder'" + "\n" +
                            "button on the translation page. Once the option has been selected and the Folder/File" + "\n" +
                            "entered then the user can click the 'Tag Audio' button to start the tagging " + "\n" +
                            "process. Once the process has been completed the message at the bottom of the page will " + "\n" +
                            "change to reflect that.")
                            

            gotoStartPage = tk.Button(self,text = "Main Menu",fg = "#191a1a", font = BUTTON_FONT,cursor = "hand2",
                              command = lambda: controller.show_frame(StartPage))
            gotoStartPage.pack(padx= 20, pady=20)

            instructionLabel = tk.Label(self,text = instructions, font = HELP_FONT)
            instructionLabel.pack()
            instructionLabel.place(relx=0.5,rely=0.5,anchor=CENTER)
            


            gotoQuit=tk.Button(self,text = "Quit",fg = "#191a1a",font = BUTTON_FONT,cursor = "hand2",
                              command = self.leave)
            gotoQuit.pack()
            gotoQuit.place(relx=0.5, rely=0.91, anchor=CENTER)

        def leave(self):
            app.destroy()
            raise SystemExit

    app = ultimate()
    app.mainloop
    w, h = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry("%dx%d+0+0" % (w, h))

    app.overrideredirect(True)
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
if __name__ == '__main__':
    main()
end = input("RUNNING PROGRAM")
