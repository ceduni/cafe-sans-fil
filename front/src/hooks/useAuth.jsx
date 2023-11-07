import { useContext, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "@/hooks/useLocalStorage";
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

  const createAccount = async (email, firstName, lastName, matricule, password) => {
    try {
      const response = await fetch(import.meta.env.VITE_API_ENDPOINT + "/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          first_name: firstName,
          last_name: lastName,
          matricule: matricule,
          password: password,
          username: matricule,
        }),
      });

      if (response.status !== 200) {
        switch (response.status) {
          case 500:
            throw new Error("Une erreur inconue est survenue (probably CORS)");

          case 422:
            displayMongoError(response);
            return null;

          default:
            throw new Error("Impossible de créer le compte");
        }
      }

      const token = await login(email, password);
      return token;
    } catch (error) {
      toast.error(error.message);
      return null;
    }
  };

  const displayMongoError = async (response) => {
    const responseError = await response.json();
    for (const error of responseError.detail) {
      switch (error.type) {
        case "string_too_short":
          const minLength = error.ctx.min_length;
          const loc = error.loc[1];
          toast.error(`Le champ ${loc} doit contenir au moins ${minLength} caractères`);
          break;

        default:
          toast.error(error.msg);
          break;
      }
    }
  };

  const handleLogin = async (event, email, password) => {
    event.preventDefault();
    const toastId = toast.loading("Connexion...");
    const token = await login(email, password);
    toast.dismiss(toastId);

    if (token) {
      toast.success("Vous êtes connecté");
      setAccessToken(token.access_token);
      setRefreshToken(token.refresh_token);
      navigate("/");
    }
  };

  const getCurrentUser = async () => {
    // TODO request to /api/auth/test-token while being JWT authenticated
    // will return the current user's data
  };

  const handleSignUp = async (event, userData) => {
    event.preventDefault();
    const { email, firstName, lastName, matricule, password, passwordConfirm } = userData;

    if (password !== passwordConfirm) {
      toast.error("Les mots de passe ne correspondent pas");
      return;
    }

    const toastId = toast.loading("Création du compte...");
    const token = await createAccount(email, firstName, lastName, matricule, password);
    toast.dismiss(toastId);

    if (token) {
      toast.success("Votre compte a été créé");
      setAccessToken(token.access_token);
      setRefreshToken(token.refresh_token);
      navigate("/");
    }
  };

  const handleLogout = () => {
    const toastId = toast.loading("Déconnexion...");
    setTimeout(() => {
      toast.dismiss(toastId);
      toast.success("Vous êtes déconnecté");
      setAccessToken(null);
      setRefreshToken(null);
      navigate("/", { replace: true });
    }, 1000);
  };

  const value = {
    token: accessToken,
    isLoggedIn: !!accessToken,
    onLogin: handleLogin,
    onSignUp: handleSignUp,
    onLogout: handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
