"""
Fantacalcio Bot - Salvataggio Automatico Formazione
VERSIONE ROBUSTA v3.0

Novità v3.0:
- Retry automatico (1 tentativo iniziale + 3 retry con attesa 30/60/120s)
- trova_elemento() con lista di selettori e fallback progressivo
- click_sicuro() con gestione ElementClickInterceptedException e fallback JS
- chiudi_tutti_popup() unificata (cookie, ads, overlay, ESC)
- Verifica conferma salvataggio con stato "incerto"
- Navigazione diretta come fallback se step-by-step fallisce
- aspetta_pagina_caricata() con WebDriverWait su readyState
- Screenshot diagnostici ad ogni step con timestamp
- HTML dump in caso di errore
- Logging su file (DEBUG) e console (INFO)
- Email differenziata per successo / incerto / fallito
"""

import os
import time
import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)

# ─────────────────────────── LOGGING ─────────────────────────────────────────

LOG_FILE = "fantacalcio_log.txt"

logger = logging.getLogger("fantacalcio")
logger.setLevel(logging.DEBUG)

_fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
_fh.setLevel(logging.DEBUG)
_fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s"))

_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s"))

logger.addHandler(_fh)
logger.addHandler(_ch)

# ─────────────────────────── COSTANTI ────────────────────────────────────────

LEGA_URL = "https://leghe.fantacalcio.it/lega-paralimpica-seregno"
FORMAZIONE_URL = f"{LEGA_URL}/area-gioco/inserisci-formazione"

MAX_RETRIES = 3
RETRY_DELAYS = [30, 60, 120]   # secondi tra i tentativi

DEFAULT_TIMEOUT = 20           # WebDriverWait standard
SHORT_TIMEOUT = 5              # per elementi opzionali (popup)


# ─────────────────────────── UTILITY ─────────────────────────────────────────

def _ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def salva_screenshot(driver, nome: str) -> str:
    filename = f"screenshot_{nome}_{_ts()}.png"
    try:
        driver.save_screenshot(filename)
        logger.debug(f"Screenshot: {filename}")
    except Exception as exc:
        logger.debug(f"Screenshot fallito ({filename}): {exc}")
    return filename


def salva_html(driver, nome: str) -> str:
    filename = f"debug_{nome}_{_ts()}.html"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.debug(f"HTML salvato: {filename}")
    except Exception as exc:
        logger.debug(f"HTML dump fallito ({filename}): {exc}")
    return filename


def aspetta_pagina_caricata(driver, timeout: int = DEFAULT_TIMEOUT):
    """Aspetta document.readyState == 'complete'."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.debug("Pagina caricata (readyState=complete)")
    except TimeoutException:
        logger.warning("Timeout aspettando readyState=complete, continuo comunque")


def trova_elemento(driver, selettori: list, timeout: int = DEFAULT_TIMEOUT):
    """
    Prova ogni (By, valore) in selettori finché uno restituisce un elemento
    visibile. Lancia NoSuchElementException se nessuno funziona.
    """
    for by, value in selettori:
        try:
            elem = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logger.debug(f"Elemento trovato: ({by}, {value!r})")
            return elem
        except TimeoutException:
            logger.debug(f"Selettore non trovato: ({by}, {value!r})")
    raise NoSuchElementException(f"Nessun selettore ha trovato l'elemento. Provati: {selettori}")


def trova_elemento_cliccabile(driver, selettori: list, timeout: int = DEFAULT_TIMEOUT):
    """Come trova_elemento ma aspetta element_to_be_clickable."""
    for by, value in selettori:
        try:
            elem = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            logger.debug(f"Elemento cliccabile trovato: ({by}, {value!r})")
            return elem
        except TimeoutException:
            logger.debug(f"Selettore cliccabile non trovato: ({by}, {value!r})")
    raise NoSuchElementException(
        f"Nessun selettore cliccabile. Provati: {selettori}"
    )


def click_sicuro(driver, elemento, max_retry: int = 3):
    """
    Scrolla l'elemento al centro, prova click standard.
    Se riceve ElementClickInterceptedException chiude popup e riprova.
    Fallback finale: click via JavaScript.
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
    time.sleep(0.5)

    for attempt in range(1, max_retry + 1):
        try:
            elemento.click()
            logger.debug(f"Click OK (tentativo {attempt})")
            return
        except ElementClickInterceptedException:
            logger.debug(f"ElementClickIntercepted (tentativo {attempt}), chiudo popup...")
            chiudi_tutti_popup(driver)
            time.sleep(1)
        except Exception as exc:
            logger.debug(f"Click fallito (tentativo {attempt}): {exc}")
            time.sleep(1)

    logger.debug("Fallback: click JavaScript")
    driver.execute_script("arguments[0].click();", elemento)


