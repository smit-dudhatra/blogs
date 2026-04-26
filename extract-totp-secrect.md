https://cavalloj.medium.com/totp-secret-extraction-from-qr-codes-ee097b4c687f

1. on google authenticator app
  go to transfer codes > export codes > select the account that you want to get the totp secret > click "next"
2. you will get the QR code
3. upload to "https://scanqr.org/#scan"
4. get the scanned data :- "otpauth-migration....................."
5. clone this repo "https://github.com/scito/extract_otp_secrets"
6. put scanned data in :- "extract_otp_secrets\src\key.txt"
7. python3 extract_otp_secrets.py key.txt
in terminal you will get your totp secret
