import os
import google.auth
from googleapiclient.discovery import build
import json
from urllib.parse import urlencode
import webbrowser
import qrcode

class deviceEnroller:
  '''Creates an object from class deviceEnroller, used for provisioning and enrolling an android device. deviceEnroller object has all methods needed to create an enrollment token.'''

  def __init__(self: object, auth_path: str, debug: bool = False):
    self.auth_path: str = auth_path
    self.debug = debug
    self.authenticate()
    self.api_client()


  def authenticate(self: object):
    '''Authenticates the service account associated with the JSON file argument passed.'''

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.auth_path
    google.auth.default()
    del self.auth_path

    if self.debug:
      print("- Authentication succeeded")


  def api_client(self: object):
    '''Builds the API client for the Android Management API upon function invoke.'''

    self.androidmanagement = build("androidmanagement", "v1")

    if self.debug:
      print("- API client built successfully")


  def patch_policy(self: object, policy_path: str, policy_name: str, policy_json: dict):
    '''Patches/updates existing policy with passed policy JSON OR creates a new one if no existing policy is found for given name.'''

    self.androidmanagement.enterprises().policies().patch(name=policy_path+policy_name, body=policy_json).execute()

    if self.debug:
      print("- Policy patched successfully")


  def policy_tokenization(self: object, enterprise_path: str, policy_path: str, policy_choice: str):
    '''Generates an enrollment token from the discovery API. Note that it indexes and returns only the QR code portion (only required section).'''

    self.enrollment_token: dict = self.androidmanagement.enterprises().enrollmentTokens().create(parent=enterprise_path, body={"policyName": policy_path+"policy"+policy_choice}).execute()["qrCode"]

    if self.debug:
      print(f"- Enrollment token generated: \n{self.enrollment_token}")


  def token_injection(self: object, wifi_info: dict):
    '''Manipulates QR code config data, by injecting in WiFi information, allowing for automatic internet connection during setup.'''

    self.enrollment_token = json.loads(self.enrollment_token)
    self.enrollment_token["android.app.extra.PROVISIONING_WIFI_SSID"] = wifi_info["ssid"]
    self.enrollment_token["android.app.extra.PROVISIONING_WIFI_PASSWORD"] = wifi_info["password"]
    self.enrollment_token["android.app.extra.PROVISIONING_WIFI_SECURITY_TYPE"] = wifi_info["security"]
    self.enrollment_token["android.app.extra.PROVISIONING_LEAVE_ALL_SYSTEM_APPS_ENABLED"] = True
    self.enrollment_token = json.dumps(self.enrollment_token)

    if self.debug:
      print("- Token injection succeeded")


  def generate_url(self: object):
    '''Encodes the returned enrollment token data into an image and generates the URL to scan the QR code.'''

    self.image = {"cht": "qr", "chs": "500x500", "chl": self.enrollment_token}
    self.qrcode_url = 'https://chart.googleapis.com/chart?' + urlencode(self.image)

    if self.debug:
      print("- URL containing QR code generated")


  def open_url(self: object):
    '''Opens the webpage containing the scannable QR code when invoked.'''
    
    webbrowser.open(self.qrcode_url, new=0)

    if self.debug:
      print("- QR code opened in web browser")


  def generate_qrcode(self: object):
    '''Generates QR code PNG image file, in project root directory.'''

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(self.enrollment_token)
    qr.make(fit=True)
    qr.make_image(fill="black").save("./qrcode.png")

    if self.debug:
      print("Local QR code PNG generated.")