def chiudi_tutti_popup(driver) -> int:
    """
    Gestisce: cookie banner, popup ads (Close/×/X), overlay/backdrop, ESC.
    Ritorna il numero di popup chiusi.
    """
    chiusi = 0

    # ── Cookie banner ──────────────────────────────────────────────────────
    for by, value in [
        (By.ID, "pt-accept-all"),
        (By.XPATH, "//button[contains(text(),'Accetta tutto') or contains(text(),'Accept all')]"),
        (By.XPATH, "//button[normalize-space(text())='Accetta' or normalize-space(text())='Accept']"),
    ]:
        try:
            btn = WebDriverWait(driver, SHORT_TIMEOUT).until(
                EC.element_to_be_clickable((by, value))
            )
            btn.click()
            logger.debug(f"Cookie banner chiuso ({value!r})")
            chiusi += 1
            time.sleep(1)
            break
        except TimeoutException:
            pass

    # ── Popup ads / bottoni Close ──────────────────────────────────────────
    close_selectors = [
        (By.XPATH, "//button[@aria-label='Close' or @aria-label='close']"),
        (By.XPATH, "//button[@title='Close' or @title='close']"),
        (By.XPATH, "//button[normalize-space(text())='×' or normalize-space(text())='X']"),
        (By.XPATH, "//div[contains(@class,'modal') or contains(@class,'dialog')]//button[contains(@class,'close')]"),
        (By.XPATH, "//button[contains(@class,'close') and not(contains(@class,'modal-close'))]"),
        (By.XPATH, "//button[contains(text(),'Chiudi') or contains(text(),'Close')]"),
    ]
    for by, value in close_selectors:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, value)))
            btn.click()
            logger.debug(f"Popup/ad chiuso ({value!r})")
            chiusi += 1
            time.sleep(1)
            break
        except TimeoutException:
            pass

    # ── Overlay / backdrop ─────────────────────────────────────────────────
    try:
        overlay = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'overlay') or contains(@class,'backdrop') "
                "or contains(@class,'modal-backdrop')]",
            ))
        )
        overlay.click()
        logger.debug("Overlay/backdrop cliccato")
        chiusi += 1
        time.sleep(1)
    except TimeoutException:
        pass

    # ── ESC fallback ───────────────────────────────────────────────────────
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        logger.debug("Tasto ESC inviato")
        time.sleep(0.5)
    except Exception:
        pass

    if chiusi:
        logger.info(f"Popup chiusi: {chiusi}")
    return chiusi


# ─────────────────────────── CHROME SETUP ────────────────────────────────────

def crea_driver() -> webdriver.Chrome:
    logger.info("Configurazione browser Chrome...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")

    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    logger.info("Browser Chrome configurato")
    return driver


# ─────────────────────────── STEP: LOGIN ─────────────────────────────────────

