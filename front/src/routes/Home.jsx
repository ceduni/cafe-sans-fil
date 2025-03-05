import { useState } from "react";
// import { Helmet } from "react-helmet-async";
import { useTranslation } from "react-i18next";
import Container from "@/components/Layout/Container";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";
import { useSearchParams } from 'react-router-dom';
import useTitle from "@/hooks/useTitle";


const Home = () => {
    const { t } = useTranslation();
    
    useTitle(t('title'));
    let [searchParams] = useSearchParams();
    const searchQuery = searchParams.get("search") || "";
    
    // const [searchQuery, setSearchQuery] = useState("");
    const isSearching = searchQuery.length > 0;

    const [storedCafes, setStoredCafes] = useState([]);

    return (
        <>
            <main className="pt-10 pb-[3.25rem] sm:py-10 space-y-6">
                <Container>
                    {isSearching ? (
                        <SearchResults searchQuery={searchQuery} setStoredCafes={setStoredCafes} storedCafes={storedCafes}  />
                    ) : (
                        <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} />
                    )}
                </Container>
            </main>
        </>
    );
};

export default Home;
