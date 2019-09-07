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
            tk.Frame.__init__(self, master)
            self.master = master
            self.initWindow()

        def initWindow(self):
            self.master.title("Decoder")
            self.pack(fill="both", expand=1)

            button_frame = tk.Frame(self)
            tk.Button(button_frame, text="Open file", command=self.openFile).pack(side="left", padx=40)
            tk.Button(button_frame, text="Decode", command=self.translateText).pack(side="left", padx=40)
            tk.Button(button_frame, text="Reset", command=self.resetDecoding).pack(side="left", padx=40)
            button_frame.pack(fill="both", expand=0, pady=5)
            code_frame = tk.LabelFrame(self, text="Code", relief="sunken")
            alphabet_frame = tk.Frame(code_frame)
            for letter in self.decode:
                letter_var = tk.StringVar()
                letter_var.set(letter)
                letter_entry = tk.Entry(alphabet_frame, textvariable=letter_var,
                                        width=2, state="disabled")
                letter_entry.pack(side="left")
                letter_entry.configure(disabledforeground="black")

            alphabet_frame.pack(fill="both", expand=0)

            decode_frame = tk.Frame(code_frame)
            for letter in self.decode:
                letter_decode = tk.StringVar()
                letter_decode.trace("w", lambda name, index, mode, letter_decode=letter_decode: self.limitCharacter(letter_decode))
                self.decode[letter] = letter_decode
                tk.Entry(decode_frame, textvariable=letter_decode, width=2).pack(side="left")

            decode_frame.pack(fill="both", expand=0, pady=5)
            code_frame.pack()

            text_frame = tk.LabelFrame(self, text="Input text", borderwidth=2, relief="sunken")
            self.text_area = tk.Text(text_frame, height=8)
            self.text_area.pack()
            text_frame.pack(fill="both", expand=0, pady=5)

            text_decode_frame = tk.LabelFrame(self, text="Decoded text", borderwidth=2, relief="sunken")
            self.text_decode_area = tk.Text(text_decode_frame, height=8)
            self.text_decode_area.pack()
            text_decode_frame.pack(fill="both", expand=0, pady=5)

        def openFile(self):
            file = filedialog.askopenfilename(title="Open code file",
                                              filetypes=(("text files","*.txt"), ("all files","*.*")))
            if(len(file)):
                with open(file, "r") as textReader:
                    self.text_area.delete(1.0, "end")
                    self.text_area.insert(1.0, textReader.read())

        def translateText(self):
            text = self.text_area.get(1.0, "end").upper()
            self.text_decode_area.delete(1.0, "end")
            decoded_text = list()
            for letter in text:
                    if(letter in self.decode):
                        if(not len(self.decode[letter].get())):
                            decoded_text.append(" ")
                        else:
                            decoded_text.append(self.decode[letter].get().lower())
                    else:
                        decoded_text.append(letter)

            self.text_decode_area.insert("1.0", "".join(decoded_text))

        def resetDecoding(self):
            for letter in self.decode:
                letter_decode = self.decode[letter]
                letter_decode.set("")
                self.decode[letter] = letter_decode

            self.text_decode_area.delete(1.0, "end")

        def limitCharacter(self, input):
            if(len(input.get()) > 0):
                input.set(input.get()[0])

    try:
        root = tk.Tk()
        root.geometry("420x400")
        Application(root)
        root.resizable(False, False)
        root.mainloop()
    except:
        messagebox.showerror("Error", sys.exc_info())
