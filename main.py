
import tkinter as tk
import tkinter.messagebox; import tkinter.ttk
import mysql.connector
import pymysql
import pymysql.cursors

MYSQL_CONNECTOR=None
USERNAME="user1"
USERTYPE="Администратор"
SELECTED_TABLE_NAME=""
def showLoginMenu():
    global bigRectLOGIN
    entry1LOGIN.place(width=1082,height=75,x=419,y=346)
    entry1LOGIN.delete(0,'end')
    entry2LOGIN.place(width=1082,height=75,x=419,y=528)
    entry2LOGIN.delete(0,'end')
    label1LOGIN.place(x=419,y=294)
    label2LOGIN.place(x=419,y=476)
    bigRectLOGIN=canvas.create_rectangle(386,255,386+1148,255+569,fill="#D9D9D9",outline="")
    buttonLOGIN.place(x=1251,y=689,width=250,height=100)

def hideLoginMenu():
    entry1LOGIN.place_forget()
    entry2LOGIN.place_forget()
    label1LOGIN.place_forget()
    label2LOGIN.place_forget()    
    canvas.delete(bigRectLOGIN)
    buttonLOGIN.place_forget()


def login():
    global MYSQL_CONNECTOR
    try:
        MYSQL_CONNECTOR=mysql.connector.connect(user=entry1LOGIN.get(),password=entry2LOGIN.get(),host="localhost",database="cursach")
        hideLoginMenu()
        showHELLOMenu()
    except mysql.connector.Error as err:
        print(err)
        tk.messagebox.showerror(title="Ошибка входа!",message="Проверьте верность пароля и логина!")
    
    




#Окно логина
root=tk.Tk()

root.title("Вход в систему")
root.minsize(1920,1080)
root.minsize(1800,900)
canvas=tk.Canvas(root,bg="white",width=1920,height=1080)
canvas.pack(fill="both",expand=True)
bigRectLOGIN=None
label1LOGIN=tk.Label(root,font="Times 32",text="Введите логин")
label2LOGIN=tk.Label(root,font="Times 32",text="Введите пароль")
entry1LOGIN=tk.Entry(root,font="Times 32",background="#484848")
entry2LOGIN=tk.Entry(root,font="Times 32",show="*",background="#484848")
buttonLOGIN=tk.Button(text="Вход",font="Times 32",background="#DF7878",activebackground="#DF7878",command=lambda:{login()})

showLoginMenu()



def showHELLOMenu():
    global bigRectHELLO,textHELLO,header
    bigRectHELLO=canvas.create_rectangle(386,255,386+1148,255+569,outline="",fill="#D9D9D9")
    header=canvas.create_rectangle(0,0,1920,50,fill="#DB9494")
    textHELLO=tk.Label(root,font="Times 28",anchor="w",justify="left",text="Здравствуйте, "+USERNAME+"!\n\nВы вошли в систему как "+USERTYPE+"\n\nДля работы с системой нажмите на одну из кнопок сверху.")
    textHELLO.place(x=476,y=392,width=939,height=273)
    buttonClients.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideHELLOMenu(),showClientsMenu()})
    buttonCredits.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideHELLOMenu(),showCreditsMenu()})
    buttonPolicies.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideHELLOMenu(),showCreditPoliciesMenu()})
    buttonExit.configure(command=lambda:{hideHELLOMenu(),showLoginMenu()})
    buttonExit.place(x=1764,y=0,width=156,height=50)
    buttonClients.place(x=0,y=0,width=400,height=50)
    buttonCredits.place(x=400,y=0,width=400,height=50)
    buttonPolicies.place(x=800,y=0,width=400,height=50)
    usernameLabel.configure(text=USERNAME)
    usernameLabel.place(x=1637,y=6,width=106,height=39)
    if USERTYPE=="Администратор":
        buttonAdminister.place(x=1200,y=0,width=400,height=50)
        buttonAdminister.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideHELLOMenu(),showAdministerMenu()})        


def hideHELLOMenu():
    canvas.delete(bigRectHELLO)
    canvas.delete(header)
    textHELLO.place_forget()    
    buttonClients.place_forget()
    buttonCredits.place_forget()
    buttonPolicies.place_forget()
    buttonExit.place_forget()
    usernameLabel.place_forget()
    if USERTYPE=="Администратор":
        buttonAdminister.place_forget()


