import React, { useState,useEffect } from 'react'
import './Login.css'
import axios from 'axios'


const Login = () => {

   const [action,setAction] = useState("Sign Up");

   const fetchAPI = async () => {
    const response = await axios.get("http://localhost:8080/api/users")
    console.log(response.data.users)
   }

   useEffect(() => {
    fetchAPI()
   }, [])

 return (

   <div className='container'>
       <div className="header">
            <div className="text">ChapelEats</div>
           <div className="text">{action}</div>
       </div>
           <div className="inputs">
               {action==="Login"?<div></div>:<div className="input">
                   <input type='name' placeholder='Name'/>
               </div>}
               <div className="input">
                   <input type='email'placeholder='Email'/>
               </div>
               <div className="input">
                   <input type='password' placeholder='Password'/>
               </div>
           </div>


       <div className="submit-container">
           <div className={action==="Login"?"submit gray":"submit"} onClick={()=>{setAction("Sign Up")}}>Sign Up</div>
           <div className={action==="Sign Up"?"submit gray":"submit"} onClick={()=>{setAction("Login")}}>Login</div>


       </div>
   </div>
 )
}


export default Login