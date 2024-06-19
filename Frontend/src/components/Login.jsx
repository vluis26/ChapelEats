import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../components/Login.css';
import axios from 'axios';

const Login = ({ setIsLoggedIn, setUserName, setUserEmail }) => {
    const [action, setAction] = useState('Sign Up');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleRegister = async () => {
        try {
            const response = await axios.post('https://chapeleats-production.up.railway.app//register', {
                name,
                email,
                password
            });
            console.log(response.data);
            setIsLoggedIn(true);
            setUserName(name);
            setUserEmail(email)
            navigate('/dashboard');
        } catch (error) {
            console.error('Error registering user:', error);
        }
    };

    const handleLogin = async () => {
        try {
            const response = await axios.post('https://chapeleats-production.up.railway.app//login', {
                email,
                password,
            });

            if (response.status === 200) {
                console.log(response.data);
                setIsLoggedIn(true);
                setUserName(response.data.name);
                setUserEmail(response.data.email); // Store user email
                navigate('/dashboard');
            } else {
                console.error('Failed to login');
            }
        } catch (error) {
            console.error('Error logging in:', error);
        }
    };
    

    return (
        <div className='container'>
            <div className='header'>
                <div className='text'>ChapelEats</div>
                <div className='text'>{action}</div>
            </div>
            <div className='inputs'>
                {action === 'Login' ? null : (
                    <div className='input'>
                        <input
                            type='text'
                            placeholder='Name'
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                )}
                <div className='input'>
                    <input
                        type='email'
                        placeholder='Email'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div className='input'>
                    <input
                        type='password'
                        placeholder='Password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
            </div>
            <div className='submit-container'>
                <div
                    className={action === 'Login' ? 'submit gray' : 'submit'}
                    onClick={() => setAction('Sign Up')}
                >
                    Sign Up
                </div>
                <div
                    className={action === 'Sign Up' ? 'submit gray' : 'submit'}
                    onClick={() => setAction('Login')}
                >
                    Login
                </div>
                <button onClick={action === 'Login' ? handleLogin : handleRegister}>
                    {action === 'Login' ? 'Login' : 'Register'}
                </button>
            </div>
        </div>
    );
};

export default Login;
