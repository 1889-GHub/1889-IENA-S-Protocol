# v3.0.0 ✠




import os
import sys
import time
import socket
import importlib
import json
import ssl
import traceback




from rich.console import Console
from tqdm import tqdm




from PROTOCOL.S import S_Redirect




Modul_1889 = importlib.import_module("1889")




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
[bold red]
╔═══════════════════════════════════════════════════════════════════════╗
                           
    Sahip Lisansı - 1889  |  Yazar - Vinnie  |  Sürüm - v3.0.0  [bold green]✠[/bold green][bold red]
                  
    S PROTOCOL - Giriş
                           
    Kullanmadan önce anonimlik işlemleri için [bold cyan]VPN[/bold cyan][bold red] veya [bold cyan]TOR[/bold cyan][bold red] açın
                                   
╠═ YETKİ - [bold green]1889 S Protokol Üyesi[/bold green]
╠═══════════════════════════════════════════════════════════════════════╣[/bold red]""")




def Display_Menu():

    Console_Instance.print("    [bold white][B][/bold white] [bold red]Geri[/bold red]")
    Console_Instance.print("    [bold white][E][/bold white] [bold red]Çıkış[/bold red]\n")

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




def Try_Connect():

    try:

        Username = Console_Instance.input("\n[bold red]╠═ Kullanıcı Adınız [/bold red]").strip()

        if not Username:
            Console_Instance.print("\n[bold red]Kullanıcı adı boş bırakılamaz[/bold red]")

            time.sleep(2)
            return None

        Password = Console_Instance.input("\n[bold red]╠═ Şifreniz [/bold red]").strip()

        if not Password:
            Console_Instance.print("\n[bold red]Şifre boş bırakılamaz[/bold red]")

            time.sleep(2)
            return None

        Host = Console_Instance.input("\n[bold red]╠═ Sunucu Adresi [/bold red]").strip()

        if not Host:
            Console_Instance.print("\n[bold red]Sunucu adresi boş bırakılamaz[/bold red]")

            time.sleep(2)
            return None

        Port_Input = Console_Instance.input("\n[bold red]╠═ Sunucu Portu [/bold red]").strip()

        if not Port_Input or not Port_Input.isdigit():
            Console_Instance.print("\n[bold red]Geçerli bir port numarası giriniz[/bold red]")

            time.sleep(2)
            return None
        
        Port = int(Port_Input)

    except (EOFError, KeyboardInterrupt):
        Console_Instance.print("\n[bold red]Giriş iptal edildi[/bold red]")

        time.sleep(1)
        return None

    Config = Load_Client_Config()

    if not Config:
        return None

    Client_Cert = Config["Client_Cert_Path"]
    Client_Key = Config["Client_Key_Path"]

    CA_Cert = Config["CA_Cert_Path"]

    if not os.path.exists(Client_Cert) or not os.path.exists(Client_Key):

        Console_Instance.print("\n[bold red]Client sertifikası veya anahtar bulunamadı[/bold red]")

        Console_Instance.print("[bold red]Beklenen yollar[/bold red]")
        Console_Instance.print(f"   Cert: {Client_Cert}")
        Console_Instance.print(f"   Key:  {Client_Key}")
        time.sleep(5)
        return None

    Context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    Context.verify_mode = ssl.CERT_REQUIRED
    Context.load_verify_locations(CA_Cert)
    
    Context.load_cert_chain(certfile=Client_Cert, keyfile=Client_Key)

    try:
        Console_Instance.print(f"\n[bold green]Mutual TLS ile bağlanılıyor {Host}:{Port}[/bold green]")

        with socket.create_connection((Host, Port), timeout=10) as Base_Socket:

            with Context.wrap_socket(Base_Socket, server_hostname=Host) as Secure_Socket:

                Console_Instance.print("\n[bold red]Mutual TLS Handshake Başarılı[/bold red]")

                Auth_Request = f"10|{Username}|{Password}\n"

                Secure_Socket.sendall(Auth_Request.encode('utf-8'))

                Response = Secure_Socket.recv(8192).decode('utf-8').strip()

                Console_Instance.print(f"\n[bold red]Sunucu yanıtı {Response[:100]}{'...' if len(Response)>100 else ''}[/bold red]")

                if not Response.startswith("10|OK|"):

                    if "FAILED" in Response:
                        Console_Instance.print("\n[bold red]Kimlik doğrulama başarısız[/bold red]")
                    
                    elif "RATE_LIMIT" in Response:
                        Console_Instance.print("\n[bold red]Rate limit aşıldı[/bold red]")
                    
                    else:
                        Console_Instance.print(f"\n[bold red]Giriş reddedildi {Response}[/bold red]")
                    
                    time.sleep(3)
                    return None

                Parts = Response.split("|")

                if len(Parts) < 4:
                    Console_Instance.print("\n[bold red]Geçersiz giriş yanıtı formatı[/bold red]")
                    return None

                Session_Token = Parts[2]
                Received_Username = Parts[3]

                Console_Instance.print(f"\n[bold green]Giriş Başarılı {Received_Username}[/bold green]")

                Console_Instance.print("\n[bold green]Oturum başlatılıyor[/bold green]")

                Connection_Data = {
                    "username": Received_Username,
                    "session_token": Session_Token,
                    "host": Host,
                    "port": Port,
                    "connected": True,
                }

                return Connection_Data

    except ssl.SSLCertVerificationError:
        Console_Instance.print("[bold red]Sertifika doğrulanamıyor[/bold red]")
        Console_Instance.print("[bold red]1889 IENA Özel bir kurumdur ve herkes elini kolunu sallayarak sunucuya erişemez[/bold red]")
        Console_Instance.print("[bold red]Sertifikalar kişiye özeldir ekipten olmayan birisi giremez ne kadar ücret saçarsa saçsın[/bold red]")
        Console_Instance.print("[bold red]Ne kadar çaba sarf ederse etsin[/bold red]")
        time.sleep(6)

    except ssl.SSLError as Exception_Object:
        Console_Instance.print(f"\n[bold red]SSL Hatası {Exception_Object}[/bold red]")

    except socket.timeout:
        Console_Instance.print("\n[bold red]Bağlantı zaman aşımına uğradı[/bold red]")

    except ConnectionRefusedError:
        Console_Instance.print("\n[bold red]Bağlantı reddedildi[/bold red]")

    except Exception as Exception_Object:
        Console_Instance.print(f"\n[bold red]Beklenmeyen hata {Exception_Object}[/bold red]")

        Console_Instance.print(f"\n[bold yellow]{traceback.format_exc()}[/bold yellow]")

        time.sleep(5)

    return None




def Main():

    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Console_Instance.print()

        Display_Menu()

        Choice = Console_Instance.input("[bold red]╠═ Giriş İçin Enter [/bold red]").strip().lower()
        
        if Choice == 'b':
            Modul_1889.Main()
            continue
    
        if Choice == 'e':
            Clear_Terminal()
            Console_Instance.print("[bold red]Çıkış Yapıldı[/bold red]")
            sys.exit(0)
        
        if Choice != '':
            Console_Instance.print("[bold red]Geçersiz seçim[/bold red]")
            time.sleep(1)
            continue

        Clear_Terminal()

        Display_Banner()

        Connection_Data = Try_Connect()

        if Connection_Data:
            Clear_Terminal()
            S_Redirect.Main(Connection_Data)
        else:
            Console_Instance.input("\n[bold red]Ana menüye dönmek için Enter[/bold red]")




if __name__ == "__main__":
    Main()