#Приветственное окно
bigRectHELLO=None
textHELLO=None
buttonClients=tk.Button(text="Клиенты",font="Times 32",background="#DB9494",activebackground="#DB9494")
buttonCredits=tk.Button(text="Кредиты",font="Times 32",background="#DB9494",activebackground="#DB9494")
buttonPolicies=tk.Button(text="Кредитные политики",font="Times 32",background="#DB9494",activebackground="#DB9494")
buttonAdminister=tk.Button(text="Администрирование",font="Times 32",background="#DB9494",activebackground="#DB9494")
header=None
buttonExit=tk.Button(text="Выйти",font="Times 32",background="#D9D9D9",activebackground="#D9D9D9")
usernameLabel=tk.Label(font="Times 32",background="#DB9494",foreground="#4E4E4E")



def showClientsMenu():
    global header
    header=canvas.create_rectangle(0,0,1920,50,fill="#DB9494")    
    buttonClients.configure(background="#D9D9D9",activebackground="#D9D9D9",command=lambda:{hideClientsMenu(),showClientsMenu()})
    buttonCredits.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideClientsMenu(),showCreditsMenu()})
    buttonPolicies.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideClientsMenu(),showCreditPoliciesMenu()})
    buttonExit.configure(command=lambda:{hideClientsMenu(),showLoginMenu()})
    buttonExit.place(x=1764,y=0,width=156,height=50)
    buttonClients.place(x=0,y=0,width=400,height=50)
    buttonCredits.place(x=400,y=0,width=400,height=50)
    buttonPolicies.place(x=800,y=0,width=400,height=50)
    usernameLabel.configure(text=USERNAME)
    usernameLabel.place(x=1637,y=6,width=106,height=39)
    entryPassportFilterCLIENTS.delete(0,'end')
    addClientButtonCLIENTS.place(x=33,y=82,width=367,height=105)
    changeClientButtonCLIENTS.place(x=408,y=82,width=367,height=105)
    labelPassportFilterCLIENTS.place(x=54,y=256,width=333,height=42)
    entryPassportFilterCLIENTS.place(x=416,y=227,width=367,height=105)
    applyFiltersButtonCLIENTS.place(x=1544,y=227,width=367,height=105)
    if USERTYPE=="Администратор":
        buttonAdminister.place(x=1200,y=0,width=400,height=50)
        buttonAdminister.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideClientsMenu(),showAdministerMenu()})    

def addClient():
    pass    

def changeClient():
    pass  

def applyFiltersPassportClients():
    pass   


#Окно с клиентами
addClientButtonCLIENTS=tk.Button(text="Добавить клиента",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=addClient)
changeClientButtonCLIENTS=tk.Button(text="Поменять данные\nвыбранного клиента",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=changeClient)
labelPassportFilterCLIENTS=tk.Label(text="Фильтр по паспорту:",font="Times 28",background="white")
entryPassportFilterCLIENTS=tk.Entry(font="Times 28",background="#D9D9D9")
applyFiltersButtonCLIENTS=tk.Button(text="Применить фильтры",font="Times 28",activebackground="#DB9494",background="#DB9494",command=applyFiltersPassportClients)
    
 



def hideClientsMenu():
    canvas.delete(header)
    buttonClients.place_forget()
    buttonCredits.place_forget()
    buttonPolicies.place_forget()
    buttonExit.place_forget()
    usernameLabel.place_forget()
    addClientButtonCLIENTS.place_forget()
    changeClientButtonCLIENTS.place_forget()
    labelPassportFilterCLIENTS.place_forget()
    entryPassportFilterCLIENTS.place_forget()
    applyFiltersButtonCLIENTS.place_forget()
    if USERTYPE=="Администратор":
        buttonAdminister.place_forget()



