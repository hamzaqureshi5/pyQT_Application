
import pandas as pd
debug=False

class PARAMETERS:
    __instance = None

    def __init__(self):
        if PARAMETERS.__instance is not None:
            raise Exception("GlobalParameters class is a singleton! Use get_instance() to access the instance.")
        else:
            PARAMETERS.__instance = self

            self.ICCID = ""
            self.IMSI = ""
            self.PIN1 = ""
            self.PUK1 = ""
            self.PIN2 = ""
            self.PUK2 = ""
            self.K4 = ""
            self.OP = ""
            self.ADM1 = ""
            self.ADM6 = ""
            self.ACC = ""
            self.DATA_SIZE=""
            self.ELECT_CHECK = False
            self.GRAPH_CHECK = False
            self.DEMO_CHECK = False

            self.pin1_rand=True
            self.puk1_rand=True
            self.pin2_rand=True
            self.puk2_rand=True
            self.adm1_rand=True
            self.adm6_rand=True
            self.acc_rand=True



            self.INPUT_DF =pd.DataFrame()
            self.ELECT_DF =pd.DataFrame()
            self.GRAPH_DF =pd.DataFrame()
            
            self.INPUT_PATH=""
            
            self.ELECT_DICT={}
            self.GRAPH_DICT={}
            self.INPUT_FILE_PARAMETERS={}
            
            #============================================#
            #=================EXTRACTOR==================#
            #============================================#
            self.EXTRCATOR_DICT={}

            self.dict1= {    
                    '0' : ['ICCID', 'Normal', "0-31"], '1' : ['IMSI', 'Normal', "0-31"], '2' : ['PIN1', 'Normal', "0-31"], 
                    '3' : ['PUK1' , 'Normal', "0-31"], '5' : ['PIN2', 'Normal', "0-31"], '6' : ['PUK2', 'Normal', "0-31"],
                    '7' : ['ADM1' , 'Normal', "0-31"], '8' : ['ADM6', 'Normal', "0-31"], '10': ['EKI' , 'Normal', "0-31"], 
                    '11': ['OPC'  , 'Normal', "0-31"], '12': ['ACC' , 'Normal', "0-3" ]
                }



    @staticmethod
    def get_instance():
        if PARAMETERS.__instance is None:
            PARAMETERS.__instance = PARAMETERS()
        return PARAMETERS.__instance

    def set_ICCID(self, value):
        self.ICCID = str(value)

    def set_IMSI(self, value):
        self.IMSI = str(value)

    def set_PIN1(self, value):
        self.PIN1 = str(value)

    def set_PUK1(self, value):
        self.PUK1 = str(value)

    def set_PIN2(self, value):
        self.PIN2 = str(value)

    def set_PUK2(self, value):
        self.PUK2 = str(value)

    def set_OP(self, value):
        self.OP = str(value)

    def set_K4(self, value):
        self.K4 = str(value)

    def set_ADM1(self, value):
        self.ADM1 = str(value)

    def set_ADM6(self, value):
        self.ADM6 = str(value)

    def set_ACC(self, value):
        self.ACC = str(value)

    def set_DATA_SIZE(self, value):
        self.DATA_SIZE = str(value)

    def set_ELECT_CHECK(self, value:bool):
        self.ELECT_CHECK = value

    def set_GRAPH_CHECK(self, value:bool):
        self.GRAPH_CHECK = value

    def set_DEMO_CHECK(self, value:bool):
        self.DEMO_CHECK = value

    def set_DEFAULT_HEADER(self, value:list):
        self.def_head = value


    def get_ICCID(self):
        return self.ICCID

    def get_IMSI(self):
         return self.IMSI
    
    def get_PIN1(self):
         return self.PIN1

    def get_PUK1(self):
         return self.PUK1

    def get_PIN2(self):
         return self.PIN2

    def get_PUK2(self):
         return self.PUK2

    def get_OP(self):
         return self.OP

    def get_K4(self):
         return self.K4

    def get_ADM1(self):
         return self.ADM1

    def get_ADM6(self):
         return self.ADM6

    def get_ACC(self):
         return self.ACC

    def get_ELECT_CHECK(self):
        return self.ELECT_CHECK

    def get_GRAPH_CHECK(self):
        return self.GRAPH_CHECK

    def get_DEMO_CHECK(self):
        return self.DEMO_CHECK

    def get_DATA_SIZE(self):
        return self.DATA_SIZE 
    
    def get_DEFAULT_HEADER(self):
        return self.def_head


    def set_PIN1_RAND(self, value:bool):
        self.pin1_rand = value

    def get_PIN1_RAND(self):
        return self.pin1_rand

    def set_PUK1_RAND(self, value:bool):
        self.puk1_rand = value

    def get_PUK1_RAND(self):
        return self.puk1_rand

    def set_PIN2_RAND(self, value:bool):
        self.pin2_rand = value

    def get_PIN2_RAND(self):
        return self.pin2_rand

    def set_PUK2_RAND(self, value:bool):
        self.puk2_rand = value

    def get_PUK2_RAND(self):
        return self.puk2_rand

    def set_ADM1_RAND(self, value:bool):
        self.adm1_rand = value

    def get_ADM1_RAND(self):
        return self.adm1_rand

    def set_ADM6_RAND(self, value:bool):
        self.adm6_rand = value

    def get_ADM6_RAND(self):
        return self.adm6_rand

    def set_ACC_RAND(self, value:bool):
        self.acc_rand = value

    def get_ACC_RAND(self):
        return self.acc_rand

    def set_INPUT_PATH(self, value:str):
        self.INPUT_PATH = value

    def get_INPUT_PATH(self):
        return self.INPUT_PATH

    def set_ELECT_DICT(self, value:dict):
        self.ELECT_DICT = value

    def get_ELECT_DICT(self):
        return self.ELECT_DICT

    def set_GRAPH_DICT(self, value:dict):
        self.GRAPH_DICT = value

    def get_GRAPH_DICT(self):
        return self.GRAPH_DICT

    def set_INPUT_FILE_PARAMETERS(self, value:dict):
        self.INPUT_FILE_PARAMETERS = value

    def get_INPUT_FILE_PARAMETERS(self):
        return self.INPUT_FILE_PARAMETERS
    
    def set_EXTRCATOR_DICT(self, value:dict):
        self.EXTRCATOR_DICT = value

    def get_EXTRCATOR_DICT(self):
        return self.EXTRCATOR_DICT

    
    
    
    def GET_ALL_PARAMS_DICT(self)->dict:
        param_dict={}
        param_dict["Demo Data"]=self.get_DEMO_CHECK()
        param_dict["OP"]=self.get_OP()
        param_dict["K4"]=self.get_K4()
        param_dict["ICCID"]=self.get_ICCID()
        param_dict["IMSI"]=self.get_IMSI()
        param_dict["PIN1"]=self.get_PIN1()
        param_dict["PUK1"]=self.get_PUK1()
        param_dict["PIN2"]=self.get_PIN2()
        param_dict["PUK2"]=self.get_PUK2()
        param_dict["ADM1"]=self.get_ADM1()
        param_dict["ADM6"]=self.get_ADM6()
        param_dict["ACC"]=self.get_ACC()
        param_dict["DATA_SIZE"]=self.get_DATA_SIZE()
        param_dict["INPUT_PATH"]=self.get_INPUT_PATH()
        print(param_dict)
        return param_dict

    def is_valid(self,param1,param_name:str):
        result=False
        param=param1
        match param_name:
            case "ICCID":
                result= len(str(param)) == 20 or len(str(param)) == 19 or len(str(param)) == 18
            case "IMSI":
                result= len(str(param)) == 15 
            case "PIN1" | "PIN2":
                    result=len(str(param)) == 4 
            case "PUK1"|"PUK2"|"ADM1"|"ADM6":
                    result=len(str(param)) == 8 
            case "OP":
                result=len(str(param)) == 32
            case "K4":
                result=len(str(param)) == 64
            case "SIZE":
                    param=int(param)
                    result=len(str(param)) != 0 or param > 0             
            case "DICT":
                    param=dict(param)
                    result = len(param) > 0
        return result

    def check_params(self)->bool:
        result=False
        if self.get_DEMO_CHECK():
            result= self.is_valid(self.get_IMSI(),"IMSI") and self.is_valid(self.get_ICCID(),"ICCID")  and self.is_valid(self.get_PIN1(),"PIN1") and self.is_valid(self.get_PUK1(),"PUK1") and self.is_valid(self.get_PIN2(),"PIN2") and self.is_valid(self.get_PUK2(),"PUK2") and self.is_valid(self.get_ADM1(),"ADM1") and self.is_valid(self.get_ADM6(),"ADM6") and self.is_valid(self.get_OP(),"OP") and self.is_valid(self.get_K4(),"K4") and self.is_valid(self.get_DATA_SIZE(),"SIZE") and self.is_valid(self.get_ELECT_DICT(),"DICT")and self.is_valid(self.get_GRAPH_DICT(),"DICT")           
        else:
            result= self.is_valid(self.get_PIN1(),"PIN1")  and self.is_valid(self.get_PUK1(),"PUK1") and self.is_valid(self.get_PIN2(),"PIN2") and self.is_valid(self.get_PUK2(),"PUK2") and self.is_valid(self.get_ADM1(),"ADM1") and self.is_valid(self.get_ADM6(),"ADM6") and self.is_valid(self.get_OP(),"OP") and self.is_valid(self.get_K4(),"K4")  and self.is_valid(self.get_ELECT_DICT(),"DICT")and self.is_valid(self.get_GRAPH_DICT(),"DICT")           
        return result
    
    
    def print_all_global_parameters(self):
        print("PIN1",self.get_PIN1())
        print("PIN2",self.get_PIN2())
        print("PIN2",self.get_PIN2())
        print("DATA SIZE",self.get_DATA_SIZE())
        
        


        




class DATA_FRAMES:
    __instance = None
    def __init__(self):
        if DATA_FRAMES.__instance is not None:
            raise Exception("GlobalParameters class is a singleton! Use get_instance() to access the instance.")
        else:
            DATA_FRAMES.__instance = self
            self.INPUT_DF =pd.DataFrame()
            self.ELECT_DF =pd.DataFrame()
            self.GRAPH_DF =pd.DataFrame()
            self.KEYS={}

    @staticmethod
    def get_instance():
        if DATA_FRAMES.__instance is None:
            DATA_FRAMES.__instance = DATA_FRAMES()
        return DATA_FRAMES.__instance



