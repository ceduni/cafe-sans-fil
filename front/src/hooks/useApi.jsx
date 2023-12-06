import { useEffect, useState } from "react";
import toast from "react-hot-toast";

const useApi = (url) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refetchIndex, setRefetchIndex] = useState(0);

  const refetch = () => setRefetchIndex((prev) => prev + 1);

  const fetchData = async () => {
    setIsLoading(true);
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
        toast.error(`${error.statusText || error.message}`);
      });
  };

  useEffect(() => {
    fetchData();
  }, [url, refetchIndex]);

  return { data, isLoading, error, setData, refetch };
};

export default useApi;
