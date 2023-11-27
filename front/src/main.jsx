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
import { AuthProvider } from "@/hooks/useAuth";

const router = createBrowserRouter([
  {
    path: "/login",
    element: (
      <AuthProvider>
        <LoggedOutOnly>
          <Login />
        </LoggedOutOnly>
      </AuthProvider>
    ),
  },
  {
    path: "/signup",
    element: (
      <AuthProvider>
        <LoggedOutOnly>
          <SignUp />
        </LoggedOutOnly>
      </AuthProvider>
    ),
  },
  {
    path: "/reset",
    element: (
      <AuthProvider>
        <LoggedOutOnly>
          <ResetPassword />
        </LoggedOutOnly>
      </AuthProvider>
    ),
  },
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
