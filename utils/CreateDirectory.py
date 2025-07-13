import os

def createDirectory(path: str, nested:bool = False) -> bool:
    try:
        if nested:
            os.mkdir(path)
        else:
            os.makedirs(path)
        return True
    except FileExistsError:
        return False
    

def deleteDirectory(path: str, nested:bool = False) -> bool:
    try:
        os.rmdir(path)
        return True
    except FileExistsError:
        return False

def deleteFile(path: str, nested:bool = False) -> bool:
    try:
        os.remove(path)
        return True
    except FileExistsError:
        return False
    
def listDirectory(path: str) -> list:
    contents = []
    try:
        contents = os.listdir(path)
    except FileNotFoundError as e:
        print(e)
    except NotADirectoryError as e1:
        print(e1)
        
    return contents