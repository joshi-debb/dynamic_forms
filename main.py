from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename

class display_gui():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.frame = Frame()
        self.text = []

        self.root.title('Generador de formularios dinamicos')
        self.root.geometry('700x400')
        self.frame.config(width=700, height=400)
        self.frame.place(x=0, y=0)

        self.btn_load_files = Button(self.frame, text="Cargar Archivo", command=self.load_file)
        self.btn_load_files.place(x=50, y=15)

        self.lbl_combo = Label(self.frame, text="Reportes")
        self.lbl_combo.place(x=540, y=30)

        self.combo_report = Combobox(self.frame,values=['Reporte de Tokens', 'Reporte de Errores', 'Manual de Usuario', 'Manual Tecnico'])
        self.combo_report.place(x=500, y=50)

        self.text_area = Text(self.frame,  height = 15, width = 80)
        self.text_area.place(x=30, y=90)

        self.btn_process = Button(self.frame,text="Analizar")
        self.btn_process.place(x=50, y=350)

        self.root.resizable(0,0)
        self.root.mainloop()
    
    def load_file(self):
        try:
            filename = askopenfilename()
            filereader = open(filename, 'r+', encoding='utf-8')
            current_file = filereader.read()
        except:
            print('error happend')
        else:
            for i in reversed(current_file):  
                self.text_area.insert("1.0", i)

                
if __name__ == '__main__':
    display_gui()
