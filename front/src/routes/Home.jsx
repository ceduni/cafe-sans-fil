import { useState } from "react";
import { Helmet } from "react-helmet-async";
import { useTranslation } from "react-i18next";
import Container from "@/components/Container";
import SearchBar from "@/components/Search/SearchBar";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";


const TX = {
    HEAD_TITLE: 'title',
    HOME_TITLE: 'home.title',
}

const Home = () => {
    const { t } = useTranslation();
    
    const [searchQuery, setSearchQuery] = useState("");
    const isSearching = searchQuery.length > 0;

    const [storedCafes, setStoredCafes] = useState([]);

    return (
        <>
            <Helmet>
                <title>{t(TX.HEAD_TITLE)}</title>
            </Helmet>
            <Container className="pt-10 pb-[3.25rem] sm:py-14 space-y-6">
                <div className="flex gap-2">
                    <h1 className="text-3xl sm:text-4xl text-opacity-90 font-secondary text-zinc-800 leading-7">
                        {t(TX.HOME_TITLE)}
                    </h1>
                </div>
                <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
            </Container>
            <main>
                <Container>
                    {isSearching ? (
                        <SearchResults searchQuery={searchQuery} storedCafes={storedCafes} />
                    ) : (
                        <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} />
                    )}
                </Container>
            </main>
        </>
    );
};

export default Home;
