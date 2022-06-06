import os
import google.auth
from googleapiclient.discovery import build
import json
from urllib.parse import urlencode
import webbrowser

class Enroller:
  '''Creates an object from class QRCode, used for provisioning and enrolling an android device. QRCode object has all methods needed to create an enrollment token.'''

  def __init__(self: object, paths: dict, debug: bool = True):
    self.paths: dict = paths
    self.debug = debug
    self.authenticate()
    self.api_client()


  def authenticate(self: object):
    '''Authenticates the service account associated with the JSON file argument passed.'''

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.paths["auth"]
    google.auth.default()

    if self.debug:
      print("- Authentication succeeded")


  def api_client(self: object):
    '''Builds the API client for the Android Management API upon function invoke.'''

    self.androidmanagement = build("androidmanagement", "v1")

    if self.debug:
      print("- API client built successfully")


  def patch_policy(self: object, policy_name: str, policy_json: dict):
    '''Patches/updates existing policy with passed policy JSON OR creates a new one if no existing policy is found for given name.'''

    self.androidmanagement.enterprises().policies().patch(name=self.paths["policy"]+policy_name, body=policy_json).execute()

    if self.debug:
      print("- Policy patched successfully")


  def list_policies(self: object):
    '''Lists all existing policies under an enterprise.'''

    try:
      return self.androidmanagement.enterprises().policies().list(parent=self.paths["enterprise"]).execute()["policies"]

    except KeyError:
      if self.debug:
        print("- No policies exist under enterprise")
        return False


  def delete_policies(self: object):
    '''Deletes all enrolled devices under enterprise.'''

    if self.list_policies():

      if self.debug:
        deleted_policies = []

      for policy in self.list_policies():
        policy_name = policy["name"]
        print(self.androidmanagement.enterprises().policies().delete(name=policy_name).execute())
        if self.debug:
          deleted_policies.append(policy_name)
      
      if self.debug:
        print("- The following policies have been deleted from the enterprise:", deleted_policies)
      
    else:
      print("- No policies exist under enterprise to delete")


  def policy_tokenization(self: object, policy_choice: int):
    '''Generates an enrollment token from the discovery API. Note that it indexes and returns only the QR code portion (only required section).'''

    if policy_choice != 5:
      self.enrollment_token: dict = self.androidmanagement.enterprises().enrollmentTokens().create(parent=self.paths["enterprise"], body={"policyName": self.paths["policy"]+"policy"+str(policy_choice)}).execute()["qrCode"]

    else:
      self.enrollment_token: dict = self.androidmanagement.enterprises().enrollmentTokens().create(parent=self.paths["enterprise"], body={"policyName": self.paths["policy"]+"devmode"}).execute()["qrCode"]


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


  def get_url(self: object):
    '''Returns URL of QR code when invoked, to make further manipulation possible rather than just printing it out.'''
    
    return self.qrcode_url


  def list_devices(self: object):
    '''Returns list of dicts containing all enrolled devices info under enterprise.'''

    try:
      return self.androidmanagement.enterprises().devices().list(parent=self.paths["enterprise"]).execute()["devices"]
    except KeyError:
      if self.debug:
        print("- No devices enrolled under enterprise")
      return False


  def list_device(self: object, device_id: str):
    '''Returns enrolled device info under enterprise.'''

    return self.androidmanagement.enterprises().devices().get(name=device_id).execute()


  def delete_devices(self: object):
    '''Deletes all enrolled devices under enterprise.'''

    if self.debug:
      deleted_devices = []

    if self.list_devices():
      for device in self.list_devices():
        device_id = device["name"][device["name"].rfind("/")+1:]
        print(self.androidmanagement.enterprises().devices().delete(name=device["name"]).execute())
        if self.debug:
          deleted_devices.append(device_id)
      
      if self.debug:
        print("- The following devices have been deleted from the enterprise:", deleted_devices)

    else:
      if self.debug:
        print("- No devices exist under enterprise to delete")


  def delete_device(self: object, device_id: str):
    '''Deletes specified enrolled device under enterprise, doubles as a remote wipe capability - does not enforce FRP.'''

    self.androidmanagement.enterprises().devices().delete(name=self.paths["enterprise"]+"/devices/"+device_id).execute()
    
    if self.debug:
      print("- Device with ID:", device_id[device_id.rfind("/"):], "has been deleted from the enterprise")


  def device_policy(self: object, device_id: str, policy_name: str):
    '''Sets the policy for an individual device by targetting its device ID.'''
    if policy_name != "5":
      self.androidmanagement.enterprises().devices().patch(name=self.paths["enterprise"]+"/devices/"+device_id, updateMask="policyName", body={"policyName": self.paths["policy"]+"policy"+policy_name}).execute()
    
    else:
      self.androidmanagement.enterprises().devices().patch(name=self.paths["enterprise"]+"/devices/"+device_id, updateMask="policyName", body={"policyName": self.paths["policy"]+"devmode"}).execute()

    if self.debug:
      print("- Device with ID:", device_id, "has been updated to policy:", policy_name)

