import React, { useState, useEffect } from "react";
import API from "../api/axios";
import io from "socket.io-client";
import { useNavigate } from "react-router-dom";

// Connect WebSocket to the deployed backend
const socket = io("https://event-platform-fullstack.onrender.com", {
    transports: ["websocket"], // Ensures WebSocket connection
});

const EventDashboard = () => {
    const [events, setEvents] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchEvents();

        socket.on("update_attendees", (data) => {
            setEvents((prevEvents) =>
                prevEvents.map((event) =>
                    event._id === data.event_id
                        ? { ...event, attendees: data.count }
                        : event
                )
            );
        });

        return () => socket.off("update_attendees");
    }, []);

    const fetchEvents = async () => {
        try {
            const { data } = await API.get("/events");
            setEvents(data);
        } catch (error) {
            alert("Failed to fetch events!");
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-blue-600">Event Dashboard</h2>
                <button onClick={handleLogout}
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition duration-300">
                    Logout
                </button>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {events.map((event) => (
                    <div key={event._id} className="bg-white p-4 rounded-lg shadow-md">
                        <h3 className="text-xl font-semibold">{event.title}</h3>
                        <p className="text-gray-600">{event.description}</p>
                        <p className="text-gray-800 font-bold mt-2">Attendees: {event.attendees.length}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EventDashboard;
