import React, { useEffect, useState, useCallback } from 'react'
import "../styles/Dashboard.css";
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';

const Dashboard = () => {
  const [ token ] = useState(() => localStorage.getItem("auth") || "");
  const [ data, setData ] = useState({});
  const navigate = useNavigate();

  const fetchLuckyNumber = useCallback(async () => {
    if (!token) return;

    let axiosConfig = {
      headers: {
        'Authorization': `Bearer ${token}`
    }
    };

    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/dashboard`, {
        ...axiosConfig,
        withCredentials: true
      });
      setData({ msg: response.data.msg, luckyNumber: response.data.secret });
    } catch (error) {
      toast.error(error.response?.data?.msg || error.message);
    }
  }, [token]);



  useEffect(() => {
    if(token === ""){
      navigate("/login");
      toast.warn("Please login first to access dashboard");
    } else {
      fetchLuckyNumber();
    }
  }, [token, fetchLuckyNumber, navigate]);

  return (
    <div className='dashboard-main'>
      <h1>Dashboard</h1>
      <p>Hi { data.msg }! { data.luckyNumber }</p>
      <Link to="/logout" className="logout-button">Logout</Link>
    </div>
  )
}

export default Dashboard