def showAdministerMenu():
    global header
    header=canvas.create_rectangle(0,0,1920,50,fill="#DB9494")    
    buttonClients.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideAdministerMenu(),showClientsMenu()})
    buttonCredits.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideAdministerMenu(),showCreditsMenu()})
    buttonPolicies.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideAdministerMenu(),showCreditPoliciesMenu()})
    buttonExit.configure(command=lambda:{hideAdministerMenu(),showLoginMenu()})
    buttonExit.place(x=1764,y=0,width=156,height=50)
    buttonClients.place(x=0,y=0,width=400,height=50)
    buttonCredits.place(x=400,y=0,width=400,height=50)
    buttonPolicies.place(x=800,y=0,width=400,height=50)
    usernameLabel.configure(text=USERNAME)
    usernameLabel.place(x=1637,y=6,width=106,height=39)
    buttonAdminister.place(x=1200,y=0,width=400,height=50)
    buttonAdminister.configure(background="#D9D9D9",activebackground="#D9D9D9",command=lambda:{hideAdministerMenu(),showAdministerMenu()})   
    buttonChooseTableADMINISTER.place(x=19,y=156,width=367,height=74)
    buttonDeleteChosenADMINISTER.place(x=735,y=83,width=367,height=105)
    buttonChangeChosenADMINISTER.place(x=1135,y=83,width=367,height=105)
    buttonAddElementADMINISTER.place(x=1535,y=83,width=367,height=105)
    labelChooseTableADMINISTER.place(x=19,y=93,width=309,height=42)  
    optionMenuTablesADMINISTER.place(x=388,y=93,width=228,height=42)
    DisplayData()

def DisplayData():
    treeView.place_forget()
    with MYSQL_CONNECTOR.cursor(pymysql.cursors.Cursor) as cursor:
        nam=SELECTED_TABLE_NAME.get()
        print(nam)
        cursor.execute("SELECT * FROM cursach."+SELECTED_TABLE_NAME.get())
        rows=cursor.fetchall()
        treeView.pack(side="bottom")
        for row in rows:
            treeView.insert("","end",values=(row[0],row[1]))
        
            
        


def chooseTableADMINISTER():
    DisplayData()
    pass

def deleteChosenADMINISTER():
    pass

def changeChosenADMINISTER():
    pass

def insertQuery(query):
    cur=MYSQL_CONNECTOR.cursor()
    cur.execute(query)
    MYSQL_CONNECTOR.commit()


def addElementADMINISTER():
    top=tk.Toplevel(root,background="white")    
    if(SELECTED_TABLE_NAME.get()=="userTypes"):
        top.minsize(400,400)
        top.maxsize(400,400)
        tk.Label(top,text="Введите название типа пользователей:",background="white").place(x=0,y=0)
        ut=tk.Entry(top,background="#D9D9D9")
        ut.place(x=0,y=50)
        
        tk.Button(top,text="Создать",activebackground="#DB9494",background="#DB9494",
                  command=lambda: {insertQuery("INSERT INTO cursach."+SELECTED_TABLE_NAME.get()+" (id, name) VALUES (0,\""+ut.get()+"\")") }).place(x=0,y=200)

    try:    
        top.transient(root)
        top.grab_set()
        top.focus_set()
        top.wait_window()
        DisplayData()
    except mysql.connector.Error as err:
        tkinter.messagebox.ERROR("Ошибка сохранения в БД!", "Проверьте, что все логическая целостность соблюдатся,\n все not-null значения не являются null,\n все уникальные значения остаются уникальными")


#Меню для администратора
buttonChooseTableADMINISTER=tk.Button(text="Выбрать таблицу",font="Times 28",activebackground="#DB9494",background="#DB9494",command=chooseTableADMINISTER)
buttonDeleteChosenADMINISTER=tk.Button(text="Удалить выбранное",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=deleteChosenADMINISTER)
buttonChangeChosenADMINISTER=tk.Button(text="Изменить выбранное",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=changeChosenADMINISTER)
buttonAddElementADMINISTER=tk.Button(text="Добавить элемент",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=addElementADMINISTER)
labelChooseTableADMINISTER=tk.Label(text="Выберите таблицу:",font="Times 28",activebackground="white",background="white")
treeView=tk.ttk.Treeview(root)
SELECTED_TABLE_NAME=tk.StringVar(root)
tables=("clients","credits","users","userTypes","pledges","timespans","overduePayments")
SELECTED_TABLE_NAME.set("clients")
optionMenuTablesADMINISTER=tk.OptionMenu(root,SELECTED_TABLE_NAME,*tables)



