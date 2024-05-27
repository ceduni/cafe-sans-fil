//recherche par item et tag dans l'application
import useApi from "@/hooks/useApi"; 
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import { CafeAPI, isAPIAvailable } from "@/utils/api";
import { useEffect, useState } from "react";
import { isEmpty } from "@/utils/helpers";

function normalizeQuery(query) {
    return query
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
}


function renderError(error) {
    return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
}

function renderEmpty() {
    return (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100">
            {Array.from({ length: 20 }).map((_, i) => (
                <CafeCardLoading key={i} />
            ))}
        </div>
    );
}

function renderCafe(cafes) {
    (
        <div className="relative top-1 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
            {cafes.map((cafe) => (
                <CafeCard cafe={cafe} key={cafe.slug} />
            ))}
        </div>
    );
}

const SearchResults = ({ searchQuery }) => {
    const query = normalizeQuery(searchQuery)


    const [isLoading, setIsLoading] = useState(true);
    const [cafes, setStoredCafes] = useState(null);
    const [error, setError] = useState(null);

    // Fetching cafe
    useEffect(() => {
        CafeAPI.search(query, setIsLoading)
            .then((data) => {
                setStoredCafes(data);
            })
            .catch((error) => {
                setError(error)
            })
    }, []);

    if (error) {
        return renderError(error);
    }

    if (isLoading && isEmpty(cafes)) {
        return renderEmpty();
    }

    return renderCafe(cafes);
};

export default SearchResults;
