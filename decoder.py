if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    import sys

    class Application(tk.Frame):

        def __init__(self, master=None):
            self.decode = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "G": "",
                           "H": "", "I": "", "J": "", "K": "", "L": "", "M": "",
                           "N": "", "O": "", "P": "", "Q": "", "R": "", "S": "",
                           "T": "", "U": "", "V": "", "W": "", "X": "", "Y": "",
                           "Z": ""}
            self.original_alphabet = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "G": "",
                                      "H": "", "I": "", "J": "", "K": "", "L": "", "M": "",
                                      "N": "", "O": "", "P": "", "Q": "", "R": "", "S": "",
                                      "T": "", "U": "", "V": "", "W": "", "X": "", "Y": "",
                                      "Z": ""}
            tk.Frame.__init__(self, master)
            self.master = master
            self.initWindow()

        def initWindow(self):
            self.master.title("Decoder")
            self.pack(fill="both", expand=1)

            button_frame_upper = tk.Frame(self)
            tk.Button(button_frame_upper, text="Open file", command=self.openFile).pack(side="left", padx=25)
            tk.Button(button_frame_upper, text="Decode", command=self.translateText).pack(side="left", padx=25)
            tk.Button(button_frame_upper, text="Add letter", command=self.addLetter).pack(side="left", padx=25)
            tk.Button(button_frame_upper, text="Reset", command=self.resetDecoding).pack(side="left", padx=25)
            button_frame_upper.pack(fill="both", expand=0, pady=5)

            button_frame_lower = tk.Frame(self)
            self.ignore = False
            self.button_var = tk.StringVar()
            self.button_var.set("Ignore first letter of each sentence")
            tk.Button(button_frame_lower, textvariable=self.button_var, command=self.decodeRule).pack()
            button_frame_lower.pack(fill="both", expand=0, pady=5)

            self.canvas = tk.Canvas(self, width=0, height=50)
            self.code_frame = tk.LabelFrame(self.canvas, text="Code", relief="sunken")
            self.code_scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.code_scrollbar.set, scrollregion=self.canvas.bbox("all"))
            self.buildCodeFrame()
            self.code_frame.pack()
            self.code_scrollbar.pack(fill="x")
            self.canvas.pack(fill="both", expand=0)
            self.canvas.create_window((0,0), window=self.code_frame)
            self.code_frame.bind("<Configure>", self.configureScrollbar)

            text_frame = tk.LabelFrame(self, text="Input text", borderwidth=2, relief="sunken")
            self.text_area = tk.Text(text_frame, height=8)
            self.text_area.pack()
            text_frame.pack(fill="both", expand=0, pady=5)

            text_decode_frame = tk.LabelFrame(self, text="Decoded text", borderwidth=2, relief="sunken")
            self.text_decode_area = tk.Text(text_decode_frame, height=8)
            self.text_decode_area.pack()
            text_decode_frame.pack(fill="both", expand=0, pady=5)

        def buildCodeFrame(self):
            self.alphabet_frame = tk.Frame(self.code_frame)
            for letter in self.original_alphabet:
                letter_var = tk.StringVar()
                letter_var.set(letter)
                letter_entry = tk.Entry(self.alphabet_frame, textvariable=letter_var,
                                        width=2, state="disabled")
                letter_entry.pack(side="left")
                letter_entry.configure(disabledforeground="black")

            self.alphabet_frame.pack(fill="both", expand=0)

            self.decode_frame = tk.Frame(self.code_frame)
            for letter in self.original_alphabet:
                letter_decode = tk.StringVar()
                letter_decode.trace("w", lambda name, index, mode, letter_decode=letter_decode: self.limitCharacter(letter_decode))
                self.decode[letter] = letter_decode
                tk.Entry(self.decode_frame, textvariable=letter_decode, width=2).pack(side="left")

            self.decode_frame.pack(fill="both", expand=0, pady=5)

        def openFile(self):
            file = filedialog.askopenfilename(title="Open code file",
                                              filetypes=(("text files","*.txt"), ("all files","*.*")))
            if(len(file)):
                with open(file, "r") as textReader:
                    self.text_area.delete(1.0, "end")
                    self.text_area.insert(1.0, textReader.read())

        def translateText(self):
            text = self.text_area.get(1.0, "end")
            self.text_decode_area.delete(1.0, "end")
            decoded_text = list()
            for letter in text:
                upper_letter = letter.upper()
                if(letter.isupper() and self.ignore):
                    decoded_text.append(letter)
                elif(upper_letter in self.decode):
                    if(not len(self.decode[upper_letter].get())):
                        decoded_text.append(" ")
                    else:
                        if(letter.isupper()):
                            decoded_text.append(self.decode[upper_letter].get().upper())
                        else:
                            decoded_text.append(self.decode[upper_letter].get().lower())
                else:
                    decoded_text.append(letter)

            self.text_decode_area.insert("1.0", "".join(decoded_text))

        def resetDecoding(self):
            self.alphabet_frame.destroy()
            self.decode_frame.destroy()
            self.buildCodeFrame()
            self.text_decode_area.delete(1.0, "end")

        def addLetter(self):
            letter_window = tk.Toplevel(self)
            letter_frame = tk.LabelFrame(letter_window, text="Add custom letter", relief="groove")
            label_text = tk.StringVar()
            label_text.set("Set custom letter")
            tk.Label(letter_frame, textvariable=label_text, height=2).pack(side="left")
            letter_var = tk.StringVar()
            letter_var.trace("w", lambda name, index, mode, letter_var=letter_var: self.limitCharacter(letter_var))
            tk.Entry(letter_frame, textvariable=letter_var).pack(side="left")
            letter_frame.pack(fill="both", expand=1, pady=5)

            button_frame = tk.Frame(letter_window)
            tk.Button(button_frame, text="Ok", command=lambda:
                      self.setLetter(letter_var, letter_window)).pack(side="left", padx=30)
            tk.Button(button_frame, text="Cancel", command=lambda:
                      self.closeWindow(letter_window)).pack(side="left", padx=30)
            button_frame.pack(fill="both", expand=1, pady=5)

        def limitCharacter(self, input):
            if(len(input.get()) > 0):
                input.set(input.get()[0])

        def configureScrollbar(self, event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def setLetter(self, letter, window):
            if(not letter.get().upper() in self.decode):
                letter_var = tk.StringVar()
                letter_var.set(letter.get().upper())
                letter_entry = tk.Entry(self.alphabet_frame, textvariable=letter_var,
                                        width=2, state="disabled")
                letter_entry.pack(side="left")
                letter_entry.configure(disabledforeground="black")

                letter_decode = tk.StringVar()
                letter_decode.trace("w", lambda name, index, mode, letter_decode=letter_decode: self.limitCharacter(letter_decode))
                self.decode[letter.get().upper()] = letter_decode
                tk.Entry(self.decode_frame, textvariable=letter_decode, width=2).pack(side="left")
                self.closeWindow(window)
            else:
                messagebox.showwarning("Warning", "The character '" + letter.get().upper() + "' already exists")
                self.addLetter()

        def closeWindow(self, window):
            window.destroy()

        def decodeRule(self):
            if(self.ignore):
                self.ignore = False
                self.button_var.set("Ignore first letter of each sentence")
            else:
                self.ignore = True
                self.button_var.set("Don't ignore first letter of each sentence")

    try:
        root = tk.Tk()
        root.geometry("425x400")
        Application(root)
        root.resizable(False, False)
        root.mainloop()
    except:
        messagebox.showerror("Error", sys.exc_info())
