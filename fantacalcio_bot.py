"""
Fantacalcio Bot - Salvataggio Automatico Formazione
VERSIONE ROBUSTA con gestione notifiche e fallback multipli

Repository: https://github.com/tuousername/fantacalcio-bot
Lega: https://leghe.fantacalcio.it/lega-paralimpica-seregno
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os
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
        logging.info("=" * 60)
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
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Per ambienti cloud Linux
        chrome_options.binary_location = os.environ.get('CHROME_BIN', '/usr/bin/google-chrome')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
        logging.info("✅ Browser configurato con successo")
    
    def chiudi_popup_cookie(self):
        """Chiude il popup dei cookie se presente"""
        try:
            logging.info("Controllo presenza popup cookie...")
            wait_popup = WebDriverWait(self.driver, 8)
            
            try:
                cookie_btn = wait_popup.until(
                    EC.element_to_be_clickable((By.ID, "pt-accept-all"))
                )
                cookie_btn.click()
                logging.info("✅ Popup cookie chiuso (Accept all)")
                time.sleep(2)
                return True
            except TimeoutException:
                logging.info("ℹ️ Popup cookie non trovato (già chiuso o non presente)")
                return False
                
        except Exception as e:
            logging.info(f"ℹ️ Gestione popup cookie: {str(e)}")
            return False
    
    def chiudi_banner_pubblicitario(self):
        """Chiude il banner pubblicitario se presente"""
        try:
            logging.info("Controllo presenza banner pubblicitario...")
            wait_banner = WebDriverWait(self.driver, 5)
            
            try:
                close_btn = wait_banner.until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//button[.//svg[@viewBox='0 0 48 48'] and .//path[contains(@d, 'M38 12.83')]]"
                    ))
                )
                close_btn.click()
                logging.info("✅ Banner pubblicitario chiuso")
                time.sleep(2)
                return True
            except TimeoutException:
                try:
                    close_btn = wait_banner.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[contains(@aria-label, 'Close') or contains(@title, 'Close')]"
                        ))
                    )
                    close_btn.click()
                    logging.info("✅ Banner pubblicitario chiuso (metodo alternativo)")
                    time.sleep(2)
                    return True
                except:
                    logging.info("ℹ️ Banner pubblicitario non trovato")
                    return False
                    
        except Exception as e:
            logging.info(f"ℹ️ Gestione banner pubblicitario: {str(e)}")
            return False
    
    def login(self):
        """Effettua il login al sito"""
        try:
            logging.info("=" * 60)
            logging.info("STEP 1: LOGIN")
            logging.info("=" * 60)
            
            # Vai alla pagina della lega
            logging.info("Navigazione a: https://leghe.fantacalcio.it/lega-paralimpica-seregno")
            self.driver.get("https://leghe.fantacalcio.it/lega-paralimpica-seregno")
            time.sleep(4)
            
            # Chiudi popup cookie
            self.chiudi_popup_cookie()
            
            # Click "Accedi"
            logging.info("Ricerca pulsante 'Accedi'...")
            accedi_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='https://leghe.fantacalcio.it/login' and contains(@class, 'btn-primary')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", accedi_btn)
            time.sleep(1)
            accedi_btn.click()
            logging.info("✅ Click su 'Accedi' effettuato")
            time.sleep(4)
            
            # Chiudi banner pubblicitario
            self.chiudi_banner_pubblicitario()
            
            # Inserisci username
            logging.info(f"Inserimento username: {self.username}")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='username']"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            logging.info("✅ Username inserito")
            time.sleep(1)
            
            # Inserisci password
            logging.info("Inserimento password...")
            password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='password']"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            logging.info("✅ Password inserita")
            time.sleep(1)
            
            # Click LOGIN
            logging.info("Click su pulsante LOGIN...")
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary') and .//span[text()='LOGIN']]"))
            )
            login_btn.click()
            logging.info("✅ Click su LOGIN effettuato")
            time.sleep(5)
            
            logging.info("✅✅ LOGIN COMPLETATO CON SUCCESSO")
            return True
            
        except Exception as e:
            logging.error(f"❌ ERRORE durante il login: {str(e)}")
            self.driver.save_screenshot(f"errore_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def naviga_alla_lega(self):
        """Naviga alla lega specifica dopo il login - VERSIONE ROBUSTA"""
        try:
            logging.info("=" * 60)
            logging.info("STEP 2: NAVIGAZIONE ALLA LEGA (ROBUSTA)")
            logging.info("=" * 60)
            
            # STEP 2.1: Click su "S-Cup Ella League"
            logging.info("Ricerca categoria 'S-Cup Ella League'...")
            categoria_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='league-name' and text()='S-Cup Ella league']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", categoria_btn)
            time.sleep(1)
            categoria_btn.click()
            logging.info("✅ Click su 'S-Cup Ella League' effettuato")
            time.sleep(3)
            
            # STEP 2.2: Click su "Lega Paralimpica Seregno" - CON FALLBACK MULTIPLI
            logging.info("Ricerca lega 'Lega Paralimpica Seregno' (con fallback per notifiche)...")
            
            lega_link = None
            metodo_usato = ""
            
            # METODO 1: Cerca per data-id (il più specifico, ignora notifiche)
            try:
                logging.info("  → Tentativo 1: Ricerca per data-id='3012920'...")
                lega_link = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@data-id='3012920']"))
                )
                metodo_usato = "data-id"
                logging.info("  ✅ Trovato con data-id")
            except TimeoutException:
                logging.info("  ⚠️ Non trovato con data-id, provo metodo alternativo...")
            
            # METODO 2: Cerca per href della lega (ignora classi e attributi aggiuntivi)
            if not lega_link:
                try:
                    logging.info("  → Tentativo 2: Ricerca per href contenente 'lega-paralimpica-seregno'...")
                    lega_link = WebDriverWait(self.driver, 8).until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//a[contains(@href, 'lega-paralimpica-seregno')]"
                        ))
                    )
                    metodo_usato = "href"
                    logging.info("  ✅ Trovato con href")
                except TimeoutException:
                    logging.info("  ⚠️ Non trovato con href, provo ricerca testuale...")
            
            # METODO 3: Cerca per testo "Lega Paralimpica Seregno" (il più robusto)
            if not lega_link:
                try:
                    logging.info("  → Tentativo 3: Ricerca per testo 'Lega Paralimpica Seregno'...")
                    lega_link = WebDriverWait(self.driver, 8).until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//a[contains(., 'Lega Paralimpica Seregno')]"
                        ))
                    )
                    metodo_usato = "testo"
                    logging.info("  ✅ Trovato con ricerca testuale")
                except TimeoutException:
                    logging.info("  ⚠️ Non trovato con ricerca testuale, provo JavaScript...")
            
            # METODO 4: JavaScript fallback - trova tutti i link e cerca per testo
            if not lega_link:
                try:
                    logging.info("  → Tentativo 4: Ricerca con JavaScript...")
                    links = self.driver.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        if "lega-paralimpica-seregno" in link.get_attribute("href") or \
                           "Lega Paralimpica Seregno" in link.text:
                            lega_link = link
                            metodo_usato = "javascript"
                            logging.info("  ✅ Trovato con JavaScript")
                            break
                except Exception as e:
                    logging.warning(f"  ⚠️ Errore con JavaScript: {str(e)}")
            
            # Se ancora non trovato, genera errore
            if not lega_link:
                raise Exception("Impossibile trovare il link della lega con nessun metodo")
            
            # Click sul link trovato
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lega_link)
            time.sleep(1)
            
            # Prova prima con click standard, poi con JavaScript se fallisce
            try:
                lega_link.click()
                logging.info(f"✅ Click su 'Lega Paralimpica Seregno' effettuato (metodo: {metodo_usato})")
            except Exception as e:
                logging.info(f"  ⚠️ Click standard fallito, provo con JavaScript...")
                self.driver.execute_script("arguments[0].click();", lega_link)
                logging.info(f"✅ Click JavaScript su 'Lega Paralimpica Seregno' effettuato (metodo: {metodo_usato})")
            
            time.sleep(4)
            
            logging.info("✅✅ NAVIGAZIONE ALLA LEGA COMPLETATA")
            return True
            
        except Exception as e:
            logging.error(f"❌ ERRORE nella navigazione alla lega: {str(e)}")
            self.driver.save_screenshot(f"errore_navigazione_lega_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            # Log aggiuntivi per debug
            try:
                logging.info("DEBUG: URL corrente: " + self.driver.current_url)
                logging.info("DEBUG: Salvando HTML della pagina per analisi...")
                with open(f"debug_pagina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
            except:
                pass
            
            return False
    
    def salva_formazione(self):
        """Salva la formazione attuale per tutte le competizioni"""
        try:
            logging.info("=" * 60)
            logging.info("STEP 3: SALVATAGGIO FORMAZIONE")
            logging.info("=" * 60)
            
            # STEP 3.1: Click su "Schiera Formazione"
            logging.info("Ricerca link 'Schiera Formazione'...")
            inserisci_formazione_link = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//a[@class='shortcut' and @href='https://leghe.fantacalcio.it/lega-paralimpica-seregno/area-gioco/inserisci-formazione']"
                ))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", inserisci_formazione_link)
            time.sleep(1)
            inserisci_formazione_link.click()
            logging.info("✅ Click su 'Schiera Formazione' effettuato")
            time.sleep(4)
            
            # STEP 3.2: Click su "Salva per tutte le competizioni"
            logging.info("Ricerca pulsante 'Salva per tutte le competizioni'...")
            salva_btn = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'btn-orange') and contains(@onclick, 'saveFormationForAllComps')]"
                ))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", salva_btn)
            time.sleep(1)
            salva_btn.click()
            logging.info("✅ Click su 'Salva per tutte le competizioni' effettuato")
            time.sleep(4)
            
            logging.info("✅✅ FORMAZIONE SALVATA CON SUCCESSO!")
            return True
            
        except Exception as e:
            logging.error(f"❌ ERRORE nel salvataggio della formazione: {str(e)}")
            self.driver.save_screenshot(f"errore_formazione_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def invia_notifica_email(self, successo, dettagli=""):
        """Invia una email di notifica con il risultato"""
        try:
            mittente = os.environ.get('GMAIL_ADDRESS')
            password = os.environ.get('GMAIL_APP_PASSWORD')
            destinatari = ['saladaniele99@gmail.com', 'davidebanini99@gmail.com']
            
            if not mittente or not password:
                logging.warning("⚠️ Credenziali email non configurate, notifica saltata")
                return False
            
            msg = MIMEMultipart('alternative')
            timestamp = datetime.now().strftime('%d/%m/%Y alle %H:%M:%S')
            
            if successo:
                msg['Subject'] = "✅ Fantacalcio Bot - Formazione Salvata!"
                testo = f"""