def step_login(driver, username: str, password: str) -> None:
    logger.info("=" * 60)
    logger.info("STEP 1: LOGIN")
    logger.info("=" * 60)

    logger.info(f"Navigazione a {LEGA_URL}")
    driver.get(LEGA_URL)
    aspetta_pagina_caricata(driver)
    time.sleep(2)
    salva_screenshot(driver, "01_homepage")

    chiudi_tutti_popup(driver)

    # Pulsante "Accedi"
    logger.info("Ricerca pulsante Accedi...")
    accedi_btn = trova_elemento_cliccabile(driver, [
        (By.XPATH, "//a[@href='https://leghe.fantacalcio.it/login' and contains(@class,'btn-primary')]"),
        (By.XPATH, "//a[contains(@href,'/login') and contains(@class,'btn')]"),
        (By.XPATH, "//a[contains(text(),'Accedi') or contains(text(),'Login')]"),
        (By.CSS_SELECTOR, "a.btn-primary[href*='login']"),
        (By.LINK_TEXT, "Accedi"),
    ])
    click_sicuro(driver, accedi_btn)
    logger.info("Click su Accedi")
    aspetta_pagina_caricata(driver)
    time.sleep(2)
    salva_screenshot(driver, "02_pagina_login")

    chiudi_tutti_popup(driver)

    # Username
    logger.info(f"Inserimento username: {username}")
    username_field = trova_elemento(driver, [
        (By.CSS_SELECTOR, "input[formcontrolname='username']"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.XPATH, "//input[@type='text' and (@placeholder='Username' or @placeholder='Email')]"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ])
    username_field.clear()
    username_field.send_keys(username)

    # Password
    logger.info("Inserimento password...")
    password_field = trova_elemento(driver, [
        (By.CSS_SELECTOR, "input[formcontrolname='password']"),
        (By.CSS_SELECTOR, "input[name='password']"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.XPATH, "//input[@type='password']"),
    ])
    password_field.clear()
    password_field.send_keys(password)
    time.sleep(1)

    # Pulsante LOGIN
    logger.info("Click su pulsante LOGIN...")
    login_btn = trova_elemento_cliccabile(driver, [
        (By.XPATH, "//button[contains(@class,'ant-btn-primary') and .//span[text()='LOGIN']]"),
        (By.XPATH, "//button[@type='submit' and contains(@class,'btn-primary')]"),
        (By.XPATH, "//button[contains(text(),'LOGIN') or contains(text(),'Login') or contains(text(),'Accedi')]"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[@type='submit']"),
    ])
    click_sicuro(driver, login_btn)
    logger.info("Click su LOGIN")
    aspetta_pagina_caricata(driver)
    time.sleep(3)
    salva_screenshot(driver, "03_dopo_login")

    chiudi_tutti_popup(driver)

    current_url = driver.current_url
    if "login" in current_url:
        raise Exception(f"Login fallito: ancora sulla pagina di login ({current_url})")
    logger.info(f"Login completato. URL corrente: {current_url}")


# ─────────────────────────── STEP: NAVIGA LEGA ───────────────────────────────

def step_naviga_alla_lega(driver) -> None:
    logger.info("=" * 60)
    logger.info("STEP 2: NAVIGAZIONE ALLA LEGA")
    logger.info("=" * 60)

    chiudi_tutti_popup(driver)

    # Categoria "S-Cup Ella League"
    logger.info("Ricerca categoria S-Cup Ella League...")
    categoria = trova_elemento_cliccabile(driver, [
        (By.XPATH, "//span[@class='league-name' and text()='S-Cup Ella league']"),
        (By.XPATH, "//span[contains(@class,'league-name') and contains(text(),'S-Cup')]"),
        (By.XPATH, "//span[contains(text(),'S-Cup Ella')]"),
    ])
    click_sicuro(driver, categoria)
    logger.info("Click su S-Cup Ella League")
    time.sleep(2)
    salva_screenshot(driver, "04_categoria")

    chiudi_tutti_popup(driver)

    # Link "Lega Paralimpica Seregno"
    logger.info("Ricerca Lega Paralimpica Seregno...")
    lega_link = trova_elemento_cliccabile(driver, [
        (By.XPATH, "//a[@data-id='3012920']"),
        (By.XPATH, "//a[contains(@href,'lega-paralimpica-seregno')]"),
        (By.XPATH, "//a[contains(.,'Lega Paralimpica Seregno')]"),
        (By.LINK_TEXT, "Lega Paralimpica Seregno"),
    ])
    click_sicuro(driver, lega_link)
    logger.info("Click su Lega Paralimpica Seregno")
    aspetta_pagina_caricata(driver)
    time.sleep(3)
    salva_screenshot(driver, "05_lega")

    chiudi_tutti_popup(driver)
    logger.info("Navigazione alla lega completata")


# ─────────────────────────── STEP: SALVA FORMAZIONE ──────────────────────────

_SALVA_SELETTORI = [
    (By.XPATH, "//button[contains(@class,'btn-orange') and contains(@onclick,'saveFormationForAllComps')]"),
    (By.XPATH, "//button[contains(text(),'Salva') and contains(text(),'competizioni')]"),
    (By.XPATH, "//button[contains(text(),'Salva') and contains(text(),'Competizioni')]"),
    (By.XPATH, "//button[contains(@onclick,'saveFormation') or contains(@onclick,'SaveFormation')]"),
    (By.XPATH, "//button[contains(@class,'btn') and contains(text(),'Salva')]"),
]

_CONFERMA_KEYWORDS = ["salvata", "successo", "confermata", "success", "saved"]


def _verifica_conferma(driver) -> bool:
    """Aspetta fino a 10s per trovare un segnale di conferma nella pagina."""
    try:
        WebDriverWait(driver, 10).until(
            lambda d: any(kw in d.page_source.lower() for kw in _CONFERMA_KEYWORDS)
        )
        logger.info("Conferma salvataggio trovata (keyword nel sorgente)")
        return True
    except TimeoutException:
        pass

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(@class,'toast') or contains(@class,'alert') "
                "or contains(@class,'notification') or contains(@class,'snack')]",
            ))
        )
        logger.info("Conferma salvataggio trovata (toast/alert)")
        return True
    except TimeoutException:
        pass

    return False


