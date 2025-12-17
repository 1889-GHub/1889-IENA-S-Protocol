# v3.0.0 ✠




import os
import json
import time
import sys
import requests
import warnings




from typing import Any
from rich.console import Console
from rich.table import Table
from rich import box
from tqdm import tqdm




from NETHUNTER import Option_H1




Console_Instance = Console()
warnings.simplefilter('ignore')




Report_Data: dict[str, Any] = {}




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
                  
    IP Sorgu Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + IP Coğrafi Konum Analizi
    + ISP ve Organizasyon Bilgisi
    + Bölge ve Zaman Dilimi Tespiti
                                         
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




def Extract_Ip_Data(Target_Ip):

    Found_Data = {}

    Not_Found = []

    Errors = []
    
    try:
        Url = f"http://ip-api.com/json/{Target_Ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as"
        Response = requests.get(Url, timeout=10)
        Data = Response.json()

        if Data["status"] != "success":
            Errors.append(f"IP sorgulanamadı: {Data.get('message', 'Bilinmeyen hata')}")
            return None, Not_Found, Errors

        Found_Data["IP adresi"] = Target_Ip

        Found_Data["Ülke"] = Data.get('country', 'Bilinmiyor')

        Found_Data["Ülke kodu"] = Data.get('countryCode', 'Bilinmiyor')

        Found_Data["Bölge"] = Data.get('regionName', 'Bilinmiyor')

        Found_Data["Bölge kodu"] = Data.get('region', 'Bilinmiyor')

        Found_Data["Şehir"] = Data.get('city', 'Bilinmiyor')

        Found_Data["Posta kodu"] = Data.get('zip', 'Bilinmiyor')

        Found_Data["Zaman dilimi"] = Data.get('timezone', 'Bilinmiyor')

        Found_Data["ISP"] = Data.get('isp', 'Bilinmiyor')

        Found_Data["Organizasyon"] = Data.get('org', 'Bilinmiyor')

        Found_Data["ASN"] = Data.get('as', 'Bilinmiyor')

        Found_Data["Enlem"] = str(Data.get('lat', 'Bilinmiyor'))

        Found_Data["Boylam"] = str(Data.get('lon', 'Bilinmiyor'))

        Found_Data["Konum"] = f"{Data.get('lat', 'N/A')}, {Data.get('lon', 'N/A')}"

        if not Data.get('city'):
            Not_Found.append("Şehir bilgisi")
        
        if not Data.get('zip'):
            Not_Found.append("Posta kodu")

        return Found_Data, Not_Found, Errors

    except requests.exceptions.RequestException:
        Errors.append("Ağ hatası")
        return None, Not_Found, Errors
    
    except Exception:
        Errors.append("IP verisi alınamadı")
        return None, Not_Found, Errors




def Create_Unified_Report(Target_Ip, Found_Data, Not_Found, Errors):

    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="IP Analiz Raporu", 
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




def Save_Report_To_Json(Target_Ip):
    try:
        Root_Dir = "IP_REPORT"
        Report_Dir = os.path.join(Root_Dir, Target_Ip.replace('.', '_'))
        Filename = "Ip_Results.json"
        
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

        Input_Ip = Console_Instance.input("[bold red]╠═ IP Adresi Girin [/bold red]").strip()

        Console_Instance.print()

        if Input_Ip.lower() == 'b':
            Option_H1.Main()
            continue
        
        if Input_Ip.lower() == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)

        if not Input_Ip:
            Console_Instance.print("[bold red]Geçersiz IP adresi[/bold red]")
            time.sleep(1)
            continue

        Reset_Report()

        Report_Data["Girdi"] = Input_Ip

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]IP adresi analiz ediliyor[/bold green]\n")

        Console_Instance.print()

        Found_Data, Not_Found, Errors = Extract_Ip_Data(Input_Ip)

        if Found_Data is None and Errors:
             Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
             Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
             continue

        Report_Data["Bulunan veriler"] = Found_Data or {}
        Report_Data["Bulunamayan veriler"] = Not_Found
        Report_Data["Hatalar"] = Errors

        Create_Unified_Report(Input_Ip, Found_Data or {}, Not_Found, Errors)
        Save_Report_To_Json(Input_Ip)

        Console_Instance.input("\n[bold red]Raporları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