def hideAdministerMenu():
    canvas.delete(header)
    buttonClients.place_forget()
    buttonCredits.place_forget()
    buttonPolicies.place_forget()
    buttonExit.place_forget()
    usernameLabel.place_forget()    
    buttonAdminister.place_forget()
    buttonChooseTableADMINISTER.place_forget()
    buttonDeleteChosenADMINISTER.place_forget()
    buttonChangeChosenADMINISTER.place_forget()
    buttonAddElementADMINISTER.place_forget()
    labelChooseTableADMINISTER.place_forget()
    optionMenuTablesADMINISTER.place_forget()


def showCreditsMenu():
    global header
    header=canvas.create_rectangle(0,0,1920,50,fill="#DB9494")    
    buttonClients.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideCreditsMenu(),showClientsMenu()})
    buttonCredits.configure(background="#D9D9D9",activebackground="#D9D9D9",command=lambda:{hideCreditsMenu(),showCreditsMenu()})
    buttonPolicies.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideCreditsMenu(),showCreditPoliciesMenu()})
    buttonExit.configure(command=lambda:{hideCreditsMenu(),showLoginMenu()})
    buttonExit.place(x=1764,y=0,width=156,height=50)
    buttonClients.place(x=0,y=0,width=400,height=50)
    buttonCredits.place(x=400,y=0,width=400,height=50)
    buttonPolicies.place(x=800,y=0,width=400,height=50)
    usernameLabel.configure(text=USERNAME)
    usernameLabel.place(x=1637,y=6,width=106,height=39)
    entryAccountFilterCREDIT.delete(0,'end')
    entryPassportFilterCREDIT.delete(0,'end')
    buttonRestructureCREDIT.place(x=17,y=83,width=367,height=105)
    buttonCreditExcreptCREDIT.place(x=393,y=83,width=367,height=105)
    buttonChangeGlobalCreditLimitCREDIT.place(x=770,y=83,width=367,height=105)
    buttonCloseAccountCREDIT.place(x=1147,y=83,width=367,height=105)
    buttonGetOverallCreditRiskCREDIT.place(x=1524,y=83,width=367,height=105)
    labelPassportFilterCREDIT.place(x=54,y=259,width=333,height=42)
    entryPassportFilterCREDIT.place(x=416,y=227,width=367,height=105)
    labelAccountFilterCREDIT.place(x=799,y=259,width=275,height=42)
    entryAccountFilterCREDIT.place(x=1161,y=227,width=367,height=105)
    buttonApplyFiltersCREDIT.place(x=1544,y=227,width=367,height=105)
    if USERTYPE=="Администратор":
        buttonAdminister.place(x=1200,y=0,width=400,height=50)
        buttonAdminister.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideCreditsMenu(),showAdministerMenu()})   


def restructureCredit():
    pass

def excreptFromCredit():
    pass

def changeGlobalCreditLimit():
    pass

def closeAccount():
    pass

def getOverallCreditRisk():
    pass

def applyFiltersButtonCREDIT():
    pass

#окно с кредитами
buttonRestructureCREDIT=tk.Button(text="Реструктуризация\nвыбранного кредита",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=restructureCredit)
buttonCreditExcreptCREDIT=tk.Button(text="Выписка по\nвыбранному кредита",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=excreptFromCredit)
buttonChangeGlobalCreditLimitCREDIT=tk.Button(text="Изменить глобальный\nкредитный лимит",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=changeGlobalCreditLimit)
buttonCloseAccountCREDIT=tk.Button(text="Закрыть счёт",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=closeAccount)
buttonGetOverallCreditRiskCREDIT=tk.Button(text="Получить общий\nкредитный риск",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=getOverallCreditRisk)
labelPassportFilterCREDIT=tk.Label(text="Фильтр по паспорту:",font="Times 28",background="white")
entryPassportFilterCREDIT=tk.Entry(font="Times 28",background="#D9D9D9")
labelAccountFilterCREDIT=tk.Label(text="Фильтр по счету:",font="Times 28",background="white")
entryAccountFilterCREDIT=tk.Entry(font="Times 28",background="#D9D9D9")
buttonApplyFiltersCREDIT=tk.Button(text="Применить фильтры",font="Times 28",activebackground="#DB9494",background="#DB9494",command=applyFiltersButtonCREDIT)


