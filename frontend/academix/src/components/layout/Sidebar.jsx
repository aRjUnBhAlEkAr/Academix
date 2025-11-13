import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";

const Sidebar = () => {
  const { user } = useContext(AuthContext);

  const menus = {
    student: [
      { name: "Dashboard", path: "/dashboard/student" },
      { name: "Courses", path: "/courses" },
      { name: "Attendance", path: "/attendance" },
    ],
    teacher: [
      { name: "Dashboard", path: "/dashboard/teacher" },
      { name: "Classes", path: "/classes" },
      { name: "Attendance", path: "/attendance" },
    ],
    college_admin: [
      { name: "Dashboard", path: "/dashboard/admin" },
      { name: "Teachers", path: "/teachers" },
      { name: "Students", path: "/students" },
      { name: "Academics", path: "/academics" },
    ],
    superuser: [
      { name: "Dashboard", path: "/dashboard/superadmin" },
      { name: "Colleges", path: "/colleges" },
      { name: "Reports", path: "/reports" },
    ],
  };

  const role = user?.role || "student";

  return (
    <aside className="sidebar">
      <ul>
        {menus[role].map((item) => (
          <li key={item.path}>
            <Link to={item.path}>{item.name}</Link>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
