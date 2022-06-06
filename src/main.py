# Imports package to manage .env info:
from dotenv import load_dotenv
# Imports OS to assist management of .env file:
import os
# Imports self made class to create enrollment token:
from android_enrollment import deviceEnroller

if __name__ == "__main__":
  print("\n------------ QR Code Enrollment Generator Started ------------\n")

  # Environment variables:
  load_dotenv("./.env")
  auth_path: str = os.environ.get("AUTH_PATH")
  enterprise_path: str = os.environ.get("ENTERPRISE_PATH")
  policy_path: str = os.environ.get("POLICY_PATH")
  wifi_info: dict = {"ssid": os.environ.get("WIFI_SSID"), "password": os.environ.get("WIFI_PASSWORD"), "security": os.environ.get("WIFI_SECURITY")}

  # Instantiating QRCode object:
  enroller_instance = deviceEnroller(auth_path, debug=True)

  # Creates the specified policy if it cannot be found:
  enroller_instance.patch_policy(policy_path, "temp", {"applications": [{"installType": "FORCE_INSTALLED", "packageName": "com.sega.sonic"}, {"installType": "FORCE_INSTALLED", "packageName": "com.sega.sonic1"}, {"installType": "FORCE_INSTALLED", "packageName": "com.sega.sonic1px"}, {"installType": "FORCE_INSTALLED", "packageName": "com.yodo1.crossyroad"}]})

  # Generates the enrollment token:
  enroller_instance.policy_tokenization(enterprise_path, policy_path, "temp")

  # QR code config manipulation:
  enroller_instance.token_injection(wifi_info)

  # Generates URL for QR code:
  enroller_instance.generate_url()

  # Displays QR code in browser automatically:
  enroller_instance.open_url()

  # Generation of QR code PNG:
  enroller_instance.generate_qrcode()
