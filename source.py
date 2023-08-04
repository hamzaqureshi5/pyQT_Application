# Only needed for access to command line arguments
import os 
import re
import sys
import time
import json
import datetime
import pandas as pd

from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QRegularExpression,QRegularExpressionMatch
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6 import QtGui 
from PyQt6.QtWidgets import QApplication,QMainWindow,QComboBox,QFileDialog, QTableWidgetItem
from PyQt6.QtCore import Qt,QEvent
from forms.main_ui import Ui_MainWindow
from STCAppScriptV6 import default_headers,preview_files_gets,generate_4_Digit,generate_8_Digit,gen_k4,gen_ki,_DATA_EXTRACTOR
from previewInputWin import PreviewInput
from previewOutputWin import PreviewOutput
from file import read_df,read_vars
from global_parameters import PARAMETERS,DATA_FRAMES
from settings import SETTINGS
from main_functions import MainClass
debug=False

class MainWindow(QMainWindow):        

    project_path=os.getcwd()        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.parameters = PARAMETERS.get_instance()
        self.dataframes = DATA_FRAMES.get_instance()
        self.sett=SETTINGS()

        #==========================================#
        #============DEFAULT VALUES================#
        #==========================================#
        self.input_path=""
        self.default_transport_key="0C556CE733FA0E53FE2DCF14A5006D2E0C556CE733FA0E53FE2DCF14A5006D2E"#default values
        self.default_operator_key="0C556CE733FA0E53FE2DCF14A5006D2E"
        self.default_init_imsi=789000000000000
        self.default_init_iccid=899222333444555000
        self.default_PIN1="1234"
        self.default_data_size=25
        self.default_elect_check=True
        self.default_graph_check=True
        self.default_demo_check=True
        self.default_headers = ['ICCID','IMSI','PIN1','PUK1','PIN2','PUK2','KI','EKI','OPC','ADM1','ADM6','ACC']
        

        # self.parameters.set_K4(self.default_transport_key)
        # self.parameters.set_OP(self.default_operator_key)
#        self.parameters.set_IMSI(self.default_init_imsi)        
#        self.parameters.set_ICCID(self.default_init_iccid)
        # self.parameters.set_PIN1(self.default_PIN1)
#        self.parameters.set_DATA_SIZE(self.default_data_size)
        self.parameters.set_ELECT_CHECK(self.default_elect_check)
        self.parameters.set_GRAPH_CHECK(self.default_graph_check)
        self.parameters.set_DEMO_CHECK(self.default_demo_check)
        self.parameters.set_DEFAULT_HEADER(self.default_headers)

        

        #print('Size: %d x %d' % (size.width(), size.height()))
        #rect = screen.availableGeometry()
        #print('Available: %d x %d' % (rect.width(), rect.heigh
        tableWidgetHeader=['Variables', 'Clip', 'Lenght']
        self.ui.tableWidget.setHorizontalHeaderLabels(tableWidgetHeader)
        self.ui.e_tableWidget.setHorizontalHeaderLabels(tableWidgetHeader)
        self.ui.de_tableWidget.setHorizontalHeaderLabels(tableWidgetHeader)
        self.ui.de_comboBox.addItems(self.extractor_columns)
        

        self.ui.main_preview.clicked.connect(self.main_preview_function)
        self.ui.generate_button.clicked.connect(self.genrate_button_func)

        self.ui.demo_data.setChecked(self.default_demo_check)
        self.ui.elect_data.setChecked(self.default_elect_check)
        self.ui.graph_data.setChecked(self.default_graph_check)

        self.ui.add_text.clicked.connect(self.add_text_to_table)
        self.ui.del_text.clicked.connect(self.delete_selected_row)
        self.ui.up_button.clicked.connect(self.move_selected_row_up)
        self.ui.dn_button.clicked.connect(self.move_selected_row_down)
        self.ui.g_default.clicked.connect(self.g_setDefault)
        self.ui.g_save.clicked.connect(self.g_getDefault)


        self.ui.e_add_text.clicked.connect(self.e_add_text_to_table)
        self.ui.e_del_text.clicked.connect(self.e_delete_selected_row)
        self.ui.e_up_button.clicked.connect(self.e_move_selected_row_up)
        self.ui.e_dn_button.clicked.connect(self.e_move_selected_row_down)
        self.ui.e_default.clicked.connect(self.e_setDefault)
        self.ui.e_save.clicked.connect(self.e_getDefault)


        self.ui.browse_button.clicked.connect(self.browse_button_func)
        self.ui.preview_in_file.clicked.connect(self.show_input_files)


        self.ui.graph_data.stateChanged.connect(self.check_state_changed)
        self.ui.elect_data.stateChanged.connect(self.check_state_changed)
        self.check_state_changed()

        self.ui.demo_data.stateChanged.connect(self.check_state_demo_data)
        self.check_state_demo_data()
        
        self.ui.op_key_auto.clicked.connect(self.auto_op_func) 
        self.ui.k4_key_auto.clicked.connect(self.auto_k4_func)
        self.ui.data_size_auto.clicked.connect(self.auto_data_size_func) 
        self.ui.imsi_auto.clicked.connect(self.auto_imsi_func)
        self.ui.iccid_auto.clicked.connect(self.auto_iccid_func)


