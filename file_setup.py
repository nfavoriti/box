import requests
import os
import json

ACCESS_TOKEN = 'u2q5TSfBzmgDWc1utBnIUNSO2PHr03qu'
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


def get_file_id_by_name(folder_id='0', target_filename='test.docx'):
    url = f'https://api.box.com/2.0/folders/{folder_id}/items'
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        items = response.json().get('entries', [])
        for item in items:
            if item['type'] == 'file' and item['name'] == target_filename:
                print(f"Found file: {item['name']} (ID: {item['id']})")
                return item['id']
        print(f"File '{target_filename}' not found in folder {folder_id}.")
        return None
    else:
        print(f"Failed to list files: {response.status_code} - {response.text}")
        return None


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


def recursively_access_files(folder_id='0', local_base_path='box_downloads'):
    os.makedirs(local_base_path, exist_ok=True)
    
    url = f'https://api.box.com/2.0/folders/{folder_id}/items'
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"[ERROR] Failed to list folder {folder_id}: {response.status_code}")
        return

    items = response.json().get('entries', [])
    
    for item in items:
        if item['type'] == 'folder':
            # Recurse into subfolder
            new_local_path = os.path.join(local_base_path, item['name'])
            recursively_access_files(item['id'], new_local_path)
        elif item['type'] == 'file':
            local_file_path = os.path.join(local_base_path, item['name'])
            if os.path.exists(local_file_path):
                print(f"[SKIP] {item['name']} already exists in {local_base_path}")
            else:
                print(f"[⬇️  DOWNLOAD] {item['name']} to {local_file_path}")
                download_file(item['id'], local_file_path)


if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    test_file_path = os.path.join(desktop_path, "test_upload.rtf") 

    print("🔼 Uploading file...")
    upload_file(test_file_path)

# if __name__ == "__main__":
#     desktop_path = os.path.expanduser("~/Desktop")
#     output_file_path = os.path.join(desktop_path, "test_downloaded.docx")
    
#     file_id = get_file_id_by_name(folder_id='0', target_filename='test.docx')
    
#     if file_id:
#         download_file(file_id, output_file_path)
