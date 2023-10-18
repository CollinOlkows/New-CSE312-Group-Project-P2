// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


import './App.css';
import React from "react";

import Homepage from './pages/homepage';


import { BrowserRouter, Route, Routes } from "react-router-dom";


function App() {
  console.log(process.env.REACT_APP_BASE_URL, "url base <--")
  return (
    <div className="App">
      <header className="App-header">
      </header>
        <BrowserRouter basename={process.env.REACT_APP_BASE_URL}>
        <Routes>

          <Route path="/" element={<Homepage />} />
        
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

// import './App.css';
// import React from "react";

// // pages 
// import Homepage from './pages/homepage';



// import { BrowserRouter, Route, Routes } from "react-router-dom";

// function App() {
//   console.log(process.env.REACT_APP_BASE_URL, "url base <--");
//   return (
//     <div className="App">
//       <header className="App-header">
//         {/* Your header content */}
//       </header>
//       <BrowserRouter basename={process.env.REACT_APP_BASE_URL}>
//         <Routes>
//           <Route path = "/" element = {<Homepage />} />
//         </Routes>
//       </BrowserRouter>
//     </div>
//   );
// }

// export default App;
