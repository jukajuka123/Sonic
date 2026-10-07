import sounddevice as sd
import vosk
import json
import queue
import pyautogui
import time
import subprocess
import pygetwindow as gw
import os
import requests
from bs4 import BeautifulSoup
import tempfile
import datetime
from word2number import w2n
import winsound
import ctypes
import sys
import os
import webbrowser
import win32gui
import win32con
import random
import webbrowser
import yt_dlp

lista_rijeci = '["sonic","save","battery","usage","on","off","speak","space","enter","left","right","english","bosnian","play","find","something","watch","volume", "up", "down", "mute","dictation","dictate","dictation","stop","search","youtube","you tube","kill","all","are","you","screenshot","news","goodbye","remind","me","and", "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten","eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty","seventy","eighty","ninety","hundred","weather","study","work","programming","microsoft","word","access","excel","power point","teams","go","to","sleep","lock","transfer","files","clear","screen","smart","kill","[unk]"]'


def run_as_admin():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not is_admin():
        # Ponovo pokreće trenutni fajl, ali traži Admin dozvolu
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit() # Gasi običnu verziju skripte

# OVO MORA BITI PRVA STVAR KOJU SKRIPTA URADI
run_as_admin()

# Putanja do modela i Chrome-a
MODEL_PATH = r"C:\VoskModel"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "https://aistudio.google.com/live?model=gemini-2.5-flash-native-audio-preview-12-2025"
provjeripodsjetnik = False
sati = None
minute = None
tekst_podsjetnika = None

# Inicijalizacija Vosk modela
model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

# 1. PRVO učitaj model (ovo traje par sekundi)
print("Učitavam model...")
model = vosk.Model(MODEL_PATH)
rec = vosk.KaldiRecognizer(model, 16000, lista_rijeci)

# 2. TEK ONDA otvori stream za mikrofon
print("Otvaram mikrofon...")

def ponovi(splitted, t):
    if(len(splitted) == 2):
        pyautogui.press(t)
    else:
        try:
            broj = w2n.word_to_num(splitted[2])
            for i in range(1,broj+1):
                pyautogui.press(t)
        except Exception as e:
            print(e)
        

#os.system("start cmd.exe @cmd /k \"cd C:\\Users\\jusuf\\Desktop\\Sonic\\remote && python slusajmail.py\"")

