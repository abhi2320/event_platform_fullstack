import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// Backend API URL
const BACKEND_URL = "https://event-platform-fullstack.onrender.com";

const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const { data } = await axios.post(`${BACKEND_URL}/login`, { email, password });
            localStorage.setItem("token", data.token);
            toast.success("Login Successful! Redirecting...");
            setTimeout(() => navigate("/events"), 1000);
        } catch (error) {
            toast.error("Invalid Credentials! Please try again.");
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-100">
            <ToastContainer position="top-right" autoClose={3000} />
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-2xl font-semibold text-center mb-4 text-blue-600">Login</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}
                        className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}
                        className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    <button type="submit"
                        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition duration-300">
                        Login
                    </button>
                </form>
                <p className="text-center mt-4">Don't have an account? 
                    <a href="/register" className="text-blue-500"> Register</a>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
