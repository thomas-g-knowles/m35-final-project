# Imports package to manage .env info:
from dotenv import load_dotenv
# Imports OS to assist management of .env file:
import os
# Imports self made class to create enrollment token:
from android_enrollment import Enroller

if __name__ == "__main__":
  print("\n------------ QR Code Enrollment Generator Started ------------\n")

  # Environment variables:
  load_dotenv("./.env")
  paths = {"enterprise": os.environ.get("ENTERPRISE_PATH"), "policy": os.environ.get("POLICY_PATH"), "auth": os.environ.get("AUTH_PATH")}
  wifi_info = {"ssid": os.environ.get("WIFI_SSID"), "password": os.environ.get("WIFI_PASSWORD"), "security": os.environ.get("WIFI_SECURITY")}

  # Instantiating QRCode object:
  my_qrcode = Enroller(paths)

  # Generates the enrollment token:
  my_qrcode.policy_tokenization("0")

  # QR code config manipulation:
  my_qrcode.token_injection(wifi_info)

  # Generates URL for QR code:
  my_qrcode.generate_url()

  # Displays QR code in browser automatically:
  my_qrcode.open_url()
