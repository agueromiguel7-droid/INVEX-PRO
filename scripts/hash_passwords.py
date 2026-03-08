import getpass

try:
    import bcrypt
except ImportError:
    print("\n[ ERROR ] La librería 'bcrypt' no está instalada.")
    print("Para instalarla, abre tu terminal y ejecuta el siguiente comando:\n")
    print("    pip install bcrypt\n")
    print("Una vez instalada, vuelve a ejecutar este script.\n")
    exit(1)

def main():
    print("=========================================================")
    print("🛡️  Generador de Contraseñas Encriptadas Invex Pro  🛡️")
    print("=========================================================")
    print("Este script te permitirá crear el 'password_hash' que")
    print("debes pegar en tu archivo Google Sheet de usuarios.")
    print("Las contraseñas no se muestran en pantalla por seguridad.\n")
    
    while True:
        # Se pide la contraseña ocultando los caracteres
        password = getpass.getpass("➡️  Ingresa la nueva contraseña a cifrar: ")
        
        # Confirmación
        confirm_password = getpass.getpass("➡️  Confirma la contraseña: ")
        
        if password != confirm_password:
            print("❌  Las contraseñas no coinciden. Intenta de nuevo.\n")
            continue
            
        if len(password) < 4:
            print("❌  La contraseña es muy corta. Usa al menos 4 caracteres.\n")
            continue
            
        break
        
    print("\nGenerando Hash Criptográfico...")
    
    # Convierte el string a bytes
    bytes_pwd = password.encode('utf-8')
    
    # Genera el salt (un valor aleatorio que se añade antes de encriptar)
    # y encripta la contraseña
    salt = bcrypt.gensalt(rounds=12)
    hash_pwd = bcrypt.hashpw(bytes_pwd, salt)
    
    print("\n✅  HASH GENERADO EXITOSAMENTE \n")
    print("Copia exactamente el siguiente texto y pégalo en la")
    print("columna 'password_hash' de tu Google Sheet:\n")
    
    # Imprime el hash decodificándolo para que se vea como texto normal
    print("---------------------------------------------------------")
    print(hash_pwd.decode('utf-8'))
    print("---------------------------------------------------------")
    print("\nNota: Cada vez que corras este programa para la misma contraseña,")
    print("el Hash será diferente, pero Streamlit igual lo reconocerá como válido.")
    print("=========================================================\n")

if __name__ == "__main__":
    main()