#        self.ui.transport_key_text.textChanged.connect(self.print)
#        self.ui.transport_key_text.textChanged.connect(lambda: self.len_check("K4",self.ui.transport_key_text.text()))
#        self.ui.op_key_text.textChanged.connect(lambda: self.len_check("OP",self.ui.op_key_text.text()))

        self.ui.k4_key_text.textChanged.connect(lambda: self.len_check("K4", self.ui.k4_key_text.text(), self.ui.k4_key_text))
        self.ui.op_key_text.textChanged.connect(lambda: self.len_check("OP", self.ui.op_key_text.text(), self.ui.op_key_text))
        self.ui.data_size_text.textChanged.connect(lambda: self.len_check("SIZE", self.ui.data_size_text.text(), self.ui.data_size_text))
        self.ui.imsi_text.textChanged.connect(lambda: self.len_check("IMSI", self.ui.imsi_text.text(), self.ui.imsi_text))
        self.ui.iccid_text.textChanged.connect(lambda: self.len_check("ICCID_MIN", self.ui.iccid_text.text(), self.ui.iccid_text))
        self.ui.pin1_text.textChanged.connect (lambda: self.len_check("PIN1",  self.ui.pin1_text.text(),  self.ui.pin1_text))
        self.ui.pin2_text.textChanged.connect (lambda: self.len_check("PIN2",  self.ui.pin2_text.text(),  self.ui.pin2_text))
        self.ui.puk1_text.textChanged.connect (lambda: self.len_check("PUK1",  self.ui.puk1_text.text(),  self.ui.puk1_text))
        self.ui.puk2_text.textChanged.connect (lambda: self.len_check("PUK2",  self.ui.puk2_text.text(),  self.ui.puk2_text))
        self.ui.adm1_text.textChanged.connect (lambda: self.len_check("ADM1",  self.ui.adm1_text.text(),  self.ui.adm1_text))
        self.ui.adm6_text.textChanged.connect (lambda: self.len_check("ADM6",  self.ui.adm6_text.text(),  self.ui.adm6_text))



        self.ui.pin1_rand_check.stateChanged.connect(self.pin1_rand_check)
        self.ui.pin2_rand_check.stateChanged.connect(self.pin2_rand_check)
        self.ui.puk1_rand_check.stateChanged.connect(self.puk1_rand_check)
        self.ui.puk2_rand_check.stateChanged.connect(self.puk2_rand_check)
        self.ui.adm1_rand_check.stateChanged.connect(self.adm1_rand_check)
        self.ui.adm6_rand_check.stateChanged.connect(self.adm6_rand_check)

        self.ui.pin1_auto.clicked.connect(self.auto_pin1_func)
        self.ui.pin2_auto.clicked.connect(self.auto_pin2_func)
        self.ui.puk1_auto.clicked.connect(self.auto_puk1_func)
        self.ui.puk2_auto.clicked.connect(self.auto_puk2_func)
        self.ui.adm1_auto.clicked.connect(self.auto_adm1_func)
        self.ui.adm6_auto.clicked.connect(self.auto_adm6_func)

        self.ui.save_seting_button.clicked.connect(self.save_settings_func)
        self.ui.load_seting_button.clicked.connect(self.load_settings_func)



        self.ui.de_browse_button.clicked.connect(self.browse_button_func)
        self.ui.de_preview_in_file.clicked.connect(self.de_show_input_files)

        self.ui.de_add_text.clicked.connect(self.de_add_text_to_table)
        self.ui.de_del_text.clicked.connect(self.de_delete_selected_row)
        self.ui.de_up_button.clicked.connect(self.de_move_selected_row_up)
        self.ui.de_dn_button.clicked.connect(self.de_move_selected_row_down)
        self.ui.de_default.clicked.connect(self.de_setDefault)

        self.ui.de_main_preview.clicked.connect(self.de_main_preview_function)
#        self.ui.generate_button.clicked.connect(self.genrate_button_func)

#    default_headers12 = m_file.default_headers
    default_headers12 = default_headers

    default_elect = ["ICCID","IMSI","PIN1","PUK1","PIN2","PUK2","ADM1","ADM6","KI","EKI","OPC","ACC"]
    default_graph = ["ICCID","ICCID","IMSI","IMSI","PIN1","PUK1","PIN2","PUK2"]
    
    # default_graph= {
    # '0': ['ICCID', 'Normal', "0-19"],
    # '1': ['IMSI', 'Normal', "0-14"],
    # '2': ['PIN1', 'Normal', "0-3"],
    # '3': ['PUK1', 'Normal', "0-7"],
    # '5': ['PIN2', 'Normal', "0-3"],
    # '6': ['PUK2', 'Normal', "0-7"],
    # '7': ['ADM1', 'Normal', "0-7"],
    # '8': ['ADM6', 'Normal', "0-7"],
    # '10': ['EKI', 'Normal', "0-31"],
    # '11': ['OPC', 'Normal', "0-31"],
    # '12': ['ACC', 'Normal', "0-3"]
    # }


    extractor_columns=[]


    def save_settings_func(self):
        self.UPDATE_ALL()
#        self.parameters.print_all_global_parameters()
        self.sett.save_settings()
        self.ui.textEdit.clear()
        self.ui.textEdit.append("Settings Saved!")
         
    def load_settings_func(self):
         self.sett.load_settings()
#         self.parameters.print_all_global_parameters()
         self.SET_ALL_FROM_SETT()
         self.ui.textEdit.clear()
         self.ui.textEdit.append("Settings Loaded!")

