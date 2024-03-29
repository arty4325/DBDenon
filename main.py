"""
En el presente modulo se encuentra la pantalla inicial de tkinter
Esta pantalla inicial se llama en las otras instancias del programa
"""


import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk




window = tk.Tk()
window.title("DenonDataBase")
window.minsize(1000,700)
window.resizable(False, False)



Inicio = tk.Canvas(window, width = 1000, height = 700)
Inicio.place(x = 0, y = 0)



def labelDest(List):
    if List == []:
        return []
    else:
        (List[0]).destrou()
        labelDest(List[1:])

def PantallaInicial(window, Inicio):
    MainLabel = tk.Label(Inicio, text = "Denon Information DB", font = ("Arial", 20))
    MainLabel.place(x = 350, y = 50)
    
    
    #Se quiere crear un boton el cual busque en el computador los datos
    def SelectFile():
        # Abre el cuadro de diálogo para seleccionar archivos
        archivo = filedialog.askopenfilename(title="Selecciona un archivo")

        # Actualiza la variable con la dirección del archivo seleccionado
        if archivo:
            variable_archivo.set(archivo)
            labelFile.config(text = "Data Base File Selected")
            
        
        
    variable_archivo = tk.StringVar()
    
    DataB = tk.Button(Inicio, command = SelectFile, text = "Search File")
    DataB.place(x = 80, y = 200)
    
    def ObtainDate():
        daySelected = combo_day.get()
        monthSelected = combo_month.get()
        yearSelected = combo_year.get()
        
        
        #Muestra la fecha seleccionada
        if daySelected != "" and monthSelected != "" and yearSelected != "":
            labelResult.config(text = f"Date Selected: {daySelected} {monthSelected} {yearSelected}")
        else:
            labelText = labelResult.cget("text")
            #print(labelText, type(labelText))
            if labelText == "":
                # Get the current date and time
                current_date_time = datetime.now()
                # Extract the year, month, and day as integers
                currentYear = current_date_time.year
                currentMonth = current_date_time.month
                currentDay = current_date_time.day
                #print(currentYear, currentMonth, currentDay, type(currentYear))
                months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                actualMonthSelected = months[currentMonth - 1]
                
                labelResult.config(text = f"Date Selected: {currentDay} {actualMonthSelected} {currentYear} (Today)")
            else: 
                labelResult.config(text = "One option is empty, need a complete date")
    
        
    # Dias
    days = [str(i) for i in range(1, 32)]
    days_label = tk.Label(window, text = "Day:")
    days_label.place(x = 80, y = 300)
    combo_day = ttk.Combobox(window, values= days, state = "readonly")
    combo_day.place(x = 80, y = 325)
    
    # Meses
    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    months_label = tk.Label(window, text = "Month:")
    months_label.place(x = 80, y = 350)
    combo_month = ttk.Combobox(window, values = months, state = "readonly")
    combo_month.place(x = 80, y = 375)
    
    
    # Years
    years = [str(i) for i in range(1990, 2030)]
    years_label = tk.Label(window, text = "Year:")
    years_label.place(x = 80, y = 400)
    combo_year = ttk.Combobox(window, values = years, state = "readonly")
    combo_year.place(x = 80, y = 425)
    
    
    DateB = tk.Button(Inicio, text = "Select Date", command = ObtainDate)
    DateB.place(x = 80, y = 450)
    
    labelResult = tk.Label(window, text = "")
    labelResult.place(x = 80, y = 475)
    
    labelFile = tk.Label(window, text = "")
    labelFile.place(x = 80, y = 225)
    
    
    # Este es el text box en el cual se va a colocar la informacoin que viene del DB
    TextBox = tk.Text(window, width = 50, height = 25)
    TextBox.insert(tk.END, "")
    TextBox.config(state = 'disabled')
    TextBox.place(x = 350, y = 150)
    
    
    ObtainDate()
    
    window.mainloop()
    

PantallaInicial(window, Inicio)