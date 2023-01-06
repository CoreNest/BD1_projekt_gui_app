import PySimpleGUI as sg
def log():
    f = open("user.dat", "r")   
    data = []
    ret =None
    while True:
        line = f.readline()
        if not line:
            break
        data.append(line.split(" "))
        
    print(data[1])
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Login'), sg.InputText("",key='-login-')],
                [sg.Text('Haslo'), sg.InputText("",key='-password-')],
                [sg.Button('Log') ]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == 'Log':
            for k in data:
                if(values['-login-'] == k[0]):
                    if(values['-password-']== k[1]):
                        ret = k[2][0]
                        print('You entered ', ret)
            if ret:
                break
            else:
                sg.popup("zly login lub haslo")        
    window.close()
    return ret or "B"