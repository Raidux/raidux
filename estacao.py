import serial
import requests
import time

 '/dev/ttyACM0', etc.
SERIAL_PORT = 'SUA_PORTA_SERIAL_AQUI' 
BAUD_RATE = 9600

THINGSPEAK_API_KEY = 'SUA_WRITE_API_KEY_AQUI'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

print("Iniciando a ponte entre Arduino e ThingSpeak...")
print(f"Escutando a porta serial: {SERIAL_PORT}")

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
  conexão estabilizar
except serial.SerialException as e:
    print(f"Erro ao conectar à porta serial: {e}")
    print("Verifique se a porta está correta e se o Arduino está conectado.")
    exit()

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        
        if line:
            print(f"Recebido do Arduino: {line}")
          
            try:
                temp, humidity, gas = line.split(',')

                payload = {
                    'api_key': THINGSPEAK_API_KEY,
                    'field1': temp,
                    'field2': humidity,
                    'field3': gas
                }
                
                response = requests.get(THINGSPEAK_URL, params=payload)
                
                if response.status_code == 200:
                    print("Dados enviados para o ThingSpeak com sucesso!")
                else:
                    print(f"Falha ao enviar dados. Status: {response.status_code}, Resposta: {response.text}")

            except ValueError:
                print(f"Formato de dados inválido recebido: '{line}'")
                
    except KeyboardInterrupt:
        print("Programa interrompido pelo usuário.")
        break
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        time.sleep(5) # Espera 5 segundos antes de tentar novamente
arduino.close()
print("Conexão serial fechada.")