#         self.ui.demo_data.setChecked(self.parameters.get_DEMO_CHECK())
#         self.ui.elect_data.setChecked(self.parameters.get_ELECT_CHECK())
#         self.ui.graph_data.setChecked(self.parameters.get_GRAPH_CHECK())

    

    def update_pin1_text(self):
        var=self.ui.pin1_text.text()
        if len(var) == 4:
            self.parameters.set_PIN1(var)
        else:
            self.parameters.set_PIN1("")
            self.ui.textEdit.append("Enter valid PIN1")

    def update_pin2_text(self):
        var = self.ui.pin2_text.text()
        if len(var) == 4:
            self.parameters.set_PIN2(var)
        else:
            self.parameters.set_PIN2("")
            self.ui.textEdit.append("Enter valid PIN2")

    def update_puk1_text(self):
        var = self.ui.puk1_text.text()
        if len(var) == 8:
            self.parameters.set_PUK1(var)
        else:
            self.parameters.set_PUK1("")
            self.ui.textEdit.append("Enter valid PUK1")

    def update_puk2_text(self):
        var = self.ui.puk2_text.text()
        if len(var) == 8:
            self.parameters.set_PUK2(var)
        else:
            self.parameters.set_PUK2("")
            self.ui.textEdit.append("Enter valid PUK2")
                

    def update_adm1_text(self):
        var = self.ui.adm1_text.text()
        if len(var) == 8:
            self.parameters.set_ADM1(var)
        else:
            self.parameters.set_ADM1("")
            self.ui.textEdit.append("Enter valid ADM1")
                

    def update_adm6_text(self):
        var = self.ui.adm6_text.text()
        if len(var) == 8:
            self.parameters.set_ADM6(var)
        else:
            self.parameters.set_ADM6("")
            self.ui.textEdit.append("Enter valid ADM6")

    def auto_pin1_func(self):
        string=generate_4_Digit()
        self.ui.pin1_text.setText(string) 

    
    def pin1_rand_check(self):
        if self.ui.pin1_rand_check.isChecked():
            self.parameters.set_PIN1_RAND(True)
        else:
            self.parameters.set_PIN1_RAND(False)

                
    def auto_pin2_func(self):
        string=generate_4_Digit()
        self.ui.pin2_text.setText(string) 

    def pin2_rand_check(self):
        if self.ui.pin2_rand_check.isChecked():
            self.parameters.set_PIN2_RAND(True)
        else:
            self.parameters.set_PIN2_RAND(False)


    def auto_puk1_func(self):
        string=generate_8_Digit()
        self.ui.puk1_text.setText(string) 

    def puk1_rand_check(self):
        if self.ui.puk1_rand_check.isChecked():
            self.parameters.set_PUK1_RAND(True)
        else:
            self.parameters.set_PUK1_RAND(False)

    def auto_puk2_func(self):
        string=generate_8_Digit()
        self.ui.puk2_text.setText(string) 


    def puk2_rand_check(self):
        if self.ui.puk2_rand_check.isChecked():
            self.parameters.set_PUK2_RAND(True)
        else:
            self.parameters.set_PUK2_RAND(False)

    def auto_adm1_func(self):
        string=generate_8_Digit()
        self.ui.adm1_text.setText(string) 

    def adm1_rand_check(self):
        if self.ui.adm1_rand_check.isChecked():
            self.parameters.set_ADM1_RAND(True)
        else:
            self.parameters.set_ADM1_RAND(False)

    def auto_adm6_func(self):
        string=generate_8_Digit()
        self.ui.adm6_text.setText(string) 
    
    def adm6_rand_check(self):
        if self.ui.adm6_rand_check.isChecked():
            self.parameters.set_ADM6_RAND(True)
        else:
            self.parameters.set_ADM6_RAND(False)

    def SET_ALL_FROM_SETT(self):
        self.ui.imsi_text.setText(self.parameters.get_IMSI())
        self.ui.iccid_text.setText(self.parameters.get_ICCID())
        self.ui.pin1_text.setText(self.parameters.get_PIN1())
        self.ui.puk1_text.setText(self.parameters.get_PUK1())
        self.ui.pin2_text.setText(self.parameters.get_PIN2())
        self.ui.puk2_text.setText(self.parameters.get_PUK2())
        self.ui.adm1_text.setText(self.parameters.get_ADM1())
        self.ui.adm6_text.setText(self.parameters.get_ADM6())
        self.ui.k4_key_text.setText(self.parameters.get_K4())
        self.ui.op_key_text.setText(self.parameters.get_OP())
        self.ui.data_size_text.setText(self.parameters.get_DATA_SIZE())        
        self.ui.pin1_rand_check.setChecked(bool(self.parameters.get_PIN1_RAND()))
        self.ui.pin2_rand_check.setChecked(bool(self.parameters.get_PIN2_RAND()))
        self.ui.puk1_rand_check.setChecked(bool(self.parameters.get_PUK1_RAND()))
        self.ui.puk2_rand_check.setChecked(bool(self.parameters.get_PUK2_RAND()))
        self.ui.adm1_rand_check.setChecked(bool(self.parameters.get_ADM1_RAND()))
        self.ui.adm6_rand_check.setChecked(bool(self.parameters.get_ADM6_RAND()))

            
    def UPDATE_ALL(self):
        if self.ui.demo_data.isChecked():
            self.get_iccid_func()
            self.get_imsi_func()
            self.get_data_size_func()          
        
        self.pin1_rand_check()
        self.pin2_rand_check()
        self.puk1_rand_check()
        self.puk2_rand_check()
        self.adm1_rand_check()
        self.adm6_rand_check()

        self.update_pin1_text()
        self.update_pin2_text()
        self.update_puk1_text()
        self.update_puk2_text()
        self.update_adm1_text()
        self.update_adm6_text()
    
        self.get_k4_func()
        self.get_op_func()
        
            

    def g_setDefault(self):
        for items in self.default_graph:
            self.g_table_append(items)
        
    def g_getDefault(self):
        self.default_graph=self.get_data_from_table()
        print(str(self.default_graph))


    def main_preview_function(self):
        self.ui.textEdit.clear()
        debug=True
        self.UPDATE_ALL()

        self.ui.textEdit.append("==================================")
        if debug:        
            self.ui.textEdit.append("=============DEBUG================") 
            temp=self.parameters.GET_ALL_PARAMS_DICT()
            self.ui.textEdit.append(str(temp))

        self.ui.textEdit.append("==================================") 

        laser=self.get_data_from_table()
        elect=self.e_get_data_from_table()
        self.parameters.set_GRAPH_DICT(self.get_data_from_table())
        self.parameters.set_ELECT_DICT(self.e_get_data_from_table())
        
