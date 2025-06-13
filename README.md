# 🚀 Git Manager Terminal Web App

O aplicație web interactivă care oferă o interfață de tip terminal pentru gestionarea unui repository Git. Proiectul este dezvoltat cu Flask + JavaScript și simulează experiența unei console Linux cu butoane rapide și interfețe moderne.

![Preview Screenshot](static/screenshot.png)

---

## 📌 Funcționalități

- ✅ Verificare instalare Git
- 📂 Inițializare repository
- ➕ Adăugare fișiere (`git add`)
- 💾 Commit cu mesaj și timestamp (`git commit`)
- 📚 Istoric vizual (`git log --graph`)
- 🌿 Gestionare branch-uri (`create`, `switch`)
- 🌐 Configurare repository remote
- 🚀 Push / 📥 Pull modificări
- ⚡ Backup rapid (add + commit + push)
- 🎛️ Interfață tip terminal, responsive și modernă

---

## 🧱 Tehnologii utilizate

| Frontend         | Backend        | Altele           |
|------------------|----------------|------------------|
| HTML5 + CSS3     | Python 3.8+    | Git CLI          |
| Vanilla JavaScript | Flask        | Bootstrap UI     |
| Font: JetBrains Mono | JSON API   | Emoji + Unicode  |

---

## ⚙️ Instalare locală

1. **Clonează repository-ul:**

```bash
git clone https://github.com/cosminiq/git-manager-web.git
cd git-manager-web
```

2. **Creează un mediu virtual (opțional dar recomandat):**

```bash
python -m venv venv
source venv/bin/activate  # sau `venv\Scripts\activate` pe Windows
```

3. **Instalează dependențele:**

```bash
pip install flask
```

4. **Pornește aplicația:**

```bash
python git_web_app.py
```

5. **Deschide browserul la:**

```
http://localhost:5000
```

---

## 🖥️ Structura proiectului

```text
.
├── git_web_app.py           # Backend Flask
├──Git Manager.py            # Aplicatie python
├── static/
│   ├── style.css            # Stil terminal UI
│   ├── script.js            
│   └── screenshot.png       # (opțional) captură de ecran
├── templates/
│   └── index.html           # Flask template (copie după index.html)
└── README.md
```

---

## 🧪 Exemple de utilizare

- Init repo: `Init Repo` ➜ creează `.git`, `.gitignore`
- Add files: `Add Files` ➜ selectează toate sau unele fișiere
- Commit: `Commit` ➜ mesaj + ora exactă
- History: vezi graficul commit-urilor
- Branches: creezi și comuți între ramuri
- Remote: adaugi URL GitHub și poți face push
- Quick Backup: combinație `add .`, `commit`, `push`

---

## 🧑‍💻 Contribuție

Contribuțiile sunt binevenite! Trimite un **pull request** sau deschide un **issue** dacă ai idei, buguri sau propuneri de îmbunătățire.

Pentru modificări:

```bash
# Pornește dev serverul Flask
python git_web_app.py
```

---

## 📜 Licență

Proiectul este licențiat sub MIT License. Vezi fișierul `LICENSE` pentru detalii.

---

## 📬 Contact

Creat de **krux** –
Pentru întrebări sau colaborări: deschide un issue sau contactează-mă pe GitHub.
