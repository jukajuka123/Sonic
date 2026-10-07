import requests
import subprocess
import os
import sys
import re

# Ensures Windows handles UTF-8 characters correctly
os.environ["PYTHONIOENCODING"] = "utf-8"

def clean_sonic_code(raw_response):
    """
    Cleans the AI response to extract only executable Python code.
    """
    # Remove Markdown code blocks if Sonic includes them
    clean_text = re.sub(r'```python|```', '', raw_response)
    
    lines = clean_text.splitlines()
    code_lines = []
    
    # Skip common conversational filler if the Modelfile fails to stop it
    ignore_prefixes = ("Note:", "Here is", "Certainly", "Sure", "This", "The")
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(ignore_prefixes):
            continue
        code_lines.append(line)
        
    return "\n".join(code_lines)

import requests, os, sys, re

# Čuvanje konteksta (zadnjih 5 poruka)


def run_agent():
    print("=== SONIC SENIOR AGENT V2 (with Memory) ===")
    
    while True:
        query = input("\nŠta želiš?: ")
        if query.lower() in ['kraj', 'exit']: break

        # Dodajemo instrukciju za sigurnost u svaki upit
        full_prompt = f"{query}\nResponse only with code:"
        
        payload = {"model": "sonic", "prompt": full_prompt, "stream": False}
        
        try:
            r = requests.post("http://localhost:11434/api/generate", json=payload)
            # Čistimo odgovor od ``` i Note-ova
            raw_code = r.json()['response']
            code = re.sub(r'```python|```', '', raw_code).strip()
            # Filtriranje linija koje nisu kod
            code = "\n".join([l for l in code.splitlines() if not l.startswith(("Note:", "Here", "Sure"))])

            print(f"\n--- GENERISANI KOD ---\n{code}\n----------------------")
            
            if input("Izvršiti? (y/n): ").lower() == 'y':
                max_retries = 2
                attempt = 0
                while attempt < max_retries:
                    try:
                        # Pokušaj izvršavanja koda
                        exec(code, globals())
                        break # Ako prođe, izađi iz retry petlje
                    
                    except ModuleNotFoundError as e:
                        # Ekstrakcija imena modula iz greške (npr. "No module named 'yt_dlp'")
                        module_name = e.name 
                        print(f"Detektovan nedostajući modul: {module_name} ---")
                        print(f"Instalacija u toku...")
                        
                        try:
                            # Instalacija preko pip-a
                            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                            print(f"Modul {module_name} je uspješno instaliran. Ponovni pokušaj...")
                            attempt += 1
                            continue # Vrati se na početak try bloka i pokušaj opet exec()
                        except Exception as install_error:
                            print(f"Neuspjela instalacija modula: {install_error}")
                            break
                            
                    except Exception as e:
                        print(f"GREŠKA: {e}")
                        break

        except Exception as e:
            print(f"Konekcija: {e}")

if __name__ == "__main__":
    run_agent()

if __name__ == "__main__":
    run_agent()