#        self.parameters.dict1 is test dictionary
        if self.parameters.check_params():
            self.dataframes.ELECT_DF,self.dataframes.GRAPH_DF,self.dataframes.KEYS= preview_files_gets()
            self.w=PreviewOutput(self.dataframes.ELECT_DF,self.dataframes.GRAPH_DF,True,True)
            self.w.show()

    def de_main_preview_function(self):
        self.ui.de_textEdit.clear()
        debug=True
#        self.UPDATE_ALL()

        self.ui.de_textEdit.append("==================================")
        if debug:        
            self.ui.de_textEdit.append("=============DEBUG================") 
#            temp=self.parameters.GET_ALL_PARAMS_DICT()
#            self.ui.textEdit.append(str(temp))

        self.ui.de_textEdit.append("==================================") 

#        laser=self.get_data_from_table()
#        elect=self.e_get_data_from_table()
        elect=self.de_get_data_from_table()
        self.ui.de_textEdit.append(str(elect)) 

        self.parameters.set_EXTRCATOR_DICT(self.de_get_data_from_table())

        # if self.parameters.check_params():
        self.dataframes.ELECT_DF=_DATA_EXTRACTOR(elect,self.dataframes.INPUT_DF,True,True,"")
        self.w=PreviewInput(self.dataframes.ELECT_DF)
        self.w.show()

    def create_output_folder(self, elect_file, graph_file, keys_file, folder_name: str, csv: bool):

        self.ui.textEdit.clear()

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        self.ui.textEdit.append("==================================")
        self.ui.textEdit.append(f"Created folder '{folder_name}'")

        p_time = time.strftime("%H_%M_%S", time.localtime())
        p_date = datetime.date.today().strftime("%Y_%m_%d")
        date_time = f"{p_date}_{p_time}"

        file_format = "CSV" if csv else "txt"

        elect_file.to_csv(os.path.join(folder_name, f"electrical_data_{date_time}.{file_format}"), index=False)
        graph_file.to_csv(os.path.join(folder_name, f"graphical_data_{date_time}.{file_format}"), index=False)

        with open(os.path.join(folder_name, f"keys_used_{date_time}.txt"), 'w') as convert_file:
            json.dump(keys_file, convert_file)
        self.ui.textEdit.append("==================================")

        self.ui.textEdit.append(f"DataFrames saved as {file_format} files.")
        self.ui.textEdit.append("==================================")

        self.ui.textEdit.append("Path: " + os.path.join(os.getcwd(), folder_name))
        self.ui.textEdit.append("==================================")
        


    # def create_output_folder(self,elect_file,graph_file,keys_file,folder_name:str,csv:bool):
        
    #     self.ui.textEdit.clear()
        
    #     if not os.path.exists(folder_name):
    #         os.makedirs(folder_name)
    #     self.ui.textEdit.append("==================================") 
    #     self.ui.textEdit.append(f"Created folder '{folder_name}'")

    #     p_time=time.asctime().replace(" ","_").replace(":","_")
    #     p_date=(str(datetime.date.today()))
    #     p_time=(str("_"+str(time.localtime().tm_hour))+"_"+str(time.localtime().tm_min)+"_"+str(time.localtime().tm_sec))
    #     date_time=(p_date+p_time).replace(" ","_").replace(":","_").replace("-","_")
    #     if csv:
    #         elect_file.to_csv(os.path.join(folder_name, "electrical_data_{}.txt".format(date_time)), index=False)
    #         graph_file.to_csv(os.path.join(folder_name, "graphical_data_{}.txt".format(date_time)), index=False)
    #         format="CSV"

    #     else:
    #         elect_file.to_csv(os.path.join(folder_name,"electrical_data_{}.txt".format(date_time)),index= False)
    #         graph_file.to_csv(os.path.join(folder_name,"graphical_data_{}.txt".format(date_time)),index= False)
    #         format="txt"

    #     with open(os.path.join(folder_name,"keys_used_{}.txt".format(date_time)), 'w') as convert_file:
    #         convert_file.write(json.dumps(keys_file))
    #     self.ui.textEdit.append("==================================") 

    #     self.ui.textEdit.append("DataFrames saved as {} files.".format(format))
    #     self.ui.textEdit.append("==================================") 

    #     self.ui.textEdit.append("Path: "+os.path.join(os.getcwd(),folder_name))
    #     self.ui.textEdit.append("==================================") 

    # #        print("DataFrames saved as {} files.".format(format))
    # #        print("Path",os.path.join(os.getcwd(),folder_name))

        # Call the function to create the folder, files, and save DataFrames
#        print("DEBUG")


    def print(self):
        screen = app.primaryScreen()
#        print('Screen: %s' % screen.name())
        size = screen.size()
#        print('Size: %d x %d' % (size.width(), size.height()))
        rect = screen.availableGeometry()
#        print('Available: %d x %d' % (rect.width(), rect.height()))
        #count=0
        # debug only 
