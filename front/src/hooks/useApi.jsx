import { useEffect, useState } from "react";
import toast from "react-hot-toast";

const buildUrl = (url) => import.meta.env.VITE_API_ENDPOINT + "/api" + url;

const fetchData = async ({url, okCb, errorCb, pre = null, post = null}) => {
    try {
        if (pre) {
            pre();
        }
        
        const response = await fetch(buildUrl(url));

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        const responseData = await response.json();

        okCb(responseData)
    } catch (error) {
        errorCb(error)
        toast.error(`${error.message}`);
    } finally {
        if (post) {
            post();
        }
    }
};

const useApi = (url, fn) => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refetchIndex, setRefetchIndex] = useState(0);

    const refetch = () => setRefetchIndex(prev => prev + 1);

    useEffect(() => {
        fetchData({
            url, 
            okCb: setData, 
            errorCb: setError,
            pre: () => setIsLoading(true),
            post: () => setIsLoading(false)});
    }, [url, refetchIndex]);

    return { data, isLoading, error, refetch };
};

export default useApi;
