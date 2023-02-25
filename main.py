import customtkinter
import tkinter as tk
from random import shuffle, randint

class StructQuestion():
    def __init__(self):
        self.Text = None
        self.Answers = [None] * 4
        self.TrueAnswer = None

File = open("Вопросы.txt", encoding = "UTF-8")

Lines = [Line.replace("\n", '') for Line in File.readlines()]
Questions_Count = randint(10,15)
Questions = [None] * Questions_Count

for i in range(Questions_Count):
    Question = StructQuestion()
    Question.Text = Lines[i * 5]
    for j, k in enumerate(range(i * 5 + 1, i * 5 + 5)):
        Line = Lines[k]
        if Line[-1] == '*':
            Question.TrueAnswer = j
            Line = Line[:-1]
        Question.Answers[j] = Line
    Questions[i] = Question

def Reg_Answer(self, question):
    global q_count, score, mistakes
    if question.TrueAnswer == self.radio_var.get():
        score += 1
    else:
        mistakes.append((q_count, self.radio_var.get()))

class StructResult():
    def __init__(self):
        self.name = ""
        self.mark = 0
        self.score = 0
        self.answers = []

File.close()
shuffle(Questions)
mode = 0
q_count = 0
score = 0
mistakes = []
Name = ""
mark = 0
Res = []
result_id = None

