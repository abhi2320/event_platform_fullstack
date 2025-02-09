import axios from "axios";

const API = axios.create({
    baseURL: "https://event-platform-fullstack.onrender.com",  // Change to your backend URL in production
});

// Attach JWT token to every request
API.interceptors.request.use((req) => {
    const token = localStorage.getItem("token");
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
    }
    return req;
});

export default API;
