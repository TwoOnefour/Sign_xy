import urllib3
from Sign_xy import Sign_xy

if __name__ == "__main__":
    urllib3.disable_warnings()
    mybot = Sign_xy()
    mybot.run()
