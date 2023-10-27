import { useContext, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";
import toast from "react-hot-toast";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useLocalStorage("token", null);
  const navigate = useNavigate();

  const fakeAuth = () =>
    new Promise((resolve) => {
      setTimeout(() => resolve("2342f2f1d131rf12"), 250);
    });

  const realAuth = async (email, password) => {
    const login = fetch(import.meta.env.VITE_API_ENDPOINT + "/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    }).then((response) => {
      if (!response.ok) {
        throw new Error("HTTP error " + response.status);
      }
      const data = response.json();
      return data.access_token;
    });
    return login;
  };

  const handleLogin = async (event, email, password) => {
    event.preventDefault();
    try {
      const token = await fakeAuth();
      setToken(token);
      navigate("/");
    } catch (error) {
      console.log(error);
    }
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
