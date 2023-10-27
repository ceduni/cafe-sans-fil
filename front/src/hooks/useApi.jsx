import { useEffect, useState } from "react";
import toast from "react-hot-toast";

const useApi = (url) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    fetch(import.meta.env.VITE_API_ENDPOINT + "/api" + url)
      .then((response) => (response.ok ? response : Promise.reject(response)))
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setIsLoading(false);
      })
      .catch((error) => {
        setError(error);
        setIsLoading(false);
        toast.error(`${error.statusText || error.message}`, {
          style: {
            padding: "16px",
          },
        });
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { data, isLoading, error };
};

export default useApi;
