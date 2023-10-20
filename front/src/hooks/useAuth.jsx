import { useContext, useState, createContext } from "react";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);

  const fakeAuth = () =>
    new Promise((resolve) => {
      setTimeout(() => resolve("2342f2f1d131rf12"), 250);
    });

  const handleLogin = async (event) => {
    event.preventDefault();
    const token = await fakeAuth();

    console.log("login");
    setToken(token);
  };

  const handleLogout = () => {
    setToken(null);
    console.log("logout");
  };

  const value = {
    token,
    onLogin: handleLogin,
    onLogout: handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
