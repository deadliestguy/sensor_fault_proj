import sys 
import os 
 
# runtime error handled korey  
class CustomException(Exception):

    # ctor 
    def __init__(self,error_msge ,ereor_details:sys ):
        # variable create korbo 
        self.error_msge = error_msge

        _,_,exc_tb = ereor_details.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    # jokhoni class er object print korbo ei function trigger hbe 
    def __str__(self):
        return "Exception occured in file name [{0}] line no [{1}] error message [{2}]".format(
            self.filename,self.lineno,self.error_msge
        )




