export const menuConfig = {
  student: [
    { label: "Dashboard", path: "/dashboard/student" },
    { label: "My Courses", path: "/student/courses" },
    { label: "Attendance", path: "/student/attendance" },
  ],

  teacher: [
    { label: "Dashboard", path: "/dashboard/teacher" },
    { label: "My Classes", path: "/teacher/classes" },
    { label: "Attendance", path: "/teacher/attendance" },
  ],

  college_admin: [
    { label: "Dashboard", path: "/dashboard/admin" },
    { label: "Students", path: "/admin/students" },
    { label: "Teachers", path: "/admin/teachers" },
    { label: "Academics", path: "/admin/academics" },
  ],

  superuser: [
    { label: "Dashboard", path: "/dashboard/superadmin" },
    { label: "Colleges", path: "/superadmin/colleges" },
    { label: "Admins", path: "/superadmin/admins" },
  ],
};
