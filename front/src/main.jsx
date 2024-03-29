import React from "react";
import ReactDOM from "react-dom/client";
import PageWrapper from "@/components/PageWrapper";
import ErrorPage from "@/components/ErrorPage";
import {
  Home,
  Login,
  SignUp,
  Profile,
  Cafe,
  ResetPassword,
  Orders,
  OrderConfirmation,
  CafeOrders,
  EditCafe,
  StaffList,
  SalesReport,
  EditMenu,
} from "@/routes";
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
        element: (
          <LoggedInOnly>
            <StaffList />
          </LoggedInOnly>
        ),
      },
      {
        path: "/cafes/:id/orders",
        element: (
          <LoggedInOnly>
            <CafeOrders />
          </LoggedInOnly>
        ),
      },
      {
        path: "/cafes/:id/edit",
        element: (
          <LoggedInOnly>
            <EditCafe />
          </LoggedInOnly>
        ),
      },
      {
        path: "/cafes/:id/edit/menu",
        element: (
          <LoggedInOnly>
            <EditMenu />
          </LoggedInOnly>
        ),
      },
      {
        path: "/cafes/:id/sales-report",
        element: (
          <LoggedInOnly>
            <SalesReport />
          </LoggedInOnly>
        ),
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
