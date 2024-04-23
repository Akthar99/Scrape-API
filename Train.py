

class Read:
    def __init__(self) -> None:
        super().__init__()
        self.dict_data = {}

    def clean_file(self):
        with open('input.txt', 'r') as file:
            rowData = file.read()
            listedData = list(rowData)
            listedData.remove('T')

            newList = [nData for nData in listedData if nData not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ":", "\n"]]

            self.editedData = ''.join(newList)
        with open('test.txt', 'w') as file2:
            file2.write(self.editedData)
    
    def processData(self, fileData: str):
        splitedData = fileData.split()
        NrepeatData = {}
        for i, data in enumerate(splitedData):
            if data not in NrepeatData:
                NrepeatData.setdefault(data , 0)
        print(NrepeatData)

with open('test.txt', 'r') as file:
    read = Read().processData(fileData=file.read())
