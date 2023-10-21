import React from "react";
import '../App.css';
import '../styles/assets/homelogo.css'
import logo from '../assets/images/photoshopped_logo/logo.png';

function Homepage() {
  return (
    <div>
      <img src={logo} alt="Logo" className="logo"/>
    </div>
  );
}

export default Homepage;