const BASE_URL = `${import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'}/api`;

async function parseApiError(response, fallbackMessage) {
    try {
        const data = await response.json();
        return data?.detail || fallbackMessage;
    } catch {
        return fallbackMessage;
    }
}

const NETWORK_ERROR = 'Cannot reach the backend. Make sure FastAPI is running on port 8000.';

export const api = {
    login: async (email, password, role = 'user') => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        formData.append('scope', role);

        let response;
        try {
            response = await fetch(`${BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            });
        } catch {
            throw new Error(NETWORK_ERROR);
        }

        if (!response.ok) {
            const detail = await parseApiError(response, 'Login failed');
            throw new Error(detail);
        }
        return response.json();
    },

    register: async (fullname, email, password) => {
        let response;
        try {
            response = await fetch(`${BASE_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ fullname, email, password }),
            });
        } catch {
            throw new Error(NETWORK_ERROR);
        }

        if (!response.ok) {
            const detail = await parseApiError(response, 'Registration failed');
            throw new Error(detail);
        }
        return response.json();
    },

    getDummyCredentials: async () => {
        const response = await fetch(`${BASE_URL}/auth/dummy-credentials`);
        if (!response.ok) {
            const detail = await parseApiError(response, 'Failed to fetch dummy credentials');
            throw new Error(detail);
        }
        return response.json();
    },

    getCurrentUser: async (token) => {
        let response;
        try {
            response = await fetch(`${BASE_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });
        } catch {
            throw new Error(NETWORK_ERROR);
        }
        if (!response.ok) throw new Error('Session expired. Please log in again.');
        return response.json();
    },

    // No backend logout endpoint — token invalidation is client-side only.
    logout: async () => Promise.resolve(),

    getIncidents: async () => {
        const response = await fetch(`${BASE_URL}/reports/`);
        if (!response.ok) throw new Error('Failed to fetch incidents');
        return response.json();
    },

    getAnalytics: async (userId) => {
        const response = await fetch(`${BASE_URL}/analytics/driving-score/${userId}`);
        if (!response.ok) throw new Error('Failed to fetch analytics');
        return response.json();
    },
};
