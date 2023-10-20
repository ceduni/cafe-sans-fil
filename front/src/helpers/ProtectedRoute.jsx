import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export const LoggedInOnly = ({ children }) => {
  const { token } = useAuth();

  if (!token) {
    return <Navigate to="/" />;
  }
  return children;
};

export const LoggedOutOnly = ({ children }) => {
  const { token } = useAuth();

  if (token) {
    return <Navigate to="/me" />;
  }
  return children;
};
