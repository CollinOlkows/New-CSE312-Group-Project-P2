import React, { useState } from 'react';
import '../../styles/components style/loginButton.css'; // Import your CSS file

function RickRoll() {
  const [isHovered, setIsHovered] = useState(false);

  const handleHover = () => {
    setIsHovered(!isHovered);
  };

  return (
    <button
      className={`button ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={handleHover}
      onMouseLeave={handleHover}
    >
      Surpise
    </button>
  );
}

export default RickRoll;