#        self.ui.textEdit.setText("Screen name : "+str(screen.name()))
#        self.ui.textEdit.append("Size is " +str(size.width())+"," +str(size.height()))
#        self.ui.textEdit.append("Available : "+ str(rect.width())+"," +str(rect.height()))
        
        
        
    def len_check(self, text, key_type, widget):
        style_sheet_good="background-color:white; height:25px; border:1px solid green; border-radius:5px;"
        style_sheet_bad="background-color:white; height:25px; border:1px solid red; border-radius:5px;"
        var =int(self.parameter_len(text))
        if  (var+1) > len(key_type):
            widget.setStyleSheet(style_sheet_bad)
        else:
            widget.setStyleSheet(style_sheet_good)
        
        
    def auto_op_func(self):
        self.ui.op_key_text.setText(str(gen_ki()))
#        self.ui.op_key_text.setText(str(self.parameters.get_OP()))
        
    def auto_k4_func(self):
        self.ui.k4_key_text.setText(str(gen_k4()))        
#        self.ui.transport_key_text.setText(str(self.parameters.get_K4()))

    def auto_data_size_func(self):
        self.ui.data_size_text.setText(str(self.default_data_size))
#        self.ui.data_size_text.setText(str(self.parameters.get_DATA_SIZE()))
        
        
    def auto_imsi_func(self):
        init_imsi=self.default_init_imsi
#        self.parameters.set_IMSI(init_imsi)
        if self.is_valid_imsi(init_imsi):
            self.ui.imsi_text.setText(str(init_imsi))
            
    def auto_iccid_func(self):
        init_iccid=self.default_init_iccid
#        self.parameters.set_ICCID(init_iccid)
        if self.is_valid_iccid(init_iccid):
            self.ui.iccid_text.setText(str(init_iccid))


    def is_valid_iccid(self, iccid):
        iccid_length = len(str(iccid))
        return iccid_length in [18, 19, 20]


    def is_valid_imsi(self, imsi):
        return len(str(imsi)) == 15

    def get_op_func(self):
        op_key=self.ui.op_key_text.text()
        if len(op_key) == 32:
            self.parameters.set_OP(op_key)
        else:
            self.ui.textEdit.append("Enter valid OP"+" len is "+ str(len(op_key)))

    def get_def_head(self):
        self.parameters.get_DEFAULT_HEADER()


    def get_k4_func(self):
        transport_key = self.ui.k4_key_text.text()
        if len(transport_key) == 64:
            self.parameters.set_K4(transport_key)
        else:
            self.ui.textEdit.append("Enter valid K4")
    
    def get_data_size_func(self):
        size = self.ui.data_size_text.text()
        if size.isdigit() and int(size) > 0:
            try:
                self.parameters.set_DATA_SIZE(size)
            except ValueError:
                self.ui.textEdit.append("Data Size must be a numeric value")
        else:
            self.parameters.set_DATA_SIZE("")            
            self.ui.textEdit.append("Enter a valid Data Size")
                

    def get_imsi_func(self):
        imsi=self.ui.imsi_text.text()
        if len(imsi) == 15 and imsi.isalnum():
            try:
                imsi=int(imsi)
                self.parameters.set_IMSI(imsi)
            except ValueError:
                self.ui.textEdit.append("IMSI must be a numeric value")
        else:
            self.parameters.set_IMSI("")
            self.ui.textEdit.append("Enter valid IMSI of Size 15 Digits")


    def get_iccid_func(self):
        iccid = self.ui.iccid_text.text()
        if len(iccid) in [18, 19, 20] and iccid.isalnum():
            try:
                iccid = int(iccid)
                self.parameters.set_ICCID(iccid)
            except ValueError:
                self.ui.textEdit.append("ICCID must be a numeric value")
        else:
            self.parameters.set_ICCID("")
            self.ui.textEdit.append("Enter a valid ICCID : Without Checksum Digit")

    def check_state_demo_data(self):
        if self.ui.demo_data.isChecked():
            self.global_demo_check=True
            self.parameters.set_DEMO_CHECK(True)
            self.ui.browse_button.setDisabled(True)
            self.ui.imsi_text.setDisabled(False)
            self.ui.iccid_text.setDisabled(False)
            self.ui.preview_in_file.setDisabled(True)
            self.ui.data_size_text.setDisabled(False)
            self.ui.imsi_auto.setDisabled(False)
            self.ui.iccid_auto.setDisabled(False)
            self.ui.data_size_auto.setDisabled(False)
        else:
            self.global_demo_check=False
            self.parameters.set_DEMO_CHECK(False)
            self.ui.browse_button.setDisabled(False)
            self.ui.imsi_text.setDisabled(True)
            self.ui.iccid_text.setDisabled(True)
            self.ui.preview_in_file.setDisabled(False)
            self.ui.data_size_text.setDisabled(True)
            self.ui.imsi_auto.setDisabled(True)
            self.ui.iccid_auto.setDisabled(True)
            self.ui.data_size_auto.setDisabled(True)


    def check_state_changed(self):
        if self.ui.graph_data.isChecked():
            self.global_graph_check=True
            self.parameters.set_GRAPH_CHECK(True)
            self.ui.comboBox.setDisabled(False)
            self.ui.tableWidget.setDisabled(False)
            self.ui.up_button.setDisabled(False)
            self.ui.dn_button.setDisabled(False)
            self.ui.add_text.setDisabled(False)
            self.ui.del_text.setDisabled(False)

            # Do this [enable respective]
        else:
            self.global_graph_check=False
            self.parameters.set_GRAPH_CHECK(False)
            self.ui.comboBox.setDisabled(True)
            self.ui.tableWidget.setDisabled(True)
            self.ui.up_button.setDisabled(True)
            self.ui.dn_button.setDisabled(True)
            self.ui.add_text.setDisabled(True)
            self.ui.del_text.setDisabled(True)

        if self.ui.elect_data.isChecked():
            self.global_elect_check=True
            self.parameters.set_ELECT_CHECK(True)            
            self.ui.e_comboBox.setDisabled(False)
            self.ui.e_tableWidget.setDisabled(False)
            self.ui.e_up_button.setDisabled(False)
            self.ui.e_dn_button.setDisabled(False)
            self.ui.e_add_text.setDisabled(False)
            self.ui.e_del_text.setDisabled(False)
            # Do this [enable respective]
        else:
            self.global_elect_check=False
            self.parameters.set_ELECT_CHECK(False)
            self.ui.e_comboBox.setDisabled(True)
            self.ui.e_tableWidget.setDisabled(True)
            self.ui.e_up_button.setDisabled(True)
            self.ui.e_dn_button.setDisabled(True)
            self.ui.e_add_text.setDisabled(True)
            self.ui.e_del_text.setDisabled(True)


    def browse_button_func(self):
        path=self.project_path
        path=os.path.join(path,"Input Files")
        fname, _ = QFileDialog.getOpenFileNames(self, "Single File", path, filter="CSV Files (*.csv)")
        self.ui.textEdit.append(str(fname))
        if len(fname) != 0:
            self.ui.filename.setText(", ".join(fname))
