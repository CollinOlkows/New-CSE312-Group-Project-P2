
import './App.css';
import React from "react";

// intializing the pages
import HomePage from './pages/homepage';
import LoginPage from './pages/login.jsx';
import FeedPage from './pages/feed.jsx';
import PostPage from './pages/post.jsx';
import ProfilePage from './pages/profile.jsx';
import SignUpPage from './pages/signup.jsx';
import SecretPage from './pages/secret-wizard-page';


import { BrowserRouter, Route, Routes } from "react-router-dom";


function App() {
  console.log(process.env.REACT_APP_BASE_URL, "url base <--")
  return (
    <div className="App">
      <header className="App-header">
      </header>
        <BrowserRouter basename={process.env.REACT_APP_BASE_URL}>
        <Routes>

          <Route path="/" element={<HomePage />} />
          <Route path="/Login" element={<LoginPage />} />
          <Route path="/Feed" element={<FeedPage />} />
          <Route path="/Post" element={<PostPage />} />
          <Route path="/Profile" element={<ProfilePage />} />
          <Route path="/Sign-up" element={<SignUpPage />} />
          <Route path="/secret-cool-wizard-page-bozo" element={<SecretPage />} />

        
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;


