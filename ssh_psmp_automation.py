import pexpect
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Function to decrypt the password
def decrypt_password(filename, key):
    backend = default_backend()

    # Read the IV and encrypted password from the file
    with open(filename, 'rb') as f:
        iv = f.read(16)  # AES block size is 16 bytes
        encrypted_password = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    # Decrypt and remove padding
    padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    password = unpadder.update(padded_password) + unpadder.finalize()

    return password.decode('utf-8')

# Function to automate SSH login
def ssh_to_server(psmp_host, psmp_user, ticket_id, reason, decrypted_password):
    ssh_command = f"ssh -l {psmp_user} -oKexAlgorithms=+diffie-hellman-group14-sha1 {psmp_host}"
    
    # Use pexpect to automate the interaction
    child = pexpect.spawn(ssh_command)

    # Wait for the password prompt and send the password
    child.expect("password:")
    child.sendline(decrypted_password)

    # Wait for the ticket ID prompt and send the ticket ID
    child.expect("Ticket ID:")
    child.sendline(ticket_id)

    # Wait for the reason prompt and send the reason
    child.expect("Reason:")
    child.sendline(reason)

    # Interact with the server (this will leave the SSH session open for further interaction)
    child.interact()

# Main logic
if __name__ == "__main__":
    # Variables
    target_server = input("Enter the target server: ")
    ticket_id = input("Enter the ticket ID: ")
    reason = input("Enter the reason: ")
    
    psmp_user = "your_psmp_user"
    psmp_host = "your_psmp_host"
    
    # Decrypt the password
    encrypted_password_file = "encrypted_password.bin"
    aes_key = b"this_is_a_32_byte_key___________"  # Same key used to encrypt

    try:
        decrypted_password = decrypt_password(encrypted_password_file, aes_key)
        print("Password decrypted successfully.")
    except Exception as e:
        print(f"Failed to decrypt password: {e}")
        exit(1)

    # SSH to the server
    ssh_to_server(psmp_host, psmp_user, ticket_id, reason, decrypted_password)
