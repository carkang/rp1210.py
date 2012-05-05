###############################################################################
# Core Python Wrapper for RP1210 dlls
###############################################################################

from ctypes import *
import ConfigParser

"""
Class: RP1210
"""
class RP1210:
    def __init__(self):
        """
        RP1210 Constructor
        """
        config = ConfigParser.RawConfigParser()
        # Todo: 1) Determine os 2) Load our own config, 3) determine windows root, 4) open ini
        config.read('c:\windows\RP121032.ini')
        # Todo: Select the correct dll and dll config name by matching config or if there is only one
        dllname = config.get('RP1210Support', 'APIImplementations').split(',')[0]
        # Todo: Open dll ini file for details of allowed configurations
        
        # Load the correct dll
        self.dll = windll.LoadLibrary(dllname)

        # Define Function Prototypes for python type checking - otherwise python depends on before and after stack pointer comparisons
        self.dll.RP1210_ClientConnect.argtypes = [c_long, c_short, c_char_p, c_long, c_long, c_short]
        self.dll.RP1210_ClientDisconnect.argtypes = [c_short]
        self.dll.RP1210_SendMessage.argtypes = [c_short, c_char_p, c_short, c_short, c_short]
        self.dll.RP1210_ReadMessage.argtypes = [c_short, c_char_p, c_short, c_short]
        self.dll.RP1210_ReadVersion.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        self.dll.RP1210_ReadDetailedVersion.argtypes = [c_short, c_char_p, c_char_p, c_char_p]
        self.dll.RP1210_GetErrorMsg.argtypes = [c_short, c_char_p]
        self.dll.RP1210_GetLastErrorMsg.argtypes = [c_short, c_void_p, c_char_p]
        self.dll.RP1210_GetHardwareStatus.argtypes = [c_short, c_char_p, c_short, c_short]
        self.dll.RP1210_SendCommand.argtypes = [c_short, c_short, c_char_p, c_short]
        
    def ClientConnect(self, Device, Protocol, TxBufSize, RxBufSize):
        return self.dll.RP1210_ClientConnect(c_long(0), Device, Protocol, TxBufSize, RxBufSize, 0)
    
    def ClientDisconnect(self, ClientId):
        return self.dll.RP1210_ClientDisconnect(ClientId)
        
    def SendMessage(self, ClientId, Message, MessageSize, Block):
        return self.dll.RP1210_SendMessage(ClientId, Message, MessageSize, 0, Block)
    
    def ReadMessage(self, ClientId, Block):
        p1 = create_string_buffer(100)
        self.dll.RP1210_ReadMessage(ClientId, p1, len(p1), Block)
        return p1.value
    
    def ReadVersion(self):
        p1 = create_string_buffer(5)
        p2 = create_string_buffer(5)
        p3 = create_string_buffer(5)
        p4 = create_string_buffer(5)
        self.dll.RP1210_ReadVersion(p1, p2, p3, p4)
        return (p1.value, p2.value, p3.value, p4.value)
    
    def ReadDetailedVersion(self, ClientId):
        p1 = create_string_buffer(17)
        p2 = create_string_buffer(17)
        p3 = create_string_buffer(17)
        self.dll.RP1210_ReadDetailedVersion(ClientId, p1, p2, p3)
        return (p1.value, p2.value, p3.value)
        
    def GetErrorMsg(self, ErrorCode):
        p1 = create_string_buffer(80)
        self.dll.RP1210_GetErrorMsg(ErrorCode, p1)
        return p1.value

    def GetLastErrorMsg(self, ErrorCode):
        p1 = c_int(0)
        p2 = create_string_buffer(80)
        self.dll.RP1210_GetLastErrorMsg(ErrorCode, byref(p1), p2)
        return (p1, p2)

    def GetHardwareStatus(self, ClientId, Block):
        p1 = create_string_buffer(18)
        self.dll.RP1210_GetHardwareStatus(ClientId, p1, 18, Block)
        return p1.value
        
    def SendCommand(self, ClientId, CommandNumber, CommandString, CommandSize):
        return self.dll.RP1210_SendCommand(CommandNumber, ClientId, CommandString, CommandSize)
    
    
    