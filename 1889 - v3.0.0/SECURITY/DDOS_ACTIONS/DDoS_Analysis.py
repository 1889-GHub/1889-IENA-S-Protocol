# v3.0.0 ✠




import os
import sys
import time
import json
import collections
import warnings




from typing import Any
from scapy.all import sniff
from scapy.layers.inet import TCP, UDP, ICMP, IP
from rich.console import Console
from rich.table import Table
from rich import box
from tqdm import tqdm




from SECURITY import Option_G1




Console_Instance = Console()
warnings.simplefilter('ignore')




Suspicious_Protocols = ["ICMP", "UDP"]
Known_Attack_Ports = [
    80, 443, 53, 22, 21, 25, 3389, 5060, 123, 161, 
    1900, 111, 137, 138, 139, 445, 69, 520, 1434
]




Traffic_Data: list[Any] = []
Report_Data: dict[str, Any] = {}




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Check_Root_Privileges():
    if os.name == 'posix':
        try:
            if os.geteuid() != 0:
                Console_Instance.print("\n[bold red]Bu kod Root yetkisi içindir[/bold red]")
                time.sleep(3)
                Option_G1.Main()
        except AttributeError:
            pass




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
                  
    DDoS Analiz Aracı

    Kullanmadan önce anononimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                                      
╠═ YETENEKLER

    + Ağ Trafiğini İzle
    + Protokol Dağılımını Analiz Et
    + Port Aktivitesini Tespit Et
    + Kaynak IP Davranışını İncele
                                         
╠═ YETKİ - [bold green]Root[/bold green]
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




def Analyze_Packet(Packet):

    global Traffic_Data

    if IP in Packet:
        Source_Ip = Packet[IP].src
        Destination_Ip = Packet[IP].dst
        Protocol = Packet[IP].proto
        Length = len(Packet)
        
        Source_Port = None
        Destination_Port = None
        
        Protocol_Name = "Bilinmiyor"
        
        if TCP in Packet:
            Protocol_Name = "TCP"
            Source_Port = Packet[TCP].sport
            Destination_Port = Packet[TCP].dport
        
        elif UDP in Packet:
            Protocol_Name = "UDP"
            Source_Port = Packet[UDP].sport
            Destination_Port = Packet[UDP].dport
        
        elif ICMP in Packet:
            Protocol_Name = "ICMP"
        
        else:
            Protocol_Name = str(Protocol)

        Traffic_Data.append({
            "Source_Ip": Source_Ip,
            "Destination_Ip": Destination_Ip,
            "Protocol": Protocol_Name,
            "Length": Length,
            "Source_Port": Source_Port,
            "Destination_Port": Destination_Port
        })




def Extract_DDoS_Data(Duration):

    Found_Data = {}

    Not_Found = []

    Errors = []
    
    try:
        sniff(prn=Analyze_Packet, timeout=Duration, store=0)
        
        if not Traffic_Data:
            Errors.append("Belirtilen süre içinde ağ trafiği yakalanamadı")
            return None, Not_Found, Errors
        
        Total_Packets = len(Traffic_Data)
        Total_Bytes = sum(P["Length"] for P in Traffic_Data)
        
        Found_Data["Toplam paket"] = str(Total_Packets)

        Found_Data["Toplam süre"] = f"{Duration} saniye"

        Found_Data["Ortalama paket/sn"] = f"{Total_Packets / Duration:.2f}" if Duration > 0 else "0.00"

        Found_Data["Toplam veri"] = f"{Total_Bytes / 1024:.2f} KB"
        

        Protocol_Counts = collections.Counter(P["Protocol"] for P in Traffic_Data)

        for Proto, Count in Protocol_Counts.items():
            Percentage = (Count / Total_Packets) * 100 if Total_Packets > 0 else 0
            Found_Data[f"Protokol {Proto}"] = f"{Count} paket ({Percentage:.2f}%)"
        
        Target_Ports = collections.Counter(P["Destination_Port"] for P in Traffic_Data if P["Destination_Port"] is not None)

        Top_Ports = dict(Target_Ports.most_common(10))
        
        for Port, Count in Top_Ports.items():
            Found_Data[f"Port {Port}"] = f"{Count} bağlantı"
        
        if not Top_Ports:
            Not_Found.append("Port aktivitesi")
        
        Source_Counts = collections.Counter(P["Source_Ip"] for P in Traffic_Data)

        Total_Sources = len(Source_Counts)
        
        Found_Data["Toplam kaynak IP"] = str(Total_Sources)
        
        Top_Sources = dict(Source_Counts.most_common(5))

        for Ip, Count in Top_Sources.items():
            Pps = Count / Duration if Duration > 0 else 0
            Found_Data[f"Kaynak IP {Ip}"] = f"{Count} paket ({Pps:.2f} P/S)"
        
        return Found_Data, Not_Found, Errors
        
    except PermissionError:
        Errors.append("Ağ trafiğini izlemek için yönetici/root yetkisi gerekli")
        return None, Not_Found, Errors

    except Exception:
        Errors.append("Ağ izleme başarısız oldu")
        return None, Not_Found, Errors




def Create_Unified_Report(Duration, Found_Data, Not_Found, Errors):

    Table_Report = Table(
        show_header=True, 
        header_style="bold red", 
        border_style="red",
        title="DDoS Analiz Raporu", 
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




def Save_Report_To_Json(Duration):
    try:
        Root_Dir = "DDoS_ANALYSIS_REPORT"
        Report_Dir = os.path.join(Root_Dir, f"Analysis_{Duration}s")
        Filename = "DDoS_Results.json"

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

        Check_Root_Privileges()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print()

        Display_Menu()

        Input_Duration = Console_Instance.input("[bold red]╠═ Analiz Süresi (Saniye) [/bold red]").strip()

        Console_Instance.print()

        if Input_Duration.lower() == 'b':
            Option_G1.Main()
            continue
    
        if Input_Duration.lower() == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)

        if not Input_Duration:
            Console_Instance.print("[bold red]Geçersiz giriş[/bold red]")
            time.sleep(1)
            continue
            
        try:
            Duration = int(Input_Duration)
            if Duration <= 0:
                Console_Instance.print("[bold red]Analiz süresi 0'dan büyük olmalı[/bold red]")
                time.sleep(1)
                continue
        
        except ValueError:
            Console_Instance.print("[bold red]Geçersiz giriş (Sadece sayı girin)[/bold red]")
            time.sleep(1)
            continue

        global Traffic_Data
        Traffic_Data = []

        Reset_Report()
    
        Report_Data["Girdi"] = f"{Duration} saniye"

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print("\n[bold green]Ağ trafiği analiz ediliyor[/bold green]\n")
        
        Console_Instance.print()

        Found_Data, Not_Found, Errors = Extract_DDoS_Data(Duration)

        if Found_Data is None and Errors:
             Console_Instance.print(f"[bold red]{Errors[0]}[/bold red]")
             Console_Instance.input("\n[bold red]Devam etmek için Enter[/bold red]")
             continue

        Report_Data["Bulunan veriler"] = Found_Data or {}
        Report_Data["Bulunamayan veriler"] = Not_Found
        Report_Data["Hatalar"] = Errors

        Create_Unified_Report(Duration, Found_Data or {}, Not_Found, Errors)
        Save_Report_To_Json(Duration)

        Console_Instance.input("\n[bold red]Raporları kontrol edin[/bold red]")




if __name__ == "__main__":
    Main()
