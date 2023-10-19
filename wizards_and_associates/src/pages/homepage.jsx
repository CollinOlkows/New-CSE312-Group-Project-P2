import React from "react";
import '../App.css';

function Homepage() {
  return (
    <div className="homepage">
      <header>
        <h1>Welcome Wizards</h1>
      </header>
      <main>
        <p>Together we can spread spells and misinformation.</p>
      </main>
    
      <img
        src={'./assets/images/photoshopped_logo/logo.png'}
        alt="" // Empty string for decorative images
        style={{
            width: '1000px',
            height: '1000px',
            border: '1px solid #000',
        }}
        />

    </div>
  );
}

export default Homepage;