def _clicca_salva(driver, prefisso_screenshot: str) -> str:
    """
    Trova e clicca il pulsante Salva, poi verifica la conferma.
    Ritorna "successo" o "incerto".
    """
    # Chiudi popup in 3 round prima di cercare il pulsante
    for _ in range(3):
        chiudi_tutti_popup(driver)
        time.sleep(1)

    salva_screenshot(driver, f"{prefisso_screenshot}_pre_salvataggio")

    logger.info("Ricerca pulsante Salva per tutte le competizioni...")
    salva_btn = trova_elemento_cliccabile(driver, _SALVA_SELETTORI)
    click_sicuro(driver, salva_btn)
    logger.info("Click su Salva per tutte le competizioni")

    conferma = _verifica_conferma(driver)
    time.sleep(2)
    salva_screenshot(driver, f"{prefisso_screenshot}_post_salvataggio")

    if conferma:
        return "successo"

    logger.warning("Nessuna conferma trovata dopo il salvataggio")
    salva_html(driver, f"{prefisso_screenshot}_incerto")
    return "incerto"


def step_salva_formazione(driver) -> str:
    """
    Tenta salvataggio via step-by-step (click Schiera Formazione),
    con fallback a navigazione diretta all'URL formazione.
    Ritorna "successo" o "incerto", oppure lancia eccezione.
    """
    logger.info("=" * 60)
    logger.info("STEP 3: SALVATAGGIO FORMAZIONE")
    logger.info("=" * 60)

    chiudi_tutti_popup(driver)

    # Tenta di cliccare "Schiera Formazione" dalla pagina lega
    navigazione_diretta = False
    try:
        logger.info("Ricerca link Schiera Formazione...")
        schiera_link = trova_elemento_cliccabile(driver, [
            (By.XPATH, "//a[@class='shortcut' and contains(@href,'inserisci-formazione')]"),
            (By.XPATH, "//a[contains(@href,'inserisci-formazione')]"),
            (By.XPATH, "//a[contains(text(),'Schiera') or contains(text(),'Formazione')]"),
            (By.LINK_TEXT, "Schiera Formazione"),
        ], timeout=15)
        click_sicuro(driver, schiera_link)
        logger.info("Click su Schiera Formazione")
        aspetta_pagina_caricata(driver)
        time.sleep(2)
    except NoSuchElementException:
        logger.warning("Link Schiera Formazione non trovato, uso navigazione diretta")
        navigazione_diretta = True

    if navigazione_diretta:
        logger.info(f"Navigazione diretta a {FORMAZIONE_URL}")
        driver.get(FORMAZIONE_URL)
        aspetta_pagina_caricata(driver)
        time.sleep(2)
        salva_screenshot(driver, "06_formazione_diretta")
        return _clicca_salva(driver, "07_diretto")

    salva_screenshot(driver, "06_pagina_formazione")
    return _clicca_salva(driver, "07")


# ─────────────────────────── EMAIL ───────────────────────────────────────────

