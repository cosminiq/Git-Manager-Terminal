#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Manager Web App - Flask Backend
Interfață web pentru gestionarea Git cu design de terminal Linux
"""

from flask import Flask, render_template, request, jsonify, session
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
import secrets

# Import GitManager class din scriptul original
import sys
sys.path.append('.')

class GitManagerWeb:
    def __init__(self):
        self.project_path = os.getcwd()
        
    def check_git_installation(self):
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            return True, "Git este instalat"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "Git nu este instalat"
    
    def check_git_repo(self):
        return os.path.exists('.git')
    
    def run_git_command(self, command):
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=self.project_path
            )
            return {
                'success': True,
                'output': result.stdout,
                'error': None
            }
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'output': None,
                'error': e.stderr if e.stderr else str(e)
            }
    
    def get_status(self):
        if not self.check_git_repo():
            return {
                'initialized': False,
                'files': [],
                'branch': None,
                'message': 'Repository nu este inițializat'
            }
        
        # Get status
        status_result = self.run_git_command(['git', 'status', '--porcelain'])
        files = []
        
        if status_result['success'] and status_result['output']:
            for line in status_result['output'].strip().split('\n'):
                if line.strip():
                    status = line[:2]
                    filename = line[3:]
                    
                    file_status = 'unknown'
                    icon = '📄'
                    
                    if status == '??':
                        file_status = 'untracked'
                        icon = '🆕'
                    elif status[0] == 'M':
                        file_status = 'modified_staged'
                        icon = '✅'
                    elif status[1] == 'M':
                        file_status = 'modified'
                        icon = '📝'
                    elif status[0] == 'A':
                        file_status = 'added'
                        icon = '➕'
                    elif status[0] == 'D':
                        file_status = 'deleted'
                        icon = '❌'
                    
                    files.append({
                        'name': filename,
                        'status': file_status,
                        'icon': icon
                    })
        
        # Get current branch
        branch_result = self.run_git_command(['git', 'branch', '--show-current'])
        current_branch = branch_result['output'].strip() if branch_result['success'] else 'main'
        
        return {
            'initialized': True,
            'files': files,
            'branch': current_branch,
            'message': 'Repository inițializat' if files else 'Working tree curat'
        }
    
    def initialize_repo(self):
        if self.check_git_repo():
            return {'success': False, 'message': 'Repository deja inițializat'}
        
        result = self.run_git_command(['git', 'init'])
        if result['success']:
            # Create .gitignore
            self.create_gitignore()
            return {'success': True, 'message': 'Repository inițializat cu succes'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def create_gitignore(self):
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# JavaScript/Node.js  
node_modules/
npm-debug.log*

# IDE
.vscode/
.idea/
*.swp
*~

# Sistema
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Config
.env
config.local.json

# Build
dist/
build/
"""
        try:
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            return True
        except:
            return False
    
    def add_files(self, files=None):
        if not self.check_git_repo():
            return {'success': False, 'message': 'Repository nu este inițializat'}
        
        if files is None or files == ['all']:
            result = self.run_git_command(['git', 'add', '.'])
        else:
            results = []
            for file in files:
                result = self.run_git_command(['git', 'add', file])
                results.append(result)
            # Return overall success
            result = {'success': all(r['success'] for r in results)}
        
        if result['success']:
            return {'success': True, 'message': 'Fișiere adăugate cu succes'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def commit_changes(self, message):
        if not message.strip():
            return {'success': False, 'message': 'Mesajul nu poate fi gol'}
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        full_message = f"{message} [{timestamp}]"
        
        result = self.run_git_command(['git', 'commit', '-m', full_message])
        
        if result['success']:
            # Get commit hash
            hash_result = self.run_git_command(['git', 'rev-parse', '--short', 'HEAD'])
            commit_hash = hash_result['output'].strip() if hash_result['success'] else 'unknown'
            
            return {
                'success': True, 
                'message': f'Commit realizat cu succes',
                'hash': commit_hash,
                'full_message': full_message
            }
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def get_commit_history(self, limit=10):
        if not self.check_git_repo():
            return {'success': False, 'commits': []}
        
        result = self.run_git_command([
            'git', 'log', '--oneline', '--graph', '--decorate', f'-{limit}'
        ])
        
        if result['success']:
            commits = []
            if result['output']:
                for line in result['output'].strip().split('\n'):
                    commits.append(line)
            return {'success': True, 'commits': commits}
        else:
            return {'success': False, 'commits': []}
    
    def get_branches(self):
        if not self.check_git_repo():
            return {'success': False, 'branches': []}
        
        result = self.run_git_command(['git', 'branch'])
        
        if result['success']:
            branches = []
            current = None
            
            for line in result['output'].strip().split('\n'):
                if line.strip():
                    if line.startswith('*'):
                        branch_name = line[2:].strip()
                        current = branch_name
                        branches.append({'name': branch_name, 'current': True})
                    else:
                        branch_name = line.strip()
                        branches.append({'name': branch_name, 'current': False})
            
            return {'success': True, 'branches': branches, 'current': current}
        else:
            return {'success': False, 'branches': []}
    
    def create_branch(self, branch_name):
        if not branch_name.strip():
            return {'success': False, 'message': 'Numele branch-ului nu poate fi gol'}
        
        result = self.run_git_command(['git', 'checkout', '-b', branch_name])
        
        if result['success']:
            return {'success': True, 'message': f'Branch {branch_name} creat și activat'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def switch_branch(self, branch_name):
        result = self.run_git_command(['git', 'checkout', branch_name])
        
        if result['success']:
            return {'success': True, 'message': f'Comutat pe branch-ul {branch_name}'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def setup_remote(self, remote_url):
        if not remote_url.strip():
            return {'success': False, 'message': 'URL-ul nu poate fi gol'}
        
        # Check existing remotes
        check_result = self.run_git_command(['git', 'remote', '-v'])
        
        if check_result['success'] and check_result['output']:
            # Remove existing origin
            self.run_git_command(['git', 'remote', 'remove', 'origin'])
        
        result = self.run_git_command(['git', 'remote', 'add', 'origin', remote_url])
        
        if result['success']:
            return {'success': True, 'message': 'Repository remote configurat'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def push_changes(self, first_push=False):
        if not self.check_git_repo():
            return {'success': False, 'message': 'Repository nu este inițializat'}
        
        # Check if remote exists
        remote_result = self.run_git_command(['git', 'remote', '-v'])
        if not remote_result['success'] or not remote_result['output']:
            return {'success': False, 'message': 'Nu este configurat repository remote'}
        
        # Get current branch
        branch_result = self.run_git_command(['git', 'branch', '--show-current'])
        current_branch = branch_result['output'].strip() if branch_result['success'] else 'main'
        
        if first_push:
            result = self.run_git_command(['git', 'push', '-u', 'origin', current_branch])
        else:
            result = self.run_git_command(['git', 'push'])
        
        if result['success']:
            return {'success': True, 'message': 'Modificări trimise pe server'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def pull_changes(self):
        result = self.run_git_command(['git', 'pull'])
        
        if result['success']:
            if "Already up to date" in result['output']:
                return {'success': True, 'message': 'Proiectul este deja la zi'}
            else:
                return {'success': True, 'message': 'Modificări descărcate și combinate'}
        else:
            return {'success': False, 'message': f'Eroare: {result["error"]}'}
    
    def quick_backup(self):
        if not self.check_git_repo():
            return {'success': False, 'message': 'Repository nu este inițializat'}
        
        # Check for changes
        status_result = self.run_git_command(['git', 'status', '--porcelain'])
        
        if not status_result['success']:
            return {'success': False, 'message': 'Nu se poate verifica status-ul'}
        
        if not status_result['output'] or not status_result['output'].strip():
            return {'success': True, 'message': 'Nu există modificări de salvat'}
        
        # Add all files
        add_result = self.run_git_command(['git', 'add', '.'])
        if not add_result['success']:
            return {'success': False, 'message': f'Eroare la adăugare: {add_result["error"]}'}
        
        # Commit with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Backup automat - {timestamp}"
        
        commit_result = self.run_git_command(['git', 'commit', '-m', commit_message])
        if not commit_result['success']:
            return {'success': False, 'message': f'Eroare la commit: {commit_result["error"]}'}
        
        # Try to push if remote exists
        remote_result = self.run_git_command(['git', 'remote', '-v'])
        if remote_result['success'] and remote_result['output']:
            push_result = self.run_git_command(['git', 'push'])
            if push_result['success']:
                return {'success': True, 'message': 'Backup complet realizat (local + server)'}
            else:
                return {'success': True, 'message': 'Backup local realizat (eroare la push)'}
        else:
            return {'success': True, 'message': 'Backup local realizat'}

# Flask App
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

git_manager = GitManagerWeb()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    git_installed, git_message = git_manager.check_git_installation()
    status = git_manager.get_status()
    
    return jsonify({
        'git_installed': git_installed,
        'git_message': git_message,
        'project_path': git_manager.project_path,
        **status
    })

@app.route('/api/init', methods=['POST'])
def api_init():
    result = git_manager.initialize_repo()
    return jsonify(result)

@app.route('/api/add', methods=['POST'])
def api_add():
    data = request.get_json()
    files = data.get('files', ['all'])
    result = git_manager.add_files(files)
    return jsonify(result)

@app.route('/api/commit', methods=['POST'])
def api_commit():
    data = request.get_json()
    message = data.get('message', '')
    result = git_manager.commit_changes(message)
    return jsonify(result)

@app.route('/api/history')
def api_history():
    limit = request.args.get('limit', 10, type=int)
    result = git_manager.get_commit_history(limit)
    return jsonify(result)

@app.route('/api/branches')
def api_branches():
    result = git_manager.get_branches()
    return jsonify(result)

@app.route('/api/branch/create', methods=['POST'])
def api_create_branch():
    data = request.get_json()
    branch_name = data.get('name', '')
    result = git_manager.create_branch(branch_name)
    return jsonify(result)

@app.route('/api/branch/switch', methods=['POST'])
def api_switch_branch():
    data = request.get_json()
    branch_name = data.get('name', '')
    result = git_manager.switch_branch(branch_name)
    return jsonify(result)

@app.route('/api/remote/setup', methods=['POST'])
def api_setup_remote():
    data = request.get_json()
    remote_url = data.get('url', '')
    result = git_manager.setup_remote(remote_url)
    return jsonify(result)

@app.route('/api/push', methods=['POST'])
def api_push():
    data = request.get_json()
    first_push = data.get('first_push', False)
    result = git_manager.push_changes(first_push)
    return jsonify(result)

@app.route('/api/pull', methods=['POST'])
def api_pull():
    result = git_manager.pull_changes()
    return jsonify(result)

@app.route('/api/backup', methods=['POST'])
def api_backup():
    result = git_manager.quick_backup()
    return jsonify(result)

if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Git Manager Web App pornește...")
    print("🌐 Accesează: http://localhost:5000")
    print("🛑 Pentru oprire: Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=5000)