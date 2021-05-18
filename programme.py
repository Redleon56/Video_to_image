import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfil
import os
from PIL import Image, ImageTk

class enregistreur ():
    '''
    Argument :
        nb_images: type = int
        
    affiche une vidéo et permet de faire défiler image par image, et d'enregistrer l'image afficher.
    
    'nb_images' est le nombre d'image parmis lesquelles ont peut se déplacer. 
    
    l'image est enregistré avec pour nom le numéro de celle-ci au sien de la video.
    '''
    def __init__(self, nb_images = 40, taille_ecran_x = 800, taille_ecran_y = 790, decalage = 750, sauve = 'r', avance = 'Right', recule = 'Left', quitter = 'q'):
        
        self.taille_ecran = (taille_ecran_x,taille_ecran_y)
        self.decalage = decalage
        
        self.fenetre = tk.Tk()

        menubar = tk.Menu(self.fenetre)

        menufichier = tk.Menu(menubar,tearoff=0)
        menufichier.add_command(label='Ouvrir',command=self.ouvrir_video)
        menufichier.add_command(label='enregistrer',command=self.enregistrer)

        menubar.add_cascade(label='Dossier', menu= menufichier)

        self.fenetre.config(menu=menubar)
        
        self.video = ''
        self.fenetre.title(self.video)

        # les valeurs ajoutées (après 150) correspondent au décallage en x et en y 
        # avec pour convention que le coin en haut à gauche à pour coordonné 0,0 
        # et le coin en bas à droite à pour coordonné la taille de votre écran.
        self.fenetre.geometry(str(self.taille_ecran[0])+"x150+"+str(self.decalage)+"+0")
        self.fenetre.resizable(0,0)
        
        self.Valeur = tk.StringVar()
        self.Valeur.set(0)
        
        self.tab = []
        
        self.compteur = tk.StringVar()
        self.compteur.set(0)
        self.nb_images = nb_images

        self.cap = cv2.VideoCapture(self.video)
        
        self.sauve = sauve
        self.avance = avance
        self.recule = recule
        self.quitter = quitter

        self.lecture()
        
    # ==================================== 
    def ouvrir_video(self):
        emplacement = tkfil.askopenfilename(parent= self.fenetre)
        if emplacement != '':
            self.video = emplacement
            self.cap = cv2.VideoCapture(self.video)
            self.defile()
            self.fenetre.title(self.video.split('/')[-1])

    # ====================================
    def defile(self):
        self.tab = []
        if (self.cap.isOpened()== False): 
            tkmsg.showerror(title='Erreur', message='Pas de vidéo')
            self.ouvrir_video()
        
        else:
            for i in range(self.nb_images):
                ret, frame = self.cap.read()
                if ret == True:
                    self.tab.append(frame)
                else:
                    break
                    
    # ====================================
    def maj(self,nouvelleValeur):
        self.ouvrir(int(nouvelleValeur))
    
    # ====================================
    def enregistrer(self):
        dossier = tkfil.asksaveasfilename(parent= self.fenetre)
        if not(dossier.endswith('.png')):
            dossier += '.png'

        i = int(self.Valeur.get())
        
        b,g,r = cv2.split(self.tab[i])       
        img = cv2.merge([r,g,b])
        
        mpimg.imsave(dossier,img)
        
        #  vous pouvez détenter le message suivant qui affichera alors une fenêtre pour confirmer l'enregistrement de l'image.    
        #  tkmsg.showinfo('Résultat',"l'image a été enregistré")

        
    # ====================================    
    def moins(self):
        i = int(self.Valeur.get())
        self.Valeur.set(str(i-1))
        self.ouvrir(i)
    
    # ====================================
    def plus(self):
        n = len(self.tab)
        i = int(self.Valeur.get()) +  1
        
        if n == 0:
            tkmsg.showerror(title='Erreur', message='Pas de vidéo')
            
        if i < n:
            self.Valeur.set(str(i))
            self.ouvrir(i)
        else:
            self.compteur.set(str(int(self.compteur.get()) + n))
            self.Valeur.set(str(0))
            self.defile()
    
    # ====================================
    def sortir(self): 
        self.cap.release()
        cv2.destroyAllWindows()
        self.fenetre.destroy()
    
    # ====================================
    def Clavier(self,event):
        touche = event.keysym
        if touche == self.avance :
            self.plus()            
        if touche == self.recule:
            self.moins()
        if touche == self.sauve:
            self.enregistrer()
        if touche == self.quitter:
            self.sortir()
    
    # ====================================
    def ouvrir(self,i):
        im = cv2.resize(self.tab[i], (self.taille_ecran[0],self.taille_ecran[1]-150))
        cv2.imshow('image',im)
        cv2.resizeWindow('image', self.taille_ecran[0],(self.taille_ecran[1]-150))
        
        # ====================================
        
    def lecture(self):
        
        self.defile()
        cv2.namedWindow('image')
        cv2.resizeWindow('image',  self.taille_ecran[0],(self.taille_ecran[1]-150))
        cv2.moveWindow('image',self.decalage,180)
        
        # Création d'un widget Scale
        echelle = tk.Scale(self.fenetre,from_=0,to=self.nb_images,resolution=1,orient=tk.HORIZONTAL,length=self.taille_ecran[0]-20,width=20,tickinterval=10,variable=self.Valeur,command=self.maj)
        echelle.place(x = 5, y = 20)
        
        self.fenetre.bind('<Key>',self.Clavier)

        demi_x = self.taille_ecran[0]/2
        
        # Création d'un widget Button (bouton +)
        tk.Button(self.fenetre,text="->",command=self.plus).place(x = demi_x*(5/4) , y = 90, width = 25, height = 25)
        
        # Création d'un widget Button (bouton -)
        tk.Button(self.fenetre,text="<-",command=self.moins).place(x = (demi_x*3/4 - 25), y = 90, width = 25, height = 25)
        
        # Création d'un widget Button(bouton 'enregistrer' )
        tk.Button(self.fenetre, text='enregistrer',command = self.enregistrer).place(x = demi_x-45, y = 90, width = 80, height = 25)
        
        # Création d'un widget Button(bouton 'quitter')
        tk.Button(self.fenetre, text='quitter',command = self.sortir).place(x = demi_x - 25, y = 120, width = 50, height = 25)
        
        self.fenetre.mainloop()
        self.cap.release()
# =========================================================================================================

# Lancement
enregistreur()
