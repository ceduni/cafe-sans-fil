import React from "react";
import ReactDOM from "react-dom/client";
import PageWrapper from "@/components/PageWrapper";
import ErrorPage from "@/components/ErrorPage";
import { Home, Login, SignUp, Profile, Cafe, ResetPassword, Orders, OrderConfirmation, CafeOrders } from "@/routes";
import StaffList from "@/components/Cafe/StaffList";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import { HelmetProvider } from "react-helmet-async";
import { LoggedInOnly, LoggedOutOnly } from "@/helpers/ProtectedRoute";

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
        element: (
          <LoggedOutOnly>
            <Login />
          </LoggedOutOnly>
        ),
      },
      {
        path: "/signup",
        element: (
          <LoggedOutOnly>
            <SignUp />
          </LoggedOutOnly>
        ),
      },
      {
        path: "/reset",
        element: (
          <LoggedOutOnly>
            <ResetPassword />
          </LoggedOutOnly>
        ),
      },
      {
        path: "/me",
        element: (
          <LoggedInOnly>
            <Profile />
          </LoggedInOnly>
        ),
      },
      {
        path: "/me/orders",
        element: (
          <LoggedInOnly>
            <Orders />
          </LoggedInOnly>
        ),
      },
      {
        path: "/confirm",
        element: <OrderConfirmation />,
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
        path: "/cafes/:id/orders",
        element: <CafeOrders />,
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
