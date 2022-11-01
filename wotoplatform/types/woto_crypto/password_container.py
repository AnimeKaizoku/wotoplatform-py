from pydantic import BaseModel
from typing import Iterable
import hashlib

class PasswordContainer256(BaseModel):
    """
    Contains a password from user input.
    Call `set_as_password` method on this class to set the user-input password.
    """
    __HEADERS_LEN = 0x03
    __HEADERS_CHARS = [0x2a, 0x21, 0x2f]
    __SIG_CHARS = [0x3c, 0x40, 0x5e, 0x2d, 0x7e, 0x5d, 0x3d, 0x29]
    
    PWD_ENCODING_VERSION = "<pwd-container::v1.0.0.0::256>"
    
    
    header: str = None
    hash256: str = None
    signature: str = None

    
    def set_as_password(self, text: str) -> None:
        self.calculate_header(text)
        self.calculate_hash(text)
        self.calculate_signature(text)

    def get_as_dict(self) -> dict:
        return {
            'header': self.header,
            'hash256': self.hash256,
            'signature': self.signature
        }
    
    def calculate_signature(self, user_input: str) -> None:
        #TODO: add support for payload data
        self.signature = self.__append_by_seps(user_input, self.__SIG_CHARS, True)
    
    def calculate_hash(self, user_input: str) -> None:
        self.hash256 = hashlib.sha256(user_input.encode()).hexdigest()
    
    def calculate_header(self, user_input: str) -> None:
        headers_list = []
        headers_list.append(len(user_input)) # 0x00
        headers_list.append(0) # 0x01 (TODO: add support for payload in header)
        headers_list.append(self.PWD_ENCODING_VERSION)
        
        if not self.has_correct_headers_len(headers_list):
            raise Exception('Invalid headers len could get generated from the input value')
        
        self.header = self.__append_by_seps(headers_list, self.__HEADERS_CHARS)
    
    
    def has_correct_headers_len(self, headers: Iterable) -> bool:
        return len(headers) == self.__HEADERS_LEN
    
    
    def __append_by_seps(
        self, 
        slices: Iterable, 
        values: list, 
        to_num: bool = False
    ) -> str:
        result_value = ''
        current_index = -1
        for current in slices:
            if to_num: current = str(ord(current))
            current_index += 1
            result_value += str(current) + chr(values[current_index % len(values)])
        return result_value
    
    
    
    


