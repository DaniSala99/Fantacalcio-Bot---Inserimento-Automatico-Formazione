"""
Fantacalcio Bot - Inserimento Automatico Formazione
Repository: https://github.com/tuousername/fantacalcio-bot
Lega: https://leghe.fantacalcio.it/lega-paralimpica-seregno

Questo script automatizza l'inserimento della formazione su leghe.fantacalcio.it
Viene eseguito automaticamente da GitHub Actions ogni martedì e giovedì alle 13:00
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurazione logging
logging.basicConfig(
    filename='fantacalcio_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FantacalcioBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configura il browser Chrome in modalità headless per ambiente cloud"""
        logging.info("Configurazione browser Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Per ambienti cloud Linux
        chrome_options.binary_location = os.environ.get('CHROME_BIN', '/usr/bin/google-chrome')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
        logging.info("Browser configurato con successo")
        
    def login(self):
        """Effettua il login al sito"""
        try:
            logging.info("Inizio processo di login...")
            self.driver.get("https://leghe.fantacalcio.it/")
            time.sleep(3)
            
            # NOTA: QUESTI SELETTORI DEVONO ESSERE PERSONALIZZATI MARTEDÌ
            # Dopo l'ispezione del sito, aggiorna questi selettori con quelli corretti
            
            # Cerca il pulsante/link di login
            logging.info("Ricerca pulsante login...")
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login') or contains(@href, 'login')]"))
            )
            login_btn.click()
            time.sleep(2)
            
            # Inserisci username/email
            logging.info("Inserimento username...")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
                # ⚠️ CAMBIA "username" con l'ID corretto trovato martedì
                # Possibili alternative: By.ID, "email" oppure By.NAME, "user_email"
            )
            username_field.clear()
            username_field.send_keys(self.username)
            
            # Inserisci password
            logging.info("Inserimento password...")
            password_field = self.driver.find_element(By.ID, "password")
            # ⚠️ CAMBIA "password" con l'ID corretto trovato martedì
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Clicca su accedi
            logging.info("Click su pulsante accedi...")
            submit_btn = self.driver.find_element(
                By.XPATH, 
                "//button[@type='submit' or contains(text(), 'Accedi') or contains(text(), 'Login')]"
            )
            submit_btn.click()
            time.sleep(5)
            
            logging.info("Login completato con successo")
            return True
            
        except Exception as e:
            logging.error(f"Errore durante il login: {str(e)}")
            self.driver.save_screenshot(f"errore_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def vai_alla_lega(self):
        """Naviga alla lega specifica"""
        try:
            logging.info("Navigazione alla lega...")
            self.driver.get("https://leghe.fantacalcio.it/lega-paralimpica-seregno")
            time.sleep(3)
            logging.info("Lega caricata con successo")
            return True
        except Exception as e:
            logging.error(f"Errore nell'accesso alla lega: {str(e)}")
            self.driver.save_screenshot(f"errore_lega_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def inserisci_formazione(self, formazione):
        """
        Inserisce la formazione predefinita
        
        Args:
            formazione (dict): Dizionario con la formazione da inserire
        """
        try:
            logging.info("Inizio inserimento formazione...")
            
            # ⚠️ QUESTO È IL PUNTO PIÙ IMPORTANTE DA PERSONALIZZARE MARTEDÌ
            # Dopo aver ispezionato il sito, dovrai aggiornare questi selettori
            
            # Cerca il pulsante "Formazione" o "Inserisci Formazione"
            logging.info("Ricerca sezione formazione...")
            formazione_btn = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//a[contains(text(), 'Formazione') or contains(@href, 'formazione')]"
                ))
            )
            formazione_btn.click()
            time.sleep(3)
            
            # ESEMPIO DI LOGICA PER INSERIRE GIOCATORI
            # ⚠️ QUESTA PARTE VA COMPLETAMENTE RISCRITTA IN BASE ALLA STRUTTURA DEL SITO
            
            logging.info("Inserimento giocatori...")
            
            # Esempio: se i giocatori si inseriscono in campi input
            titolari = formazione.get('titolari', {})
            
            # Portiere
            if 'portiere' in titolari:
                logging.info(f"Inserimento portiere: {titolari['portiere']}")
                # ⚠️ Sostituisci con il selettore corretto
                # campo_portiere = self.driver.find_element(By.ID, "portiere_1")
                # campo_portiere.send_keys(titolari['portiere'])
            
            # Difensori
            if 'difensori' in titolari:
                for i, difensore in enumerate(titolari['difensori']):
                    logging.info(f"Inserimento difensore {i+1}: {difensore}")
                    # ⚠️ Sostituisci con il selettore corretto
                    # campo = self.driver.find_element(By.ID, f"difensore_{i+1}")
                    # campo.send_keys(difensore)
            
            # Centrocampisti
            if 'centrocampisti' in titolari:
                for i, centro in enumerate(titolari['centrocampisti']):
                    logging.info(f"Inserimento centrocampista {i+1}: {centro}")
                    # ⚠️ Sostituisci con il selettore corretto
            
            # Attaccanti
            if 'attaccanti' in titolari:
                for i, attaccante in enumerate(titolari['attaccanti']):
                    logging.info(f"Inserimento attaccante {i+1}: {attaccante}")
                    # ⚠️ Sostituisci con il selettore corretto
            
            time.sleep(2)
            
            # Salva la formazione
            logging.info("Salvataggio formazione...")
            salva_btn = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//button[contains(text(), 'Salva') or contains(text(), 'Conferma')]"
                ))
            )
            salva_btn.click()
            time.sleep(3)
            
            logging.info("✅ Formazione inserita con successo!")
            return True
            
        except Exception as e:
            logging.error(f"Errore nell'inserimento della formazione: {str(e)}")
            self.driver.save_screenshot(f"errore_formazione_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def invia_notifica_email(self, successo, dettagli=""):
        """Invia una email di notifica con il risultato"""
        try:
            mittente = os.environ.get('GMAIL_ADDRESS')
            password = os.environ.get('GMAIL_APP_PASSWORD')
            destinatario = 'saladaniele99@gmail.com'
            
            if not mittente or not password:
                logging.warning("Credenziali email non configurate, notifica saltata")
                return False
            
            msg = MIMEMultipart('alternative')
            timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            if successo:
                msg['Subject'] = "✅ Fantacalcio Bot - Formazione inserita!"
                corpo = f"""
                ✅ FORMAZIONE INSERITA CON SUCCESSO!
                
                Data e ora: {timestamp}
                Lega: Lega Paralimpica Seregno
                
                La tua formazione è stata inserita automaticamente.
                
                {dettagli}
                
                ---
                🤖 Fantacalcio Bot Automatico
                """
            else:
                msg['Subject'] = "❌ ERRORE Fantacalcio Bot - Formazione NON inserita!"
                corpo = f"""
                ❌ ERRORE NELL'INSERIMENTO FORMAZIONE!
                
                Data e ora: {timestamp}
                Lega: Lega Paralimpica Seregno
                
                Si è verificato un errore durante l'inserimento automatico.
                
                Dettagli: {dettagli}
                
                ⚠️ AZIONE RICHIESTA: Inserisci manualmente la formazione su:
                https://leghe.fantacalcio.it/lega-paralimpica-seregno
                
                ---
                🤖 Fantacalcio Bot Automatico
                """
            
            msg['From'] = mittente
            msg['To'] = destinatario
            msg.attach(MIMEText(corpo, 'plain'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(mittente, password)
                server.send_message(msg)
            
            logging.info(f"✉️ Email di notifica inviata a {destinatario}")
            return True
            
        except Exception as e:
            logging.error(f"Errore nell'invio email: {str(e)}")
            return False
    
    def esegui(self, formazione):
        """Esegue l'intero processo"""
        dettagli_errore = ""
        
        try:
            self.setup_driver()
            
            if not self.login():
                raise Exception("Login fallito")
            
            if not self.vai_alla_lega():
                raise Exception("Impossibile accedere alla lega")
            
            if not self.inserisci_formazione(formazione):
                raise Exception("Impossibile inserire la formazione")
            
            logging.info("✅ Processo completato con successo!")
            self.invia_notifica_email(True, "Tutti i giocatori inseriti correttamente.")
            return True
            
        except Exception as e:
            dettagli_errore = str(e)
            logging.error(f"❌ Errore generale: {dettagli_errore}")
            self.invia_notifica_email(False, f"Errore: {dettagli_errore}\n\nControlla i log su GitHub Actions.")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Browser chiuso")


def carica_formazione():
    """Carica la formazione dal file JSON"""
    try:
        with open('formazione.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("File formazione.json non trovato, uso formazione default")
        return {
            'titolari': {
                'portiere': 'Portiere Default',
                'difensori': ['Difensore1', 'Difensore2', 'Difensore3'],
                'centrocampisti': ['Centro1', 'Centro2', 'Centro3', 'Centro4'],
                'attaccanti': ['Attaccante1', 'Attaccante2', 'Attaccante3']
            }
        }


# ESECUZIONE PRINCIPALE
if __name__ == "__main__":
    print("🤖 Fantacalcio Bot - Avvio in corso...")
    print(f"⏰ Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Leggi credenziali da variabili d'ambiente (GitHub Secrets)
    username = os.environ.get('FANTACALCIO_USERNAME')
    password = os.environ.get('FANTACALCIO_PASSWORD')
    
    if not username or not password:
        print("❌ ERRORE: Credenziali non configurate!")
        print("Configura FANTACALCIO_USERNAME e FANTACALCIO_PASSWORD nei GitHub Secrets")
        exit(1)
    
    # Carica la formazione
    formazione = carica_formazione()
    print(f"📋 Formazione caricata: {formazione.get('modulo', 'N/A')}")
    
    # Esegui il bot
    bot = FantacalcioBot(username, password)
    successo = bot.esegui(formazione)
    
    if successo:
        print("✅ Operazione completata con successo!")
        exit(0)
    else:
        print("❌ Operazione fallita. Controlla i log.")
        exit(1)