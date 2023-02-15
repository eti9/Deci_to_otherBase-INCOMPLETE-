
from PySide2 import QtWidgets
from numpy import double


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.base_dict = {"DECI" : 10, "HEXA" : 16, "BIN" : 2, "OCTAL" : 8}
        self.base_list = ["DECI","HEXA", "BIN", "OCTAL"]
        self.input_mask_list = [".","0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
        self.setWindowTitle("Mathematique appliqué en informatique")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
        self.setup_css()
        
    def setup_ui(self): 
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout2 = QtWidgets.QHBoxLayout(self)
        self.spn_number_to_convert = QtWidgets.QLineEdit()
        self.cbb_base_start = QtWidgets.QComboBox()
        self.text_to = QtWidgets.QLabel(" to ")
        self.cbb_base_target = QtWidgets.QComboBox()
        self.btn_convert =QtWidgets.QPushButton("Convertir, explication apparaitrons en dessous : ")
        self.text_box = QtWidgets.QLabel("")
        self.text_box.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.text_box.setLineWidth(1)
        
        self.layout2.addWidget(self.spn_number_to_convert)
        self.layout2.addWidget(self.cbb_base_start)
        self.layout2.addWidget(self.text_to)
        self.layout2.addWidget(self.cbb_base_target)   
        
        self.layout.addLayout(self.layout2)
        self.layout.addWidget(self.btn_convert)
        self.layout.addWidget(self.text_box)    

    def set_default_values(self):
        
        self.cbb_base_target.addItems(self.base_list)
        self.cbb_base_start.addItems(self.base_list)
        self.text_to.adjustSize()
        
    def setup_connections(self):
        self.cbb_base_start.activated.connect(self.compute_base)
        self.spn_number_to_convert.textChanged.connect(self.compute_base)
        self.btn_convert.clicked.connect(self.compute_calcul)
        
    
        
    def compute_base(self):
        base_chosen = self.cbb_base_start.currentText()
        
        if (base_chosen == "DECI"):
            set = 10
            self.spn_number_to_convert.setText(self.input_mask_correction(set, self.spn_number_to_convert.text()))
        if(base_chosen == "HEXA"):
            set = 16
            self.spn_number_to_convert.setText(self.input_mask_correction(set, self.spn_number_to_convert.text()))
        if(base_chosen == "BIN"):
            set = 2
            self.spn_number_to_convert.setText(self.input_mask_correction(set, self.spn_number_to_convert.text()))
        if(base_chosen == "OCTAL"):
            set = 8
            self.spn_number_to_convert.setText(self.input_mask_correction(set, self.spn_number_to_convert.text()))
            
   
        
    def compute_calcul(self):
        
        self.hexa_dict = {10 : "A", 11 : "B", 12 : "C", 13 : "D", 14 : "E", 15 : "F"}
        if (self.cbb_base_start.currentText() == "DECI"):
           self.deci_to_()
           
           
    def deci_to_(self):
        #Compteur pour ne pas overstack
            string_result = ""
            memoire = 0
            
            #Variable entier
            diviseur = self.base_dict.get(self.cbb_base_target.currentText())
            string_list = self.spn_number_to_convert.text().split(".")
            resultat_division = int(string_list[0])
            
            resultat_multiplication = 0.0
            #Variable decimale
            if (len(string_list) > 1):
                if(string_list[1] != ""):
                    resultat_multiplication = string_list[1]
            multiplicateur = diviseur
            
            #Premiere ligne du string
            string_result += " Le resultat est a lire de bas vers le haut pour les"
            string_result += "\n entiers puis de haut vers le bas pour les decimals!"
            string_result += "\n A droite pour les entiers et a gauche pour les decimals!"
            string_result += "\n Ceci est un aide au devoir pour vous verifier!"
            string_result += "\n _________________________________________________________"
            string_result += "\n Entier           Decimal"
            string_result += f"\n{resultat_division} | {diviseur}"
            
            i = len(string_result)
            while (i < 20):
                string_result += " "
                i = i+1
            string_result += f"       . {resultat_multiplication} x {multiplicateur}\n"

            #Deuxieme ligne du string
            for i in f"{resultat_division} | {diviseur}":
                string_result += "-"
            i = len(f"{resultat_division} | {diviseur}")
            while (i < 20):
                string_result += " "
                i = i+1
            for i in f"0 ,| {resultat_multiplication} x {multiplicateur}":
                string_result += "-"
            string_result += "\n"
            
            carac_min = len(f"{resultat_division}")
            #Deux opération en parralle
            while (resultat_division != 0 or (resultat_multiplication != 0 and memoire < 20)):
                
                curr_string = ""
                
                #Calcul Entier
                if(resultat_division != 0):
                    reste_division = resultat_division % diviseur
                
                    if (reste_division >9):
                        reste_division = self.hexa_dict.get(reste_division)
                
                    resultat_division = resultat_division // diviseur
                    i=len(f"{resultat_division}")
                    while (i < carac_min):
                        curr_string += "  "
                        i=i+1
                    curr_string +=f"{resultat_division} | {reste_division}"
                
                #Filling_space
                i = len(curr_string)
                while (i < 20):
                    curr_string += " "
                    i = i+1
                 
                #Calcul decimal avec un stack overflow limit de 20 si périodique
                if(resultat_multiplication != 0 and memoire < 20):
                    memoire = memoire +1
                    resultat_multiplication = float(f"0.{resultat_multiplication}")
                    resultat_multiplication = resultat_multiplication*multiplicateur
                    
                    res_list = f"{resultat_multiplication}".split(".")
                    res_entier = int(res_list[0])
                    resultat_multiplication = int(res_list[1])
                    
                    if (res_entier >9):
                        res_entier = self.hexa_dict.get(res_entier)
                    
                    curr_string += f" {res_entier} | {resultat_multiplication}"
                curr_string += "\n"
                string_result += curr_string
            self.text_box.setText(string_result)
    
    def input_mask_correction(self, input_mask_range, input_to_correct):
        onePoint= False
        input_corrected = ""
        for e in input_to_correct:
            i=0
            while (i <=input_mask_range):
                
                if (self.input_mask_list[i] == e.upper()):
                    if (i==0):
                        if(onePoint == False): 
                            onePoint=True
                            input_corrected += e
                        else: 
                            i = 20
                    else : 
                        input_corrected += e
                        i = 20
                i = i+1 
                     
        return input_corrected
    
    def setup_css(self):
        pass


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()