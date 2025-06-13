// Git Manager Terminal Interface - JavaScript
class GitManagerUI {
    constructor() {
        this.apiBase = '/api';
        this.currentStatus = null;
        this.selectedFiles = [];
        this.init();
    }

    async init() {
        this.addConsoleMessage('🚀 Git Manager Terminal inițializat', 'success');
        await this.refreshStatus();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    // API Communication
    async apiCall(endpoint, method = 'GET', data = null) {
        try {
            const config = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data) {
                config.body = JSON.stringify(data);
            }

            const response = await fetch(`${this.apiBase}${endpoint}`, config);
            const result = await response.json();
            
            return result;
        } catch (error) {
            console.error('API Error:', error);
            this.addConsoleMessage(`❌ Eroare API: ${error.message}`, 'error');
            return { success: false, message: error.message };
        }
    }

    // Status Management
    async refreshStatus() {
        try {
            const status = await this.apiCall('/status');
            this.currentStatus = status;
            this.updateStatusDisplay(status);
            this.updateButtons(status);
            this.updatePath(status.project_path);
        } catch (error) {
            this.addConsoleMessage(`❌ Eroare la actualizarea status: ${error.message}`, 'error');
        }
    }

    updateStatusDisplay(status) {
        const statusContent = document.getElementById('status-content');
        
        if (!status.git_installed) {
            statusContent.innerHTML = `
                <div class="status-card">
                    <h4>⚠️ Git Status</h4>
                    <div class="value">Nu este instalat</div>
                    <div class="description">Git nu este disponibil în sistem</div>
                </div>
            `;
            return;
        }

        if (!status.initialized) {
            statusContent.innerHTML = `
                <div class="status-card">
                    <h4>📂 Repository</h4>
                    <div class="value">Neinițializat</div>
                    <div class="description">Apasă "Init Repo" pentru început</div>
                </div>
                <div class="status-card">
                    <h4>📁 Locație</h4>
                    <div class="value">${this.truncatePath(status.project_path)}</div>
                    <div class="description">Directorul curent de lucru</div>
                </div>
            `;
            return;
        }

        const fileCount = status.files ? status.files.length : 0;
        const modifiedCount = status.files ? status.files.filter(f => f.status !== 'untracked').length : 0;
        const untrackedCount = status.files ? status.files.filter(f => f.status === 'untracked').length : 0;

        statusContent.innerHTML = `
            <div class="status-card">
                <h4>🌿 Branch</h4>
                <div class="value">${status.branch || 'main'}</div>
                <div class="description">Branch-ul curent activ</div>
            </div>
            <div class="status-card">
                <h4>📊 Fișiere</h4>
                <div class="value">${fileCount}</div>
                <div class="description">Modificate: ${modifiedCount}, Noi: ${untrackedCount}</div>
            </div>
            <div class="status-card">
                <h4>📍 Status</h4>
                <div class="value">${status.message}</div>
                <div class="description">${fileCount === 0 ? 'Working tree curat' : 'Modificări detectate'}</div>
            </div>
            <div class="status-card">
                <h4>📁 Locație</h4>
                <div class="value">${this.truncatePath(status.project_path)}</div>
                <div class="description">Directorul de lucru</div>
            </div>
        `;

        // Show files if any
        if (status.files && status.files.length > 0) {
            const filesHtml = status.files.map(file => `
                <div class="file-item">
                    <span class="file-icon">${file.icon}</span>
                    <span class="file-name">${file.name}</span>
                    <span class="file-status status-${file.status}">${this.getStatusText(file.status)}</span>
                </div>
            `).join('');

            statusContent.innerHTML += `
                <div class="status-card" style="grid-column: 1 / -1;">
                    <h4>📄 Fișiere Modificate</h4>
                    <div class="file-list">
                        ${filesHtml}
                    </div>
                </div>
            `;
        }
    }

    updateButtons(status) {
        const initBtn = document.getElementById('init-btn');
        const addBtn = document.getElementById('add-btn');
        const commitBtn = document.getElementById('commit-btn');
        const historyBtn = document.getElementById('history-btn');
        const branchBtn = document.getElementById('branch-btn');
        const pushBtn = document.getElementById('push-btn');
        const pullBtn = document.getElementById('pull-btn');
        const backupBtn = document.getElementById('backup-btn');

        if (!status.git_installed) {
            [addBtn, commitBtn, historyBtn, branchBtn, pushBtn, pullBtn, backupBtn].forEach(btn => {
                btn.disabled = true;
            });
            return;
        }

        initBtn.disabled = status.initialized;
        
        const hasFiles = status.files && status.files.length > 0;

        [addBtn, commitBtn, historyBtn, branchBtn, pushBtn, pullBtn, backupBtn].forEach(btn => {
            btn.disabled = !status.initialized;
        });

        commitBtn.disabled = !hasFiles;
        pushBtn.disabled = !hasFiles;
        backupBtn.disabled = !hasFiles;
    }

    updatePath(path) {
        const pathElement = document.getElementById('current-path');
        if (pathElement) {
            pathElement.textContent = this.truncatePath(path);
        }
    }

    truncatePath(path, maxLength = 40) {
        return path.length > maxLength ? '...' + path.slice(-maxLength) : path;
    }