✅ FORMAZIONE SALVATA CON SUCCESSO!

📅 Data e ora: {timestamp}
🏆 Lega: Lega Paralimpica Seregno
👤 Username: saladany99

La formazione attuale è stata salvata automaticamente per tutte le competizioni.

✅ Titolari: mantenuti come configurato
✅ Panchina: mantenuta come configurata
✅ Nessuna modifica apportata

Non è necessaria alcuna azione da parte tua.
Buona fortuna! ⚽

---
🤖 Messaggio automatico dal Fantacalcio Bot
                """
            else:
                msg['Subject'] = "❌ URGENTE - Fantacalcio Bot: Formazione NON salvata!"
                testo = f"""
❌ ERRORE NEL SALVATAGGIO FORMAZIONE!

📅 Data e ora: {timestamp}
🏆 Lega: Lega Paralimpica Seregno
👤 Username: saladany99

⚠️ ERRORE:
{dettagli}

🚨 AZIONE RICHIESTA:
Inserisci/Salva MANUALMENTE la formazione prima dell'inizio delle partite!

👉 Vai su: https://leghe.fantacalcio.it/lega-paralimpica-seregno/area-gioco/inserisci-formazione

---
🤖 Messaggio automatico dal Fantacalcio Bot
                """
            
            msg['From'] = mittente
            msg['To'] = ', '.join(destinatari)
            msg.attach(MIMEText(testo, 'plain'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(mittente, password)
                server.send_message(msg)
            
            logging.info(f"✉️ Email di notifica inviata a {', '.join(destinatari)}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Errore nell'invio email: {str(e)}")
            return False
    
    def esegui(self):
        """Esegue l'intero processo"""
        dettagli_errore = ""
        
        try:
            self.setup_driver()
            
            if not self.login():
                raise Exception("Login fallito - Controlla log e screenshot")
            
            if not self.naviga_alla_lega():
                raise Exception("Navigazione alla lega fallita - Controlla log e screenshot")
            
            if not self.salva_formazione():
                raise Exception("Impossibile salvare la formazione - Controlla screenshot")
            
            logging.info("=" * 60)
            logging.info("✅✅✅ PROCESSO COMPLETATO CON SUCCESSO! ✅✅✅")
            logging.info("=" * 60)
            self.invia_notifica_email(True, "Formazione salvata correttamente senza modifiche.")
            return True
            
        except Exception as e:
            dettagli_errore = str(e)
            logging.error("=" * 60)
            logging.error(f"❌❌❌ PROCESSO FALLITO: {dettagli_errore}")
            logging.error("=" * 60)
            self.invia_notifica_email(False, f"Errore: {dettagli_errore}\n\nControlla i log e screenshot su GitHub Actions.")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Browser chiuso")