def invia_email(stato: str, dettagli: str = "") -> bool:
    """
    Invia notifica email.
    stato: "successo" | "incerto" | "fallito"
    """
    mittente = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    destinatari = ["saladaniele99@gmail.com", "davidebanini99@gmail.com"]

    if not mittente or not app_password:
        logger.warning("Credenziali email non configurate, notifica saltata")
        return False

    timestamp = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
    link_manuale = FORMAZIONE_URL

    if stato == "successo":
        subject = "Fantacalcio Bot - Formazione Salvata!"
        body = f"""FORMAZIONE SALVATA CON SUCCESSO!

Data e ora: {timestamp}
Lega: Lega Paralimpica Seregno

Operazioni eseguite:
- Login effettuato correttamente
- Navigazione alla lega completata
- Click su "Salva per tutte le competizioni" effettuato
- Salvataggio confermato dal sito

Non e' necessaria alcuna azione da parte tua. Buona fortuna!

---
Fantacalcio Bot v3.0 (automatico)
"""
    elif stato == "incerto":
        subject = "Fantacalcio Bot - Salvataggio INCERTO (verifica consigliata)"
        body = f"""ATTENZIONE: SALVATAGGIO INCERTO

Data e ora: {timestamp}
Lega: Lega Paralimpica Seregno

Il bot ha cliccato "Salva per tutte le competizioni", ma non ha trovato
una conferma esplicita di salvataggio nella pagina.

E' opportuno verificare manualmente che la formazione sia salvata:
{link_manuale}

Se non risulta salvata, inseriscila prima dell'inizio delle partite.

{('Dettagli tecnici: ' + dettagli) if dettagli else ''}
---
Fantacalcio Bot v3.0 (automatico)
"""
    else:  # fallito
        subject = "URGENTE - Fantacalcio Bot: Formazione NON salvata!"
        body = f"""ERRORE NEL SALVATAGGIO FORMAZIONE!

Data e ora: {timestamp}
Lega: Lega Paralimpica Seregno

ERRORE (dopo {MAX_RETRIES + 1} tentativi):
{dettagli}

AZIONE RICHIESTA:
Inserisci/salva MANUALMENTE la formazione prima delle partite!

Link diretto:
{link_manuale}

Controlla i log e gli screenshot negli Artifacts di GitHub Actions.

---
Fantacalcio Bot v3.0 (automatico)
"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = mittente
        msg["To"] = ", ".join(destinatari)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(mittente, app_password)
            server.send_message(msg)

        logger.info(f"Email ({stato}) inviata a {', '.join(destinatari)}")
        return True
    except Exception as exc:
        logger.error(f"Errore invio email: {exc}")
        return False


# ─────────────────────────── PROCESSO PRINCIPALE ─────────────────────────────

def esegui_processo(username: str, password: str) -> str:
    """
    Crea driver, esegue tutti gli step e chiude il driver.
    Ritorna "successo" o "incerto". Lancia eccezione in caso di errore.
    """
    driver = crea_driver()
    try:
        step_login(driver, username, password)
        step_naviga_alla_lega(driver)
        stato = step_salva_formazione(driver)
        salva_screenshot(driver, "99_finale")
        return stato
    except Exception:
        try:
            salva_screenshot(driver, "errore")
            salva_html(driver, "errore")
        except Exception:
            pass
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        logger.info("Browser chiuso")


def main():
    logger.info("=" * 70)
    logger.info("FANTACALCIO BOT v3.0 - Salvataggio Automatico Formazione")
    logger.info(f"Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("Lega: Lega Paralimpica Seregno")
    logger.info(f"Notifiche email: saladaniele99@gmail.com + davidebanini99@gmail.com")
    logger.info("=" * 70)

    username = os.environ.get("FANTACALCIO_USERNAME")
    password = os.environ.get("FANTACALCIO_PASSWORD")

    if not username or not password:
        logger.error("ERRORE: FANTACALCIO_USERNAME o FANTACALCIO_PASSWORD non configurati")
        raise SystemExit(1)

    logger.info(f"Username: {username}")

    ultimo_errore = None

    for tentativo in range(1, MAX_RETRIES + 2):  # 1..4 (1 iniziale + 3 retry)
        logger.info(f"{'─' * 40}")
        logger.info(f"TENTATIVO {tentativo}/{MAX_RETRIES + 1}")
        logger.info(f"{'─' * 40}")
        try:
            stato = esegui_processo(username, password)
            if stato == "successo":
                logger.info("PROCESSO COMPLETATO CON SUCCESSO!")
            else:
                logger.warning("PROCESSO COMPLETATO CON STATO INCERTO")
            invia_email(stato)
            raise SystemExit(0)
        except SystemExit:
            raise
        except Exception as exc:
            ultimo_errore = exc
            logger.error(f"Tentativo {tentativo} fallito: {exc}")
            if tentativo <= MAX_RETRIES:
                delay = RETRY_DELAYS[tentativo - 1]
                logger.info(f"Attendo {delay}s prima del tentativo {tentativo + 1}...")
                time.sleep(delay)

    # Tutti i tentativi esauriti
    logger.error("=" * 60)
    logger.error(f"TUTTI I {MAX_RETRIES + 1} TENTATIVI FALLITI")
    logger.error("=" * 60)
    invia_email("fallito", str(ultimo_errore))
    raise SystemExit(1)


if __name__ == "__main__":
    main()
