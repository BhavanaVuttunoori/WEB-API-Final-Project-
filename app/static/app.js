// API Base URL
const API_BASE = '';

// State
let token = localStorage.getItem('token');
let currentUser = null;

// Utility Functions
function showMessage(message, type = 'info') {
    const toast = document.getElementById('message-toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(API_BASE + endpoint, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'An error occurred');
    }

    return response.json();
}

// Auth Functions
async function login(username, password) {
    const data = await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    });

    token = data.access_token;
    localStorage.setItem('token', token);
    await loadUserProfile();
    showPage('calculator-page');
    showMessage('Login successful!', 'success');
}

async function register(username, email, password) {
    await apiRequest('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, email, password }),
    });

    showMessage('Registration successful! Please login.', 'success');
    showPage('login-page');
}

function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    showPage('login-page');
    showMessage('Logged out successfully', 'info');
}

async function loadUserProfile() {
    try {
        currentUser = await apiRequest('/api/users/me');
        document.getElementById('profile-username').value = currentUser.username;
        document.getElementById('profile-email').value = currentUser.email;
    } catch (error) {
        showMessage(error.message, 'error');
        logout();
    }
}

// Calculator Functions
async function performCalculation(operand1, operation, operand2) {
    try {
        const result = await apiRequest('/api/calculations/', {
            method: 'POST',
            body: JSON.stringify({
                operand1: parseFloat(operand1),
                operation,
                operand2: parseFloat(operand2),
            }),
        });

        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <strong>Result:</strong> ${operand1} ${getOperationSymbol(operation)} ${operand2} = ${result.result}
        `;
        resultDiv.classList.add('show');
        showMessage('Calculation performed successfully!', 'success');
        return result;
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

function getOperationSymbol(operation) {
    const symbols = {
        add: '+',
        subtract: '-',
        multiply: '×',
        divide: '÷',
        power: '^',
        modulo: '%',
    };
    return symbols[operation] || operation;
}

function getOperationName(operation) {
    const names = {
        add: 'Addition',
        subtract: 'Subtraction',
        multiply: 'Multiplication',
        divide: 'Division',
        power: 'Power',
        modulo: 'Modulo',
    };
    return names[operation] || operation;
}

// History Functions
async function loadHistory() {
    try {
        const calculations = await apiRequest('/api/calculations/');
        const tbody = document.getElementById('history-tbody');
        tbody.innerHTML = '';

        if (calculations.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No calculations yet</td></tr>';
            return;
        }

        calculations.forEach(calc => {
            const row = document.createElement('tr');
            const date = new Date(calc.created_at).toLocaleString();
            row.innerHTML = `
                <td>${date}</td>
                <td>${getOperationName(calc.operation)}</td>
                <td>${calc.operand1} ${getOperationSymbol(calc.operation)} ${calc.operand2}</td>
                <td><strong>${calc.result}</strong></td>
                <td>
                    <button class="btn btn-danger" onclick="deleteCalculation(${calc.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadStatistics() {
    try {
        const stats = await apiRequest('/api/users/me/statistics');
        
        document.getElementById('stat-total').textContent = stats.total_calculations;
        document.getElementById('stat-avg').textContent = stats.average_result.toFixed(2);
        document.getElementById('stat-most').textContent = 
            stats.most_used_operation ? getOperationName(stats.most_used_operation) : '-';

        const breakdown = document.getElementById('operations-breakdown');
        breakdown.innerHTML = '<h4>Operations Breakdown:</h4>';
        
        if (Object.keys(stats.calculations_by_operation).length === 0) {
            breakdown.innerHTML += '<p>No calculations yet</p>';
        } else {
            Object.entries(stats.calculations_by_operation).forEach(([op, count]) => {
                breakdown.innerHTML += `
                    <div class="operation-item">
                        <span>${getOperationName(op)}</span>
                        <span><strong>${count}</strong></span>
                    </div>
                `;
            });
        }
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function deleteCalculation(id) {
    if (!confirm('Are you sure you want to delete this calculation?')) {
        return;
    }

    try {
        await apiRequest(`/api/calculations/${id}`, {
            method: 'DELETE',
        });
        showMessage('Calculation deleted successfully', 'success');
        await loadHistory();
        await loadStatistics();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Profile Functions
async function updateProfile(username, email) {
    try {
        await apiRequest('/api/users/me', {
            method: 'PUT',
            body: JSON.stringify({ username, email }),
        });
        showMessage('Profile updated successfully!', 'success');
        await loadUserProfile();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function changePassword(currentPassword, newPassword) {
    try {
        await apiRequest('/api/users/me/change-password', {
            method: 'POST',
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword,
            }),
        });
        showMessage('Password changed successfully!', 'success');
        document.getElementById('password-form').reset();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Show appropriate page based on token
    if (token) {
        loadUserProfile().then(() => {
            showPage('calculator-page');
        });
    } else {
        showPage('login-page');
    }

    // Login form
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        await login(username, password);
    });

    // Register form
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        await register(username, email, password);
    });

    // Switch between login and register
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        showPage('register-page');
    });

    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        showPage('login-page');
    });

    // Calculator form
    document.getElementById('calculator-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const operand1 = document.getElementById('operand1').value;
        const operation = document.getElementById('operation').value;
        const operand2 = document.getElementById('operand2').value;
        await performCalculation(operand1, operation, operand2);
    });

    // Profile form
    document.getElementById('profile-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('profile-username').value;
        const email = document.getElementById('profile-email').value;
        await updateProfile(username, email);
    });

    // Password form
    document.getElementById('password-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        await changePassword(currentPassword, newPassword);
    });

    // Navigation links
    const navLinks = {
        'nav-calculator': 'calculator-page',
        'nav-calculator-2': 'calculator-page',
        'nav-calculator-3': 'calculator-page',
        'nav-history': 'history-page',
        'nav-history-2': 'history-page',
        'nav-history-3': 'history-page',
        'nav-profile': 'profile-page',
        'nav-profile-2': 'profile-page',
        'nav-profile-3': 'profile-page',
    };

    Object.entries(navLinks).forEach(([linkId, pageId]) => {
        document.getElementById(linkId).addEventListener('click', (e) => {
            e.preventDefault();
            showPage(pageId);
            if (pageId === 'history-page') {
                loadHistory();
                loadStatistics();
            }
        });
    });

    // Logout buttons
    ['logout-btn', 'logout-btn-2', 'logout-btn-3'].forEach(id => {
        document.getElementById(id).addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    });
});
