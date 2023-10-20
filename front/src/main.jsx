import React from "react";
import ReactDOM from "react-dom/client";
import Home from "./routes/Home";
import PageWrapper from "./components/PageWrapper";
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
    element: <PageWrapper />,
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
        path: "/cafes/:id",
        element: <Cafe />,
      },
      {
        path: "/cafes/:id/staff",
        element: <StaffList />,
      },
      {
        path: "/cafes/:id/order/:orderId",
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