def hideCreditsMenu():
    canvas.delete(header)
    buttonClients.place_forget()
    buttonCredits.place_forget()
    buttonPolicies.place_forget()
    buttonExit.place_forget()
    usernameLabel.place_forget()
    buttonRestructureCREDIT.place_forget()
    buttonCreditExcreptCREDIT.place_forget()
    buttonChangeGlobalCreditLimitCREDIT.place_forget()
    buttonCloseAccountCREDIT.place_forget()
    buttonGetOverallCreditRiskCREDIT.place_forget()
    labelPassportFilterCREDIT.place_forget()
    entryPassportFilterCREDIT.place_forget()
    labelAccountFilterCREDIT.place_forget()
    entryAccountFilterCREDIT.place_forget()
    buttonApplyFiltersCREDIT.place_forget()
    if USERTYPE=="Администратор":
        buttonAdminister.place_forget()


def showCreditPoliciesMenu():
    global header
    header=canvas.create_rectangle(0,0,1920,50,fill="#DB9494")    
    buttonClients.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideCreditPoliciesMenu(),showClientsMenu()})
    buttonCredits.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideCreditPoliciesMenu(),showCreditsMenu()})
    buttonPolicies.configure(background="#D9D9D9",activebackground="#D9D9D9",command=lambda:{hideCreditPoliciesMenu(),showCreditPoliciesMenu()})
    buttonExit.configure(command=lambda:{hideCreditPoliciesMenu(),showLoginMenu()})
    buttonExit.place(x=1764,y=0,width=156,height=50)
    buttonClients.place(x=0,y=0,width=400,height=50)
    buttonCredits.place(x=400,y=0,width=400,height=50)
    buttonPolicies.place(x=800,y=0,width=400,height=50)
    usernameLabel.configure(text=USERNAME)
    usernameLabel.place(x=1637,y=6,width=106,height=39)
    buttonCreatePOLICY.place(x=17,y=83,width=367,height=105)
    buttonDeletePOLICY.place(x=393,y=83,width=367,height=105)
    buttonChangePOLICY.place(x=770,y=83,width=367,height=105)
    buttonViewPOLICY.place(x=1147,y=83,width=367,height=105)
    buttonStressTestPOLICY.place(x=1524,y=83,width=367,height=105)
    if USERTYPE=="Администратор":
        buttonAdminister.place(x=1200,y=0,width=400,height=50)
        buttonAdminister.configure(background="#DB9494",activebackground="#DB9494",command=lambda:{hideCreditPoliciesMenu(),showAdministerMenu()})   


def createPOLICY():
    pass

def deletePOLICY():
    pass

def changePOLICY():
    pass

def viewPOLICY():
    pass

def stressTestPOLICY():
    pass

#окно с кредитными политиками
buttonCreatePOLICY=tk.Button(text="Создать кредитную\nполитику",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=createPOLICY)
buttonDeletePOLICY=tk.Button(text="Удалить выбранную\nкредитную политику",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=deletePOLICY)
buttonChangePOLICY=tk.Button(text="Изменить выбранную\nкредитную политику",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=changePOLICY)
buttonViewPOLICY=tk.Button(text="Просмотр\nвыбранной политики",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=viewPOLICY)
buttonStressTestPOLICY=tk.Button(text="Стресс-тестирование\nвыбранной политики",font="Times 28",activebackground="#D9D9D9",background="#D9D9D9",command=stressTestPOLICY)


def hideCreditPoliciesMenu():
    canvas.delete(header)
    buttonClients.place_forget()
    buttonCredits.place_forget()
    buttonPolicies.place_forget()
    buttonExit.place_forget()
    usernameLabel.place_forget()
    buttonCreatePOLICY.place_forget()
    buttonDeletePOLICY.place_forget()
    buttonChangePOLICY.place_forget()
    buttonViewPOLICY.place_forget()
    buttonStressTestPOLICY.place_forget()
    if USERTYPE=="Администратор":
        buttonAdminister.place_forget() 


root.mainloop() 
