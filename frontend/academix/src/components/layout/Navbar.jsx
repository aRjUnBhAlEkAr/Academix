import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import "../../styles/Layout.css";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <header className="navbar">
      <h3>Welcome, {user?.first_name || user?.email}</h3>

      <button className="logout-btn" onClick={logout}>
        Logout
      </button>
    </header>
  );
};

export default Navbar;