with sd.RawInputStream(samplerate=16000, blocksize=2000, dtype='int16',
                       channels=1, callback=callback):
    
    # 3. Odmah očisti queue za svaki slučaj
    while not q.empty():
        try:
            q.get_nowait()
        except:
            break
            
    rec.Reset()
    print(">>> SPREMAN! Sad te čujem odmah.")
    while True:
        if provjeripodsjetnik:
            now = datetime.datetime.now()
            if(now.hour == sati and now.minute == minute):
                print("Namjestio si podsjetnik u ovom vremenu: "+tekst_podsjetnika)
                provjeripodsjetnik = False
                notes = [523, 659, 784, 1046] # C-E-G-C (C-dur akord)
                for n in notes:
                    winsound.Beep(n, 150)
                for n in reversed(notes):
                    winsound.Beep(n, 150)

                pyautogui.hotkey('win','d')
                time.sleep(0.5)
                # 2. Pronađi prozor koji se zove TAČNO "sonic"
                pronadjen = False
                for prozor in gw.getAllWindows():
                    if prozor.title == r"Administrator: C:\Program Files\Python314\python.exe" or prozor.title == r"C:\Program Files\Python314\python.exe":  # Mora biti identično (pazi na velika/mala slova)
                        try:
                            prozor.restore()
                            prozor.activate()
                            pronadjen = True
                            break # Prekidamo potragu jer smo našli šta nam treba
                        except Exception:
                            pass

        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result['text'].lower()
            
            if text:
                print(f"Čuo sam: {text}")

            if text.startswith("sonic") or text.startswith("sony"):

                if "sonic" == text:
                    notes = [440]
                    for n in notes:
                        winsound.Beep(n, 150)
                
                elif "volume up" in text:
                    pyautogui.press('volumeup', presses=5)
                    print(">>> Pojacavam zvuk")

                elif "volume down" in text:
                    pyautogui.press('volumedown', presses=5)
                    print(">>> Smanjujem zvuk")

                elif "mute" in text:
                    pyautogui.press('volumemute')
                    print(">>> Zvuk ugasen")

                elif "clear screen" in text:
                    pyautogui.hotkey('win', 'd')
                    print(">>> Ekran Cist")

                elif "screenshot" in text:
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    pyautogui.screenshot(f"C:\\Screenshots\\shot_{timestamp}.png")
                    print(">>> Screenshot spremljen!")

                    putanja_do_foldera = r"C:\Screenshots"
                    # Komanda koja otvara File Explorer
                    os.startfile(putanja_do_foldera)
                
                elif "transfer files" in text:
                    os.system(r'start "" "C:\Program Files\LocalSend\localsend_app.exe"')
                    print(">>> Mozes poslati")
                
                elif "search" in text:
                    query = text.replace("search", "").strip()
                    newquery = query.replace("sonic", "").strip()
                    import webbrowser
                    webbrowser.open(f"https://www.google.com/search?q={newquery}")
                    print(">>> Searchamo")
                
                elif "sonic lock" == text or "sonic look" == text or "sony look" == text or "sony lock" == text:
                    import ctypes
                    ctypes.windll.user32.LockWorkStation()
                    print(">>> Zakljucan")
                
                elif "sonic go to sleep" in text or "sonic go two sleep" in text:
                    print(">>> Šaljem PC na spavanje...")
                    
                    # 2. Sačekaj 3 sekunde da se audio drajver 'opusti'
                    time.sleep(3)
                    
                    # 3. Sada šaljemo komandu za Sleep koja više nema prepreka
                    # Prvi parametar $false osigurava da ide u Sleep, a ne u Hibernate
                    cmd = 'powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)"'
                    
                    os.system(cmd)

                elif "sonic notes" == text or "sony notes" == text:
                    os.system(r'start "" "C:\Windows\notepad.exe"')

                elif "sonic microsoft" in text or "sony microsoft" in text:
                    if "microsoft word" in text:
                        os.system(r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"')
                    elif "microsoft access" in text:
                        os.system(r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Access.lnk"')
                    elif "microsoft excel" in text:
                        os.system(r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"')
                    elif "microsoft power point" in text:
                        os.system(r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"')
                    elif "microsoft teams" in text:
                        os.system('start ms-teams.exe')

                elif "sonic youtube" == text or "sonic you tube" == text or "sony youtube" == text or "sony you tube" == text :
                    os.system("start chrome \"https://youtube.com\"")

                elif "sonic work" == text:
                    link1 = "https://mail.google.com/mail/u/0/#inbox"
                    link2 = "https://tester.test.io/"
                    link3 = "https://www.utest.com/"

                    # --new-window kreira svjež prozor
                    # Zatim samo nižeš linkove pod navodnicima
                    os.system(f'start chrome --new-window "{link1}" "{link2}" "{link3}"')
    
                    # 3. PowerShell magija koja pronalazi Chrome prozor i maksimizira ga
                    ps_cmd = (
                        'powershell -command "'
                        '$member = \'[DllImport(\\"user32.dll\\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);\'; '
                        '$type = Add-Type -MemberDefinition $member -Name \"Win32ShowWindow\" -PassThru; '
                        '$hwnd = (Get-Process chrome | Where-Object { $_.MainWindowTitle -ne \'\' }).MainWindowHandle | Select-Object -First 1; '
                        'if ($hwnd) { $type::ShowWindow($hwnd, 3) }"'
                    )
                    
                    os.system(ps_cmd)
                
                elif "sonic study" == text:
                    os.system('powershell "Get-Process | Where-Object { $_.MainWindowTitle -ne \'\' -and $_.ProcessName -notmatch \'python|womic|explorer|cmd\' } | Stop-Process -Force"')
                    
                    link1 = "https://drive.google.com/drive/u/0/folders/1r9mhl5BWbl8lBi_mYcmdlSh0PiNI1Uzr"
                    link2 = "https://youtube.com"
                    link3 = "https://gemini.google.com/app"
                    os.system(f'start chrome --new-window "{link1}" "{link2}" "{link3}"')
    
                    # 3. PowerShell magija koja pronalazi Chrome prozor i maksimizira ga
                    ps_cmd = (
                        'powershell -command "'
                        '$member = \'[DllImport(\\"user32.dll\\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);\'; '
                        '$type = Add-Type -MemberDefinition $member -Name \"Win32ShowWindow\" -PassThru; '
                        '$hwnd = (Get-Process chrome | Where-Object { $_.MainWindowTitle -ne \'\' }).MainWindowHandle | Select-Object -First 1; '
                        'if ($hwnd) { $type::ShowWindow($hwnd, 3) }"'
                    )
                    os.system(ps_cmd)
                
                elif "sonic programming" == text:
                    os.system("code")
                
                elif "sonic kill all" == text:
                    os.system('powershell "Get-Process | Where-Object { $_.MainWindowTitle -ne \'\' -and $_.ProcessName -notmatch \'python|womic|explorer|cmd\' } | Stop-Process -Force"')

                elif "sonic dictate" == text or "sonic dictation" == text or "sonic stop dictate" == text:
                    pyautogui.hotkey("win","h")

                
                elif "sonic weather" == text or "sonic whether" == text:
                    webbrowser.open("https://www.accuweather.com/en/ba/sarajevo/33028/weather-forecast/33028")
                
                elif "sonic news" == text:
                    # --- 1. DEO: Prikupljanje podataka ---
                    url = 'https://crna-hronika.info/'
                    headers = {'User-Agent': 'Mozilla/5.0'}

                    try:
                        response = requests.get(url, headers=headers)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        elementi = soup.find_all(class_="title uk-margin-small")
                        
                        naslovi = [el.get_text(strip=True) for el in elementi]

                        if not naslovi:
                            print("Nisu pronađeni elementi.")
                        else:
                            # --- 2. DEO: Kreiranje privremenog fajla ---
                            # Koristimo tempfile da izbegnemo probleme sa dozvolama
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tf:
                                tf.write(f"PRONAĐENO ELEMENATA: {len(naslovi)}\n")
                                tf.write("="*30 + "\n\n")
                                for n in naslovi:
                                    tf.write(f"{n}\n")
                                temp_path = tf.name # Putanja do tog fajla

                            # --- 3. DEO: Otvaranje u Notepadu ---
                            os.startfile(temp_path)
                            print(f"Uspešno! Notepad otvoren.")

                    except Exception as e:
                        print(f"Greška: {e}")
                
                elif "sonic remind me" in text:
                    now = datetime.datetime.now()
                    print(f"trenutno vrijeme: {now.hour}:{now.minute}")
                    newtext = text.replace("sonic remind me", "")
                    if "and" not in text:
                        pass
                    try:
                        delovi = newtext.split(" and ")

                        satistr = delovi[0]
                        minutestr = delovi[1]
                    except:
                        print("nisam mogao da namjestim, nisam te dobro cuo: ")
                        print(text)
                    try:
                        sati = w2n.word_to_num(satistr)
                        minute = w2n.word_to_num(minutestr)
                    except:
                        print("nisam mogao da namjestim, nisam te dobro cuo: ")
                        print(text)
                    print("Namjestio sam podsjetnik za " + str(sati) + ":" + str(minute))
                    provjeripodsjetnik = True
                    tekst_podsjetnika = input("Cekam Unos za sta te podsjecam: ")
                    print("namjestio podsjetnik: "+ tekst_podsjetnika)
                
                
                elif "sonic smart" == text:
                    os.system("start cmd.exe @cmd /k \"cd C:\\Users\\jusuf\\Desktop\\svega\\projekti\\sonic && python lama.py\"")
                    pyautogui.hotkey("win","h")

                elif "sonic kill" == text:
                    hwnd = win32gui.GetForegroundWindow()
                    if hwnd:
                        # 2. Pošalji WM_CLOSE poruku toj ručki
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

                elif "sonic play something" in text.lower():

                    # 1. Odabir liste kanala na osnovu jezika u komandi
                    if "english" in text.lower():
                        my_channels = [
                            "@Fireship",
                            "@NetworkChuck",
                            "@Veritasium",
                            "@fern-tv"
                        ]
                    elif "bosnian" in text.lower():
                        my_channels = [
                            "@FISTProHD",
                            "@NMK"
                        ]
                    else:
                        # Fallback ako u komandi nije izgovoren jezik (kombinuje sve)
                        my_channels = [
                            "@FISTProHD",
                            "@NMK",
                            "@Fireship",
                            "@NetworkChuck",
                            "@Veritasium",
                            "@fern-tv"
                        ]

                    # Nasumično biramo jedan kanal i sklapamo URL do svih njegovih videa
                    selected_channel = random.choice(my_channels)
                    channel_url = f"https://www.youtube.com/{selected_channel}/videos"
                    
                    print(f"Sonic preuzima sve videa sa kanala {selected_channel}...")

                    ydl_opts = {
                        'quiet': True,
                        'extract_flat': True,  # Ekstremno brzo - izvlači samo listu i trajanja bez skidanja
                        'playlistend': 400,    # Ograničenje na zadnjih 400 videa radi brzine
                    }

                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(channel_url, download=False)
                            
                            if info and 'entries' in info:
                                # 2. Specifično filtriranje na osnovu odabranog kanala
                                if selected_channel == "@NMK":
                                    # Samo videa > 10 min sa "(NMK HRVATSKA)" u naslovu
                                    long_videos = [
                                        v for v in info['entries'] 
                                        if v and v.get('duration') and v.get('duration') >= 600
                                        and "(NMK HRVATSKA)" in v.get('title', '').upper()
                                    ]

                                elif selected_channel == "@FISTProHD":
                                    # Samo videa > 10 min sa "LUD, ZBUNJEN, NORMALAN" ili "KRIZA" u naslovu
                                    long_videos = [
                                        v for v in info['entries'] 
                                        if v and v.get('duration') and v.get('duration') >= 600
                                        and any(show in v.get('title', '').upper() for show in ["LUD, ZBUNJEN, NORMALAN", "KRIZA"])
                                    ]

                                else:
                                    # Za sve ostale kanale samo tražimo duže od 10 min (600 sekundi)
                                    long_videos = [
                                        v for v in info['entries'] 
                                        if v and v.get('duration') and v.get('duration') >= 600
                                    ]

                                # 3. Pokretanje odabranog videa
                                if long_videos:
                                    chosen_video = random.choice(long_videos)
                                    video_id = chosen_video.get('id')
                                    video_title = chosen_video.get('title', 'Video')
                                    
                                    print(f"Puštam sa kanala {selected_channel}: {video_title}")
                                    webbrowser.open(f"https://www.youtube.com/watch?v={video_id}&autoplay=1")
                                    time.sleep(5)
                                    pyautogui.press('f')
                                else:
                                    print(f"Kanal {selected_channel} nema odgovarajućih videa po zadanom filteru.")
                            else:
                                print("Nisam uspio učitati videa sa kanala.")
                    except Exception as e:
                        print(f"Greška pri pretrazi kanala: {e}")

                elif "sonic left" in text:
                    splitted = text.split()
                    ponovi(splitted, "left")

                elif "sonic right" in text:
                    splitted = text.split()
                    ponovi(splitted, "right")

                elif "sonic up" in text:
                    splitted = text.split()
                    ponovi(splitted, "up")

                elif "sonic down" in text:
                    splitted = text.split()
                    ponovi(splitted, "down")

                elif "sonic space" == text:
                    pyautogui.press("space")
                elif "sonic enter" == text:
                    pyautogui.press("enter")

                elif "sonic save battery on" == text:
                    os.system("powercfg /setdcvalueindex SCHEME_CURRENT SUB_ENERGYSAVER ESBATTTHRESHOLD 100")
                    os.system("powercfg /setactive scheme_current")
                    os.system('powershell -Command "(Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 30)"')
                    os.system("powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 50")
                    os.system("powercfg /setactive SCHEME_CURRENT")

                elif "sonic save battery off" == text:
                    os.system("powercfg /setdcvalueindex SCHEME_CURRENT SUB_ENERGYSAVER ESBATTTHRESHOLD 20")
                    os.system("powercfg /setactive scheme_current")
                    os.system('powershell -Command "(Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 100)"')
                    os.system("powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100")
                    os.system("powercfg /setactive SCHEME_CURRENT")

                elif "sonic usage" == text:
                    os.startfile(r"C:\Users\jusuf\OneDrive\Desktop\Sonic\Usage.txt")

