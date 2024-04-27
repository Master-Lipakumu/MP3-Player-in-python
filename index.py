from pygame import mixer, USEREVENT
from tkinter import *
import tkinter.font as font
from tkinter import filedialog

# Initialisation de Pygame mixer
mixer.init()

# Fonction pour ajouter plusieurs chansons à la liste de lecture
def addsongs():
    temp_song = filedialog.askopenfilenames(initialdir="Music/",
                                            title="Choose a song",
                                            filetypes=(("mp3 Files", "*.mp3"),))
    for s in temp_song:
        s = s.replace("C:/Users/B2U/Music/", "")
        songs_list.insert(END, s)
        
# Fonction pour supprimer une chanson de la liste de lecture
def deletesong():
    curr_song = songs_list.curselection()
    songs_list.delete(curr_song[0])
    
# Fonction pour lire ou reprendre la chanson sélectionnée
def Play():
    global paused
    if paused:
        mixer.music.unpause()
        status_label.config(text="Now playing: " + songs_list.get(ACTIVE))
        paused = False
    else:
        song = songs_list.get(ACTIVE)
        song = f'C:/Users/B2U/Music/{song}'
        mixer.music.load(song)
        mixer.music.play()
        status_label.config(text="Now playing: " + songs_list.get(ACTIVE))
        mixer.music.set_endevent(USEREVENT)  # Définit un événement de fin de musique

# Fonction pour mettre en pause la chanson
def Pause():
    global paused
    mixer.music.pause()
    status_label.config(text="Paused: " + songs_list.get(ACTIVE))
    paused = True

# Fonction pour arrêter la chanson
def Stop():
    mixer.music.stop()
    status_label.config(text="Music stopped")
    songs_list.selection_clear(ACTIVE)

# Fonction pour passer à la chanson précédente
def Previous():
    previous_one = songs_list.curselection()
    if previous_one:
        previous_one = int(previous_one[0]) - 1
        if previous_one >= 0:
            temp2 = songs_list.get(previous_one)
            temp2 = f'C:/Users/B2U/Music/{temp2}'
            mixer.music.load(temp2)
            mixer.music.play()
            status_label.config(text="Now playing: " + songs_list.get(previous_one))
            songs_list.selection_clear(0, END)
            songs_list.activate(previous_one)
            songs_list.selection_set(previous_one)

# Fonction pour passer à la chanson suivante
def Next():
    next_one = songs_list.curselection()
    if next_one:
        next_one = int(next_one[0]) + 1
        if next_one < songs_list.size():
            temp = songs_list.get(next_one)
            temp = f'C:/Users/B2U/Music/{temp}'
            mixer.music.load(temp)
            mixer.music.play()
            status_label.config(text="Now playing: " + songs_list.get(next_one))
            songs_list.selection_clear(0, END)
            songs_list.activate(next_one)
            songs_list.selection_set(next_one)

# Fonction pour augmenter le volume
def IncreaseVolume():
    current_volume = mixer.music.get_volume()
    if current_volume < 1.0:
        new_volume = min(1.0, current_volume + 0.1)
        mixer.music.set_volume(new_volume)
        status_label.config(text=f"Volume increased to {int(new_volume * 100)}%")

# Fonction pour diminuer le volume
def DecreaseVolume():
    current_volume = mixer.music.get_volume()
    if current_volume > 0.0:
        new_volume = max(0.0, current_volume - 0.1)
        mixer.music.set_volume(new_volume)
        status_label.config(text=f"Volume decreased to {int(new_volume * 100)}%")

# Fonction appelée lorsque la musique se termine
def MusicEnd(event):
    pass

# Création de la fenêtre principale
root = Tk()
root.title('Mona Technology Music Player')

# Création de la liste des chansons
songs_list = Listbox(root, selectmode=SINGLE, bg="black", fg="white",
                    font=('arial', 15), height=12, width=47, 
                    selectbackground="gray", selectforeground="black")

songs_list.grid(columnspan=9)

# Définition de la police pour les boutons
defined_font = font.Font(family='Helvetica')

# Boutons de contrôle
play_button = Button(root, text="|>", width=3, command=Play)
play_button['font'] = defined_font
play_button.grid(row=1, column=0)

pause_button = Button(root, text="||", width=3, command=Pause)
pause_button['font'] = defined_font
pause_button.grid(row=1, column=1)

stop_button = Button(root, text="¤", width=3, command=Stop)
stop_button['font'] = defined_font
stop_button.grid(row=1, column=2)

previous_button = Button(root, text="<", width=3, command=Previous)
previous_button['font'] = defined_font
previous_button.grid(row=1, column=3)

next_button = Button(root, text=">", width=3, command=Next)
next_button['font'] = defined_font
next_button.grid(row=1, column=4)

increase_volume_button = Button(root, text="+", width=3, command=IncreaseVolume)
increase_volume_button['font'] = defined_font
increase_volume_button.grid(row=1, column=5)

decrease_volume_button = Button(root, text="-", width=3, command=DecreaseVolume)
decrease_volume_button['font'] = defined_font
decrease_volume_button.grid(row=1, column=6)

# Bouton pour ajouter ou supprimer des chansons
add_button = Button(root, text="+ Songs", width=10, command=addsongs)
add_button.grid(row=2, column=0, pady=10)

delete_button = Button(root, text="- Song", width=10, command=deletesong)
delete_button.grid(row=2, column=1, pady=10)

# Étiquette d'état
status_label = Label(root, text="", fg="green", font=('arial', 12))
status_label.grid(row=3, columnspan=7)

# Variable pour suivre l'état de lecture
paused = False

# Menu
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Menu", menu=add_song_menu)
add_song_menu.add_command(label="Add songs", command=addsongs)
add_song_menu.add_command(label="Delete song", command=deletesong)

# Définit un événement de fin de musique
mixer.music.set_endevent(USEREVENT)
root.bind(USEREVENT, MusicEnd)

# Boucle principale
mainloop()
