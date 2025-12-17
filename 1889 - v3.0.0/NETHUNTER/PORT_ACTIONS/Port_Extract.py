# v3.0.0 ✠




import os
import json
import time
import sys
import socket
import concurrent.futures
import warnings




from typing import Any
from rich.console import Console
from rich.table import Table
from rich import box
from tqdm import tqdm
from scapy.layers.inet import IP, TCP, ICMP
from scapy.volatile import RandShort
from scapy.sendrecv import sr1, send
from contextlib import redirect_stderr
from io import StringIO




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
                  
    Port Tarama Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + SYN Port Taraması
    + UDP Port Taraması
    + Servis Banner Tespiti
    + İşletim Sistemi Algılama
                                         
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




def Syn_Scan(Target_Ip, Target_Port):
    try:
        Src_Port = RandShort()
        Syn_Packet = IP(dst=Target_Ip)/TCP(sport=Src_Port, dport=Target_Port, flags="S")
        Response = sr1(Syn_Packet, timeout=1, verbose=False)

        if Response and Response.haslayer(TCP):

            Tcp_Layer = Response.getlayer(TCP)
            if Tcp_Layer:

                if Tcp_Layer.flags == 0x12:
                    Rst_Packet = IP(dst=Target_Ip)/TCP(sport=Src_Port, dport=Target_Port, flags="R")
                    send(Rst_Packet, verbose=False)
                    return "open"
                
                elif Tcp_Layer.flags == 0x14:
                    return "closed"
        return "filtered"
    
    except Exception:
        return "filtered"




def Get_Banner(Target_Ip, Port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
            S.settimeout(2)
            S.connect((Target_Ip, Port))
            S.send(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n") 

            Banner_Full = S.recv(1024).decode().strip()
            Banner_First_Line = Banner_Full.split('\n')[0].strip()
            return Banner_First_Line
        
    except Exception:
        return None




def Detect_Os(Target_Ip):
    try:
        Response = sr1(IP(dst=Target_Ip)/ICMP(), timeout=1, verbose=False)
        if Response and Response.haslayer(IP):
            Ip_Layer = Response.getlayer(IP)
            if Ip_Layer:
                Ttl = Ip_Layer.ttl
                if Ttl <= 64:
                    return "Linux/Unix"
                elif Ttl <= 128:
                    return "Windows"
                else:
                    return "Bilinmiyor"
            return "Bilinmiyor"
        
    except Exception:
        return "Bilinmiyor"




def Extract_Port_Data(Target_Ip, Scan_Type, Custom_Range=None):

    Found_Data = {}

    Not_Found = []

    Errors = []
    
    try:
        Fake_Stderr = StringIO()

        with redirect_stderr(Fake_Stderr):
            
            if Scan_Type == "hızlı":
                Ports = [22, 80, 443, 3306, 8080, 53, 21, 23, 25, 110, 137, 138, 139, 445]
            
            elif Scan_Type == "hepsi":
                Ports = list(range(1, 65536))
            
            elif Scan_Type == "manuel" and Custom_Range:
                try:
                    Start_Port, End_Port = map(int, Custom_Range.split('-'))
                    Ports = list(range(Start_Port, End_Port + 1))
                
                except ValueError:
                    Errors.append("Geçersiz port aralığı formatı")
                    return None, Not_Found, Errors
                
            else:
                Errors.append("Geçersiz tarama tipi")
                return None, Not_Found, Errors

            Os_Detected = Detect_Os(Target_Ip)

            Found_Data["Hedef IP"] = Target_Ip

            Found_Data["İşletim sistemi"] = Os_Detected

            Found_Data["Taranan port sayısı"] = str(len(Ports))

            Found_Data["Tarama tipi"] = Scan_Type

            Open_Ports = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as Executor:
                Futures = {Executor.submit(Syn_Scan, Target_Ip, Port): Port for Port in Ports}
                for Future in tqdm(concurrent.futures.as_completed(Futures), total=len(Futures), bar_format="{l_bar}{bar}|", colour='red'):
                    Port = Futures[Future]
                    Status = Future.result()
                    if Status == "open":
                        Banner = Get_Banner(Target_Ip, Port)
                        Service = Banner if Banner else "Bilinmiyor"
                        Open_Ports.append({"port": Port, "service": Service})
                        Found_Data[f"Port {Port}"] = f"Açık - Servis: {Service}"

            if not Open_Ports:
                Not_Found.append("Açık port bulunamadı")

        return Found_Data, Not_Found, Errors

    except Exception:
        Errors.append("Port taraması başarısız oldu")
        return None, Not_Found, Errors




def Create_Unified_Report(Target_Ip, Found_Data, Not_Found, Errors):

    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="Port Tarama Raporu", 
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
        Root_Dir = "PORT_SCAN_REPORT"
        Report_Dir = os.path.join(Root_Dir, Target_Ip.replace('.', '_'))
        Filename = "Port_Scan_Results.json"
        
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

        Input_Ip = Console_Instance.input("[bold red]╠═ Hedef IP Adresi Girin [/bold red]").strip().strip('"').strip("'")

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

        Scan_Type = Console_Instance.input("[bold red]╠═ Tarama Tipi (Hızlı / Hepsi / Manuel) [/bold red]").strip().strip('"').strip("'").lower()

        Console_Instance.print()

        Custom_Range = None

        if Scan_Type == "manuel":
            Custom_Range = Console_Instance.input("[bold red]╠═ Port Aralığı (örn: 1-1000) [/bold red]").strip().strip('"').strip("'")
            Console_Instance.print()

        if Scan_Type not in ["hızlı", "hepsi", "manuel"]:
            Console_Instance.print("[bold red]Geçersiz tarama tipi[/bold red]")
            time.sleep(1)
            continue

        Reset_Report()
        
        Report_Data["Girdi"] = Input_Ip

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]Port taraması yapılıyor[/bold green]\n")
        
        Console_Instance.print()

        Found_Data, Not_Found, Errors = Extract_Port_Data(Input_Ip, Scan_Type, Custom_Range)

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
