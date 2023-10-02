from tkinter import *
from time import sleep
import customtkinter as ctk
from PIL import ImageTk,Image
import cv2
import math
import os
import shutil
import extract_stego_image as ext
import run_stego_algorithm as run_stego
from subprocess import call, STDOUT
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox
#config windows title bar
#set variable for opening files
#File path declare
filepath_realtime = os.path.dirname(os.path.realpath(__file__))
img_note = ctk.CTkImage(Image.open(filepath_realtime+'/import.png'),size=(15, 15))
img_newnote = ctk.CTkImage(Image.open(filepath_realtime+'/file.png'),size=(15, 15))
img_video = ctk.CTkImage(Image.open(filepath_realtime+'/film.png'),size=(15, 15))
img_execute = ctk.CTkImage(Image.open(filepath_realtime+'/gear.png'),size=(15, 15))
img_getmess = ctk.CTkImage(Image.open(filepath_realtime+'/decrypt.png'),size=(15, 15))
img_playvideo = ctk.CTkImage(Image.open(filepath_realtime+'/play.png'),size=(30, 30))
img_readtxtfile = ctk.CTkImage(Image.open(filepath_realtime+'/reading-mode.png'),size=(27,27))
global open_status_name
open_status_name = False
#config windows title bar
#set variable for opening files
global file_name #duong dan file messages
file_name = ''
global filename_video #duong dan file video
filename_video = ''
global frame_playvideo



#defines root windows
root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')
#declare menu
my_menu = Menu(root)
root.config(menu=my_menu,background='white')
#declare windows display
root.geometry('700x700')
root.maxsize(width=900,height=900)
root.minsize(width=500,height=300)
root.title('Converting tools')
root.iconbitmap(filepath_realtime+'/convert.ico')
#icon on windows
#root.iconbitmap(r'/home/tieulong/Desktop/VideoBangDCT/convert.ico')


def loading():
    pass

def split_string(s_str, count=10):
    per_c = math.ceil(len(s_str) / count)
    c_cout = 0
    out_str = ''
    split_list = []
    for s in s_str:
        out_str += s
        c_cout += 1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str = ''
            c_cout = 0
    if c_cout != 0:
        split_list.append(out_str)
    return split_list


def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")
    temp_folder = "./tmp"
    txt_label = ctk.CTkLabel(frame_playvideo,text='Thư mục tmp đang được tạo...',font=('Arial',20))
    txt_label.pack(pady = 10)
    print("Thư mục tmp đang được tạo!!!")
    loading()
    vidcap = cv2.VideoCapture(video)
    count = 0
    # if os.path.exists("./tmp") and os.access("./tmp", os.R_OK):
    #     print("File exists and is readable")
    # else:
    #     print("File does not exist or is not readable")
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1


# casdasdhjasd

def encode_string(input_string):
    # os.system("python3 run_stego_algorithm.py ./tmp/0.png ./tmp/0.png "+input_string)
    #  run_stego.f_run_stego("./tmp/0.png","Nhom12 hello test")
    root = "./tmp/"
    split_string_list = split_string(input_string)

    for i in range(0, len(split_string_list)):
        f_name = "{}{}.png".format(root, i)
        run_stego.f_run_stego(f_name, split_string_list[i])
    # print("[INFO] frame {} holds {}".format(f_name,split_string_list[i]))


#   secret_enc=lsb.hide(f_name,split_string_list[i])
#  secret_enc.save(f_name)

def decode_string(video):
    if filename_video != '':
        input_dialog = ctk.CTkInputDialog(title='Notification', text='Type name of output messages')
        input_dialog.iconbitmap(filepath_realtime + '/gear.png')
        f_plaintext = str(input_dialog.get_input())
        frame_extraction(video)
        # os.system("python3 extract_stego_image.py ./tmp/0.png")

        # print(ext.extract_stego("./tmp/0.png"))
        secret = []
        root = "./tmp/"
        for i in range(0, 12):
            f_name_out = "{}{}.png".format(root, i)
            secret_dec = str(ext.extract_stego(f_name_out))
            if secret_dec == "None":
                break
            secret.append(secret_dec)
        string_secrect = ''.join([i for i in secret])
        messagebox.showinfo('Notification','Successfully decode your Video!!!')
        print("Secret Text là: ")
        print(string_secrect)
        txt_label = ctk.CTkLabel(frame_playvideo,text='Hidden content inside your input video: ',font=('Arial',20)).pack()
        txt_label1 = ctk.CTkLabel(frame_playvideo,text=string_secrect).pack(pady = 10)
        f = open(f_plaintext, "w")
        f.write(string_secrect)
        f.close()
        # clean_tmp()


