import requests

domain = '5sim.biz'
apikey_base = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ0OTQ5NjUsImlhdCI6MTY4Mjk1ODk2NSw' \
              'icmF5IjoiYTI4ODM2NzIxMDI4NTMzOWRmYzk5ZmE0YWUzNmI4ZTkiLCJzdWIiOjE2MTczNzV9.qz5KfbQyOvc' \
              'hxeEPnEO--faVgNn-8O-R4iiXSoilZc8qMDg2SIM7lY4QthQA3kDUIvdvOBSPb5Digbx49jgvOVaxgbLQbD1a' \
              'RaYpz0L_-uAwbusa6OHPIkmROz2qmMqRl8fBe-GzBT24HJowZEzEHd4rm7AlTzH5dDYVpeqCsqdmTWNkOWrgo8' \
              'FWnGsy9q3EP2bCAJchqN6h8M1XmC_1saoTXD51GxDaJtRiYVFtaDBvJwQkBQmfZdyjXRGraZ7Hv_KWu4PS7Yfs' \
              'NAy1asTs509d9kAvn_v1LBZjY1E33hFQa6BKdchHlis5-Gq5KuiznmfgFhCMvAxO1uAyWC6k9g'
product = 'other'


def five_sim_buy():
    phone = None
    num_id = None

    url_buy = f'https://{domain}/v1/user/buy/activation/russia/any/other'
    headers = {
        'Authorization': f'Bearer {apikey_base}',
        'Accept': 'application/json'
    }
    buy = requests.get(url_buy, headers=headers)
    try:
        phone = buy.json()['phone']
        num_id = buy.json()['id']
    except:
        pass
    # gr - +49, eng - +44, aus - +61, Lithuania - +370

    return phone, num_id


def five_sim_check(num_id):
    headers = {
        'Authorization': f'Bearer {apikey_base}',
        'Accept': 'application/json'
    }
    url_check = f'https://{domain}/v1/user/check/{num_id}'
    check = requests.get(url_check, headers=headers)

    try:
        sms_code = check.json()["sms"][0]["code"]
        return sms_code

    except:
        print("Код не пришел")
        return False
