import React from "react";
import ReactDOM from "react-dom/client";
import Home from "./routes/Home";
import NavbarWrapper from "./components/NavbarWrapper";
import ErrorPage from "./components/ErrorPage";
import Login from "./routes/Login";
import SignUp from "./routes/SignUp";
import Profile from "./routes/Profile";
import Cafe from "./routes/Cafe";
import StaffList from "./components/ui/StaffList";
import OrderHeader from "./components/ui/OrderHeader";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import { HelmetProvider } from "react-helmet-async";

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
        path: "/me",
        element: <Profile />,
      },
      {
        path: "/cafe/:id",
        element: <Cafe />,
      },
      {
        path: "/cafe/:id/staff",
        element: <StaffList />,
      },
      {
        path: "/cafe/:id/order/:orderId",
        element: <OrderHeader />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <HelmetProvider>
      <RouterProvider router={router} />
    </HelmetProvider>
  </React.StrictMode>
);