    getStatusText(status) {
        switch (status) {
            case 'untracked': return 'Neurmărit';
            case 'modified': return 'Modificat';
            case 'added': return 'Adăugat';
            case 'deleted': return 'Șters';
            case 'modified_staged': return 'Modificat (stag.)';
            default: return 'Necunoscut';
        }
    }

    addConsoleMessage(message, type = 'info') {
        const consoleEl = document.getElementById('console');
        const line = document.createElement('div');
        line.className = `console-line ${type}`;
        line.innerHTML = `
            <span class="prompt">git@manager:~$</span>
            <span class="output">${message}</span>
        `;
        consoleEl.appendChild(line);
        consoleEl.scrollTop = consoleEl.scrollHeight;
    }

    clearConsole() {
        const consoleEl = document.getElementById('console');
        consoleEl.innerHTML = '';
    }

    setupEventListeners() {
        const exampleItems = document.querySelectorAll('.example-item');
        exampleItems.forEach(item => {
            item.addEventListener('click', () => {
                this.setCommitMessage(item.textContent);
            });
        });

        const radios = document.querySelectorAll('input[name="add-type"]');
        radios.forEach(radio => {
            radio.addEventListener('change', () => {
                const fileList = document.getElementById('file-list');
                if (radio.value === 'specific') {
                    this.populateFileList();
                    fileList.style.display = 'block';
                } else {
                    fileList.style.display = 'none';
                }
            });
        });
    }

    setCommitMessage(message) {
        const input = document.getElementById('commit-message');
        input.value = message;
    }

    startAutoRefresh() {
        setInterval(() => this.refreshStatus(), 10000); // 10 secunde
    }

    async initRepo() {
        const result = await this.apiCall('/init', 'POST');
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        await this.refreshStatus();
    }

    showAddModal() {
        const modal = document.getElementById('add-modal');
        modal.style.display = 'block';
    }

    async populateFileList() {
        const fileList = document.getElementById('file-list');
        fileList.innerHTML = '';
        if (this.currentStatus && this.currentStatus.files) {
            this.currentStatus.files.forEach(file => {
                const div = document.createElement('div');
                div.innerHTML = `
                    <label>
                        <input type="checkbox" value="${file.name}" />
                        <span class="file-name">${file.name}</span>
                    </label>
                `;
                fileList.appendChild(div);
            });
        }
    }

    async addFiles() {
        const selected = [];
        const type = document.querySelector('input[name="add-type"]:checked').value;
        if (type === 'specific') {
            const checkboxes = document.querySelectorAll('#file-list input[type="checkbox"]:checked');
            checkboxes.forEach(cb => selected.push(cb.value));
        }

        const result = await this.apiCall('/add', 'POST', { files: type === 'all' ? ['all'] : selected });
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        this.closeModal('add-modal');
        await this.refreshStatus();
    }

    showCommitModal() {
        document.getElementById('commit-modal').style.display = 'block';
    }

    async commitChanges() {
        const message = document.getElementById('commit-message').value;
        const result = await this.apiCall('/commit', 'POST', { message });
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        this.closeModal('commit-modal');
        await this.refreshStatus();
    }

    async showHistory() {
        const modal = document.getElementById('history-modal');
        modal.style.display = 'block';

        const container = document.getElementById('history-content');
        container.innerHTML = '<div class="loading">Se încarcă...</div>';

        const result = await this.apiCall('/history');
        if (result.success && result.commits) {
            container.innerHTML = result.commits.map(line => `<div class="commit-line">${line}</div>`).join('');
        } else {
            container.innerHTML = `<div class="error">Eroare la încărcarea istoricului</div>`;
        }
    }

    async showBranches() {
        const modal = document.getElementById('branches-modal');
        modal.style.display = 'block';

        const list = document.getElementById('branches-list');
        list.innerHTML = '<div class="loading">Se încarcă...</div>';

        const result = await this.apiCall('/branches');
        if (result.success && result.branches) {
            list.innerHTML = result.branches.map(branch => `
                <div class="branch-item ${branch.current ? 'current' : ''}">
                    <span>${branch.name}</span>
                    ${!branch.current ? `<button onclick="app.switchBranch('${branch.name}')">Comută</button>` : ''}
                </div>
            `).join('');
        } else {
            list.innerHTML = `<div class="error">Eroare la încărcarea branch-urilor</div>`;
        }
    }

    async createBranch() {
        const name = document.getElementById('new-branch-name').value;
        const result = await this.apiCall('/branch/create', 'POST', { name });
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        await this.showBranches();
        await this.refreshStatus();
    }

    async switchBranch(name) {
        const result = await this.apiCall('/branch/switch', 'POST', { name });
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        await this.refreshStatus();
    }

    async setupRemote() {
        const url = document.getElementById('remote-url').value;
        const result = await this.apiCall('/remote/setup', 'POST', { url });
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        this.closeModal('remote-modal');
        await this.refreshStatus();
    }

    async pushChanges() {
        const result = await this.apiCall('/push', 'POST', { first_push: false });
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        await this.refreshStatus();
    }

    async pullChanges() {
        const result = await this.apiCall('/pull', 'POST');
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        await this.refreshStatus();
    }

    async quickBackup() {
        const result = await this.apiCall('/backup', 'POST');
        this.addConsoleMessage(result.message, result.success ? 'success' : 'error');
        await this.refreshStatus();
    }

    closeModal(id) {
        document.getElementById(id).style.display = 'none';
    }
}

// Instanțierea aplicației
const app = new GitManagerUI();
