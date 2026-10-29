from pyngrok import ngrok
import subprocess
import time
import threading
import os

# 🔑 ADD YOUR AUTHTOKEN HERE
NGROK_AUTHTOKEN = "34TObHXO5ZLa1jgrRbIvRToYZxS_51z8yMhDGyR4GwQ6Q2zXK"  # Replace with your actual token

def run_django_server():
    """Run Django development server"""
    print("Starting Django server...")
    os.system("python manage.py runserver")

def start_ngrok_tunnel():
    """Start ngrok tunnel"""
    print("Starting ngrok tunnel...")
    
    # Wait a moment for Django to start
    time.sleep(3)
    
    # Set authtoken
    print("Setting up ngrok authentication...")
    ngrok.set_auth_token(NGROK_AUTHTOKEN)
    
    # Start the tunnel
    print("Creating secure tunnel...")
    public_url = ngrok.connect(8000)
    print(f"\n🎉 SUCCESS! Your public URL is: {public_url}")
    print("📱 Use this URL on your phone!")
    print("\n⏹️  Press Ctrl+C to stop")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping ngrok...")
        ngrok.kill()

if __name__ == "__main__":
    # Start Django server in a separate thread
    django_thread = threading.Thread(target=run_django_server)
    django_thread.daemon = True
    django_thread.start()
    
    # Start ngrok
    start_ngrok_tunnel()