class GetName(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        global Name, Questions, Questions_Count, mark, score
        self.geometry("400x220")
        self.maxsize(400,220)
        self.title("Save")

        self.my_frame = customtkinter.CTkLabel(master = self, text = "Введите фамилию и имя", font = ("Comic Sans", 16, "normal"))
        self.my_frame.pack(pady=20)

        self.input_field = customtkinter.CTkTextbox(master=self, font = ("Comic Sans", 16, "normal"), width=350, height = 30, corner_radius=10)
        self.input_field.pack(pady = 8, ipady = 6)

        self.save_button = customtkinter.CTkButton(master=self, text="Сохранить", width=150, height = 40, command=self.name_button_callback)
        self.save_button.pack(pady = 10)

    def name_button_callback(self):
        Name = self.input_field.get(1.0,customtkinter.END)
        if Name != "\n":
            GetName.destroy(self)
            f = open("Результаты.txt","a",encoding = "UTF-8")
            f.write("-" + Name)
            f.write("*" + str(mark) + "\n")
            f.write(">" + str(score) + "\n")
            r = 0
            for i in range(Questions_Count):
                question = Questions[i]
                if r < len(mistakes):
                    if i == mistakes[r][0]:
                        f.write(question.Text + "\n" + question.Answers[mistakes[r][1]] + "\n" + question.Answers[question.TrueAnswer] + "\n")
                        r += 1
                    else:
                        f.write(question.Text + "\n" + question.Answers[question.TrueAnswer] + "\n" + question.Answers[question.TrueAnswer] + "\n")
                else:
                        f.write(question.Text + "\n" + question.Answers[question.TrueAnswer] + "\n" + question.Answers[question.TrueAnswer] + "\n")
            f.close()
        else:
            tk.messagebox.showinfo("Ошибка", "Пустое поле")
        

            
    

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("350x220")
        self.maxsize(400,220)
        self.title("Режим")

        self.ch = customtkinter.CTkLabel(master=self, text = "Выберите режим", font = ("Comic Sans", 18, "normal"))
        self.ch.pack(pady = 8)

        self.ex_mode_button = customtkinter.CTkButton(master=self, text="Экзамен", text_color = "#eaeaea", font = ("Comic Sans", 16, "normal"), width=300, height=50, command=self.ex_mode_button_callback)
        self.ex_mode_button.pack(pady = 4)

        self.ch = customtkinter.CTkLabel(master=self, text = "- или -")
        self.ch.pack()

        self.tr_mode_button = customtkinter.CTkButton(master=self, text="Тренировка", text_color = "#eaeaea", font = ("Comic Sans", 16, "normal"), width=300, height=50, command=self.tr_mode_button_callback)
        self.tr_mode_button.pack(pady = 5)

    def ex_mode_button_callback(self):
        global mode
        mode = 1
        ToplevelWindow.destroy(self)
    
    def tr_mode_button_callback(self):
        global mode
        mode = 2
        ToplevelWindow.destroy(self)
        
class ResultsWindow(customtkinter.CTkToplevel):
    def __init__(self):
        global score, Questions_Count, mistakes, Name, mark
        super().__init__()
        self.geometry("1200x700")
        self.minsize(600,350)
        self.title("Результат")
        if Name != "":
            self.name_label = customtkinter.CTkLabel(master=self, text = "Name", font = ("Comic Sans", 20, "normal"))
            self.name_label.pack()

        self.question_label = customtkinter.CTkLabel(master=self, text = "Ваш результат: {0}/{1}".format(score, Questions_Count), font = ("Comic Sans", 24, "normal"))
        self.question_label.pack(padx=20, pady=20)

        per = score / Questions_Count
        if per >= 0.85 : mark = 5
        elif (per < 0.85 and per >= 0.7): mark = 4
        elif (per < 0.7 and per >=0.5): mark = 3
        else: mark = 2

        self.mark_label = customtkinter.CTkLabel(master=self, text = "Оценка: " + str(mark), font = ("Comic Sans", 20, "normal"))
        self.mark_label.pack(pady = 10)

        ApplicationStylte = tk.ttk.Style()
        ApplicationStylte.configure("Treeview.Heading", font = ("Consolas", 18, "normal"))
        ApplicationStylte.configure("Treeview", font = ("Consolas", 14, "normal"))

        columns = ("#1", "#2", "#3")
        self.tree = tk.ttk.Treeview(self, show="headings", columns=columns)
        self.tree.heading("#1", text="Вопрос")
        self.tree.heading("#2", text="Ваш ответ")
        self.tree.heading("#3", text="Правильный ответ")
        ysb = tk.ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree.pack(fill = "both", expand = 1, pady = 20, padx = 20)

        r = 0
        for i in range (Questions_Count):
            question = Questions[i]
            if r < len(mistakes):
                if i == mistakes[r][0]:
                    self.tree.insert("", tk.END, values=(question.Text, question.Answers[mistakes[r][1]], question.Answers[question.TrueAnswer]))
                    r += 1
                else:
                    self.tree.insert("", tk.END, values=(question.Text, question.Answers[question.TrueAnswer], question.Answers[question.TrueAnswer]))
            else:
                self.tree.insert("", tk.END, values=(question.Text, question.Answers[question.TrueAnswer], question.Answers[question.TrueAnswer]))

        self.save_button = customtkinter.CTkButton(master=self, text="Сохранить результат", command=self.save_button_callback, width = 200, height = 50)
        self.save_button.pack(padx = 10, pady = 15)

        self.name_window = None

    def open_window(self):
        if self.name_window is None or not self.name_window.winfo_exists():
            self.name_window = GetName()
        else:
            self.name_window.focus_set()

    def save_button_callback(self):
        self.open_window()

class Results_list(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        global Names, Res
        self.geometry("600x250")
        self.minsize(600,250)
        self.title("Оценки")

        self.info_window = None
        
        f = open("Результаты.txt","r",encoding = "UTF-8")
        c = -1
        q = 0
        cort = [""] * 3
        for i in f:
            if i[0] == "-":
                c+=1
                Res.append(StructResult())
                Res[c].name = i[1:]
            elif i[0] == "*":
                Res[c].mark = int(i[1:])
            elif i[0] == ">":
                Res[c].score = int(i[1:])
            else:
                match q:
                    case 0:
                        cort[0] = i
                        q += 1
                    case 1:
                        cort[1] = i
                        q += 1
                    case 2:
                        cort[2] = i
                        Res[c].answers.append(cort)
                        cort = [""] * 3
                        q = 0

        self.alert_label = customtkinter.CTkLabel(master=self, text = "Нажмите дважды для подробной информации", font = ("Comic Sans", 18, "normal"))
        self.alert_label.pack(pady = 20)

        ApplicationStylte = tk.ttk.Style()
        ApplicationStylte.configure("Treeview.Heading", font = ("Consolas", 20, "normal"))
        ApplicationStylte.configure("Treeview", font = ("Consolas", 16, "normal"))
        
        columns = ("#1", "#2")
        self.tree = tk.ttk.Treeview(self, show="headings", columns=columns)
        self.tree.heading("#1", text="Студент")
        self.tree.heading("#2", text="Оценка")
        self.tree.column("#1", anchor = tk.CENTER)
        self.tree.column("#2", anchor = tk.CENTER)
        ysb = tk.ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree.pack(fill = "both", pady = 20, padx = 30)
        self.tree.bind('<Double-Button-1>', self.selectItem)

        for i in range(len(Res)):
            if Res[i].mark != 0:
                self.tree.insert("", tk.END, values=(Res[i].name, Res[i].mark, i))


    def selectItem(self,a):
        global result_id
        curItem = self.tree.focus()
        result_id = self.tree.item(curItem)['values'][2]
        if self.info_window is None or not self.info_window.winfo_exists():
            self.info_window = Results()
        else:
            self.info_window.focus_set()


class Results(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        global Res, result_id
        self.geometry("1000x600")
        self.minsize(1000,600)
        self.title("Результат")

        j = result_id
        q = 0
        for i in Res[j].answers:
            q += 1

        self.empty_label = customtkinter.CTkLabel(master=self, text = "")
        self.empty_label.pack()

        self.name_label = customtkinter.CTkLabel(master=self, text = Res[j].name, font = ("Comic Sans", 20, "normal"))
        self.name_label.pack()

        self.score_label = customtkinter.CTkLabel(master=self, text = "Результат: {0}/{1}".format(Res[j].score,q), font = ("Comic Sans", 16, "normal"))
        self.score_label.pack()

        self.mark_label = customtkinter.CTkLabel(master=self, text = "Оценка: " + str(Res[j].mark), font = ("Comic Sans", 14, "normal"))
        self.mark_label.pack()

        ApplicationStylte = tk.ttk.Style()
        ApplicationStylte.configure("Treeview.Heading", font = ("Consolas", 14, "normal"))
        ApplicationStylte.configure("Treeview", font = ("Consolas", 13, "normal"))

        columns = ("#1", "#2", "#3")
        self.tree = tk.ttk.Treeview(self, show="headings", columns=columns)
        self.tree.heading("#1", text="Вопрос")
        self.tree.heading("#2", text="Ответ")
        self.tree.heading("#3", text="Правильный ответ")
        ysb = tk.ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree.pack(fill = "both", expand = 1, pady = 20, padx = 20)

        for i in Res[j].answers:
            self.tree.insert("", tk.END, values=(i[0], i[1], i[2]))

        

        


class App(customtkinter.CTk): # Главное окно
    def __init__(self):
        super().__init__()
        global Questions, mode, Questions_Count
        
        self.geometry("600x320")
        self.minsize(600,320)
        self.title("Программа для тестирования")

        Questions_Count = randint(10,15)

        self.toplevel_window = None
        self.open_toplevel()

        self.main_label = customtkinter.CTkLabel(master=self, text = "Программирование", font = ("Comic Sans", 32, "normal"))
        self.main_label.pack(pady=25)

        self.start_button = customtkinter.CTkButton(master=self, text="Начать тестирование", font = ("Comic Sans", 24, "normal"), width=300, height=100, command=self.start_button_callback)
        self.start_button.pack(padx=20, pady=10)

        self.res_button = customtkinter.CTkButton(master=self, text="Результаты", font = ("Comic Sans", 16, "normal"), width=200, height=50, command=self.res_button_callback)
        self.res_button.pack(padx=20, pady=20)

        self.result_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow()
            self.grab_set()
        else:
            self.toplevel_window.focus()

    def start_button_callback(self):
        match mode:
            case 0: self.open_toplevel()
            case 1:
                self.ex_mode()
                self.main_label.destroy()
                self.start_button.destroy()
                self.res_button.destroy()
            case 2:
                self.tr_mode()
                self.main_label.destroy()
                self.start_button.destroy()
                self.res_button.destroy()

    def open_result(self):
        if self.result_window is None or not self.result_window.winfo_exists():
            self.result_window = Results_list()
        else:
            self.result_window.focus()

    def res_button_callback(self):
        self.open_result()
    
    
    def ex_mode(self): #EX_MODE
        global Questions, q_count, Questions_Count
        question = Questions[q_count]
        self.question_label = customtkinter.CTkLabel(master=self, text = question.Text)
        self.question_label.pack(padx=20, pady=10)
        
        def next_button_callback():
            global q_count
            Reg_Answer(self, question)
            q_count += 1
            if q_count == Questions_Count:
                None
            else:
                if q_count == Questions_Count:
                    self.end_button.destroy()
                else:
                    self.next_button.destroy()
                self.question_label.destroy()
                answer_1.destroy()
                answer_2.destroy()
                answer_3.destroy()
                answer_4.destroy()
                self.ex_mode()

        def open_result():
            if self.result_window is None or not self.result_window.winfo_exists():
                self.result_window = ResultsWindow()
                self.grab_set()
            else:
                self.result_window.focus()
        
        def end_button_callback(question):
            global Name
            self.end_button.destroy()
            self.question_label.destroy()
            answer_1.destroy()
            answer_2.destroy()
            answer_3.destroy()
            answer_4.destroy()
            Reg_Answer(self, question)
            self.result_window = None
            open_result()
            self.geometry("400x220")
            self.minsize(400,220)

            restart_button = customtkinter.CTkButton(master=self, text="Начать заново", width=250, height=80, command=restart_button_callback)
            restart_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def restart_button_callback():
            global mistakes, q_count, mode, score
            mistakes = []
            q_count = 0
            mode = 0
            score = 0
            
            App.destroy(self)
            app=App()
            app.mainloop()

            

        self.radio_var = customtkinter.IntVar()
        self.radio_var.set(-1)
        
        def radiobutton_event():
            if q_count == Questions_Count - 1:
                self.end_button.configure(state = "normal")
            else:
                self.next_button.configure(state = "normal")

        answer_1 = customtkinter.CTkRadioButton(master=self, text=question.Answers[0], command=radiobutton_event, variable= self.radio_var, value=0)
        answer_2 = customtkinter.CTkRadioButton(master=self, text=question.Answers[1], command=radiobutton_event, variable= self.radio_var, value=1)
        answer_3 = customtkinter.CTkRadioButton(master=self, text=question.Answers[2], command=radiobutton_event, variable= self.radio_var, value=2)
        answer_4 = customtkinter.CTkRadioButton(master=self, text=question.Answers[3], command=radiobutton_event, variable= self.radio_var, value=3)

        answer_1.pack(padx=20, pady=10)
        answer_2.pack(padx=20, pady=10)
        answer_3.pack(padx=20, pady=10)
        answer_4.pack(padx=20, pady=10)

        if q_count == Questions_Count - 1:
            self.end_button = customtkinter.CTkButton(master=self, text="Закончить", command=lambda:end_button_callback(question), state = "disabled")
            self.end_button.pack(padx=20, pady=25)
        else:
            self.next_button = customtkinter.CTkButton(master=self, text="Дальше", command=next_button_callback, state = "disabled")
            self.next_button.pack(padx=20, pady=25)



    def tr_mode(self): #tr_mode
        global Questions, q_count, Questions_Count
        question = Questions[q_count]
        self.question_label = customtkinter.CTkLabel(master=self, text = question.Text)
        self.question_label.pack(padx=20, pady=10)

        def restart_button_callback():
            global mistakes, q_count, mode, score
            mistakes = []
            q_count = 0
            mode = 0
            score = 0
            
            App.destroy(self)
            app=App()
            app.mainloop()

        self.radio_var = customtkinter.IntVar()
        self.radio_var.set(-1)
        
        def radiobutton_event():
            if q_count == Questions_Count - 1:
                self.end_button.configure(state = "normal")
            else:
                self.next_button.configure(state = "normal")

        answer_1 = customtkinter.CTkRadioButton(master=self, text=question.Answers[0], command=radiobutton_event, variable= self.radio_var, value=0)
        answer_2 = customtkinter.CTkRadioButton(master=self, text=question.Answers[1], command=radiobutton_event, variable= self.radio_var, value=1)
        answer_3 = customtkinter.CTkRadioButton(master=self, text=question.Answers[2], command=radiobutton_event, variable= self.radio_var, value=2)
        answer_4 = customtkinter.CTkRadioButton(master=self, text=question.Answers[3], command=radiobutton_event, variable= self.radio_var, value=3)

        answer_1.pack(padx=20, pady=10)
        answer_2.pack(padx=20, pady=10)
        answer_3.pack(padx=20, pady=10)
        answer_4.pack(padx=20, pady=10)

        def next_button_callback(question):
            global q_count
            if question.Answers[self.radio_var.get()] == question.Answers[question.TrueAnswer]:
                if q_count == Questions_Count:
                    self.end_button.destroy()
                else:
                    self.next_button.destroy()
                self.question_label.destroy()
                answer_1.destroy()
                answer_2.destroy()
                answer_3.destroy()
                answer_4.destroy()
                question = Questions[q_count]
                q_count += 1
                self.tr_mode()
            else:
                match self.radio_var.get() + 1:
                    case 1: answer_1.configure(text_color = "red")
                    case 2: answer_2.configure(text_color = "red")
                    case 3: answer_3.configure(text_color = "red")
                    case 4: answer_4.configure(text_color = "red")

        def end_button_callback(question):
            if question.Answers[self.radio_var.get()] == question.Answers[question.TrueAnswer]:
                self.end_button.destroy()
                self.question_label.destroy()
                answer_1.destroy()
                answer_2.destroy()
                answer_3.destroy()
                answer_4.destroy()

                self.geometry("400x220")
                self.minsize(400,220)

                restart_button = customtkinter.CTkButton(master=self, text="Начать заново", width=250, height=80, command=restart_button_callback)
                restart_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
            else:
                match self.radio_var.get() + 1:
                    case 1: answer_1.configure(text_color = "red")
                    case 2: answer_2.configure(text_color = "red")
                    case 3: answer_3.configure(text_color = "red")
                    case 4: answer_4.configure(text_color = "red")

        if q_count == Questions_Count - 1:
            self.end_button = customtkinter.CTkButton(master=self, text="Закончить", command=lambda:end_button_callback(question), state = "disabled")
            self.end_button.pack(padx=20, pady=25)
        else:
            self.next_button = customtkinter.CTkButton(master=self, text="Дальше", command=lambda:next_button_callback(question), state = "disabled")
            self.next_button.pack(padx=20, pady=25)

        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