def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        # print("[INFO] tmp files are cleaned up")



btn_giautin = ctk.CTkButton(root,image=img_execute,border_spacing=10,text='Execute',width=60,height=10,font=("Arial",12),fg_color='#ff9900',hover_color='#cc7a00',text_color='#0d0d0d',command=lambda :onClickExecute())
btn_giautin.pack(side=BOTTOM,anchor=NE,pady=15,padx=10)
btn_getmessages = ctk.CTkButton(root,image=img_getmess,border_spacing=10,text='Get Messages',width=60,height=10,font=("Arial",12),fg_color='#ff9900',hover_color='#cc7a00',text_color='#0d0d0d',command=lambda :onClick_getmess())
btn_getmessages.pack(side=BOTTOM,anchor=NE,pady=0,padx=10)

def onClick_getmess():
    if filename_video != '':
        lbl = Label(root, text=filename_video)
        lbl.pack(anchor=W, side=BOTTOM)
        decode_string(str(filename_video))
    else:
        messagebox.showerror('Error','No input video found')
#onClick execute

def onClickExecute():
    if file_name != '' and filename_video != '':
        #lbl = Label(root,text=file_name)
        #lbl.pack(anchor=W,side=BOTTOM)
        input_string = open(file_name, "r").read()
        f_name = str(filename_video)
        input_dialog = ctk.CTkInputDialog(title='Notification',text='Type name of output video')
        input_dialog.iconbitmap(filepath_realtime+'/gear.png')
        f_video_output = str(input_dialog.get_input())
        frame_extraction(filename_video)
        # -q:a kieem tra va thiet lap chat luong audio, -map thiet lap luong` chi tao ra file audio mp3
        call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"),stderr=STDOUT)

        encode_string(input_string)
         # Dua cac anh ve lai video chua co audio
        call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mov", "-y"], stdout=open(os.devnull, "w"),stderr=STDOUT)
        # Ket hop video va audio lai de ra video moi
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        os.system("mv video.mov " + f_video_output)
        # clean_tmp()
        label = Label(frame_playvideo,text='Successfully Executed!!!',font=('Arial',20))
        label.pack(pady=10)
    else:
        messagebox.showerror('Error!!!','You must import : Messages and Video file!!!')
#Create menu bars
def onClickMenu():
    pass
#file menu
file_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label='New...',command=onClickMenu)
file_menu.add_separator()
file_menu.add_command(label='Exit...',command=root.quit)
#edit menu
edit_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label='Change font',command=onClickMenu)
edit_menu.add_separator()
edit_menu.add_command(label='Change text size',command=onClickMenu)

help_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Help",menu=help_menu)
help_menu.add_command(label='Intruction',command=onClickMenu)
help_menu.add_separator()
help_menu.add_command(label='Contact',command=onClickMenu)
#option menu
#define onClick events
def onClick_openfiles():
    global file_name
    mess_frame.filemessage = filedialog.askopenfilename(initialdir=filepath_realtime,title='Open messages files...',filetypes=(('text files','*.txt'),('All files','*.*')))
    file_name = str(mess_frame.filemessage)
    box_txt = ctk.CTkTextbox(mess_frame, width=350, height=30)
    if file_name != '':
        box_txt.insert(END, file_name)
        box_txt.grid(padx=20, row=1, column=1)

