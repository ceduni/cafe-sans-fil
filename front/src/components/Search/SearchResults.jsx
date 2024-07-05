//recherche par item et tag dans l'application
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
    return (
        <div className="relative top-1 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
            {cafes.map((cafe) => (
                <CafeCard cafe={cafe} key={cafe.slug} />
            ))}
        </div>
    );
}

const SearchResults = ({ searchQuery, setStoredCafes, storedCafes }) => {
    const query = normalizeQuery(searchQuery);

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetching cafe
    useEffect(() => {
        setIsLoading(true);
        CafeAPI.search(query, setIsLoading)
            .then((data) => {
                setStoredCafes(data);
                setError(null);
                setIsLoading(false);
            })
            .catch((error) => {
                setError(error);
                setIsLoading(false);
            });
    }, [query, setStoredCafes]);

    if (error) {
        return renderError(error);
    }

    if (isLoading && isEmpty(storedCafes)) {
        return renderEmpty();
    }

    return renderCafe(storedCafes);
};

export default SearchResults;
