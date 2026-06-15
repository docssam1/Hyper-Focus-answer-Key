"""
GFIELD HF — Drive 원본 문제 이미지 54개 → GitHub 업로드
실행: python hf_upload_problems.py
"""

import os
import base64
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── 설정 ──────────────────────────────────────────
CREDENTIALS_PATH = os.path.expanduser(
    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '~/gfield-drive-worker.json')
)
GITHUB_TOKEN  = os.environ['GITHUB_TOKEN']
GITHUB_REPO   = 'docssam1/Hyper-Focus-answer-Key'
GITHUB_BRANCH = 'main'
GITHUB_PATH   = 'premier-hyper-focus/assets/problems'

# ── Drive fileId 매핑 (typeId: fileId) ────────────────────
DRIVE_MAP = {
     1: '1URE_YndY7-9hANd96BH4QNORrjU202kT',
     2: '1izACmtZNjecfi1P8xCkp2pcrBEMT98bb',
     3: '1LUujCTkOWdHHFfONHDfyRi4KorzBmO6x',
     4: '1rLXIiAjUQ-XiMTDL1Jpk90lPCGngV6h0',
     5: '17l8AbFtGhRM0zsDvZKANAvv0lHSCJ7T_',
     6: '1OwhUDu-DFYd-K08ixW3A_CvPVUUvjvaH',
     7: '1QgdTacsWHuvzpU31nlAMmIr7sB8Qcm5S',
     8: '1YVvBgEAwW6Lzg2bEMG7ORgnhGz7KEAtF',
     9: '1-gChjOlE8hcVuw7yqBiTmYmB2WvzwCWa',
    10: '1peOvsjCTsA-BeiJMeLuYbg9ACZIobHK7',
    11: '1oX5OJf4h5oMwKvstXLIga3b080AVAYDo',
    12: '1Q2NbQDr6_mNfpobg5a0z2wzu25JLztO1',
    13: '1IKh1_EgM8KpFBGD6vTqFHkvGShF1GAzt',
    14: '1Vc-moAlNqGi6A88MfYsSKkpY4ExSCCGi',
    15: '1ucWa86phfmL_iFR-UwQinq9Mj8XCtDxq',
    16: '1sjD8nFuOTdA51nijGKejyXuhF_uli16D',
    17: '1ZQWPmVi6sLRseGiviS4liNuOqJS81Xbx',
    18: '14NkAN7rwVRd36BzFwI87KQvaLZOi4SR7',
    19: '15emsZRX6FTuJHAjYDb8xMLgoRZSk_Vz3',
    20: '1qeMtG4vYKM_8-S0nqfUzpl24rfXrPLYy',
    21: '1nnHs5-lCbB914ymglAdauKw36RszVVqn',
    22: '1obF_swj4tuePROxUqxvhezDhaejn9AZL',
    23: '1R2pGMMaopmE-ir_cJdB-5sqKQQIAtdmW',
    24: '1OzNZYQk2AwotJHmRZuSBkeiDHnLI19_I',
    25: '1Mav_S_Evba4OfjzopsxbTZ9HUkxndY-t',
    26: '1zLx1CeWma8i4ThrFP-lbVcfKlc809Dyb',
    27: '1onYEDehOA040OUrxjkhd88wuWOymja_p',
    28: '14DTP93BfWlzhzTZqp0sfyJw2z5cf-BP2',
    29: '1-cCfOhtEaOSGAID4j3ujtlzc-u0T-teQ',
    30: '1pr6OQlEtTEdfT3AhzOMIni2lgmUJPI8B',
    31: '1QHDLFBHxJ3ZMpG8av7kTrrEVuuPiQXG2',
    32: '1HJ1BXbJt441jW_kgfruEW81qISajwZiA',
    33: '1oybK_PW7wzwERmRLkJxKusSuJX3JNvyH',
    34: '1me4pJB1-XySYsTq0-kmmP-8I_L8SvYC4',
    35: '1GxblME6K2H6QVizDzF20WQu6OoEfr5Tv',
    36: '10a9qma7ecq-RTfOiuxfvtkkfA74pJLNQ',
    37: '1wxe-sMOmsqmRaVmt7knssJ5Vul6Bzq-V',
    38: '1fp6tmM8pJE-AIHDQx2jMjbTaJ6AdTWet',
    39: '1l6LFbQgaFVZ0PZd8b2ZGUccLdWJ72DkB',
    40: '1jyq6cV-FDaLAWpWMlwfVT8oiKWpqaXjE',
    41: '1rc3XkdZIufL6xUIhqjFCE9GGxU-GiEUt',
    42: '1ro7065of9eZPg2u6UF3AFkDTFXj9rDh2',
    43: '10emBJXn5FSndzFFyIIcZpCy2Dcil_RpX',
    44: '1flm4Q08JTE3yT9woIB1OwPgaRbDo29vy',
    45: '1_T4-D1vkMIgLhlig08vr6lvGFZ_MyGcp',
    46: '1c9ZqhvHYV2X8RjtxpdsV3A0fouFU7O-7',
    47: '1U6It45KgDZqF5HmLBAY42a_8Nwk0CDyU',
    48: '1R2h6plhDbI2gpCImRk-7jkMB2tLE_gHs',
    49: '1ay481B1zpKQI0tMpbUUn8R9QOWeqOgtA',
    50: '11UZmF4_Vw5hU0n4_vXNS160TtKN4uLtV',
    51: '14Y2VL5PbNnsuamQNonPM6TuorTfJw4rS',
    52: '1lCDo4qMt0EoIV3sd1Zkye67oG81X333W',
    53: '15nM0anVqi7Pt8yzyDb8zsqngqp4HD7Jz',
    54: '1UnRZqp0vS1ZRZPW1hxQV_SHAXCgnYPgC',
}


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    return build('drive', 'v3', credentials=creds)


def download_image(service, file_id):
    return service.files().get_media(fileId=file_id).execute()


def upload_to_github(path, image_bytes, message):
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{path}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {'message': message, 'content': b64, 'branch': GITHUB_BRANCH}
    if sha:
        data['sha'] = sha
    r = requests.put(url, headers=headers, json=data)
    if r.status_code in [200, 201]:
        print(f'  ✅ {path}')
    else:
        print(f'  ❌ {path} — {r.status_code}: {r.text[:100]}')


def main():
    print('Drive 연결 중...')
    service = get_drive_service()
    print(f'{len(DRIVE_MAP)}개 업로드 시작\n')

    for type_id, file_id in sorted(DRIVE_MAP.items()):
        github_path = f'{GITHUB_PATH}/{type_id:02d}.png'
        print(f'[{type_id:02d}] 다운로드 중...')
        try:
            image_bytes = download_image(service, file_id)
            upload_to_github(
                github_path,
                image_bytes,
                f'add: 원본 문제 이미지 {type_id:02d}.png'
            )
        except Exception as e:
            print(f'  ❌ 오류: {e}')

    print('\n완료!')


if __name__ == '__main__':
    main()