#            self.ui.textEdit.append(str(fname))
            self.ui.textEdit.append(f"Selected {len(fname)} file(s).")
#            self.global_input_path=fname[0]
            self.parameters.set_INPUT_PATH(fname[0])
            

    def show_input_files(self):
        
        path=self.parameters.get_INPUT_PATH()
        df_input = pd.DataFrame()
        match path:
            case ""|" ":
                self.ui.textEdit.append("No file selected")
            case _:
                self.dataframes.INPUT_DF=pd.read_csv(path,dtype=str)

                if self.dataframes.INPUT_DF.empty==False:
                    self.w = PreviewInput(self.dataframes.INPUT_DF)
                    self.w.show()
          
    def de_show_input_files(self):
        
        path=self.parameters.get_INPUT_PATH()
        df_input = pd.DataFrame()
        match path:
            case ""|" ":
                self.ui.textEdit.append("No file selected")
            case _:
                self.dataframes.INPUT_DF=pd.read_csv(path,dtype=str)
                self.ui.de_textEdit.append(str(tuple(self.dataframes.INPUT_DF.columns)))
                self.extractor_columns=self.dataframes.INPUT_DF.columns
                self.ui.de_comboBox.addItems(self.extractor_columns)


                if self.dataframes.INPUT_DF.empty==False:
                    self.w = PreviewInput(self.dataframes.INPUT_DF)
                    self.w.show()
#     def show_input_files(self):
#         path=self.parameters.get_INPUT_PATH()
#         df_input = pd.DataFrame()
#         match path:
#             case ""|" ":
#                 self.ui.textEdit.append("No file selected")
#             case _:
# #                self.dataframes.INPUT_DF=pd.read_csv(path)
#                 with open(path, 'r', encoding='utf-8') as file:
#                     fp = file.read()
#                 self.parameters.set_INPUT_FILE_PARAMETERS(read_vars(fp))
#                 self.dataframes.INPUT_DF=read_df(fp)
#                 if self.dataframes.INPUT_DF.empty==False:
#                     self.w = PreviewInput(self.dataframes.INPUT_DF)
#                     self.w.show()


    def extractor_funciton(self,dest,src):
        
        
        pass
    


    def parameter_len(self,param):
        lenght=0 
        match param:
            case "ICCID_MIN":
                lenght=18
            case "ICCID":
                lenght=20
            case "IMSI":
                lenght=15
            case "PIN1"|"PIN2"|"ACC":
                lenght=4
            case "PUK1"|"PUK2"|"ADM1"|"ADM6":
                lenght=8
            case "KI"|"EKI"|"OPC":
                lenght=32
            case "K4":
                lenght=64
            case "SIZE":
                lenght=1
            case _:
                lenght=32
        return str(lenght-1)
#        return "0-"+str(lenght-1)

# ===================================================================================#
# ===================================================================================#
# =========================GRAPHICAL DATA FUNCTIONS==================================#
# ===================================================================================#
# ===================================================================================#

    def g_table_append(self,text:str):
        drop_down_menu = ['Normal', 'Right','Center', 'Left']

        if text !="   -SELECT-":
            # Create a new row in the table
            row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(row_count + 1)

            self.combo_box = QComboBox()            
            self.combo_box.addItems(drop_down_menu)

            # Set the combo box as the widget for the desired cell
            self.ui.tableWidget.setCellWidget(row_count, 1, self.combo_box)
            # Add the text to the table
            item = QTableWidgetItem(text)
            self.ui.tableWidget.setItem(row_count, 0, item)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item1 = QTableWidgetItem("0-"+self.parameter_len(text.lstrip()))
#            item1 = QTableWidgetItem(self.parameter_len(text.lstrip()))
            self.ui.tableWidget.setItem(row_count, 2, item1)
            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget_debug(self.ui.tableWidget)



    def g_clear_table(self):
        rows=self.ui.tableWidget.rowCount()
        for row in range(rows):
            self.ui.tableWidget.removeRow(row)
    

    def add_text_to_table(self):
