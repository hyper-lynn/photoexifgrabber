##############################################
##############################################
##                                          ##
##      *Developer  :   LynnMyatAung        ##
##      *name       : Photo's exif grabber  ##
##      *version    :   1                   ##
##                                          ##
##############################################
##############################################



from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import os,tkinter
from PIL import Image
from PIL.ExifTags import TAGS
from GPSPhoto import gpsphoto
from tkintermapview import TkinterMapView

font = ("Verdana", 10)
g = "green"
b = "black"
x = ""

#create window
root = Tk()

root.title("Photo Exif Grabber")
root["bg"]="black"
root.geometry("1200x600+100+30")
# root.resizable(width=False, height=False)

#function


#image path
def dispaly_path(file):
    file_ent.delete(0,"end")
    file_ent.insert(END,str(file))
    global x
    x = file


#browse
def open_file():
    global filepath
    
    file = fd.askopenfile(title="Select photo")
    if file:
        filepath = os.path.abspath(file.name)
        dispaly_path(filepath)
    filepath = filepath
     

#Grab
def grab_exif():
    global data
    image = Image.open(filepath)
    image.verify()
    data = image._getexif()
    if not data:
        messagebox.showerror("Error","No Metadata found")
    
    labeled = {}
    for (key, val) in data.items():
        labeled[TAGS.get(key)] = val

    rp = open("report/report.txt","a")
    for x in labeled:
       rp.write(f"{x} : {labeled[x]}\n")
    rp.close()
    with open("report/report.txt", "r") as f:
        d = f.read()
        text.insert(tkinter.END,d)


def showmap():
    global geo
    data = gpsphoto.getGPSData(filepath)
    lati = data["Latitude"]
    longi = data["Longitude"]
    show_geo.insert(END,f"{lati},{longi}")
    geo = map_widget.set_marker(lati,longi,text="Photo's Location")


def restart():
    geo.delete()
    rp = open("report/report.txt","w")
    rp.write("")
    rp.close()
    show_geo.delete(0,END)
    text.delete("1.0",END)

#set icon
icon = PhotoImage(file="ico.png")
root.iconphoto(False,icon)

#bar
scroll_bar = Scrollbar(root)

#label
name = Label(root,text="Photo's Exif Grabber",font=("Verdana", 16),fg=g,bg=b).pack()
slb = Label(root,text="Select File",font=font,fg=g,bg=b)
mlb = Label(root,text=" Meta Data ",font=font,fg=g,bg=b)
geolb = Label(root,text="Latitude",font=font,fg=g,bg=b)

#entry
file_ent = Entry(root,background="#fdfff5",width="100")
show_meta = Entry(root,background="#fdfff5",width="100")
show_geo = Entry(root,background="#fdfff5",width="50")

#button
btn = Button(root,text="Browse",fg=g,bg="gray",font=font,command=open_file)
btn2 = Button(root,text="Grab",fg=g,bg="gray",font=font,command=grab_exif)
btn3 = Button(root,text="find geolocation",fg=g,bg="gray",font=font,command=showmap)
btn4 = Button(root,text="restart",fg=g,bg="gray",font=font,command=restart)


#text
text = tkinter.Text(root, height=26, width=50)
scroll = tkinter.Scrollbar(root)
text.configure(yscrollcommand=scroll.set)

#tkintermapview
map_widget = TkinterMapView(root, width=700, height=420, corner_radius=0)
map_widget.set_position(16.8409, 96.1735)
map_widget.set_zoom(4)

location = map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
# location = map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

#palce the widgets
slb.place(x=30,y=50)
file_ent.place(x=130,y=50)
btn.place(x=750,y=47)
btn2.place(x=820,y=47)
btn3.place(x=871,y=47)
btn4.place(x=995,y=47)
mlb.place(x=40,y=86)
geolb.place(x=470,y=86)
show_geo.place(x=550,y=90)
text.place(x=30,y=119)
map_widget.place(x=470,y=119)

# img.place(x=200,y=400)

root.mainloop()