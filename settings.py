from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QWidget
from global_parameters import PARAMETERS


            
class SETTINGS(QWidget):
    __instance = None
    def __init__(self):
#        if SETTINGS.__instance is not None:
#            raise Exception("SETTINGS class is a singleton! Use get_instance() to access the instance.")
#        else:
#            SETTINGS.__instance = self
            self.param1=PARAMETERS.get_instance()
            self.IMSI_SETT=QSettings("IMSI","")
            self.ICCID_SETT=QSettings("ICCID","")
            self.PIN1_SETT=QSettings("PIN1","")
            self.PUK1_SETT=QSettings("PUK1","")
            self.PIN2_SETT=QSettings("PIN2","")
            self.PUK2_SETT=QSettings("PUK2","")
            self.ADM1_SETT=QSettings("ADM1","")
            self.ADM6_SETT=QSettings("ADM6","")
            self.ACC_SETT=QSettings("ACC","")
            self.K4_SETT=QSettings("K4","")
            self.OP_SETT=QSettings("OP","")
            self.DATA_SIZE_SETT=QSettings("DATA_SIZE","")
            
            self.PIN1_RAND_CHECK_SETT=QSettings("PIN1_RAND","")
            self.PIN2_RAND_CHECK_SETT=QSettings("PIN2_RAND","")
            self.PUK1_RAND_CHECK_SETT=QSettings("PUK1_RAND","")
            self.PUK2_RAND_CHECK_SETT=QSettings("PUK2_RAND","")
            self.ADM1_RAND_CHECK_SETT=QSettings("ADM1_RAND","")
            self.ADM6_RAND_CHECK_SETT=QSettings("ADM6_RAND","")
            
        
    # @staticmethod
    # def get_instance():
    #     if SETTINGS.__instance is None:
    #         SETTINGS.__instance = SETTINGS()
    #     return SETTINGS.__instance

    def __del__(self):
        self.save_settings()

    def BoolToValue(self,value:bool):
        if isinstance(value, bool):
            if value==True:
                return "True"
            else:
                return "False"
        else:
            return value
        
    def valueToBool(self,value:str):
        if isinstance(value,str):
            if value.upper()=="TRUE":
                return True
            else:
                return False
        else:
            return value


    def save_settings(self):
        self.IMSI_SETT.setValue("IMSI",self.param1.get_IMSI())
        self.ICCID_SETT.setValue("ICCID",self.param1.get_ICCID())
        self.PIN1_SETT.setValue("PIN1",self.param1.get_PIN1())
        self.PUK1_SETT.setValue("PUK1",self.param1.get_PUK1())
        self.PIN2_SETT.setValue("PIN2",self.param1.get_PIN2())
        self.PUK2_SETT.setValue("PUK2",self.param1.get_PUK2())
        self.ADM1_SETT.setValue("ADM1",self.param1.get_ADM1())
        self.ADM6_SETT.setValue("ADM6",self.param1.get_ADM6())
        self.K4_SETT.setValue("K4",self.param1.get_K4())
        self.OP_SETT.setValue("OP",self.param1.get_OP())
        self.DATA_SIZE_SETT.setValue("DATA_SIZE",self.param1.get_DATA_SIZE())

        self.PIN1_RAND_CHECK_SETT.setValue("PIN1_RAND",self.BoolToValue(self.param1.get_PIN1_RAND()))
        self.PIN2_RAND_CHECK_SETT.setValue("PIN2_RAND",self.BoolToValue(self.param1.get_PIN2_RAND()))
        self.PUK1_RAND_CHECK_SETT.setValue("PUK1_RAND",self.BoolToValue(self.param1.get_PUK1_RAND()))
        self.PUK2_RAND_CHECK_SETT.setValue("PUK2_RAND",self.BoolToValue(self.param1.get_PUK2_RAND()))
        self.ADM1_RAND_CHECK_SETT.setValue("ADM1_RAND",self.BoolToValue(self.param1.get_ADM1_RAND()))
        self.ADM6_RAND_CHECK_SETT.setValue("ADM6_RAND",self.BoolToValue(self.param1.get_ADM6_RAND()))

    def load_settings(self):
        self.param1.set_IMSI(self.IMSI_SETT.value("IMSI"))
        self.param1.set_ICCID(self.ICCID_SETT.value("ICCID"))
        self.param1.set_PIN1(self.PIN1_SETT.value("PIN1"))
        self.param1.set_PUK1(self.PUK1_SETT.value("PUK1"))
        self.param1.set_PIN2(self.PIN2_SETT.value("PIN2"))
        self.param1.set_PUK2(self.PUK2_SETT.value("PUK2"))
        self.param1.set_ADM1(self.ADM1_SETT.value("ADM1"))
        self.param1.set_ADM6(self.ADM6_SETT.value("ADM6"))
        self.param1.set_K4(self.K4_SETT.value("K4"))
        self.param1.set_OP(self.OP_SETT.value("OP"))
        self.param1.set_DATA_SIZE(self.DATA_SIZE_SETT.value("DATA_SIZE"))        

        self.param1.set_PIN1_RAND(self.valueToBool(self.PIN1_RAND_CHECK_SETT.value("PIN1_RAND")))
        self.param1.set_PIN2_RAND(self.valueToBool(self.PIN2_RAND_CHECK_SETT.value("PIN2_RAND")))
        self.param1.set_PUK1_RAND(self.valueToBool(self.PUK1_RAND_CHECK_SETT.value("PUK1_RAND")))
        self.param1.set_PUK2_RAND(self.valueToBool(self.PUK2_RAND_CHECK_SETT.value("PUK2_RAND")))
        self.param1.set_ADM1_RAND(self.valueToBool(self.ADM1_RAND_CHECK_SETT.value("ADM1_RAND")))
        self.param1.set_ADM6_RAND(self.valueToBool(self.ADM6_RAND_CHECK_SETT.value("ADM6_RAND")))



#s=SETTINGS()
#s.save_settings()
#s.load_settings()
