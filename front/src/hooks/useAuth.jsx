import { useContext, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";
import toast from "react-hot-toast";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useLocalStorage("accessToken", null);
  const [refreshToken, setRefreshToken] = useLocalStorage("refreshToken", null);
  const navigate = useNavigate();

  const login = async (email, password) => {
    try {
      const response = await fetch(import.meta.env.VITE_API_ENDPOINT + "/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (response.status !== 200) {
        throw new Error("Identifiant ou mot de passe incorrect");
      }

      const token = await response.json();
      return token;
    } catch (error) {
      toast.error(error.message);
      return null;
    }
  };

  const handleLogin = async (event, email, password) => {
    event.preventDefault();
    const token = await login(email, password);

    if (token) {
      toast.success("Vous êtes connecté");
      setAccessToken(token.access_token);
      setRefreshToken(token.refresh_token);
      navigate("/");
    }
  };

  const handleLogout = () => {
    toast.success("Vous êtes déconnecté");
    setAccessToken(null);
    setRefreshToken(null);
    navigate("/", { replace: true });
  };

  const value = {
    token: accessToken,
    onLogin: handleLogin,
    onLogout: handleLogout,
    isLoggedIn: !!accessToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