#        drop_down_menu = ['Normal', 'Right','Center', 'Left']
        self.ui.tableWidget.setHorizontalHeaderLabels(['Variables', 'Clip', 'Lenght'])
        
        text = self.ui.comboBox.currentText()
        self.g_table_append(text)
                        
        
    def delete_selected_row(self):
        row_count = self.ui.tableWidget.rowCount()
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.tableWidget.removeRow(selected_row)

    def move_selected_row_up(self):
        selected_row = self.ui.tableWidget.currentRow()
        if 0 < selected_row <= self.ui.tableWidget.rowCount():
            self.ui.tableWidget.insertRow(selected_row - 1)
            self.copy_row(selected_row + 1, selected_row - 1)
            self.ui.tableWidget.removeRow(selected_row + 1)
            self.ui.tableWidget.selectRow(selected_row - 1)


    def move_selected_row_down(self):
        selected_row = self.ui.tableWidget.currentRow()
        if  0 <= selected_row < self.ui.tableWidget.rowCount()-1:
            self.ui.tableWidget.insertRow(selected_row + 2)
            self.copy_row(selected_row, selected_row + 2)
            self.ui.tableWidget.removeRow(selected_row)
            self.ui.tableWidget.selectRow(selected_row + 1)



    def copy_row(self, source_row, target_row):
        for column in range(self.ui.tableWidget.columnCount()):
            source_item = self.ui.tableWidget.item(source_row, column)
            if source_item is not None:
                target_item = QTableWidgetItem(source_item.text())
                self.ui.tableWidget.setItem(target_row, column, target_item)
                target_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


        self.source_widget = self.ui.tableWidget.cellWidget(source_row, 1)
        if isinstance(self.source_widget, QComboBox):
            drop_down_menu = ['Normal', 'Right','Center', 'Left']
            self.target_widget = QComboBox()
            self.target_widget.addItems(drop_down_menu)
            source_text = self.source_widget.currentText()
            self.target_widget.setCurrentText(source_text)
#            self.target_widget.addItems([self.source_widget.currentText()])
            self.ui.tableWidget.setCellWidget(target_row, 1, self.target_widget)
            

    def get_data_from_table(self):
        max_rows = self.ui.tableWidget.rowCount()
        var = []
        dict_ret = {}
        for i in range(0, max_rows):
            var = self.ui.tableWidget.item(i, 0).text()
            widget = self.ui.tableWidget.cellWidget(i, 1)
            clip = ""
            if isinstance(widget, QComboBox):
                clip = widget.currentText()

            cell_value = 0
            cell_text = ""
            table_item = self.ui.tableWidget.item(i, 2)
            if table_item is not None:
                cell_text = table_item.text()
                cell_value = str((cell_text))
            dict_ret[str(i)] = [str(var.lstrip()), str(clip), cell_value]
        return dict_ret

    def table_widget_debug(self,widget):
        pass
#        self.ui.textEdit.append("TOTAL ROWS : "+ str(widget.rowCount()))
#        self.ui.textEdit.append("SELECTED ROW : "+str(widget.currentRow()))

# ===================================================================================#
# ===================================================================================#
# ========================ELECTRICAL DATA FUNCTIONS==================================#
# ===================================================================================#
# ===================================================================================#

    def e_setDefault(self):
        for items in self.default_elect:
            self.e_table_append(items)

    def e_getDefault(self):
        self.default_elect=self.e_get_data_from_table()

    def e_table_append(self,text:str):
        drop_down_menu = ['Normal', 'Right','Center', 'Left']
        if text !="   -SELECT-":
            row_count = self.ui.e_tableWidget.rowCount()
            self.ui.e_tableWidget.setRowCount(row_count + 1)

            col1 = QTableWidgetItem(text)
            self.ui.e_tableWidget.setItem(row_count, 0, col1)
            col1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setFlags(col1.flags() & Qt.ItemFlag.ItemIsEditable)

            self.e_combo_box = QComboBox()
            self.e_combo_box.addItems(drop_down_menu)
            self.ui.e_tableWidget.setCellWidget(row_count, 1, self.e_combo_box)
            
            col3 = QTableWidgetItem("0-"+self.parameter_len(text.lstrip()))
            self.ui.e_tableWidget.setItem(row_count, 2, col3)
            col3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            

    def e_add_text_to_table(self):

        self.ui.e_tableWidget.setHorizontalHeaderLabels(['Variables', 'Clip', 'Lenght'])
        text = self.ui.e_comboBox.currentText()
        self.e_table_append(text)



    def e_delete_selected_row(self):
        selected_row = self.ui.e_tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.e_tableWidget.removeRow(selected_row)

    def e_move_selected_row_up(self):
        selected_row = self.ui.e_tableWidget.currentRow()
        if 0 < selected_row <= self.ui.e_tableWidget.rowCount():
            self.ui.e_tableWidget.insertRow(selected_row - 1)
            self.e_copy_row(selected_row + 1, selected_row - 1)
            self.ui.e_tableWidget.removeRow(selected_row + 1)
            self.ui.e_tableWidget.selectRow(selected_row - 1)


    def e_move_selected_row_down(self):
        selected_row = self.ui.e_tableWidget.currentRow()
        table_widget = self.ui.e_tableWidget
        if 0 <= selected_row < table_widget.rowCount() - 1:
            table_widget.insertRow(selected_row + 2)
            self.e_copy_row(selected_row, selected_row + 2)
            table_widget.removeRow(selected_row)
            table_widget.selectRow(selected_row + 1)


    def e_copy_row(self, source_row, target_row):
        for column in range(self.ui.e_tableWidget.columnCount()):
            source_item = self.ui.e_tableWidget.item(source_row, column)
            if source_item is not None:
                target_item = QTableWidgetItem(source_item.text())
                self.ui.e_tableWidget.setItem(target_row, column, target_item)
                target_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


        self.source_widget = self.ui.e_tableWidget.cellWidget(source_row, 1)
        if isinstance(self.source_widget, QComboBox):
            self.target_widget = QComboBox()
            drop_down_menu = ['Normal', 'Right','Center', 'Left']
            self.target_widget.addItems(drop_down_menu)
            source_text = self.source_widget.currentText()
            self.target_widget.setCurrentText(source_text)
            self.ui.e_tableWidget.setCellWidget(target_row, 1, self.target_widget)

    def e_get_data_from_table(self):
        max_rows = self.ui.e_tableWidget.rowCount()
        var = []
        dict_ret = {}
        for i in range(0, max_rows):
            var = self.ui.e_tableWidget.item(i, 0).text()
            widget = self.ui.e_tableWidget.cellWidget(i, 1)
            clip = ""
            if isinstance(widget, QComboBox):
                clip = widget.currentText()

            cell_value = 0
            cell_text = ""
            table_item = self.ui.e_tableWidget.item(i, 2)
            if table_item is not None:
                cell_text = table_item.text()
                cell_value = str((cell_text))
            dict_ret[str(i)] = [str(var.lstrip()), str(clip), cell_value]
        return dict_ret

    def genrate_button_func(self):        
        self.create_output_folder(self.dataframes.ELECT_DF,self.dataframes.GRAPH_DF,self.dataframes.KEYS,"OutPut",False)        
        self.progress_bar()

    
    def progress_bar(self):
        float_value = 0
        integer_value = 0
        while integer_value < 100:
            time.sleep(0.0001)
            float_value += 1
            integer_value = int(float_value)  # Map the float value to the 0-100 integer range
            self.ui.progressBar.setValue(integer_value)
