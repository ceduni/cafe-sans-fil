import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export const LoggedInOnly = ({ children }) => {
  const { isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }
  return children;
};

export const LoggedOutOnly = ({ children }) => {
  const { isLoggedIn } = useAuth();

  if (isLoggedIn) {
    return <Navigate to="/me" />;
  }
  return children;
};