# ESECUZIONE PRINCIPALE
if __name__ == "__main__":
    print("=" * 70)
    print("🤖  FANTACALCIO BOT - Salvataggio Automatico Formazione")
    print("=" * 70)
    print(f"⏰  Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🏆  Lega: Lega Paralimpica Seregno")
    print(f"📧  Email notifiche: saladaniele99@gmail.com")
    print("=" * 70)
    print()
    
    username = os.environ.get('FANTACALCIO_USERNAME')
    password = os.environ.get('FANTACALCIO_PASSWORD')
    
    if not username or not password:
        print("❌ ERRORE: Credenziali non configurate!")
        print("Configura FANTACALCIO_USERNAME e FANTACALCIO_PASSWORD nei GitHub Secrets")
        exit(1)
    
    print(f"👤  Username: {username}")
    print(f"🔒  Password: {'*' * len(password)}")
    print()
    print("🚀  Avvio bot...")
    print("💡  Modalità: Salvataggio formazione attuale (senza modifiche)")
    print()
    
    bot = FantacalcioBot(username, password)
    successo = bot.esegui()
    
    print()
    print("=" * 70)
    if successo:
        print("✅  OPERAZIONE COMPLETATA CON SUCCESSO!")
        print("📧  Controlla saladaniele99@gmail.com per la conferma")
        print("🏆  Formazione salvata per tutte le competizioni")
        exit(0)
    else:
        print("❌  OPERAZIONE FALLITA")
        print("📄  Controlla fantacalcio_log.txt per i dettagli")
        print("📧  Dovresti aver ricevuto una email di notifica errore")
        print("🔍  Screenshot salvato in errore_*.png")
        exit(1)
