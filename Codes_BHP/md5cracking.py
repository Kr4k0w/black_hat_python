import hashlib;

def HashCracking(wordpassword): 
    global ps_file;
    try:
        ps_file = open(wordpassword, "r");
    except:
        print("[-] No Such File At That Path:");
        quit();


ps_hash = input("[*] Enter MD5 Hash Value:");
wordpassword = input("[*] Enter Path to The Password File:");
HashCracking(wordpassword);

for word in ps_file:
    print("[*] Trying:", word.strip("\n"));
    enc_wd = word.encode('utf-8');
    md5digest = hashlib.md5(enc_wd.strip()).hexdigest();

    if md5digest == ps_hash:
        print("[*] Password found:", word);
        exit(0);

print("[-] Password not is list!");