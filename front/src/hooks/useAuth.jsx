import { useContext, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useLocalStorage("accessToken", null);
  const [refreshToken, setRefreshToken] = useLocalStorage("refreshToken", null);
  const [user, setUser] = useLocalStorage("user", null);
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
        switch (response.status) {
          case 403:
            const responseText = await response.text();
            if (responseText.includes("temporarily")) {
              throw new Error("Trop de tentatives de connexion, réessayez plus tard");
            }

          default:
            throw new Error("Identifiant ou mot de passe incorrect");
        }
      }

      const token = await response.json();
      return token;
    } catch (error) {
      toast.error(error.message);
      return null;
    }
  };

  const handleLogin = async (event, credentials, setCredentials, setHasSubmitted) => {
    event.preventDefault();
    setHasSubmitted(true);
    const { email, password } = credentials;

    const toastId = toast.loading("Connexion...");
    const token = await login(email, password);
    toast.dismiss(toastId);

    if (token) {
      toast.success("Vous êtes connecté");
      setAccessToken(token.access_token);
      setRefreshToken(token.refresh_token);

      navigate("/");
      setUser(await getCurrentUser());
    } else {
      setHasSubmitted(false);
      setCredentials({ ...credentials, password: "" });
    }
  };

  const createAccount = async (email, firstName, lastName, matricule, password) => {
    try {
      const response = await fetch(import.meta.env.VITE_API_ENDPOINT + "/api/auth/register", {
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

          case 409:
            const responseError = await response.json();
            if (responseError.detail.includes("already exists")) {
              throw new Error("Un compte avec ces informations existe déjà");
            }

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

  const handleSignUp = async (event, userData, setHasSubmitted) => {
    event.preventDefault();
    setHasSubmitted(true);
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
      setUser(await getCurrentUser());
    } else {
      setHasSubmitted(false);
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

        case "value_error":
          if (error.loc[1] === "email") {
            toast.error("L'adresse email est invalide");
          }
          if (error.loc[1] === "password") {
            toast.error(error.msg);
          }
          break;

        default:
          toast.error(error.msg);
          break;
      }
    }
  };

  const getCurrentUser = async () => {
    try {
      const response = await authenticatedRequest.get("/users/@me");
      console.log(response);
      return response.data;
    } catch (error) {
      toast.error(error.message);
      return null;
    }
  };

  const handleLogout = () => {
    const toastId = toast.loading("Déconnexion...");
    setTimeout(() => {
      toast.dismiss(toastId);
      toast.success("Vous êtes déconnecté");
      setAccessToken(null);
      setRefreshToken(null);
      setUser(null);
      navigate("/", { replace: true });
    }, 1000);
  };

  const verifyPassword = async (password) => {
    try {
      const currentUser = await getCurrentUser();
      if (!currentUser) {
        return false;
      }

      const response = await fetch(import.meta.env.VITE_API_ENDPOINT + "/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: currentUser.username,
          password,
        }),
      });

      return response.status === 200;
    } catch (error) {
      return false;
    }
  };

  const handleDeleteAccount = async () => {
    try {
      const user = await getCurrentUser();
      const response = await authenticatedRequest.delete(`/users/${user.username}`);
      if (response.status === 200) {
        setAccessToken(null);
        setRefreshToken(null);
        setUser(null);
        navigate("/", { replace: true });
        toast.success("Votre compte a été supprimé");
      } else {
        toast.error("Une erreur est survenue lors de la suppression de votre compte");
      }
    } catch (error) {
      toast.error("Une erreur est survenue lors de la suppression de votre compte");
    }
  };

  const value = {
    token: accessToken,
    isLoggedIn: accessToken && refreshToken && user,
    onLogin: handleLogin,
    onSignUp: handleSignUp,
    onLogout: handleLogout,
    onAccountDelete: handleDeleteAccount,
    verifyPassword: verifyPassword,
    user: user,
    setUser: setUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
