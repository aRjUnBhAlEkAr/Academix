import React from "react";
import { NavLink } from "react-router-dom";
import { menuConfig } from "./menuConfig";
import "../../styles/Layout.css";

const Sidebar = ({ role }) => {
  const menus = menuConfig[role] || [];

  return (
    <aside className="sidebar">
      <div className="sidebar-title">Academix</div>

      <nav>
        {menus.map((item, idx) => (
          <NavLink
            key={idx}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "sidebar-link active" : "sidebar-link"
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
