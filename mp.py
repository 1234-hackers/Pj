
import requests
import base64

# Your M-Pesa credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
shortcode = "your_shortcode"
lipa_na_mpesa_online_passkey = "your_passkey"
lipa_na_mpesa_online_shortcode = "your_lipa_na_mpesa_online_shortcode"
lipa_na_mpesa_online_callback_url = "your_callback_url"

# Base URL for Safaricom API
base_url = "https://sandbox.safaricom.co.ke"

# Generate the OAuth token
def generate_access_token():
    url = base_url + "/oauth/v1/generate?grant_type=client_credentials"
    headers = {
        "Authorization": "Basic " + base64.b64encode((consumer_key + ":" + consumer_secret).encode()).decode(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    access_token = response.json().get("access_token")
    return access_token

# Initiate payment
def initiate_payment(msisdn, amount, account_reference, transaction_desc):
    access_token = generate_access_token()
    url = base_url + "/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": lipa_na_mpesa_online_shortcode,
        "Password": base64.b64encode((lipa_na_mpesa_online_shortcode + lipa_na_mpesa_online_passkey + datetime.now().strftime("%Y%m%d%H%M%S")).encode()).decode(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": msisdn,
        "PartyB": lipa_na_mpesa_online_shortcode,
        "PhoneNumber": msisdn,
        "CallBackURL": lipa_na_mpesa_online_callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Example usage:
initiate_payment("customer_phone_number", "amount", "account_reference", "transaction_description")