def onClick_openfilesvideo():
    global filename_video
    video_frame.filevideo = filedialog.askopenfilename(initialdir=filepath_realtime,title='Open video files...',filetypes=(('MOV files','*.mov'),))
    filename_video = str(video_frame.filevideo)
    box_txt = ctk.CTkTextbox(video_frame,width=350,height=30)
    if filename_video != '':
        box_txt.insert(END,filename_video)
        box_txt.grid(padx=20,row = 1,column =1)

#define onClick create new file
def onClick_createnewfile():
    def clear():
        my_boxtext.delete(1.0,END)
    def opentxtfile():
        global text_file
        top.attributes('-topmost',False)
        text_file = filedialog.askopenfilename(initialdir=filepath_realtime,title='Open messages text file',filetypes=(('text files','*.txt'),('All files','*.*')))
        name = text_file
        print(filepath_realtime)
        print(name)
        #define global name
        if text_file:
            global open_status_name
            open_status_name = text_file
        text_file1 = open(text_file,'r')
        messages = text_file1.read()
        name = name.replace('/','\\')
        name = name.replace(filepath_realtime + '\\','')
        top.title(f'{name} - TextPad ')
        status_bar.config(text=f'{name}      ')
        #insert into text box
        my_boxtext.insert(END, messages)
        text_file1.close()
        top.attributes('-topmost',True)
    def savetxtfile():
        global open_status_name
        if open_status_name:
            text_file = open(open_status_name,'w')
            text_file.write(my_boxtext.get(1.0,END))
            messagebox.showinfo('Notifications','File was saved successfully')
            text_file.close()
            status_bar.config(text=f'{open_status_name}      ')
        else:
            saveastxtfile()
        top.destroy()
    def saveastxtfile():
        text_file = filedialog.asksaveasfilename(defaultextension='.*',initialdir=filepath_realtime,title='Save File',filetypes=(('text files','*.txt'),('All files','*.*')))
        if text_file:
            name = text_file
            name = name.replace(filepath_realtime,"")
            top.title(f'{name} - TextPad ')
            status_bar.config(text=f'{name}      ')
            #save it
            text_file = open(text_file,'w')
            text_file.write(my_boxtext.get(1.0,END))
            text_file.close()
    def newtxtfile():
        my_boxtext.delete(1.0,END)
        top.title('New File - Textpad')
        status_bar.config(text='New File      ')
    #define open new window
    top = ctk.CTkToplevel()
    top.geometry("500x300")
    top.title('TextPad')
    top.attributes('-topmost',True)
    #define frame of new window
    text_frame = ctk.CTkFrame(top)
    text_frame.pack(fill='both',expand=True)
    text_scroll = ctk.CTkScrollbar(text_frame)
    text_scroll.pack(side=RIGHT, fill=Y)
    my_boxtext = ctk.CTkTextbox(master=text_frame,padx=5,pady=5)
    my_boxtext.pack(fill='both',expand=True)
    text_scroll.configure(command=my_boxtext.yview)
    btn_frame = Frame(top)
    btn_frame.pack()
    #define a menu
    my_textboxmenu = Menu(top)
    top.config(menu=my_textboxmenu)
    #add file menu
    file_textboxmenu = Menu(my_textboxmenu,tearoff=False)
    my_textboxmenu.add_cascade(label='File',menu=file_textboxmenu)
    file_textboxmenu.add_command(label='Open',command=lambda : opentxtfile())
    file_textboxmenu.add_command(label='Save',command=lambda : savetxtfile())
    file_textboxmenu.add_command(label='Save As',command=lambda : saveastxtfile())
    file_textboxmenu.add_command(label='New',command=lambda : newtxtfile())
    file_textboxmenu.add_separator()
    file_textboxmenu.add_command(label='Exit',command=top.destroy)
    #add edit menu
    edit_textboxmenu = Menu(my_textboxmenu,tearoff=False)
    my_textboxmenu.add_cascade(label='Edit', menu=edit_textboxmenu)
    edit_textboxmenu.add_command(label='Cut')
    edit_textboxmenu.add_command(label='Copy')
    edit_textboxmenu.add_command(label='Undo')
    edit_textboxmenu.add_command(label='Redo')
    edit_textboxmenu.add_separator()
    edit_textboxmenu.add_command(label='Clear All',command=lambda :clear())
    #add status bar
    status_bar = Label(top,text='Ready      ',anchor=E)
    status_bar.pack(fill=X,side=BOTTOM,ipady=10)
