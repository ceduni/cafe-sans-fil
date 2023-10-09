import React from "react";
import ReactDOM from "react-dom/client";
import Home from "./routes/Home";
import NavbarWrapper from "./components/NavbarWrapper";
import ErrorPage from "./components/ErrorPage";
import Login from "./routes/Login";
import SignUp from "./routes/SignUp";
import Search from "./routes/Search";
import Profile from "./routes/Profile";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <NavbarWrapper />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/signup",
        element: <SignUp />,
      },
      {
        path: "/search",
        element: <Search />,
      },
      {
        path: "/me",
        element: <Profile />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
