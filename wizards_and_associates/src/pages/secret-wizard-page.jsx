import React from "react";
import '../App.css';
import LoginButton from "../components/buttons/loginButton.jsx";
import LogOutButton from "../components/buttons/logoutButton";
import RickRoll from "../components/buttons/rickrollButton";
import SignUpButton from "../components/buttons/signupButton";

function WizardPage() {
  return (
    <div className="homepage">
        <LoginButton />
        <RickRoll />
        <SignUpButton />
        <LogOutButton />
      <header>
        <h1>Welcome to the Finders of the Secret Club BOZO</h1>
      </header>
      <main>
        <p>Kanye west and noahn kahn listeners</p>
      </main>
      <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ?si=PHMe5lQnEyoawqt1" 
        title="YouTube video player" frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen>
        </iframe>
    </div>
  );
}

export default WizardPage;