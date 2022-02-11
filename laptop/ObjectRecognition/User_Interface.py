
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
import pickle
import scratch
import Recognition_test
import threading
import time
from tkinter import ttk
import training

if __name__ == "__main__":

    window = tk.Tk()
    window.title('Navigation Helper Helmet System')
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    ww = 450
    wh = 330
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    window.resizable(width=False, height=False)

    # welcome image
    canvas = tk.Canvas(window, height=200, width=500)
    image_file = tk.PhotoImage(file='d:/ObjectRecognition/logo.png')
    image = canvas.create_image(160, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')

    # user information
    tk.Label(window, text='User name: ').place(x=70, y=200)
    tk.Label(window, text='Password: ').place(x=70, y=240)

    var_usr_name = tk.StringVar()
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=200)
    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=240)


    def usr_login():
        usr_name = var_usr_name.get()
        usr_pwd = var_usr_pwd.get()
        try:
            with open('usrs_info.txt', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_info.txt', 'wb') as usr_file:
                usrs_info = {'pi': '12345678'}
                pickle.dump(usrs_info, usr_file)
        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]:
                situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
                situation.write('0')
                situation.close()
                situation = open('D:/ObjectRecognition/translate/User_control_motor.txt', 'w+')
                situation.write('0')
                situation.close()
                tk.messagebox.showinfo(title='Attention',
                                       message='Please make sure you heard the voice "System has been started" from raspberry pi before you start to work.')
                window.destroy()
                global window1
                window1=tk.Tk()
                window1.title('Navigation Helper Helmet System')
                sw = window1.winfo_screenwidth()
                sh = window1.winfo_screenheight()
                ww = 620
                wh = 800
                x = (sw - ww) / 2
                y = (sh - wh) / 2
                window1.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
                window1.resizable(width=False, height=False)
                function1 = threading.Thread(target=scratch.transffer)
                function1.setDaemon(True)
                function2 = threading.Thread(target=Recognition_test.run)
                function2.setDaemon(True)

                def activate():
                    situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
                    situation.write('1')
                    situation.close()
                    if function1.isAlive():
                        pass
                    #time.sleep(1)
                    else:
                        function1.start()

                def deactivate():
                    situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
                    situation.write('-1')
                    situation.close()
                    time.sleep(2)
                    window1.destroy()

                def reboot():
                    situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
                    situation.write('-3')
                    situation.close()
                    time.sleep(2)
                    window1.destroy()

                def motor():
                    f = open('D:/ObjectRecognition/translate/User_control_motor.txt', 'r+')
                    token = f.readline()
                    if token == '0':
                        situation = open('D:/ObjectRecognition/translate/User_control_motor.txt', 'w+')
                        situation.write('1')
                        tk.messagebox.showinfo('Motor', 'The motor is working.')
                    else:
                        situation = open('D:/ObjectRecognition/translate/User_control_motor.txt', 'w+')
                        situation.write('0')
                        tk.messagebox.showinfo('Motor', 'The motor is stoping.')


                def DIY_distance():
                    def DIY(rotate):
                        nd = new_distance.get()
                        situation1 = open('D:/ObjectRecognition/translate/User_distance.txt', 'wb')
                        situation1.write(nd.encode())
                        situation1.close()
                        situation2 = open('D:/ObjectRecognition/translate/User_rotation.txt', 'wb')
                        situation2.write(str(rotate).encode())
                        situation2.close()
                        tk.messagebox.showinfo('Custom settings', 'The data has been successfully changed.')
                        User_DIY.destroy()

                    def Rotation(self):
                        global rotate
                        if new_rotate.get()=='normal':
                            rotate = 2
                        elif new_rotate.get()=='slow':
                            rotate = 4
                        elif new_rotate.get()=='very slow':
                            rotate = 8

                    User_DIY=tk.Toplevel(window1)
                    sw = User_DIY.winfo_screenwidth()
                    sh = User_DIY.winfo_screenheight()
                    ww = 400
                    wh = 250
                    x = (sw - ww) / 2
                    y = (sh - wh) / 2
                    User_DIY.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
                    User_DIY.title('Custom settings')
                    User_DIY.resizable(width=False, height=False)

                    new_distance = tk.StringVar()
                    #new_distance.set('2')
                    tk.Label(User_DIY,text='Distance:').place(x=125, y=50)
                    entry_new_distance = tk.Entry(User_DIY, width=8, textvariable=new_distance)
                    entry_new_distance.place(x=190, y=52)
                    tk.Label(User_DIY, text='meter').place(x=240, y=50)

                    new_rotate = ttk.Combobox(User_DIY, width=8, state='readonly')
                    new_rotate.pack()
                    new_rotate.grid(padx=190,pady=120)
                    tk.Label(User_DIY, text='Rotation:').place(x=125, y=120)
                    new_rotate['value'] = ('normal','slow','very slow')
                    new_rotate.current(0)
                    rotate = 2
                    new_rotate.bind("<<Comboboxselected>>", Rotation)

                    btn_comfirm = tk.Button(User_DIY, text='confirm', command=lambda: DIY(rotate))
                    btn_comfirm.place(x=175,y=185)
                    User_DIY.bind("<Return>", DIY)

                    User_DIY.iconbitmap("d:/ObjectRecognition/logo.ico")

                def retraining():
                    def screen():
                        nn = new_name.get()
                        nu = new_number.get()
                        if nn == ' ' or nu == ' ':
                            tk.messagebox.showerror(title='Error', message='Your input is invalid, try again.')
                        if messagebox.askokcancel("Warning", "The same name's picture would be covered."):
                            Train.destroy()
                            situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
                            situation.write('2')
                            situation.close()
                            time.sleep(0.5)
                            function1.start()
                            function4 = threading.Thread(target=training.CatchPICFromVideo(int(nu.strip()), 'D:/ObjectRecognition/data/%s' % (nn)))
                            function4.start()

                    def fun(self):
                        screen()

                    tk.messagebox.showinfo('Attention', 'This function is only used for prepare add new user in face recognition.')
                    Train = tk.Toplevel(window1)
                    sw = Train.winfo_screenwidth()
                    sh = Train.winfo_screenheight()
                    ww = 400
                    wh = 250
                    x = (sw - ww) / 2
                    y = (sh - wh) / 2
                    Train.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
                    Train.title('Custom settings')
                    Train.resizable(width=False, height=False)

                    new_name = tk.StringVar()
                    tk.Label(Train, text='Name:').place(x=125, y=50)
                    entry_new_name = tk.Entry(Train, width=8, textvariable=new_name)
                    entry_new_name.place(x=190, y=52)

                    new_number = tk.StringVar()
                    tk.Label(Train, text='Number of pictures:').place(x=90, y=90)
                    entry_new_name = tk.Entry(Train, width=8, textvariable=new_number)
                    entry_new_name.place(x=220, y=92)

                    btn_comfirm = tk.Button(Train, text='confirm', command=screen)
                    btn_comfirm.place(x=175, y=185)
                    Train.bind("<Return>", fun)
                    Train.iconbitmap("d:/ObjectRecognition/logo.ico")
                    Train.mainloop()







                #translate = tk.Button(window1, text='Translate', command=function1.start)
                #translate.place(x=80, y=70)
                recognition = tk.Button(window1, text='recognition', command=function2.start, height=5, width=45)
                recognition.place(x=0, y=230)
                activatation = tk.Button(window1, text='activate', command=activate, height=5, width=45)
                activatation.place(x=0, y=340)
                deactivatation = tk.Button(window1, text='deactivate', command=deactivate, height=5, width=45)
                deactivatation.place(x=0, y=560)
                ras_reboot = tk.Button(window1, text='reboot', command=reboot, height=5, width=45)
                ras_reboot.place(x=0, y=670)
                user_distance = tk.Button(window1, text='parameter', command=DIY_distance, height=5, width=45)
                user_distance.place(x=0, y=10)
                Retrain = tk.Button(window1, text='Retraining', command=retraining, height=5, width=45)
                Retrain.place(x=0, y=120)
                revolve = tk.Button(window1, text='motor', command=motor, height=5, width=45)
                revolve.place(x=0, y=450)
                tk.Label(window1, text='0, Before main system running,press "para\nmeter" button to indentify recognition\ndistance and moter rotation if it\nis nessary.\n\n'
                                       '1, press "recognition" button in order to\nlet recognition system start to prepare.\n\n'
                                       '2, wait a few seconds, then press "activate"\nbutton which makes the raspberry pi \nstart to translate vedio and play voice.\n\n'
                                       '3, If you want to record the recognition\ndetail, please push o button on keyboard.\nPush p button if you want to stop record.\nThe mp4 file is saved in root dictionary.\n\n'
                                       '4, If you want to let moter working, press\n"motor" botton to let it begin to work.\nYou can also press it once again to stop\nit.\n\n'
                                       '5, If you want to close the whole system,\npress the "deactive" button. UI and\nraspberrypi would close automatically.\n\n'
                                       '                        Notice:\n1, If you did not hear the voice guide\ncorrectly, press the "reboot" button to let\nthe whole system reboot.\n'
                                       '2, If you did not follow the rules of system,\nit may work improperly. Use "reboot" to\nrestart it if something wrong with the system.\n'
                                       '3, Close the UI directly will not close\nthe raspberrypi, but close the program on\nit. The program will not start again until\nreboot raspberrpi. Make sure you need to\nclose raspberry pi or not before exit.\n',
                         justify=tk.LEFT,).place(x=350, y=30)
                #tk.Label(window, text='Password: ').place(x=70, y=240)
                #refresh = tk.Button(window1, text='refresh', command=threading.Thread(target=init(function2)).start)
                #refresh.place(x=230, y=220)

                def on_closing():
                    if messagebox.askokcancel("Quit", "Do you want to quit?"):
                        situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
                        situation.write('-2')
                        situation.close()
                        time.sleep(3)
                        window1.destroy()

                #def printtext():
                    #if function1.is_alive():
                        #EditText.insert(1.0, "The translation is working...")
                    #else:
                        #EditText.insert(1.0, "The translation is closed.")
                #EditText = tk.Text(window1, width=20, height=10)
                #EditText.grid(row=2, column=3)
                #printtext()

                window1.protocol("WM_DELETE_WINDOW", on_closing)
                window1.iconbitmap("d:/ObjectRecognition/logo.ico")
                window1.mainloop()
            else:
                tk.messagebox.showerror(title='Error', message='Your password is wrong, try again.')
        else:
            tk.messagebox.showerror(title='Error', message='Your username is wrong, try again.')


    def test_fun(self):
        usr_login()

    # login and sign up button
    btn_login = tk.Button(window, text='Login', command=usr_login)
    btn_login.place(x=210, y=270)
    window.bind("<Return>", test_fun)
    #tk.messagebox.showinfo(title='Attention',
                           #message='Please log in after heard the voice "System has been started" from raspberry pi')
    window.iconbitmap("d:/ObjectRecognition/logo.ico")
    window.mainloop()






