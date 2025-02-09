import React, { useState, useEffect } from "react";
import API from "../api/axios";  // Using Axios for API calls
import io from "socket.io-client";
import { useNavigate } from "react-router-dom";

const socket = io("https://event-platform-fullstack.onrender.com");

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
        <div>
            <h2>Events</h2>
            <button onClick={handleLogout}>Logout</button>
            {events.map((event) => (
                <div key={event._id}>
                    <h3>{event.title}</h3>
                    <p>{event.description}</p>
                    <p>Attendees: {event.attendees.length}</p>
                </div>
            ))}
        </div>
    );
};

export default EventDashboard;
