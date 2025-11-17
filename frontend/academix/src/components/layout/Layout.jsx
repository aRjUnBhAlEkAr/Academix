import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import "../../styles/Layout.css";

const Layout = ({ children }) => {
  const { user } = useContext(AuthContext);

  if (!user) return null; // Safety check

  return (
    <div className="layout-container">
      <Sidebar role={user.role} />
      <div className="layout-content">
        <Navbar />
        <main className="content-area">{children}</main>
      </div>
    </div>
  );
};

export default Layout;
