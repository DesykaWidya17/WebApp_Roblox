"""
Simple Roblox web dashboard (Flask) with Docker integration.

Files generated when you run this script:
- roblox_webapp.py  (this file)
- Dockerfile
- requirements.txt
- docker-compose.yml

How it works:
- Web UI: visit http://localhost:5000/ and search a Roblox username
- API endpoint: /api/user/<username> returns JSON with basic user info and avatar URL

Run locally:
    python roblox_webapp.py

Build Docker image:
    docker build -t roblox-webapp .
    docker run -p 5000:5000 roblox-webapp

This single-file script writes the Dockerfile, requirements.txt and docker-compose.yml to disk
so you can build and run inside Docker without copying additional files.
"""

from flask import Flask, render_template_string, jsonify
import requests
import os

# ===================== HTML Frontend =====================
APP_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Roblox Web Dashboard</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 2rem; max-width: 900px; margin: auto; }
      input[type=text]{ padding: .5rem; width: 300px }
      button{ padding: .5rem 1rem }
      .card{ border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin-top: 1rem }
      img.avatar{ border-radius: 8px }
    </style>
  </head>
  <body>
    <h1>Roblox Web Dashboard</h1>
    <p>Masukkan username Roblox untuk melihat profil dasar.</p>
    <form id="searchForm" onsubmit="return searchUser();">
      <input id="username" type="text" placeholder="Roblox username" required />
      <button type="submit">Cari</button>
    </form>

    <div id="result"></div>

    <script>
      async function searchUser(){
        const u = document.getElementById('username').value.trim();
        if(!u) return false;
        const res = await fetch(`/api/user/${encodeURIComponent(u)}`);
        const data = await res.json();
        const container = document.getElementById('result');
        if(res.ok && data.found){
          container.innerHTML = `
            <div class="card">
              <h2>${data.username} (${data.userId})</h2>
              <img class="avatar" src="${data.avatar_url}" alt="avatar" width="150" height="150" />
              <p><strong>Created:</strong> ${data.created}</p>
              <p><a href="https://www.roblox.com/users/${data.userId}/profile" target="_blank">Open profile on Roblox</a></p>
            </div>`;
        } else {
          container.innerHTML = `<div class="card"><p>User not found or an error occurred.</p></div>`;
        }
        return false;
      }
    </script>
  </body>
</html>
"""

# ===================== Flask App =====================
app = Flask(__name__)

def fetch_user(username):
    """Fetch basic Roblox user data by username."""
    try:
        resp = requests.get(
            'https://api.roblox.com/users/get-by-username',
            params={'username': username},
            timeout=8
        )
        if resp.status_code != 200:
            return {'found': False, 'error': f'HTTP {resp.status_code}'}

        data = resp.json()
        if not data or 'Id' not in data or data.get('Id') == 0:
            return {'found': False}

        user_id = data['Id']
        username_real = data.get('Username', username)

        # Get creation date
        created = None
        try:
            details = requests.get(f'https://users.roblox.com/v1/users/{user_id}', timeout=8)
            if details.status_code == 200:
                jd = details.json()
                created = jd.get('created') or jd.get('createdDate')
        except Exception:
            pass

        avatar_url = f'https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png'

        return {
            'found': True,
            'username': username_real,
            'userId': user_id,
            'created': created,
            'avatar_url': avatar_url
        }

    except Exception as e:
        return {'found': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template_string(APP_HTML)

@app.route('/api/user/<username>')
def api_user(username):
    info = fetch_user(username)
    status = 200 if info.get('found') else 404
    return jsonify(info), status

# ===================== Docker Support =====================
DOCKERFILE = '''
# Dockerfile for Roblox Web Dashboard
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY roblox_webapp.py ./
EXPOSE 5000
ENV FLASK_ENV=production
CMD ["python", "roblox_webapp.py"]
'''

REQUIREMENTS = '''
Flask>=2.2
requests>=2.25
'''

DOCKER_COMPOSE = '''
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    restart: unless-stopped
'''

def ensure_supporting_files():
    created = []
    if not os.path.exists('Dockerfile'):
        with open('Dockerfile', 'w', encoding='utf-8') as f:
            f.write(DOCKERFILE)
        created.append('Dockerfile')
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(REQUIREMENTS)
        created.append('requirements.txt')
    if not os.path.exists('docker-compose.yml'):
        with open('docker-compose.yml', 'w', encoding='utf-8') as f:
            f.write(DOCKER_COMPOSE)
        created.append('docker-compose.yml')
    return created

if __name__ == '__main__':
    created = ensure_supporting_files()
    if created:
        print('Created supporting files:', ', '.join(created))
        print('You can build the Docker image with: docker build -t roblox-webapp .')
    else:
        print('Supporting files already exist.')

    # ✅ FIXED: Listen to all network interfaces so Jenkins can access it
    app.run(host='0.0.0.0', port=5000)
