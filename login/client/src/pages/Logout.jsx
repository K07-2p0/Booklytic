import React, { useEffect } from 'react'
import "../styles/Logout.css";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';

const Logout = () => {

    const navigate = useNavigate();

    useEffect(() => {
        const logoutUser = async () => {
            try {
                await axios.post(`${import.meta.env.VITE_API_URL}/logout`, {}, {
                    withCredentials: true
                });
            } catch (error) {
                console.log("Logout API error:", error);
            }
            localStorage.removeItem("auth");
            setTimeout(() => {
                navigate("/");
            }, 3000);
        };
        logoutUser();
    }, [navigate]);

  return (
    <div className='logout-main'>
    <h1>Logout Successful!</h1>
    <p>You will be redirected to the landing page in 3 seconds...</p>
  </div>
  )
}

export default Logout