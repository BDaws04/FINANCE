def loadKeys():
    with open("AlgorithmicTradingALPACA\Keys.txt") as file:
        try:
           API_KEY = file.readline().strip()
           SECRET_KEY = file.readline().strip()
        except Exception as e:
            print(f"{e}")
        return API_KEY, SECRET_KEY