#define messages frame
mess_frame = ctk.CTkFrame(master=root,corner_radius=10)
mess_frame.pack(padx=20,pady=20,anchor=W)
box_txt = ctk.CTkTextbox(mess_frame, width=350, height=30)
box_txt.grid(padx=20, row=1, column=1)
#define video frame
video_frame = ctk.CTkFrame(master=root,corner_radius=10)
video_frame.pack(padx=20,pady=20,anchor=W)
box_txt = ctk.CTkTextbox(video_frame,width=350,height=30)
box_txt.grid(padx=20,row = 1,column =1)
#define title of frame messages
title_mess = ctk.CTkLabel(mess_frame,text='Messages File')
title_mess.grid(row = 0)
title_mess = ctk.CTkLabel(mess_frame,text='Path File')
title_mess.grid(row = 0,column = 1)
#define button of messages frame
btn = ctk.CTkButton(mess_frame,image=img_newnote,border_spacing=10,text='Import files...',command=lambda : onClick_openfiles()).grid(pady=5,row=1,column=0)
btn2 = ctk.CTkButton(mess_frame,image=img_note,border_spacing=10,text='Create new...',command=lambda : onClick_createnewfile()).grid(padx=20,pady=10,row=2,column=0)
btn_readtxtfile = ctk.CTkButton(mess_frame,image=img_readtxtfile,hover_color='#8B0000',width=10,height=20,corner_radius=5,text='').grid(padx=20,row=1,column=2)

#-------------------------------

#define title of frame video
title_video = ctk.CTkLabel(video_frame,text='Video File')
title_video.grid(row = 0)
title_video = ctk.CTkLabel(video_frame,text='Path File')
title_video.grid(row = 0,column = 1)
#define button of video frame
btn_importvideo = ctk.CTkButton(video_frame,image=img_video,border_spacing=10,corner_radius=8,text='Import files...',command=lambda : onClick_openfilesvideo()).grid(pady=0,padx=20,row=1,column=0)
title_video1 = ctk.CTkLabel(video_frame,text='')
title_video1.grid(row =2)
btn_watchvideo = ctk.CTkButton(video_frame,image=img_playvideo,hover=True,hover_color='#8B0000',width=10,height=10,border_spacing=0,corner_radius=5,text='').grid(padx=20,row=1,column=2)
#-----------------------------------
#define frame of video segment
label_playvideo = ctk.CTkLabel(master=root,text='CONSOLE SCREEN',width=120,height=25,corner_radius=8)
label_playvideo.pack(pady=0,padx=20)
frame_playvideo = ctk.CTkFrame(master=root,corner_radius=10)
frame_playvideo.pack(pady=10,padx=20,fill='both',expand=True)
#
# Create loading animation
# Loading text...\
def loading():
    def play_animation():
        for i in range(200):
            for j in range(16):
                Label(frame_playvideo,bg='#FFBD09',width=2,height=1).place(x=(j+12) * 22,y=253)
                sleep(0.06)
                frame_playvideo.update_idletasks()
                #make block dark
                Label(frame_playvideo,bg='#1F2732',width=2,height=1).place(x=(j+12) * 22,y=253)
        frame_playvideo.destroy()
        exit(0)

    Label(master=frame_playvideo,text="Loading...",font='Bahnschrift 15',foreground='#FFBD09').place(x=150, y=250)
    for i in range(16):
        Label(frame_playvideo,width=2,height=1).place(x=(i+12)*22,y=253)#,bg='#1F2732'
        sleep(0.2)

# frame_playvideo.update()
# play_animation()
# video_player = ctk.CTkVideo(frame_playvideo, fill='both',expand=True)
# video_player.pack()
#
# # Set the video source
# video_player.set_source('path_to_video_file.mp4')

# Start the video player
# video_player.play()


root.mainloop()
