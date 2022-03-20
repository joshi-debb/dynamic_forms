from re import I
from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from typing import List
from click import command

from jinja2 import Environment, select_autoescape
from jinja2.loaders import FileSystemLoader

from os import startfile

class Token:
    def __init__(self, token: str, lexeme: str, row: int, col: int) -> None:
        self.token: str = token
        self.lexeme: str = lexeme
        self.row: int = row
        self.col: int = col

    def show_token(self):
        print('Se ha encontrado el token {} que contiene el lexema {} en la fila {} y columna {}'.format(self.token,self.lexeme,self.row, self.col))

class HTML_GUI:
    def __init__(self) -> None:
        self.tipo: str = ''
        self.valor: str = ''
        self.fondo: str = ''
        self.valores: list = []
        self.evento: str = ''

    def show_guis(self):
        print('< tipo: {}, valor: {}, fondo: {}, valores: {}, evento: {} >'.format(self.tipo, self.valor, self.fondo, self.valores, self.evento))

class Errors:
    def __init__(self, line: int, col: int, char: str) -> None:
        self.line: int = line
        self.col: int = col
        self.char: str = char
    
    def show_errors(self):
        print('Se ha encontrado el error {} en la fila {} y columna {} '.format(self.char, self.line, self.col))

def automata(starter: str):
    #agregando al final
    starter += '\n'
    #lista de tokens
    tokens: List[Token] = []
    #lista de errores
    errores: List[Errors] = []
    #estado inicial
    state: int = 0
    tmp_state: int = 0
    #estado actual
    lexeme: str = ''
    #apuntador
    pointer: int = 0
    #Contador de filas y columnas
    row: int = 1
    col: int = 0

    while pointer < len(starter):
        char = starter[pointer]
        # state inicial
        if state == 0:
            #Lista de transiciones
            #Si el caracter es un simbolo [~>>[]<>,:]
            if(ord(char) == 60 or ord(char) == 62 or ord(char) == 58 or ord(char) == 44 or ord(char) == 91 or ord(char) == 93 or ord(char) == 126):
                state = 1
                tmp_state = 1
                pointer += 1
                col += 1
                lexeme += char
            #Si el caracter es una letra minuscula [a-z,ñ]
            elif((ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164):
                state = 2
                pointer += 1
                col += 1
                lexeme += char
            #Si el caracter es una comilla doble ["]
            elif char == '"':
                state = 3
                pointer += 1
                col += 1
                lexeme += char
            #Si el caracter es una comilla simple [']
            elif char == "'":
                state = 4
                pointer += 1
                col += 1
                lexeme += char

            # caracteres ignorados
            #si es un salto de linea [\n]
            elif (ord(char) == 10):
                row += 1
                col = 0
                pointer += 1
            #si es un tabulador horizontal [\t]
            elif (ord(char) == 9):
                col += 1
                pointer += 1
            #si es un espacio en blanco ['']
            elif (ord(char) == 32):
                row += 1
                col = 0
                pointer += 1

            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        #estado 2 -> reservadas
        elif state == 2:
            if((ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164):
                pointer += 1
                col += 1
                lexeme += char
            else:
                if lexeme in ['formulario','tipo','valor','fondo','valores', 'evento']:
                    tokens.append(Token('reservada', lexeme, row, col))
                elif lexeme in ['info','entrada']:
                    tokens.append(Token('iframe', lexeme, row, col))
                else:
                    errores.append(Errors(row, col, lexeme))
                    pointer += 1
                    col += 1
                state = 0
                lexeme = ''

        #estado 3 -> literal
        elif state == 3:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                state = 5
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        elif state == 5:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                pointer += 1
                col += 1
                lexeme += char
            elif char == '"':
                state = 1
                tmp_state = 5
                pointer += 1
                col += 1
                lexeme += char
            elif ord(char) == 45 or ord(char) == 58 or ord(char) == 32:
                state = 7
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        elif state == 7:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                pointer += 1
                col += 1
                lexeme += char
            elif char == '"':
                state = 1
                tmp_state = 7
                pointer += 1
                col += 1
                lexeme += char


        #estado 4 -> subliteral
        elif state == 4:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                state = 6
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        elif state == 6:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                pointer += 1
                col += 1
                lexeme += char
            elif char == "'":
                state = 1
                tmp_state = 6
                pointer += 1
                col += 1
                lexeme += char
            elif ord(char) == 45 or ord(char) == 58 or ord(char) == 32:
                state = 8
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        elif state == 8:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                pointer += 1
                col += 1
                lexeme += char
            elif char == "'":
                state = 1
                tmp_state = 8
                pointer += 1
                col += 1
                lexeme += char

        #estado 1 -> Aceptacion General
        elif state == 1:
            if tmp_state == 5 or tmp_state == 7:
                state = 0
                tmp_state = 0
                tokens.append(Token('literal', lexeme, row, col))
                lexeme = ''
            elif tmp_state == 6 or tmp_state == 8:
                state = 0
                tmp_state = 0
                tokens.append(Token('subliteral', lexeme, row, col))
                lexeme = ''
            elif tmp_state == 1:
                state = 0
                tmp_state = 0
                tokens.append(Token('simbolo', lexeme, row, col))
                lexeme = ''

    return tuple(tokens), tuple(errores)

def scanner(tokens: List[Token]):
    list_parameters: List[HTML_GUI] = []
    tmp_parameters: list = []
    html_gui: list = []
    tmp_parameters.append(html_gui)
    tmp = ''
    tmp2 = " "
    for i in range(len(tokens)):
        if tokens[i].token == 'simbolo' and tokens[i].lexeme == '<':
            new_html_gui: list = []
            tmp_parameters.append(new_html_gui)
            continue
        tmp_parameters[-1].append(tokens[i])
    try:
        for html_gui in tmp_parameters:
            params = HTML_GUI()

            # extraer tipo
            for i in range(len(html_gui)):
                if html_gui[i].token == 'reservada' and html_gui[i].lexeme == 'tipo' and html_gui[i+1].token == 'simbolo' and html_gui[i+1].lexeme == ':' and html_gui[i+2].token == 'literal' and (html_gui[i+3].token == 'reservada' or html_gui[i+3].token == 'simbolo'):
                    for tmp_tipo in html_gui[i + 2].lexeme:
                        if tmp_tipo == '"':
                            tmp_tipo = tmp2
                        else:
                            tmp += tmp_tipo
                    params.tipo = tmp
                    tmp = ''
                    break

            # extraer valor
            for j in range(len(html_gui)):
                if html_gui[j].token == 'reservada' and html_gui[j].lexeme == 'valor' and html_gui[j+1].token == 'simbolo' and html_gui[j+1].lexeme == ':' and html_gui[j+2].token == 'literal' and (html_gui[j+3].token == 'reservada' or html_gui[j+3].token == 'simbolo'):
                    for tmp_valor in html_gui[j + 2].lexeme:
                        if tmp_valor == '"':
                            tmp_valor = tmp2
                        else:
                            tmp += tmp_valor
                    params.valor = tmp
                    tmp = ''
                    break

            # extraer fondo
            for k in range(len(html_gui)):
                if html_gui[k].token == 'reservada' and html_gui[k].lexeme == 'fondo' and html_gui[k+1].token == 'simbolo' and html_gui[k+1].lexeme == ':' and html_gui[k+2].token == 'literal' and (html_gui[k+3].token == 'reservada' or html_gui[k+3].token == 'simbolo'):
                    for tmp_fondo in html_gui[k + 2].lexeme:
                        if tmp_fondo == '"':
                            tmp_fondo = tmp2
                        else:
                            tmp += tmp_fondo
                    params.fondo = tmp
                    tmp = ''
                    break
            
            # extraer evento
            for l in range(len(html_gui)):
                if html_gui[l].token == 'iframe':
                    params.evento = html_gui[l].lexeme
                    break

            # extraer valores
            count = 0
            flag: bool = False
            list: List[Token] = []
            while count < len(html_gui):
                if html_gui[count].token == 'reservada' and html_gui[count].lexeme == 'valores' and html_gui[count+1].token == 'simbolo' and html_gui[count+1].lexeme == ':' and html_gui[count+2].token == 'simbolo' and html_gui[count+2].lexeme == '[':
                    flag = True
                    count += 3
                    continue
                if html_gui[count].token == 'simbolo' and html_gui[count].lexeme == ']':
                    flag = False
                    count += 1
                    continue
                if flag:
                    list.append(html_gui[count])
                count += 1
            
                auxlist: List[str] = []
                for i in range(len(list)):
                    if list[i].token == 'subliteral':
                        for tmp_subliteral in list[i].lexeme:
                            if tmp_subliteral == "'":
                                tmp_subliteral = tmp2
                            else:
                                tmp += tmp_subliteral
                        auxlist.append(tmp)
                        tmp = ''
            params.valores = auxlist
            list_parameters.append(params)
        return list_parameters
    except:
        html_gui = 'null'

def process_tokens(tokens):
    env = Environment(loader=FileSystemLoader('Templates/'),
                    autoescape=select_autoescape(['html']))
    template = env.get_template('report_tokens.html')

    html_file = open('oficial_report_tokens.html', 'w+', encoding='utf-8')
    html_file.write(template.render(tokens=tokens))
    html_file.close()
    startfile('oficial_report_tokens.html')

def process_errors(errs):
    env = Environment(loader=FileSystemLoader('Templates/'),
                    autoescape=select_autoescape(['html']))
    template = env.get_template('report_errors.html')

    html_file = open('oficial_report_errors.html', 'w+', encoding='utf-8')
    html_file.write(template.render(errs=errs))
    html_file.close()
    startfile('oficial_report_errors.html')

def process_Gui(parameters):
    env = Environment(loader=FileSystemLoader('Templates/'),
                    autoescape=select_autoescape(['html']))
    template = env.get_template('gui.html')
    html_file = open('oficial_gui.html', 'w+', encoding='utf-8')
    html_file.write(template.render(parameters=parameters))
    html_file.close()
    startfile('oficial_gui.html')

def process_input(text):
    env = Environment(loader=FileSystemLoader('Templates/'),
                    autoescape=select_autoescape(['html']))
    template = env.get_template('input_text.html')
    html_file = open('OUT_text.html', 'w+', encoding='utf-8')
    html_file.write(template.render(text=text))
    html_file.close()

class display_gui():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.frame = Frame()
        self.text = []

        self.root.title('Generador de formularios dinamicos')
        self.root.geometry('700x400')
        self.frame.config(width=700, height=400)
        self.frame.place(x=0, y=0)

        self.btn_load_files = Button(self.frame, text="Cargar Archivo",command=self.load_file)
        self.btn_load_files.place(x=50, y=15)

        self.lbl_combo = Label(self.frame, text="Reportes")
        self.lbl_combo.place(x=540, y=30)

        self.combo_report = Combobox(self.frame, values=['Reporte de Tokens', 'Reporte de Errores', 'Manual de Usuario', 'Manual Tecnico'])
        self.combo_report.place(x=500, y=50)

        self.text_area = Text(self.frame,  height = 15, width = 80)
        self.text_area.place(x=30, y=90)

        self.btn_process = Button(self.frame,text="Analizar", command=self.analyzer)
        self.btn_process.place(x=50, y=350)

        self.btn_clear = Button(self.frame,text="Limpiar", command=self.clearText_area)
        self.btn_clear.place(x=590, y=350)

        self.root.resizable(0,0)
        self.root.mainloop()
    
    def getText_area(self):
        self.text = (self.text_area.get(1.0, tk.END+"-1c"))
    
    def clearText_area(self):
        self.text_area.delete("1.0","end")

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

    def analyzer(self):
        
        self.getText_area()
        tokens, errs = automata(self.text)

        process_input(self.text)

        #print(self.text)
        parameters = scanner(tokens)

        if parameters != None:
            for i in parameters:
                i.show_guis()
            process_Gui(parameters)
        else:
            print('No hay parametros para la GUI')
        
        for i in tokens:
            i.show_token()
        print('<>=<>=<>=<>=<>=<>=<>=<>=<>=<> ERRORES <>=<>=<>=<>=<>=<>=<>=<>=<>=<>')
        for j in errs:
            j.show_errors()

        if len(self.text) != 0:
            if self.combo_report.get() == 'Reporte de Tokens':
                process_tokens(tokens)
            elif self.combo_report.get() == 'Reporte de Errores':
                process_errors(errs)
        else:
            print('No hay nada que reportar')

if __name__ == '__main__':
    display_gui()
