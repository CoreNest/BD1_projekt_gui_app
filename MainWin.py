import psycopg2
import PySimpleGUI as sg


class MainWin:
    def MainLoop(self ):
        while True:  # Event Loop
            window, event, values = sg.read_all_windows()
            # print(window, event, values, end = "\n\n") # testing info TODO delete befor lunch
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                if (window == self.windowMain):
                    break
                else:
                    for i in range(len(self.windows)):
                        if self.windows[i] == window:
                            self.windows[i].close()
                            del self.windows[i]
                            break

            elif event == 'Dodaj rekord':
                self.DodajRekord(values)
            elif event == 'Sprawdź tabele':
                self.windows.append(self.prostyWidokTabeli(
                    values['-tabela-']))
                print(len(self.windows))
            elif event =='Raporty1': 
                self.windows.append(self.prostyWidokTabeli(
                   "preatyarmy"   ))
            elif event =='Raporty2': 
                self.windows.append(self.prostyWidokTabeli(
                   "heroesability"))
            elif event =='Raporty3': 
                self.windows.append(self.prostyWidokTabeli(
                   "zamekprodukuje"))
            elif event =='Raporty4': 
                self.windows.append(self.prostyWidokTabeli(
                   "kingdom_strenght_show"))
            elif event =='Zamknij pod okna': 
                for win in self.windows:
                     win.close()
                self.windows.clear()
                
            
        self.windowMain.close()
        self.conn.close()
        self.conn2.close()
        return 0
    
    def DodajRekord(self, values):
        if(self.poziomdostepu == "S" or self.poziomdostepu == "W"):
            Tabela = values['-tabela-']
            coll = self.TableCol[Tabela]
            stringCol = ""
            stringColVall = ""
            for x in coll:
                if(values[f"-IN_{Tabela}_{x}-"]!=''):
                    if stringCol != "" :
                        stringCol += ', '
                    stringCol += x
                    if stringColVall :
                        stringColVall += ', '
                    val = values[f"-IN_{Tabela}_{x}-"]
                    stringColVall += "'"+val+"'" 
                
            cur = self.conn.cursor()
            try:        
                cur.execute(f"INSERT INTO \"{Tabela}\" ({stringCol}) values  ({stringColVall});"   )
            except Exception as e:
                sg.popup_error(f"{e.pgerror}")
            self.conn.commit()
            print(f" dodanie rekordu do Tabeli{Tabela}: ({stringCol})  {stringColVall}")
        else:
            sg.popup("nie masz uprawnień do dodawania rekordów")
    
    # get all coll identification
    def getLayoutForTable(self,name):
        cur = self.conn2.cursor()
        cur.execute("SELECT *\
                    FROM information_schema.columns\
                    WHERE table_schema = 'public'\
                    AND table_name   = '"+name+"'\
                        ;")
        rows = cur.fetchall()
        tab = []
        coll = []
        for row in rows:
            co = " " or row[5]
            if (row[5] != "nextval('\""+name+"_id_seq\"'::regclass)"):
                tab.append([sg.Text(row[3], size=(12, 1)),sg.Text(f"({row[5]})", size=(15, 1)),sg.Text(f"({row[7]})", size=(10, 1)),
                            sg.Input(key="-IN_"+name+'_'+row[3]+'-')])
                coll.append(row[3] or '')                
            else:
                tab.append([sg.Text(row[3], size=(37, 1)),
                            sg.Text("auto incrementacja")])
        self.TableCol[name] = coll 
        return tab

    def getBaseTab(self):
        cur = self.conn.cursor()        
        cur.execute(
            "SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';") 
        rows = cur.fetchall()
        tab = []
        for row in rows:
            name = row[2]
            tab.append(sg.Tab(name, self.getLayoutForTable(name)))
        return tab
    
    def __init__(self,poziomdostepu="S", database="bbsssvid", username="bbsssvid", password= "9QxksMlVDsQ1iF3N46ax6jYZ5ueB-gle", host="mel.db.elephantsql.com", port="5432")  :
        self.poziomdostepu = poziomdostepu
        self.conn = psycopg2.connect(database=database, user=username, password=password, host=host, port=port)
        self.conn2 = psycopg2.connect(database=database, user=username, password= password, host=host, port=port)
        print("Opened database successfully")
        sg.theme('Dark')
        self.TableCol = dict([])
        self.TableColAll = dict([])
        self.col = [
            [sg.Button('Dodaj rekord')],
            [sg.Button('Sprawdź tabele')],
            [sg.Button('Raporty1')],
            [sg.Button('Raporty2')],
            [sg.Button('Raporty3')],
            [sg.Button('Raporty4')],
            [sg.Button('Zamknij pod okna')]
            ]
        self.layout =[
            [
            sg.Column(self.col),
            sg.TabGroup([self.getBaseTab()], key='-tabela-', tab_location='top', selected_title_color='purple')
            ],
            [sg.Text("*wartości defoltowe w () jeśli None dana jest wymagana")] ]
        
        self.windowMain = sg.Window('GUI DB Menager', self.layout, finalize=True)
        self.windows = []
        self.MainLoop()
        
    def prostyWidokTabeli(self, name):    
        cur = self.conn.cursor()
        # all information of any table takem from data base
        layout = None
        if(self.poziomdostepu == "S" or self.poziomdostepu == "R"):
            cur.execute("SELECT * FROM \""+name+"\"")
            rows = cur.fetchall()
            dane = []
            column_names = [desc[0] for desc in cur.description]
            for row in rows:
                wiersz =[row[i] for i in range(len(row))]
                dane.append(wiersz)               
                    
            layout=[[sg.Table(values=dane, headings=column_names, justification= "center" , num_rows= len(rows) if len(rows)<=25 else 25 )]]
        else:
            layout=[[sg.Text("nie masz uprawnień do odczytu")]]
        return sg.Window(name, layout,finalize=True)
        