import subprocess
import os
import time
from datetime import datetime

def get_ip():
    try:
        # Koristimo tvog favorita ipconfig.me
        return subprocess.check_output("curl -s https://ifconfig.me", shell=True).decode().strip()
    except:
        return None

print("faza 1: Uzimamo pravi IP")
moj_pravi_ip = get_ip()

if not moj_pravi_ip:
    print("Greška ne mogu dohvatiti IP. Provjeri internet!")
    exit()

print(f"Pravi IP je markiran kao zabranjen: {moj_pravi_ip}")
# --- FAZA 2: ČEKANJE NA TOR ---
time.sleep(10)
print("\nfaza 2: Mozes se povezati sa SSTap")
while True:
    trenutni = get_ip()
    if trenutni and trenutni != moj_pravi_ip:
        print(f"SSTap radi, Novi IP: {trenutni}")
        print("WOOF WOOF PRATIM")
        break
    time.sleep(2)

# --- FAZA 3: STRAŽA (WATCHDOG) ---
try:
    while True:
        provera = get_ip()
        if provera == moj_pravi_ip:
            print("\ndetektovan je tvoj pravi IP - aktiviram kill switch")
            # 1. Odmah seci mrežu
            os.system('netsh interface set interface "Ethernet" admin=disabled')
            # 2. Pogasi sve prozore (Tvoja komanda)
            os.system('powershell "Get-Process | Where-Object { $_.MainWindowTitle -ne \'\'} | Stop-Process -Force"')
            break
            
        elif provera is None:
            # Ako curl ne uspe, verovatno SSTap menja čvor, sačekaj malo
            pass
        else:
            # IP je drugačiji od tvog pravog (Tor radi i menja čvorove)
            timenow = datetime.now()
            print(f"[{timenow.hour}:{timenow.minute}:{timenow.second}] Siguran si. Trenutni Tor IP: {provera}", end="\r")
            
        time.sleep(1)
except KeyboardInterrupt:
    print("\nWatchdog ugašen ručno.")