#        self.ui.progressBar.setValue(0)            
#        self.ui.progressBar.setHidden(True)

# ===================================================================================#
# ===================================================================================#
# ========================EXTRACTOR DATA FUNCTIONS==================================#
# ===================================================================================#
# ===================================================================================#
    def de_setDefault(self):
#        for items in self.default_elect:
        for items in self.extractor_columns:
            self.de_table_append(items)

    def de_table_append(self,text:str):
        drop_down_menu = ['Normal', 'Right','Center', 'Left']
        if text !="   -SELECT-":
            row_count = self.ui.de_tableWidget.rowCount()
            self.ui.de_tableWidget.setRowCount(row_count + 1)

            col1 = QTableWidgetItem(text)
            self.ui.de_tableWidget.setItem(row_count, 0, col1)
            col1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setFlags(col1.flags() & Qt.ItemFlag.ItemIsEditable)

            self.de_combo_box = QComboBox()
            self.de_combo_box.addItems(drop_down_menu)
            self.ui.de_tableWidget.setCellWidget(row_count, 1, self.de_combo_box)
            
            col3 = QTableWidgetItem("0-"+self.parameter_len(text.lstrip()))
            self.ui.de_tableWidget.setItem(row_count, 2, col3)
            col3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            

    def de_add_text_to_table(self):
        self.ui.de_tableWidget.setHorizontalHeaderLabels(['Variables', 'Clip', 'Lenght'])
        text = self.ui.de_comboBox.currentText()
        self.de_table_append(text)



    def de_delete_selected_row(self):
        selected_row = self.ui.de_tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.de_tableWidget.removeRow(selected_row)

    def de_move_selected_row_up(self):
        selected_row = self.ui.de_tableWidget.currentRow()
        if 0 < selected_row <= self.ui.de_tableWidget.rowCount():
            self.ui.de_tableWidget.insertRow(selected_row - 1)
            self.de_copy_row(selected_row + 1, selected_row - 1)
            self.ui.de_tableWidget.removeRow(selected_row + 1)
            self.ui.de_tableWidget.selectRow(selected_row - 1)


    def de_move_selected_row_down(self):
        selected_row = self.ui.de_tableWidget.currentRow()
        table_widget = self.ui.de_tableWidget
        if 0 <= selected_row < table_widget.rowCount() - 1:
            table_widget.insertRow(selected_row + 2)
            self.de_copy_row(selected_row, selected_row + 2)
            table_widget.removeRow(selected_row)
            table_widget.selectRow(selected_row + 1)


    def de_copy_row(self, source_row, target_row):
        for column in range(self.ui.de_tableWidget.columnCount()):
            source_item = self.ui.de_tableWidget.item(source_row, column)
            if source_item is not None:
                target_item = QTableWidgetItem(source_item.text())
                self.ui.de_tableWidget.setItem(target_row, column, target_item)
                target_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


        self.source_widget = self.ui.de_tableWidget.cellWidget(source_row, 1)
        if isinstance(self.source_widget, QComboBox):
            self.target_widget = QComboBox()
            drop_down_menu = ['Normal', 'Right','Center', 'Left']
            self.target_widget.addItems(drop_down_menu)
            source_text = self.source_widget.currentText()
            self.target_widget.setCurrentText(source_text)
            self.ui.de_tableWidget.setCellWidget(target_row, 1, self.target_widget)

    def de_get_data_from_table(self):
        max_rows = self.ui.de_tableWidget.rowCount()
        var = []
        dict_ret = {}
        for i in range(0, max_rows):
            var = self.ui.de_tableWidget.item(i, 0).text()
            widget = self.ui.de_tableWidget.cellWidget(i, 1)
            clip = ""
            if isinstance(widget, QComboBox):
                clip = widget.currentText()

            cell_value = 0
            cell_text = ""
            table_item = self.ui.de_tableWidget.item(i, 2)
            if table_item is not None:
                cell_text = table_item.text()
                cell_value = str((cell_text))
            dict_ret[str(i)] = [str(var.lstrip()), str(clip), cell_value]
        return dict_ret


    def closeEvent(self, event):
        print("AUTOMATIC SETTING SAVED SUCESSFULLY")
#        self.save_settings_func()
#        event.accept()


def run_application():
    pass
     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
