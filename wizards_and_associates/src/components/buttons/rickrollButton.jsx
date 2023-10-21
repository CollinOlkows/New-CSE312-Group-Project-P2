import React, { useState } from 'react';
import '../../styles/components style/loginButton.css'; // Import your CSS file

function RickRoll() {
  const [isHovered, setIsHovered] = useState(false);

  const handleHover = () => {
    setIsHovered(!isHovered);
  };

  const navigateToSecretPage = () => {
    // Define your custom navigate function here
    const navigate = (url) => {
      window.location.href = url;
    };

    navigate('/secret-cool-wizard-page-bozo'); // Use your custom navigate function to navigate
  };

  return (
    <button
      className={`button ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={handleHover}
      onMouseLeave={handleHover}
      onClick={navigateToSecretPage} // Add an onClick event to trigger navigation
    >
      Surprise
    </button>
  );
}

export default RickRoll;
