"""
Programa para poder controlar una Base de Datos Denon 
Autor: Oscar Arturo Acuna Duran
"""


import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

from collections import defaultdict



window = tk.Tk()
window.title("DenonDataBase")
window.minsize(1000,700)
window.resizable(False, False)



Inicio = tk.Canvas(window, width = 1000, height = 700)
Inicio.place(x = 0, y = 0)


#Esta funcion destruye los label en el momento en el que se pasa a otra pantalla 
def labelDest(List):
    if List == []:
        return []
    else:
        (List[0]).destrou()
        labelDest(List[1:])

#Pantalla inicial de Tkinter
def PantallaInicial(window, Inicio):
    
    # Label que muestra el nombre de la aplicacion en grande en la interfaz 
    MainLabel = tk.Label(Inicio, text = "Denon Information DB", font = ("Arial", 20))
    MainLabel.place(x = 350, y = 50)
    
    
    #Se quiere crear un boton el cual busque en el computador los datos
    def SelectFile():
        
        # Abre el cuadro de diálogo para seleccionar archivos
        archivo = filedialog.askopenfilename(title="Selecciona un archivo")

        # Actualiza la variable con la dirección del archivo seleccionado
        if archivo:
            variable_archivo.set(archivo)
            print(variable_archivo.get())
            labelFile.config(text = "Data Base File Selected")
            # Se coloca esto para poder permitir que se elijan los años
            # (FALTA) Solo aparezcan años con registro
            enableYear()
            
        
    # Obtiene la direccion del archivo como un string 
    variable_archivo = tk.StringVar()
    
    # Boton que acciona Select File para abrir el buscador de archivos
    DataB = tk.Button(Inicio, command = SelectFile, text = "Search File")
    DataB.place(x = 80, y = 200)
    
    
    #Funcion que permite obtener el dia
    def ObtainDate():
        
        #Configuracion de dia, mes y año
        daySelected = combo_day.get()
        monthSelected = combo_month.get()
        yearSelected = combo_year.get()
        
        
        #Muestra la fecha seleccionada
        if daySelected != "" and monthSelected != "" and yearSelected != "":
            labelResult.config(text = f"Date Selected: {daySelected} {monthSelected} {yearSelected}")
        else:
            #Esto se ejecuta al instanciar la aplicacion
            labelText = labelResult.cget("text")
            if labelText == "":
                # Se obtiene el dia presente
                current_date_time = datetime.now()
                # Se obtiene el año, mes y dia como int
                currentYear = current_date_time.year
                currentMonth = current_date_time.month
                currentDay = current_date_time.day
                
                months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                actualMonthSelected = months[currentMonth - 1]
                #Se coloca un Label con el dia presente cuando se abre la aplicacion
                labelResult.config(text = f"Date Selected: {currentDay} {actualMonthSelected} {currentYear} (Today)")
            else: 
                #En el caso en el que el usuario no coloque uno de los datos se muestra el siguiente mensaje
                labelResult.config(text = "One option is empty, need a complete date")
                
    def ObtainSongs():
        # Quiero obtener en el formato establecido la fecha
        # Se obtiene el Label de la fecha como un string
        dateResult = labelResult.cget("text")
        separateData = dateResult.split()
        selectedDay = int(separateData[2])
        months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        strMonth = separateData[3]
        selectedMonth = months.index(strMonth) + 1
        selectedYear = int(separateData[4])
        
        #A partir de este punto se tiene un int para Mes Año y Dia
        #Se agrega un 0 en el mes si es menor a 10 por que ese es el formato de la DB
        #Ej si es septiembre debe de ser 09 y no 9
        if selectedMonth < 10:
            finalStructure = str(selectedYear) + "-" + "0" +str(selectedMonth) + "-" + str(selectedDay)
        else:
            finalStructure = str(selectedYear) + "-" + str(selectedMonth) + "-" + str(selectedDay)
        
        #Se establece la conexcion a sqlite
        conection = sqlite3.connect(variable_archivo.get())
        cursor = conection.cursor()
        #Comando que permite obtener la ultima ves que sono a partir de la tabla Track
        cursor.execute('SELECT timeLastPlayed FROM Track')
        results = cursor.fetchall()
        
        #Los datos arrojados en timeLastPlayed estan en un formato Unix, se quiere pasar a un formato legible
        UnixFormat = []
        for result in results:
            UnixFormat.append(result[0])
        
        #En dates estan los timeLastPlayed pero en un formato legible
        dates = [datetime.fromtimestamp(ts) for ts in UnixFormat]
        #Se hace un String de los datos de Dates para poder manipularlos en Python
        dtString = []
        for date in dates:
            dtString += [date.strftime("%Y-%m-%d %H:%M:%S")]
        
        #Se hace una lista de llaves para poder llevar el control en el formato Unix
        keyList = []
        for date in dtString:
            if finalStructure in date:
                keyList.append(dtString.index(date))
        
        #Como lo anterior esta en Tuplas se hace TimeMarks para tenerlo en una Lista
        timeMarks = []
        for i in keyList:
            timeMarks.append(results[i][0])
            
        #Ahora se van a hacer unas consultas para obtener los nombres de las canciones
        songNames = []
        placeHolders = ','.join(['?' for _ in range(len(timeMarks))])
        cursor.execute("SELECT title, artist FROM Track WHERE timeLastPlayed IN ({})".format(placeHolders), timeMarks)
        #La variable finalResults tiene lo que se obtuvo en cursor
        finalResults = cursor.fetchall()
        
        
        #Borrar lo que esta en el textBox (HACERLO)
        
        #Se colocan los datos en el TextBox
        TextBox.config(state = 'normal')
        
        Counter = 1
        for result in finalResults:
            subResult = result[0].split()
            finResult = subResult[2:]
            finalStr = ""
            for i in finResult:
                finalStr += i + " "
            TextBox.insert(tk.END, str(Counter) + " - " + result[1] + " - " + finalStr + "\n")
            Counter += 1
        TextBox.config(state = "disabled")
        
        
        
        
        
    
        
    # Dias
    days = [str(i) for i in range(1, 32)]
    days_label = tk.Label(window, text = "Day:")
    days_label.place(x = 80, y = 400)
    combo_day = ttk.Combobox(window, values= days, state = "disabled")
    combo_day.place(x = 80, y = 425)
    
    def enableDay():
        combo_day.config(state = "readonly")
    
    def disableDay():
        combo_day.config(state = "disabled")
    
    # Meses
    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    months_label = tk.Label(window, text = "Month:")
    months_label.place(x = 80, y = 350)
    combo_month = ttk.Combobox(window, values = months, state = "disabled")
    combo_month.place(x = 80, y = 375)
    
    def enableMonth():
        combo_month.config(state = "readonly")
    
    def disableMonth():
        combo_month.config(state = "disabled")
    
    
    # Years
    def onYearSelected(event):
        selectedValue = combo_year.get()
        enableMonth()
        print("Selected value: ", selectedValue)
    
    years = [str(i) for i in range(1990, 2030)]
    years_label = tk.Label(window, text = "Year:")
    years_label.place(x = 80, y = 300)
    combo_year = ttk.Combobox(window, values = years, state = "disabled")
    combo_year.place(x = 80, y = 325)
    
    #Bind to onYearSelected
    combo_year.bind("<<ComboboxSelected>>", onYearSelected)
    
    def enableYear():
        #Se quiere obtener los años disponibles para solo mostrar esos
        conection = sqlite3.connect(variable_archivo.get())
        cursor = conection.cursor()
        #Se obtiene la ultima ves que sono a partir de tabla Track
        cursor.execute('SELECT timeLastPlayed FROM Track')
        results = cursor.fetchall()
        
        #Estan en formato Unix, se convierten
        UnixFormat = []
        for result in results:
            UnixFormat.append(result[0])
        dates = [datetime.fromtimestamp(ts) for ts in UnixFormat]
        dtString = []
        
        for date in dates:
            dtString += [date.strftime("%Y-%m-%d %H:%M:%S")]
        
        #print(dtString)
        # en dtString estan todas las fechas
        # Ahora se va a proceder a obtener solamente los años
        
        yearsWithTrack = []
        for year in dtString:
            if int(year[0:4]) in yearsWithTrack:
                pass
            else:
                yearsWithTrack.append(int(year[0:4]))
        combo_year.config(values = yearsWithTrack)
        combo_year.config(state = "readonly")
        
        
    def disableYear():
        combo_year.config(state = "disabled")
        
    
    
    
    DateB = tk.Button(Inicio, text = "Select Date", command = ObtainDate)
    DateB.place(x = 80, y = 450)
    
    ObtainResults = tk.Button(Inicio, text = "Obtain Results", command = ObtainSongs)
    ObtainResults.place(x = 80, y = 550)
    
    labelResult = tk.Label(window, text = "")
    labelResult.place(x = 80, y = 475)
    
    labelFile = tk.Label(window, text = "")
    labelFile.place(x = 80, y = 225)
    
    
    # Este es el text box en el cual se va a colocar la informacoin que viene del DB
    TextBox = tk.Text(window, width = 75, height = 25)
    TextBox.insert(tk.END, "")
    TextBox.config(state = 'disabled')
    TextBox.place(x = 350, y = 150)
    
    
    ObtainDate()
    
    window.mainloop()
    

PantallaInicial(window, Inicio)