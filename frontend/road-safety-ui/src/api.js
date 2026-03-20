const BASE_URL = 'http://localhost:8000/api';

export const api = {
    login: async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });
        if (!response.ok) throw new Error("Login failed");
        return response.json();
    },

    register: async (fullname, email, password) => {
        const response = await fetch(`${BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ fullname, email, password }),
        });
        if (!response.ok) throw new Error("Registration failed");
        return response.json();
    },

    getIncidents: async () => {
        const response = await fetch(`${BASE_URL}/reports/`);
        if (!response.ok) throw new Error("Failed to fetch incidents");
        return response.json();
    },

    getAnalytics: async (userId) => {
        const response = await fetch(`${BASE_URL}/analytics/driving-score/${userId}`);
        if (!response.ok) throw new Error("Failed to fetch analytics");
        return response.json();
    }
};
