# v3.0.0 ✠




import os
import json
import time
import sys
import ssl
import socket
import re
import requests
import warnings




from typing import Any
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table
from rich import box
from tqdm import tqdm




from SECURITY import Option_G1




Console_Instance = Console()
warnings.simplefilter('ignore')




Report_Data: dict[str, Any] = {}




Suspicious_Sites = [
    "grabify", "bit.ly", "tinyurl", "ow.ly", "is.gd", "shorturl.at", "adf.ly", "goo.gl",
    "t.co", "v.gd", "lnkd.in", "short.ly", "clkim.com", "iplogger", "blasze.tk", 
    "gyazo.com", "ps3cfw.com", "yip.su", "02ip.ru", "iplis.ru", "cutt.ly", "rb.gy"
]




Phishing_Keywords = [
    "verify", "account", "suspended", "confirm", "secure", "update", "login",
    "banking", "paypal", "amazon", "apple", "microsoft", "netflix", "security",
    "urgent", "immediately", "expire", "click", "prize", "winner", "free"
]




Suspicious_Tlds = [
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".work", ".click",
    ".link", ".download", ".stream", ".loan", ".win", ".bid"
]




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Loading_Animation(Duration):
    Console_Instance.print("[green]Yükleniyor...[/green]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='green'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():
    Console_Instance.print(r"""
[bold red]
╔═══════════════════════════════════════════════════════════════════════╗

    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green][bold red]
                  
    Link Analiz Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + Linkte Bulunan Herşeyi Gösterir
                                         
╠═ YETKİ - [bold blue]Normal[/bold blue]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():
    Console_Instance.print("    [bold white][B] [bold red]Geri[/bold red][/bold white]")
    Console_Instance.print("    [bold white][E] [bold red]Çıkış[/bold red][/bold white]\n")
    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]\n")




def Reset_Report():
    global Report_Data
    Report_Data = {
        "Girdi": "",
        "Bulunan veriler": {},
        "Bulunamayan veriler": [],
        "Hatalar": []
    }




def Analyze_Structure(Url):
    Parsed = urlparse(Url)
    Data = {}
    
    Data["Alan adı"] = Parsed.netloc
    Data["Protokol"] = Parsed.scheme
    Data["URL uzunluğu"] = f"{len(Url)} karakter"
    Data["IP tespiti"] = "Evet" if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", Parsed.netloc) else "Hayır"
    Data["@ sembolü"] = "Var" if '@' in Url else "Yok"
    Data["Şüpheli uzantı"] = next((T for T in Suspicious_Tlds if Parsed.netloc.endswith(T)), "Normal")
    
    Keywords = [K for K in Phishing_Keywords if K in Url.lower()]
    Data["Riskli kelimeler"] = ", ".join(Keywords) if Keywords else "Yok"
    
    return Data




def Analyze_Ssl(Url):
    Data = {}
    try:
        Parsed = urlparse(Url)
        Hostname = Parsed.hostname or Parsed.netloc.split(':')[0]
        Context = ssl.create_default_context()
        
        with socket.create_connection((Hostname, 443), timeout=10) as Sock:
            with Context.wrap_socket(Sock, server_hostname=Hostname) as Secure_Sock:
                Cert = Secure_Sock.getpeercert()

                if Cert is None:
                    Data["SSL durumu"] = "Sertifika alınamadı"
                    return Data

                Data["SSL durumu"] = "Geçerli"
                Data["Süre sonu"] = Cert.get('notAfter', 'N/A')
                
                Issuer = {}
                for Tup in Cert.get('issuer', []):
                    if isinstance(Tup, tuple) and len(Tup) >= 2:
                        if isinstance(Tup[0], tuple) and len(Tup[0]) > 1:
                            Issuer[Tup[0][1]] = Tup[1]
                        elif isinstance(Tup[0], str):
                            Issuer[Tup[0]] = Tup[1]
                        
                Data["Yayıncı"] = Issuer.get('organizationName', 'Bilinmiyor')

                Trusted_Cas = ['DigiCert', "Let's Encrypt", 'GlobalSign', 'Comodo', 'Sectigo']
                Issuer_Name = Issuer.get('organizationName', '')
                Is_Trusted = any(Ca in Issuer_Name for Ca in Trusted_Cas)
                Data["Otorite"] = "Güvenilir" if Is_Trusted else "Bilinmiyor"
                
    except Exception:
        Data["SSL durumu"] = "Bağlantı hatası / SSL yok"
    
    return Data




def Analyze_Network_And_Content(Url):
    Network_Data = {}
    Content_Data = {}
    Errors = []
    
    try:
        Response = requests.get(Url, timeout=10, verify=True, allow_redirects=True)
        
        Network_Data["Durum kodu"] = str(Response.status_code)
        Network_Data["Yönlendirme sayısı"] = str(len(Response.history))
        Network_Data["Son hedef"] = Response.url
        
        Redirects = [R.url for R in Response.history]
        Suspicious = [Site for Site in Suspicious_Sites for R in Redirects if Site in R]
        Network_Data["Şüpheli yönlendirme"] = ", ".join(Suspicious) if Suspicious else "Yok"

        Html = Response.text.lower()
        Content_Data["Form sayısı"] = str(len(re.findall(r'<form', Html)))
        Content_Data["Şifre alanı"] = str(Html.count('type="password"') + Html.count("type='password'"))
        Content_Data["İframe sayısı"] = str(Html.count('<iframe'))
        Content_Data["Script sayısı"] = str(Html.count('<script'))
        
        Headers = Response.headers
        Security_Headers = ['Strict-Transport-Security', 'X-Frame-Options', 'X-XSS-Protection']
        Missing = [H for H in Security_Headers if H not in Headers]
        Content_Data["Eksik güvenlik başlıkları"] = ", ".join(Missing) if Missing else "Tamam"

    except requests.exceptions.RequestException:
        Errors.append("Ağ hatası")
    except Exception:
        Errors.append("Analiz hatası")
        
    return Network_Data, Content_Data, Errors




def Extract_Link_Data(Url):
    Found_Data = {}
    Not_Found = []
    Errors = []
    
    try:
        Structure = Analyze_Structure(Url)
        Ssl_Info = {}
        
        if Url.startswith("https"):
            Ssl_Info = Analyze_Ssl(Url)
        else:
            Ssl_Info["SSL durumu"] = "HTTP (Güvensiz)"
            Not_Found.append("HTTPS protokolü")

        Network, Content, Network_Errors = Analyze_Network_And_Content(Url)
        
        if Structure:
            for Key, Value in Structure.items():
                Found_Data[Key] = Value
                
        if Ssl_Info:
            for Key, Value in Ssl_Info.items():
                Found_Data[Key] = Value
                
        if Network:
            for Key, Value in Network.items():
                Found_Data[Key] = Value
                
        if Content:
            for Key, Value in Content.items():
                Found_Data[Key] = Value
        
        if Network_Errors:
            Errors.extend(Network_Errors)
            
        return Found_Data, Not_Found, Errors
        
    except Exception:
        Errors.append("URL analiz edilemedi")
        return None, Not_Found, Errors




def Create_Unified_Report(Url, Found_Data, Not_Found, Errors):

    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="Link Analiz Raporu", 
        title_style="bold red",
        box=box.HEAVY_HEAD,
        min_width=80
    )

    Table_Report.add_column("Kategori", style="bold yellow", justify="left")
    Table_Report.add_column("Bilgi", style="white", justify="left")

    if Found_Data:
        Table_Report.add_section()
        for Key, Value in Found_Data.items():
            Table_Report.add_row("Bulunan veriler", f"[bold cyan]{Key}[/bold cyan] {Value}")

    if Not_Found:
        Table_Report.add_section()
        for Item in Not_Found:
            Table_Report.add_row("[bold red]Bulunamayan Veri[/bold red]", Item)

    if Errors:
        Table_Report.add_section()
        for Error in Errors:
            Table_Report.add_row("[bold red]Hata[/bold red]", Error)

    Console_Instance.print(Table_Report)
    time.sleep(2)




def Save_Report_To_Json(Url):
    try:
        Root_Dir = "PHISHING_REPORT"
        Parsed = urlparse(Url)
        Report_Dir = os.path.join(Root_Dir, Parsed.netloc.replace(':', '_').replace('.', '_'))
        Filename = "Phishing_Results.json"
        
        os.makedirs(Report_Dir, exist_ok=True)
        Filepath = os.path.join(Report_Dir, Filename)
        
        Report_Data["Zaman damgası"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(Filepath, 'w', encoding='utf-8') as Output_File:
            json.dump(Report_Data, Output_File, ensure_ascii=False, indent=4)
            
        Console_Instance.print(f"\n[bold green]Rapor kaydedildi[/bold green] [white]{Filepath}[/white]")
    except Exception:
        pass




def Main():
    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print()

        Display_Menu()

        Input_Url = Console_Instance.input("[bold red]╠═ URL Yapıştır [/bold red]").strip()

        Console_Instance.print()

        if Input_Url.lower() == 'b':
            Option_G1.Main()
            continue
        if Input_Url.lower() == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)

        if not Input_Url:
            Console_Instance.print("[bold red]Geçersiz URL[/bold red]")
            time.sleep(1)
            continue
        
        if not Input_Url.startswith('http'):
            Console_Instance.print("[bold red]URL http:// veya https:// ile başlamalı[/bold red]")
            time.sleep(1)
            continue

        Reset_Report()
        Report_Data["Girdi"] = Input_Url

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]URL analiz ediliyor[/bold green]\n")
        Console_Instance.print()

        Found_Data, Not_Found, Errors = Extract_Link_Data(Input_Url)

        if Found_Data is None and Errors:
             Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
             Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
             continue

        Report_Data["Bulunan veriler"] = Found_Data or {}
        Report_Data["Bulunamayan veriler"] = Not_Found
        Report_Data["Hatalar"] = Errors

        Create_Unified_Report(Input_Url, Found_Data or {}, Not_Found, Errors)
        Save_Report_To_Json(Input_Url)

        Console_Instance.input("\n[bold red]Raporları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
