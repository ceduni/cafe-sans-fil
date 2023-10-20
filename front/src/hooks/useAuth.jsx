import { useContext, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useLocalStorage("token", null);
  const navigate = useNavigate();

  const fakeAuth = () =>
    new Promise((resolve) => {
      setTimeout(() => resolve("2342f2f1d131rf12"), 250);
    });

  const handleLogin = async (event) => {
    event.preventDefault();
    const token = await fakeAuth();

    console.log("login");
    setToken(token);
    navigate("/");
  };

  const handleLogout = () => {
    setToken(null);
    console.log("logout");
    navigate("/", { replace: true });
  };

  const value = {
    token,
    onLogin: handleLogin,
    onLogout: handleLogout,
    isLoggedIn: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
