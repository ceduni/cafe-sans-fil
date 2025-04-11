import { useState, useRef, useEffect } from "react";
// import { Helmet } from "react-helmet-async";
import { useTranslation } from "react-i18next";
import Container from "@/components/Layout/Container";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";
import { useSearchParams } from 'react-router-dom';
import useTitle from "@/hooks/useTitle";
import EventBoard from "@/components/Event/EventBoard"


const Home = () => {
    const { t } = useTranslation();

    useTitle(t('title'));
    let [searchParams] = useSearchParams();
    const searchQuery = searchParams.get("search") || "";

    // const [searchQuery, setSearchQuery] = useState("");
    const isSearching = searchQuery.length > 0;

    const [storedCafes, setStoredCafes] = useState([]);
    
    const [storedEvents, setStoredEvents] = useState([]);

    const cafeRef = useRef<HTMLDivElement>(null);
    const [gridHeight, setGridHeight] = useState(null);

    useEffect(() => {
        if (cafeRef.current) {
            setGridHeight(cafeRef.current.height);
            console.log(gridHeight);
        }
    }, [storedCafes]);

    return (
        <>
            <main className="pt-10 pb-[3.25rem] sm:py-10 space-y-6 inline-flex justify-between">
                <Container className="">
                    {isSearching ? (
                        <SearchResults searchQuery={searchQuery} setStoredCafes={setStoredCafes} storedCafes={storedCafes}  />
                    ) : (
                        <CafeList  ref={cafeRef} setStoredCafes={setStoredCafes} storedCafes={storedCafes} />
                    )}
                </Container>
                <Container className="overflow-y-auto" style={{ height: gridHeight ? `${gridHeight}px` : undefined }}>
                    <EventBoard setStoredEvents={setStoredEvents} storedEvents={storedEvents}/>                    
                </Container>
            </main>
        </>
    );
};

export default Home;
