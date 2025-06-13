#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Manager - Script pentru gestionarea versiunilor cu Git
Creat pentru proiecte web (Python + JavaScript + HTML + CSS)
Autor: Asistent AI | Data: 2025

EXPLICAȚII FUNDAMENTALE DESPRE GIT:
===================================

Git este un sistem de control al versiunilor care îți permite să:
1. Salvezi "instantanee" (snapshot-uri) ale proiectului la diferite momente
2. Urmărești toate modificările făcute în cod
3. Revii la versiuni anterioare dacă ceva se strică
4. Colaborezi cu alți developeri
5. Creezi "ramuri" (branches) pentru funcționalități noi

CONCEPTE CHEIE:
- Repository (repo): Folderul care conține proiectul și istoricul Git
- Commit: Un "snapshot" al proiectului la un moment dat
- Staging area: Zona unde pregătești fișierele pentru commit
- Branch: O ramură de dezvoltare (implicit ai "main" sau "master")
- Remote: Repository-ul de pe server (ex: GitHub, GitLab)

WORKFLOW STANDARD:
1. Modifici fișierele în proiect
2. Adaugi fișierele în staging area (git add)
3. Creezi un commit cu aceste modificări (git commit)
4. Trimiți commit-urile pe server (git push)
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import json

class GitManager:
    def __init__(self):
        self.project_path = os.getcwd()
        self.git_version = None         
        self.git_config = None          
        self.git_exists = self.check_git_installation()
        self.repo_initialized = self.check_git_repo()



    def check_git_installation(self):
        """Verifică dacă Git este instalat în sistem și obține informații detaliate"""
        try:
            # Verifică versiunea Git
            result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
            self.git_version = result.stdout.strip()
            
            # Obține configurația Git
            self.git_config = {}
            try:
                name_result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                        capture_output=True, text=True)
                self.git_config['name'] = name_result.stdout.strip() if name_result.returncode == 0 else "Nu este configurat"
                
                email_result = subprocess.run(['git', 'config', '--global', 'user.email'], 
                                            capture_output=True, text=True)
                self.git_config['email'] = email_result.stdout.strip() if email_result.returncode == 0 else "Nu este configurat"
            except:
                self.git_config = {'name': 'Nu se poate accesa', 'email': 'Nu se poate accesa'}
            
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.git_version = None
            self.git_config = None
            return False

    def display_git_info(self):
        """Afișează informații detaliate despre Git și ghid de instalare"""
        print("\n" + "="*80)
        print("🔍 VERIFICAREA INSTALĂRII GIT")
        print("="*80)
        
        if self.git_exists:
            print("✅ Git este instalat și funcțional!")
            print(f"📦 {self.git_version}")
            
            print(f"\n👤 Configurația globală:")
            print(f"   Nume: {self.git_config['name']}")
            print(f"   Email: {self.git_config['email']}")
            
            if self.git_config['name'] == "Nu este configurat" or self.git_config['email'] == "Nu este configurat":
                print("\n⚠️  RECOMANDARE: Configurează numele și email-ul pentru Git!")
                print("   Aceasta se va face automat la prima inițializare a repository-ului.")
            
            print(f"\n🎯 Git este gata de utilizare!")
            
        else:
            print("❌ Git NU este instalat pe sistem!")
            print("\n📥 GHID DE INSTALARE GIT:")
            print("-" * 40)
            print("🖥️  Pentru Windows:")
            print("   1. Descarcă de la: https://git-scm.com/download/win")
            print("   2. Rulează installer-ul descărcat")
            print("   3. Urmează pașii din wizard (setările default sunt OK)")
            print("   4. Restart terminal/command prompt după instalare")
            
            print("\n🐧 Pentru Linux (Ubuntu/Debian):")
            print("   sudo apt update && sudo apt install git")
            
            print("\n🐧 Pentru Linux (CentOS/RHEL):")
            print("   sudo yum install git")
            
            print("\n🍎 Pentru macOS:")
            print("   1. Descarcă de la: https://git-scm.com/download/mac")
            print("   2. SAU folosește Homebrew: brew install git")
            print("   3. SAU instalează Xcode Command Line Tools: xcode-select --install")
            
            print("\n✅ După instalare:")
            print("   1. Restart terminal-ul")
            print("   2. Testează cu: git --version")
            print("   3. Rulează din nou acest script")
            
            print("\n🎓 Pentru începători:")
            print("   - Git este gratuit și open source")
            print("   - Este standardul industriei pentru controlul versiunilor")
            print("   - Funcționează pe toate sistemele de operare")
            print("   - Este folosit de milioane de developeri mondial")
            
            print("\n🔗 Resurse utile:")
            print("   📖 Documentația oficială: https://git-scm.com/docs")
            print("   🎬 Tutorial video: https://www.youtube.com/watch?v=8JJ101D3knE")
            print("   📚 Carte gratuită: https://git-scm.com/book")
            
            return False
        
        print("="*80)
        return True
    
    def check_git_repo(self):
        """Verifică dacă directorul curent este un repository Git"""
        return os.path.exists('.git')
    
    def run_git_command(self, command, show_output=True):
        """
        Execută o comandă Git și returnează rezultatul
        
        Args:
            command (list): Comanda Git ca listă de stringuri
            show_output (bool): Dacă să afișeze output-ul comenzii
        
        Returns:
            tuple: (success, output, error)
        """
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=self.project_path
            )
            if show_output and result.stdout:
                print(f"✅ Succes: {result.stdout}")
            return True, result.stdout, None
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            if show_output:
                print(f"❌ Eroare: {error_msg}")
            return False, None, error_msg
    
    def display_header(self):
        """Afișează header-ul aplicației"""
        print("\n" + "="*80)
        print("🚀 GIT MANAGER - GESTIONAREA VERSIUNILOR PENTRU PROIECTUL TĂU WEB")
        print("="*80)
        print(f"📁 Directorul curent: {self.project_path}")
        print(f"📊 Status Git: {'✅ Repository inițializat' if self.repo_initialized else '❌ Repository neinițializat'}")
        print(f"🔧 Git instalat: {'✅ Da' if self.git_exists else '❌ Nu'}")
        print("="*80)
    
    def show_git_status(self):
        """
        EXPLICAȚIE: 'git status' îți arată starea curentă a proiectului:
        - Ce fișiere au fost modificate
        - Ce fișiere sunt pregătite pentru commit (staged)
        - Ce fișiere nu sunt urmărite de Git (untracked)
        """
        print("\n📊 STATUS CURENT AL REPOSITORY-ULUI:")
        print("-" * 50)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        success, output, error = self.run_git_command(['git', 'status', '--porcelain'])
        
        if success:
            if not output:
                print("✅ Nu există modificări. Proiectul este curat!")
            else:
                print("📝 Fișiere modificate:")
                lines = output.strip().split('\n')
                for line in lines:
                    status = line[:2]
                    filename = line[3:]
                    
                    if status == '??':
                        print(f"  🆕 {filename} (fișier nou, neadăugat)")
                    elif status[0] == 'M':
                        print(f"  ✏️  {filename} (modificat și staged)")
                    elif status[1] == 'M':
                        print(f"  📝 {filename} (modificat, dar nu staged)")
                    elif status[0] == 'A':
                        print(f"  ➕ {filename} (adăugat pentru commit)")
                    elif status[0] == 'D':
                        print(f"  ❌ {filename} (șters)")
        
        # Afișează și branch-ul curent
        success, branch_output, _ = self.run_git_command(['git', 'branch', '--show-current'], False)
        if success and branch_output:
            print(f"\n🌿 Branch curent: {branch_output.strip()}")
    
    def initialize_repository(self):
        """
        EXPLICAȚIE: Inițializarea unui repository Git
        
        Această operație creează folderul .git în directorul curent,
        care va conține toate informațiile despre versiuni.
        Se face o singură dată pentru fiecare proiect.
        """
        print("\n🚀 INIȚIALIZAREA REPOSITORY-ULUI GIT")
        print("-" * 40)
        
        if self.repo_initialized:
            print("⚠️  Repository-ul este deja inițializat!")
            return
        
        print("📖 Se inițializează un repository Git nou...")
        print("   Aceasta va crea folderul .git pentru urmărirea versiunilor.")
        
        success, output, error = self.run_git_command(['git', 'init'])
        
        if success:
            self.repo_initialized = True
            print("\n✅ Repository Git inițializat cu succes!")
            
            # Configurare inițială
            print("\n🔧 Configurare inițială Git:")
            name = input("👤 Introdu numele tău (pentru commits): ").strip()
            email = input("📧 Introdu email-ul tău: ").strip()
            
            if name:
                self.run_git_command(['git', 'config', 'user.name', name], False)
            if email:
                self.run_git_command(['git', 'config', 'user.email', email], False)
            
            print("\n📝 Se creează fișierul .gitignore pentru proiectul web...")
            self.create_gitignore()
        else:
            print(f"❌ Eroare la inițializarea repository-ului: {error}")
    
    def create_gitignore(self):
        """
        EXPLICAȚIE: .gitignore
        
        Fișierul .gitignore spune Git-ului ce fișiere să ignore.
        Pentru proiecte web, de obicei ignorăm:
        - Fișiere temporare
        - Dependințe (node_modules, __pycache__)
        - Fișiere de configurare locale
        - Logs și fișiere de sistem
        """
        gitignore_content = """# Fișiere Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Fișiere JavaScript/Node.js  
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Fișiere IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Fișiere sistem
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Fișiere temporare
*.tmp
*.temp

# Fișiere de configurare locale
.env
config.local.json

# Build outputs
dist/
build/
"""
        
        try:
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("✅ Fișierul .gitignore a fost creat!")
        except Exception as e:
            print(f"⚠️  Nu am putut crea .gitignore: {e}")
    
    def add_files(self):
        """
        EXPLICAȚIE: git add
        
        Comanda 'git add' adaugă fișierele în "staging area" - 
        zona unde pregătești modificările pentru a fi salvate.
        
        Opțiuni:
        - git add . (adaugă toate fișierele modificate)
        - git add <nume_fișier> (adaugă un fișier specific)
        """
        print("\n➕ ADĂUGAREA FIȘIERELOR PENTRU COMMIT")
        print("-" * 45)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        print("📖 Opțiuni pentru adăugarea fișierelor:")
        print("1. Adaugă toate fișierele modificate (git add .)")
        print("2. Adaugă fișiere specifice")
        print("3. Vizualizează fișierele modificate întâi")
        
        choice = input("\n🔢 Alege opțiunea (1-3): ").strip()
        
        if choice == '1':
            print("\n📦 Se adaugă toate fișierele modificate...")
            success, output, error = self.run_git_command(['git', 'add', '.'])
            if success:
                print("✅ Toate fișierele au fost adăugate în staging area!")
            
        elif choice == '2':
            # Afișează fișierele disponibile
            success, output, error = self.run_git_command(['git', 'status', '--porcelain'], False)
            if success and output:
                print("\n📝 Fișiere modificate disponibile:")
                files = []
                for line in output.strip().split('\n'):
                    filename = line[3:]
                    files.append(filename)
                    print(f"  - {filename}")
                
                file_input = input("\n📁 Introdu numele fișierelor (separate prin spațiu): ")
                files_to_add = file_input.strip().split()
                
                for filename in files_to_add:
                    success, _, error = self.run_git_command(['git', 'add', filename])
                    if success:
                        print(f"✅ {filename} adăugat!")
                    else:
                        print(f"❌ Eroare la {filename}: {error}")
        
        elif choice == '3':
            self.show_git_status()
            input("\nApasă Enter pentru a continua...")
    
    def commit_changes(self):
        """
        EXPLICAȚIE: git commit
        
        Un commit este ca o "fotografie" a proiectului la un moment dat.
        Fiecare commit are:
        - Un mesaj descriptiv (ce ai modificat)
        - Un hash unic (identificator)
        - Data și autorul
        - Toate modificările incluse
        
        Mesajul de commit ar trebui să fie clar și descriptiv!
        """
        print("\n💾 SALVAREA MODIFICĂRILOR (COMMIT)")
        print("-" * 40)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        # Verifică dacă există fișiere în staging area
        success, output, error = self.run_git_command(['git', 'diff', '--cached', '--name-only'], False)
        
        if not success or not output:
            print("⚠️  Nu există fișiere pregătite pentru commit!")
            print("💡 Folosește opțiunea 'Adaugă fișiere' întâi.")
            return
        
        print("📝 Fișiere pregătite pentru commit:")
        for filename in output.strip().split('\n'):
            print(f"  ✅ {filename}")
        
        print("\n📖 Exemple de mesaje bune de commit:")
        print("  - 'Adaugă funcționalitatea de login'")
        print("  - 'Corectează bug-ul din calculatorul de preț'") 
        print("  - 'Îmbunătățește design-ul paginii principale'")
        print("  - 'Adaugă validare pentru formularul de contact'")
        
        message = input("\n✏️  Introdu mesajul pentru commit: ").strip()
        
        if not message:
            print("❌ Mesajul nu poate fi gol!")
            return
        
        # Adaugă timestamp pentru mesaj
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        full_message = f"{message} [{timestamp}]"
        
        success, output, error = self.run_git_command(['git', 'commit', '-m', full_message])
        
        if success:
            print(f"\n🎉 Commit realizat cu succes!")
            print(f"📝 Mesaj: {full_message}")
            
            # Afișează hash-ul commit-ului
            success, hash_output, _ = self.run_git_command(['git', 'rev-parse', '--short', 'HEAD'], False)
            if success:
                print(f"🔐 Hash commit: {hash_output.strip()}")
        else:
            print(f"❌ Eroare la commit: {error}")
    
    def view_commit_history(self):
        """
        EXPLICAȚIE: git log
        
        Istoricul commit-urilor îți arată toate "fotografiile" 
        salvate ale proiectului, în ordine cronologică inversă.
        """
        print("\n📚 ISTORICUL COMMIT-URILOR")
        print("-" * 35)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        print("🔍 Opțiuni pentru vizualizarea istoricului:")
        print("1. Ultimele 10 commit-uri (format compact)")
        print("2. Ultimele 5 commit-uri (format detaliat)")
        print("3. Toate commit-urile (format compact)")
        
        choice = input("\n🔢 Alege opțiunea (1-3): ").strip()
        
        if choice == '1':
            success, output, error = self.run_git_command([
                'git', 'log', '--oneline', '--graph', '--decorate', '-10'
            ])
        elif choice == '2':
            success, output, error = self.run_git_command([
                'git', 'log', '--graph', '--pretty=format:%h - %an, %ar : %s', '-5'
            ])
        elif choice == '3':
            success, output, error = self.run_git_command([
                'git', 'log', '--oneline', '--graph', '--decorate'
            ])
            
        if not success:
            print("❌ Nu s-a putut afișa istoricul. Poate nu există commit-uri încă?")
    
    def create_branch(self):
        """
        EXPLICAȚIE: git branch
        
        Branch-urile (ramurile) îți permit să lucrezi la funcționalități
        noi fără să afectezi codul principal. 
        
        Workflow tipic:
        1. Creezi un branch nou pentru o funcționalitate
        2. Lucrezi pe acel branch
        3. Când termini, îl combini înapoi în main (merge)
        """
        print("\n🌿 CREAREA UNUI BRANCH NOU")
        print("-" * 32)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        # Afișează branch-urile existente
        success, output, error = self.run_git_command(['git', 'branch'], False)
        if success:
            print("🌿 Branch-uri existente:")
            for line in output.strip().split('\n'):
                if line.strip():
                    current = "👉" if line.startswith('*') else "  "
                    print(f"{current} {line.strip()}")
        
        print("\n📖 Exemple de nume pentru branch-uri:")
        print("  - feature/login-system")
        print("  - bugfix/calculator-error") 
        print("  - improvement/ui-design")
        print("  - hotfix/security-patch")
        
        branch_name = input("\n🏷️  Introdu numele noului branch: ").strip()
        
        if not branch_name:
            print("❌ Numele branch-ului nu poate fi gol!")
            return
        
        # Creează și comută pe noul branch
        success1, _, error1 = self.run_git_command(['git', 'checkout', '-b', branch_name])
        
        if success1:
            print(f"✅ Branch-ul '{branch_name}' a fost creat și activat!")
            print("💡 Acum lucrezi pe noul branch. Toate commit-urile vor fi pe acesta.")
        else:
            print(f"❌ Eroare la crearea branch-ului: {error1}")
    
    def switch_branch(self):
        """
        EXPLICAȚIE: git checkout
        
        Comută între branch-uri existente.
        Când comuti pe un branch, fișierele din proiect
        se schimbă pentru a reflecta starea acelui branch.
        """
        print("\n🔄 COMUTAREA ÎNTRE BRANCH-URI")
        print("-" * 35)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        # Afișează branch-urile disponibile
        success, output, error = self.run_git_command(['git', 'branch'], False)
        
        if not success or not output:
            print("❌ Nu s-au putut afișa branch-urile!")
            return
        
        branches = []
        current_branch = None
        
        print("🌿 Branch-uri disponibile:")
        for line in output.strip().split('\n'):
            if line.strip():
                if line.startswith('*'):
                    branch_name = line[2:].strip()
                    current_branch = branch_name
                    print(f"  👉 {branch_name} (curent)")
                else:
                    branch_name = line.strip()
                    print(f"     {branch_name}")
                branches.append(branch_name)
        
        if len(branches) <= 1:
            print("⚠️  Există doar un branch. Creează mai întâi un branch nou!")
            return
        
        target_branch = input(f"\n🎯 Pe care branch vrei să comuti? ").strip()
        
        if target_branch == current_branch:
            print(f"⚠️  Ești deja pe branch-ul '{target_branch}'!")
            return
        
        if target_branch not in branches:
            print(f"❌ Branch-ul '{target_branch}' nu există!")
            return
        
        success, output, error = self.run_git_command(['git', 'checkout', target_branch])
        
        if success:
            print(f"✅ Ai comutat pe branch-ul '{target_branch}'!")
        else:
            print(f"❌ Eroare la comutare: {error}")
    
    def setup_remote_repository(self):
        """
        EXPLICAȚIE: Remote repository
        
        Un remote repository este o copie a proiectului pe un server
        (GitHub, GitLab, etc.). Îți permite să:
        - Faci backup online
        - Colaborezi cu alții
        - Accesezi proiectul de pe orice device
        """
        print("\n🌐 CONFIGURAREA REPOSITORY-ULUI REMOTE")
        print("-" * 45)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        # Verifică dacă există deja un remote
        success, output, error = self.run_git_command(['git', 'remote', '-v'], False)
        
        if success and output:
            print("🔗 Repository-uri remote existente:")
            print(output)
            
            overwrite = input("\n🤔 Vrei să schimbi repository-ul remote? (y/n): ").lower()
            if overwrite != 'y':
                return
        
        print("\n📖 Pentru a configura un remote repository:")
        print("1. Creează un repository nou pe GitHub/GitLab")
        print("2. Copiază URL-ul repository-ului (HTTPS sau SSH)")
        print("3. Nu inițializa cu README dacă ai deja fișiere locale")
        
        print("\n🔗 Exemple de URL-uri:")
        print("  HTTPS: https://github.com/username/repository-name.git")
        print("  SSH:   git@github.com:username/repository-name.git")
        
        remote_url = input("\n🌐 Introdu URL-ul repository-ului remote: ").strip()
        
        if not remote_url:
            print("❌ URL-ul nu poate fi gol!")
            return
        
        # Adaugă remote-ul
        success, output, error = self.run_git_command(['git', 'remote', 'add', 'origin', remote_url])
        
        if success:
            print("✅ Repository-ul remote a fost configurat!")
            
            # Întreabă dacă vrea să facă primul push
            push_now = input("\n🚀 Vrei să trimiți proiectul pe server acum? (y/n): ").lower()
            if push_now == 'y':
                self.push_to_remote(first_push=True)
        else:
            print(f"❌ Eroare la configurarea remote-ului: {error}")
    
    def push_to_remote(self, first_push=False):
        """
        EXPLICAȚIE: git push
        
        Trimite commit-urile locale pe repository-ul remote.
        Aceasta face backup și sincronizează modificările cu serverul.
        """
        print(f"\n🚀 {'PRIMUL PUSH PE SERVER' if first_push else 'TRIMITEREA MODIFICĂRILOR PE SERVER'}")
        print("-" * 50)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        # Verifică dacă există remote
        success, output, error = self.run_git_command(['git', 'remote', '-v'], False)
        if not success or not output:
            print("❌ Nu este configurat niciun repository remote!")
            print("💡 Folosește opțiunea 'Configurare repository remote' întâi.")
            return
        
        # Obține branch-ul curent
        success, branch_output, error = self.run_git_command(['git', 'branch', '--show-current'], False)
        current_branch = branch_output.strip() if success else 'main'
        
        if first_push:
            print("📤 Se face primul push și se setează branch-ul ca upstream...")
            command = ['git', 'push', '-u', 'origin', current_branch]
        else:
            print(f"📤 Se trimit modificările pe branch-ul '{current_branch}'...")
            command = ['git', 'push']
        
        success, output, error = self.run_git_command(command)
        
        if success:
            print("🎉 Modificările au fost trimise cu succes pe server!")
            if first_push:
                print("✅ Branch-ul a fost setat ca upstream.")
        else:
            print(f"❌ Eroare la push: {error}")
            if "failed to push" in error.lower():
                print("\n💡 Posibile soluții:")
                print("  - Verifică dacă ai permisiuni pe repository")
                print("  - Poate ai nevoie să faci 'git pull' întâi")
    
    def pull_from_remote(self):
        """
        EXPLICAȚIE: git pull
        
        Descarcă și combină modificările de pe server cu cele locale.
        Util când lucrezi în echipă sau de pe mai multe device-uri.
        """
        print("\n📥 DESCĂRCAREA MODIFICĂRILOR DE PE SERVER")
        print("-" * 45)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        success, output, error = self.run_git_command(['git', 'pull'])
        
        if success:
            if "Already up to date" in output:
                print("✅ Proiectul este deja la zi!")
            else:
                print("🔄 Modificările au fost descărcate și combinate!")
        else:
            print(f"❌ Eroare la pull: {error}")
    
    def show_project_structure(self):
        """Afișează structura proiectului pentru a înțelege ce fișiere există"""
        print("\n📁 STRUCTURA PROIECTULUI")
        print("-" * 30)
        
        def show_tree(path, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return
            
            try:
                items = sorted(os.listdir(path))
                dirs = [item for item in items if os.path.isdir(os.path.join(path, item)) and not item.startswith('.')]
                files = [item for item in items if os.path.isfile(os.path.join(path, item)) and not item.startswith('.')]
                
                # Afișează directoarele
                for i, directory in enumerate(dirs):
                    is_last = (i == len(dirs) - 1) and len(files) == 0
                    print(f"{prefix}{'└── ' if is_last else '├── '}📁 {directory}/")
                    
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    show_tree(os.path.join(path, directory), new_prefix, max_depth, current_depth + 1)
                
                # Afișează fișierele
                for i, file in enumerate(files):
                    is_last = i == len(files) - 1
                    
                    # Iconițe pentru diferite tipuri de fișiere
                    if file.endswith(('.py',)):
                        icon = "🐍"
                    elif file.endswith(('.html', '.htm')):
                        icon = "🌐"
                    elif file.endswith(('.css',)):
                        icon = "🎨"
                    elif file.endswith(('.js',)):
                        icon = "⚡"
                    elif file.endswith(('.json',)):
                        icon = "📋"
                    elif file.endswith(('.md',)):
                        icon = "📝"
                    elif file.endswith(('.git')):
                        continue  # Skip .git files
                    else:
                        icon = "📄"
                    
                    print(f"{prefix}{'└── ' if is_last else '├── '}{icon} {file}")
                        
            except PermissionError:
                print(f"{prefix}❌ Acces interzis")
        
        print(f"📁 {os.path.basename(self.project_path)}/")
        show_tree(self.project_path)
        
        print(f"\n📊 Repository Git: {'✅ Inițializat' if self.repo_initialized else '❌ Neinițializat'}")
    
    def show_help(self):
        """Afișează ghidul complet pentru Git"""
        help_text = """
🎓 GHID COMPLET GIT PENTRU ÎNCEPĂTORI
=====================================

🔹 CE ESTE GIT?
Git este un sistem de control al versiunilor - ca un "Time Machine" pentru codul tău.
Îți permite să salvezi diferite versiuni ale proiectului și să revii la ele oricând.

🔹 WORKFLOW STANDARD:
1. 📝 Modifici fișierele în proiect
2. ➕ Adaugi fișierele în "staging area" (git add)
3. 💾 Creezi un "commit" - salvezi o versiune (git commit)
4. 🚀 Trimiți pe server pentru backup (git push)

🔹 CONCEPTE CHEIE:

📦 REPOSITORY (REPO):
- Folderul care conține proiectul + istoricul Git
- Se creează cu "git init"

💾 COMMIT:
- O "fotografie" a proiectului la un moment dat
- Are mesaj descriptiv, dată, autor
- Hash unic pentru identificare

🌿 BRANCH:
- "Ramuri" de dezvoltare paralele
- "main/master" = ramura principală
- Creezi branch-uri pentru funcționalități noi

🌐 REMOTE:
- Repository pe server (GitHub, GitLab)
- Backup online + colaborare
- Se sincronizează cu "push" și "pull"

🔹 COMENZI PRINCIPALE:

git init          → Inițializează repository
git add .         → Adaugă toate fișierele modificate
git commit -m     → Salvează o versiune cu mesaj
git status        → Arată ce s-a modificat
git log           → Afișează istoricul commit-urilor
git push          → Trimite pe server
git pull          → Descarcă de pe server
git branch        → Gestionează branch-uri
git checkout      → Comută între branch-uri

🔹 SFATURI PENTRU MESAJE DE COMMIT:
✅ Bune: "Adaugă funcția de login", "Corectează bug în calculator"
❌ Rele: "Update", "Fix", "Changes"

🔹 FIȘIERUL .gitignore:
Spune Git-ului ce să ignore (fișiere temporare, cache, etc.)

🔹 CÂND SĂ FACI COMMIT:
- După fiecare funcționalitate completă
- Înainte de modificări majore
- La sfârșitul zilei de lucru
- Când ceva funcționează bine

🔹 BEST PRACTICES:
- Commit-uri mici și frecvente
- Mesaje descriptive
- Testează înainte de commit
- Folosește branch-uri pentru experimente
- Fă backup regulat cu push

🔹 CAZURI DE URGENȚĂ:
- Dacă strici ceva: "git checkout -- <fișier>"
- Pentru a vedea diferențele: "git diff"
- Pentru a reveni la commit anterior: "git reset"



🎨 Indicatorii Git în VS Code:
Litere (Status):

U = Untracked (🆕 Fișier nou, neadăugat în Git)
M = Modified (✏️ Fișier modificat față de ultimul commit)
A = Added (➕ Fișier nou adăugat în staging area)
D = Deleted (❌ Fișier șters)
R = Renamed (🔄 Fișier redenumit)
C = Copied (📋 Fișier copiat)

Culorile (în majoritatea temelor):

🟢 Verde - Fișiere noi (Untracked) sau adăugate
🟡 Galben/Portocaliu - Fișiere modificate
🔴 Roșu - Fișiere șterse sau cu conflicte
⚪ Alb/Normal - Fișiere fără modificări

📍 Unde le vezi:

În Explorer (panoul cu fișiere din stânga)
În tab-uri (sus, unde sunt deschise fișierele)
În Source Control (panoul Git din stânga - icoana cu ramificația)

🔍 Exemple practice:
📁 proiectul-meu/
├── 🟢 U  nou_fisier.py        (fișier nou, neadăugat)
├── 🟡 M  index.html           (modificat)
├── 🟢 A  style.css            (nou și adăugat în staging)
├── 🔴 D  vechi_script.js      (șters)
└── ⚪    README.md             (fără modificări)
🎯 Workflow vizual:

Creezi/modifici un fișier → Apare U (verde) sau M (galben)
Faci git add → Devine A (verde în staging)
Faci git commit → Dispare indicatorul (devine normal)


Acest script automatizează toate aceste operații pentru tine! 🚀
"""
        print(help_text)
        input("\n📖 Apasă Enter pentru a continua...")
    
    def create_quick_backup(self):
        """
        Funcție rapidă pentru backup complet:
        - Verifică dacă există modificări
        - Adaugă toate fișierele
        - Face commit cu timestamp
        - Face push dacă există remote
        """
        print("\n⚡ BACKUP RAPID COMPLET")
        print("-" * 25)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        print("🔍 Se verifică dacă există modificări...")
        
        # Verifică mai întâi dacă există modificări
        success_status, status_output, _ = self.run_git_command(['git', 'status', '--porcelain'], False)
        
        if not success_status:
            print("❌ Nu se poate verifica status-ul repository-ului!")
            return
        
        if not status_output or not status_output.strip():
            print("✅ Nu există modificări de salvat!")
            print("💡 Proiectul este deja la zi cu ultimul commit.")
            
            # Arată ultimul commit
            success_log, log_output, _ = self.run_git_command(['git', 'log', '-1', '--oneline'], False)
            if success_log and log_output:
                print(f"📝 Ultimul commit: {log_output.strip()}")
            return
        
        # Afișează ce modificări vor fi salvate
        print("📝 Modificări detectate:")
        for line in status_output.strip().split('\n'):
            status = line[:2]
            filename = line[3:]
            
            if status == '??':
                print(f"  🆕 {filename} (fișier nou)")
            elif 'M' in status:
                print(f"  ✏️  {filename} (modificat)")
            elif 'A' in status:
                print(f"  ➕ {filename} (adăugat)")
            elif 'D' in status:
                print(f"  ❌ {filename} (șters)")
            else:
                print(f"  📄 {filename}")
        
        # Confirmă backup-ul
        confirm = input("\n🤔 Vrei să continui cu backup-ul? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Backup anulat.")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Backup automat - {timestamp}"
        
        print("\n🔄 Se execută backup-ul complet...")
        
        # 1. Add all files
        print("  1️⃣ Adaugă toate fișierele...")
        success1, _, error1 = self.run_git_command(['git', 'add', '.'], False)
        
        if not success1:
            print(f"❌ Eroare la adăugarea fișierelor: {error1}")
            return
        
        # 2. Commit
        print("  2️⃣ Creează commit...")
        success2, commit_output, error2 = self.run_git_command(['git', 'commit', '-m', commit_message], False)
        
        if not success2:
            # Verifică diferite tipuri de erori
            if error2 and "nothing to commit" in error2.lower():
                print("✅ Nu există modificări de salvat după add!")
                print("💡 Posibil că toate modificările sunt deja în ultimul commit.")
            elif error2 and "please tell me who you are" in error2.lower():
                print("❌ Git nu știe cine ești! Configurează numele și email-ul:")
                print("💡 Folosește opțiunea din meniu pentru configurarea inițială.")
            else:
                print(f"❌ Eroare la commit:")
                print(f"   {error2}")
                print("\n💡 Posibile soluții:")
                print("   - Verifică dacă ai configurat numele și email-ul Git")
                print("   - Rulează 'git config --global user.name \"Numele Tău\"'")
                print("   - Rulează 'git config --global user.email \"email@tău.com\"'")
            return
        
        print("✅ Commit creat cu succes!")
        
        # 3. Push dacă există remote
        print("  3️⃣ Verifică repository remote...")
        success3, remote_output, _ = self.run_git_command(['git', 'remote', '-v'], False)
        
        if success3 and remote_output:
            print("  4️⃣ Trimite pe server...")
            success4, push_output, error4 = self.run_git_command(['git', 'push'], False)
            
            if success4:
                print("🎉 Backup complet realizat cu succes!")
                print(f"💾 Commit: {commit_message}")
                print("🌐 Trimis pe server!")
            else:
                print("⚠️  Commit realizat local dar eroare la push:")
                print(f"   {error4}")
                print("\n💡 Posibile soluții:")
                print("   - Verifică conexiunea la internet")
                print("   - Verifică permisiunile pe repository")
                print("   - Poate ai nevoie să faci 'git pull' întâi")
        else:
            print("🎉 Backup local realizat cu succes!")
            print(f"💾 Commit: {commit_message}")
            print("💡 Configurează un repository remote pentru backup online.")
    
    def emergency_restore(self):
        """
        Funcții de urgență pentru restaurarea fișierelor
        """
        print("\n🆘 RESTAURARE DE URGENȚĂ")
        print("-" * 30)
        
        if not self.repo_initialized:
            print("❌ Repository-ul nu este inițializat!")
            return
        
        print("⚠️  ATENȚIE: Aceste operații pot șterge modificările nesalvate!")
        print("\n🔧 Opțiuni de restaurare:")
        print("1. Restaurează un fișier specific la ultima versiune")
        print("2. Restaurează toate fișierele la ultimul commit")
        print("3. Vizualizează diferențele pentru un fișier")
        print("4. Înapoi la meniul principal")
        
        choice = input("\n🔢 Alege opțiunea (1-4): ").strip()
        
        if choice == '1':
            # Afișează fișierele modificate
            success, output, error = self.run_git_command(['git', 'status', '--porcelain'], False)
            if success and output:
                print("\n📝 Fișiere modificate:")
                modified_files = []
                for line in output.strip().split('\n'):
                    if line[1] == 'M':  # Modified but not staged
                        filename = line[3:]
                        modified_files.append(filename)
                        print(f"  📝 {filename}")
                
                if not modified_files:
                    print("✅ Nu există fișiere modificate de restaurat!")
                    return
                
                filename = input("\n📁 Care fișier să fie restaurat? ").strip()
                if filename in modified_files:
                    confirm = input(f"⚠️  Sigur vrei să restaurezi '{filename}'? Modificările se vor PIERDE! (yes/no): ")
                    if confirm.lower() == 'yes':
                        success, _, error = self.run_git_command(['git', 'checkout', '--', filename])
                        if success:
                            print(f"✅ {filename} a fost restaurat!")
                        else:
                            print(f"❌ Eroare: {error}")
            else:
                print("✅ Nu există fișiere modificate!")
        
        elif choice == '2':
            confirm = input("⚠️  ATENȚIE! Toate modificările nesalvate se vor PIERDE! Continui? (yes/no): ")
            if confirm.lower() == 'yes':
                success, _, error = self.run_git_command(['git', 'reset', '--hard', 'HEAD'])
                if success:
                    print("✅ Toate fișierele au fost restaurate la ultimul commit!")
                else:
                    print(f"❌ Eroare: {error}")
        
        elif choice == '3':
            filename = input("📁 Pentru care fișier să afișez diferențele? ").strip()
            if filename:
                success, output, error = self.run_git_command(['git', 'diff', filename])
                if success:
                    if not output:
                        print("✅ Nu există diferențe pentru acest fișier!")
                    # Output is already displayed by run_git_command
                else:
                    print(f"❌ Eroare: {error}")
    
    def show_main_menu(self):
        """Afișează meniul principal al aplicației"""


        # Afișează informații despre Git înainte de a începe
        if not self.display_git_info():                    
            input("\n📖 Apasă Enter pentru a ieși...")     
            return                                         
        
        input("\n📖 Apasă Enter pentru a continua...")    


        while True:
            self.display_header()
            
            if not self.git_exists:
                print("\n❌ EROARE: Git nu este instalat pe sistem!")
                print("📥 Descarcă Git de la: https://git-scm.com/downloads")
                print("🔄 Reinstalează și rulează din nou acest script.")
                break
            
            print("\n🎯 MENIU PRINCIPAL:")
            print("=" * 50)
            
            # Meniu pentru repository neinițializat
            if not self.repo_initialized:
                print("🚀 1.  Inițializează repository Git")
                print("📁 2.  Vizualizează structura proiectului")
                print("🎓 3.  Ghid complet Git pentru începători")
                print("❌ 0.  Ieșire")
                
                choice = input("\n🔢 Alege opțiunea: ").strip()
                
                if choice == '1':
                    self.initialize_repository()
                elif choice == '2':
                    self.show_project_structure()
                elif choice == '3':
                    self.show_help()
                elif choice == '0':
                    print("\n👋 La revedere! Git este acum configurat pentru proiectul tău!")
                    break
                else:
                    print("❌ Opțiune invalidă!")
                    
                input("\n📖 Apasă Enter pentru a continua...")
            
            # Meniu pentru repository inițializat
            else:
                print("📊 1.  Verifică status-ul proiectului")
                print("➕ 2.  Adaugă fișiere pentru commit")
                print("💾 3.  Salvează modificările (commit)")
                print("📚 4.  Vizualizează istoricul commit-urilor")
                print("🌿 5.  Creează branch nou")
                print("🔄 6.  Comută între branch-uri")
                print("🌐 7.  Configurează repository remote")
                print("🚀 8.  Trimite pe server (push)")
                print("📥 9.  Descarcă de pe server (pull)")
                print("⚡ 10. Backup rapid complet")
                print("🆘 11. Restaurare de urgență")
                print("📁 12. Vizualizează structura proiectului")
                print("🎓 13. Ghid complet Git")
                print("❌ 0.  Ieșire")
                
                choice = input("\n🔢 Alege opțiunea: ").strip()
                
                if choice == '1':
                    self.show_git_status()
                elif choice == '2':
                    self.add_files()
                elif choice == '3':
                    self.commit_changes()
                elif choice == '4':
                    self.view_commit_history()
                elif choice == '5':
                    self.create_branch()
                elif choice == '6':
                    self.switch_branch()
                elif choice == '7':
                    self.setup_remote_repository()
                elif choice == '8':
                    self.push_to_remote()
                elif choice == '9':
                    self.pull_from_remote()
                elif choice == '10':
                    self.create_quick_backup()
                elif choice == '11':
                    self.emergency_restore()
                elif choice == '12':
                    self.show_project_structure()
                elif choice == '13':
                    self.show_help()
                elif choice == '0':
                    print("\n👋 Proiectul tău este sigur cu Git! La revedere!")
                    break
                else:
                    print("❌ Opțiune invalidă!")
                
                input("\n📖 Apasă Enter pentru a continua...")

def main():
    """Funcția principală care pornește aplicația"""
    try:
        print("🔧 Se inițializează Git Manager...")
        manager = GitManager()
        manager.show_main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicația a fost închisă de utilizator. La revedere!")
    except Exception as e:
        print(f"\n❌ Eroare neașteptată: {e}")
        print("🐛 Te rog să raportezi această eroare!")

if __name__ == "__main__":
    main()