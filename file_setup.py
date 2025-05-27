import requests
import os
import json

ACCESS_TOKEN = 'eUedV5ZCdxtdxFaPDetKDa4L1uR4cCf0'
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# ---- 1. Upload a new file ----
def upload_file(file_path, folder_id='0'):
    url = 'https://upload.box.com/api/2.0/files/content'
    file_name = os.path.basename(file_path)
    attributes = {
        'name': file_name,
        'parent': {'id': folder_id}
    }

    with open(file_path, 'rb') as file_stream:
        files = {
            'attributes': (None, json.dumps(attributes), 'application/json'),
            'file': (file_name, file_stream)
        }
        response = requests.post(url, headers=HEADERS, files=files)

    if response.status_code == 201:
        file_id = response.json()['entries'][0]['id']
        print(f'File uploaded successfully! File ID: {file_id}')
    else:
        print(f'Upload failed: {response.status_code} - {response.text}')

# ---- 2. Download a file ----
def download_file(file_id, output_path):
    url = f'https://api.box.com/2.0/files/{file_id}/content'
    response = requests.get(url, headers=HEADERS, stream=True)

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f'Downloaded to {output_path}')
    else:
        print(f'Error downloading: {response.text}')

# ---- 3. Update (upload new version) ----
def update_file(file_id, new_file_path):
    url = f'https://upload.box.com/api/2.0/files/{file_id}/content'
    file_name = new_file_path.split('/')[-1]

    with open(new_file_path, 'rb') as file_stream:
        files = {
            'file': (file_name, file_stream)
        }
        response = requests.post(url, headers=HEADERS, files=files)

    if response.status_code == 201:
        print('File updated successfully.')
    else:
        print(f'Error updating file: {response.text}')

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    test_file_path = os.path.join(desktop_path, "test.rtf")  # Change to your actual filename if different

    print("🔼 Uploading file...")
    upload_file(test_file_path)
