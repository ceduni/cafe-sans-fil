import axios from "axios";
import toast from "react-hot-toast";

const authenticatedRequest = axios.create({
  baseURL: import.meta.env.VITE_API_ENDPOINT + "/api",
});

// Intercepter les requêtes pour ajouter le token d'authentification

authenticatedRequest.interceptors.request.use(
  (config) => {
    const token = JSON.parse(localStorage.getItem("accessToken"));
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepter les réponses pour gérer les erreurs d'authentification

authenticatedRequest.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Le token est expiré ou invalide
    if (error.response?.status === 403 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = useLocalStorage("refreshToken", null);
        const token = await authenticatedRequest.post("/auth/refresh", refreshToken);
        localStorage.setItem("accessToken", JSON.stringify(token.access_token));
        localStorage.setItem("refreshToken", JSON.stringify(token.refresh_token));

        // On réessaie la requête avec le nouveau token
        originalRequest.headers["Authorization"] = `Bearer ${token.access_token}`;
        return axios(originalRequest);
      } catch (error) {
        console.log(error);
        toast.error("Vous devez vous connecter à nouveau");
        // TODO investiguer pourquoi le refresh token ne fonctionne pas
        // localStorage.setItem("accessToken", JSON.stringify(null));
        // localStorage.setItem("refreshToken", JSON.stringify(null));
        // window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default authenticatedRequest;
