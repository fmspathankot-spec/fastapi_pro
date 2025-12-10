from passlib.context import CryptContext
"""
This line imports the CryptContext class from the passlib.context module. Passlib is a Python library for secure password
hashing and verification, supporting multiple algorithms like bcrypt, PBKDF2, and others. CryptContext is a key class that
 creates a "context" object for handling password hashing with configurable schemes (algorithms), 
allowing easy switching between them and automatic handling of deprecated ones.
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
This line creates an instance of CryptContext with the bcrypt scheme as 
the default and sets deprecated to "auto". The bcrypt scheme is a strong password hashing algorithm that is recommended
 for secure password storage. The deprecated parameter is set to "auto" to automatically handle deprecation of 
 schemes in the future.
"""

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

"""
This function takes a plain password string as input and returns its hashed version using the bcrypt algorithm.
It uses the CryptContext instance created earlier to perform the hashing.
"""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
"""
This function takes a plain password string and a hashed password string as input and returns a boolean 
indicating whether the plain password matches the hashed password. It uses the CryptContext instance created earlier to
 perform the verification.
"""
