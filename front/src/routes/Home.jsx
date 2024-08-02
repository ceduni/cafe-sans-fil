import { useState } from "react";
import { Helmet } from "react-helmet-async";
import { useTranslation } from "react-i18next";
import Container from "@/components/Container";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";
import { useSearchParams } from 'react-router-dom';
import RecommendedCafeList from "@/components/Cafe/RecommendedCafeList";
import Filters from "@/components/Cafe/Filters";


const TX = {
    HEAD_TITLE: 'title',
    HOME_TITLE: 'home.title',
}

const Home = () => {
    const { t } = useTranslation();
    let [searchParams] = useSearchParams();
    const searchQuery = searchParams.get("search") || "";
    
    // const [searchQuery, setSearchQuery] = useState("");
    const isSearching = searchQuery.length > 0;

    const [storedCafes, setStoredCafes] = useState([]);

    const [filters, setFilters] = useState({
        openOnly: false,
        pavillon: t("select.all"),
        takesCash: false,
        takesCreditCard: false,
        takesDebitCard: false,
    });

    return (
        <>
            <Helmet>
                <title>{t(TX.HEAD_TITLE)}</title>
            </Helmet>
            <main className="pt-10 pb-[3.25rem] sm:py-10 space-y-6">
                <Filters filters={filters} setFilters={setFilters} cafes={storedCafes} />
                <Container>
                    <RecommendedCafeList storedCafes={storedCafes} filters={filters} />
                </Container>
                <Container>
                    <h2 className="text-3xl font-bold text-gray-900">Tous les cafés</h2>
                    {isSearching ? (
                        <SearchResults searchQuery={searchQuery} setStoredCafes={setStoredCafes} storedCafes={storedCafes}  />
                    ) : (
                        <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} filters={filters} />
                    )}
                </Container>
            </main>
        </>
    );
};

export default Home;