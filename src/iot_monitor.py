import time
import thingspeak 
import Adafruit_DHT

# Configuration
CHANNEL_ID = "YOUR_CHANNEL_ID"
WRITE_KEY = "YOUR_WRITE_KEY"
SENSOR_PIN = 4
SENSOR_TYPE = Adafruit_DHT.DHT11

def monitor_environment():
    """
    Reads from DHT11 sensor and uploads data to ThingSpeak cloud dashboard.
    Note: 'thingspeak' library handles the HTTP API calls.
    """
    channel = thingspeak.Channel(id=CHANNEL_ID, write_key=WRITE_KEY)
    
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
            
            if humidity is not None and temperature is not None:
                print(f"Temp: {temperature:.1f}C  Humidity: {humidity:.1f}%")
                
                # Upload to ThingSpeak Cloud
                channel.update({'field1': temperature, 'field2': humidity})
                print("Data uploaded successfully.")
            else:
                print("Sensor Read Failed - Retrying...")
                
        except Exception as e:
            print(f"Connection/Sensor Error: {e}")
        
        time.sleep(15) # ThingSpeak free tier update interval

if __name__ == "__main__":
    monitor_environment()
