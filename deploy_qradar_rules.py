import os
import glob
import json
import requests
import urllib3

# Self-signed SSL sertifikat xəbərdarlığını söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = os.environ.get("QRADAR_HOST")
SEC_TOKEN = os.environ.get("QRADAR_SEC_TOKEN")

if not QRADAR_HOST or not SEC_TOKEN:
    print("[!] Xəta: QRADAR_HOST və ya QRADAR_SEC_TOKEN tapılmadı!")
    exit(1)

headers = {
    'SEC': SEC_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# rules/ qovluğundakı bütün .json fayllarını oxuyuruq
rule_files = glob.glob('rules/*.json')

print(f"[*] Cəmi {len(rule_files)} QRadar rule faylı tapıldı.")

for file_path in rule_files:
    print(f"[*] İşlənilir: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            rule_data = json.load(f)
        
        # QRadar Custom Rules API Endpoint
        url = f"https://{QRADAR_HOST}/api/analytics/custom_rules"
        
        response = requests.post(url, headers=headers, json=rule_data, verify=False, timeout=15)
        
        if response.status_code in [200, 201]:
            print(f"[+] {file_path} uğurla QRadar-a yükləndi.")
        else:
            print(f"[-] {file_path} yüklənərkən xəta oldu! Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[!] Xəta baş verdi ({file_path}): {str(e)}")
