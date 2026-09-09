from cryptography.fernet import Fernet
import os
from logging import error, info
from exc import SALTNotConfigured

class __Keys:
            def __init__(self) -> None:
                self.raw_token_key = os.getenv("TOKEN_KEY")
                self.raw_user_id_key = os.getenv("USER_ID_KEY")
                self.raw_password_key = os.getenv("PASSWORD_KEY")

            def __contains__(self, item) -> bool:
                return item in (self.raw_token_key, self.raw_user_id_key, self.raw_password_key)


class Utils():
    def __init__(self) -> None:
        keys = __Keys()
        
        if None in keys:
            raise SALTNotConfigured
        
        token_key = keys.raw_token_key.encode("utf-8") # type: ignore
        user_id_key = keys.raw_user_id_key.encode("utf-8") # type: ignore
        password_key = keys.raw_password_key.encode("utf-8") # type: ignore
        
        self.chiper_suite_token = Fernet(key=token_key)
        self.chiper_suite_user_id = Fernet(key=user_id_key)
        self.chiper_suite_password = Fernet(key=password_key)
        
    
    def encrypt_token(self, token: str) -> str:
        return self.chiper_suite_token.encrypt(token.encode("utf-8")).decode("utf-8")
    
    def decrypt_token(self, encrypted_token: str)-> str:
        return self.chiper_suite_token.decrypt(encrypted_token.encode("utf-8")).decode("utf-8")
    
    
    def encrypt_user_id(self, user_id: str)-> str:
        return self.chiper_suite_user_id.encrypt(user_id.encode("utf-8")).decode("utf-8")
    
    def decrypt_user_id(self, encrypted_user_id: str) -> str:
        return self.chiper_suite_user_id.decrypt(encrypted_user_id.encode("utf-8")).decode("utf-8")
    
    
    def encrypt_password(self, password: str):
        return self.chiper_suite_password.encrypt(password.encode("utf-8")).decode("utf-8")
    
    def decrypt_password(self, encrypted_password: str):
        return self.chiper_suite_password.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")
        