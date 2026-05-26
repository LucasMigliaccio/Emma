import os
import subprocess


APP_PATH = r"C:\Users\LMGG1\Desktop\Softbarber\dist\SoftBarber\SoftBarber.exe"



def open_app():
    if not os.path.exists(APP_PATH):
        print("No se encontro la aplicacion")
        return

    subprocess.Popen([APP_PATH], shell=False)
    print("Aplicacion abierta")


if __name__ == "__main__":
    open_app()