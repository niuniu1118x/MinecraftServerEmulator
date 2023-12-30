import socket
import configparser
import os

def read_config():
    if not os.path.exists('config.cfg'):
        generate_default_config()

    config = configparser.ConfigParser()
    config.read('config.cfg')

    motd_line1 = config.get('ServerConfig', 'motd_line1')
    motd_line2 = config.get('ServerConfig', 'motd_line2')
    logo_path = config.get('ServerConfig', 'logo_path')

    return motd_line1, motd_line2, logo_path

def generate_default_config():
    default_config = """
[ServerConfig]
motd_line1 = Welcome to My Minecraft Server!
motd_line2 = Enjoy your stay!
logo_path = path/to/your/logo.png
"""
    with open('config.cfg', 'w') as file:
        file.write(default_config)

def send_motd_logo(motd_line1, motd_line2, logo_path, client_socket):
    combined_motd = f"{motd_line1}\n{motd_line2}"

    motd_packet = bytearray()
    motd_packet.extend([0x00, 0x00])
    motd_packet.extend([len(combined_motd) & 0xFF, (len(combined_motd) >> 8) & 0xFF])
    motd_packet.extend(map(ord, combined_motd))
    client_socket.sendall(motd_packet)

    try:
        with open(logo_path, 'rb') as file:
            logo_data = file.read()
    except FileNotFoundError:
        print("Logo file not found.")
        return

    logo_packet = bytearray()
    logo_packet.extend([0x00, 0x01])
    logo_packet.extend([len(logo_data) & 0xFF, (len(logo_data) >> 8) & 0xFF])
    logo_packet.extend(logo_data)
    client_socket.sendall(logo_packet)

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 25565))
    server_socket.listen(5)
    print("Minecraft server listening on port 25565")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")

        motd_line1, motd_line2, logo_path = read_config()
        send_motd_logo(motd_line1, motd_line2, logo_path, client_socket)

        client_socket.close()

if __name__ == "__main__":
    run_server()
