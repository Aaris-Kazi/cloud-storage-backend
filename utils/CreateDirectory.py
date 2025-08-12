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
    
def listDirectoryV2(path: str) -> dict:
    contents = {}
    try:
        for entry in os.listdir(path):
            full_path: str = os.path.join(path, entry)
            dirType:str = "file" if os.path.isfile(full_path) else "folder" 
            data: list = contents.get(dirType, [])
            data.append({"name": entry})
            contents.update({dirType: data})

    except FileNotFoundError as e:
        print(e)
    except NotADirectoryError as e1:
        print(e1)
        
    return contents