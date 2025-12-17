# v3.0.0 ✠




import os
import time
import sys
import socket
import ssl
import json




from tqdm import tqdm
from rich.console import Console




from PROTOCOL.S import S_Profile




Console_Instance = Console()




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Loading_Animation(Duration):
    Console_Instance.print("[green]Yükleniyor...[/green]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='green'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():
    Console_Instance.print(r"""
[bold red]╔═══════════════════════════════════════════════════════════════════════╗

    ┓┏┓┏┓┏┓
    ┃┣┫┣┫┗┫
    ┻┗┛┗┛┗┛
                           
    S PROTOCOL                 
                           
    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green]

╠═ DURUM - [bold green]BAĞLI[/bold green]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("[bold red]╠══    [bold cyan]İLETİŞİM[/bold cyan][/bold red]\n")

    Console_Instance.print("    [bold white][ 1 ][/bold white] [bold cyan]Sohbet Merkezi[/bold cyan]\n")

    Console_Instance.print("[bold red]╠══    [bold yellow]DOSYA İŞLEMLERİ[/bold yellow][/bold red]\n")

    Console_Instance.print("    [bold white][ 2 ][/bold white] [bold yellow]Dosya Transfer Merkezi[/bold yellow]\n")

    Console_Instance.print("[bold red]╠══    [bold red]PROFIL[/bold red][/bold red]\n")

    Console_Instance.print("    [bold white][ 3 ][/bold white] [bold red]Profilin[/bold red]\n\n")


    Console_Instance.print("[bold red]╠═══════════════════════════════════════════════════════════════════════╣\n")

    Console_Instance.print("    [bold white][ B ][/bold white]  [bold red]Geri ( Bağlantıyı Kes )[/bold red]\n")

    Console_Instance.print("    [bold white][ E ][/bold white]  [bold red]Çıkış ( Bağlantıyı Kes )[/bold red]\n")

    Console_Instance.print("[bold red]╚═══════════════════════════════════════════════════════════════════════╝[/bold red]\n")




def Load_Client_Config():

    Config_Path = "Client_Config.json"
    
    if not os.path.exists(Config_Path):
        Console_Instance.print("\n[bold red]Client_Config.json adlı dosyayı ne yaptın? Eğer sildiysen onu geri indir o silinemez[/bold red]")
        return None

    try:
        with open(Config_Path, 'r', encoding='utf-8') as F:
            return json.load(F)
    
    except Exception as Exception_Object:
        Console_Instance.print(f"\n[bold red]Config yüklenemedi {Exception_Object}[/bold red]")
        return None




def Secure_Logout(Connection_Data):
    
    if not Connection_Data:
        return

    Config = Load_Client_Config()

    if not Config:
        return

    Client_Cert = Config["Client_Cert_Path"]
    Client_Key = Config["Client_Key_Path"]
    CA_Cert = Config["CA_Cert_Path"]

    if not os.path.exists(Client_Cert) or not os.path.exists(Client_Key):
        Console_Instance.print("\n[bold red]Sertifikalar eksik[/bold red]")

        return

    SSL_Context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    SSL_Context.verify_mode = ssl.CERT_REQUIRED
    SSL_Context.load_verify_locations(CA_Cert)
    SSL_Context.load_cert_chain(certfile=Client_Cert, keyfile=Client_Key)

    Base_Socket = None
    Secure_Socket = None

    try:

        Base_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Base_Socket.settimeout(5)

        Secure_Socket = SSL_Context.wrap_socket(
            Base_Socket, 
            server_hostname=Connection_Data['host']
        )
        
        Secure_Socket.connect((Connection_Data['host'], Connection_Data['port']))
        
        Logout_Message = f"11|{Connection_Data['session_token']}\n"
        
        Secure_Socket.sendall(Logout_Message.encode('utf-8'))
        
        Response = Secure_Socket.recv(8192).decode('utf-8').strip()
        
        if Response == "11|OK":
            Console_Instance.print("\n[bold red]Bağlantı kesildi[/bold red]")
        
        else:
            Console_Instance.print("\n[bold red]Bağlantı kesildi[/bold red]")

    except ConnectionRefusedError:
        Console_Instance.print("\n[bold red]Sunucu kapalı[/bold red]")
    
    except socket.timeout:
        Console_Instance.print("\n[bold red]Sunucu zaman aşımına uğradı[/bold red]")
    
    except ssl.SSLError as Exception_Object:
        Console_Instance.print(f"\n[bold red]SSL hatası {Exception_Object}[/bold red]")
    
    except Exception as Exception_Object:
        Console_Instance.print(f"\n[bold red]Genel hata {Exception_Object}[/bold red]")
    
    finally:
        try:
            if Secure_Socket:
                Secure_Socket.close()
        
        except Exception:
            pass
    
        try:
            if Base_Socket:
                Base_Socket.close()
        
        except Exception:
            pass




def Main(Connection_Data=None):

    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print()

        Display_Menu()

        Choice = Console_Instance.input("[bold red]╠═ Komut Girin [/bold red]").strip().lower()

        if Choice == '1':
            
            time.sleep(2)
        
        if Choice == '2':
            
            time.sleep(2)
        
        if Choice == '3':
            time.sleep(2)
            S_Profile.Main(Connection_Data)
            

        if Choice == 'b':
            Secure_Logout(Connection_Data)
            time.sleep(2)
            break
        
        if Choice == 'e':
            Secure_Logout(Connection_Data)
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)




if __name__ == "__main__":
    Main()
