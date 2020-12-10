import requests


def upload_resume(resume, url, token):
    files = {
        "file": resume,
    }
    print(files)
    headers = {
        "Authorization": "Token " + token,
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryyrV7KO0BoCBuDbTL"
    }

    res = requests.put(url, files=files, headers=headers)

    return res
