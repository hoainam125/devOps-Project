import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import UserPanel from './components/UserPanel';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex flex-col justify-center">
        <nav className="bg-white shadow-md py-4">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between">
              <Link to="/login" className="text-blue-600 font-bold">Login</Link>
              <Link to="/signup" className="text-blue-600 font-bold">Signup</Link>
              <Link to="/panel" className="text-blue-600 font-bold">User Panel</Link>
            </div>
          </div>
        </nav>
        <main className="flex-grow">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/panel" element={<UserPanel />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

