import Container from "@/components/Container";
import { Helmet } from "react-helmet-async";
import SearchBar from "@/components/Search/SearchBar";
import { useState } from "react";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";

const Home = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const isSearching = searchQuery.length > 0;

  const [storedCafes, setStoredCafes] = useState([]);

  return (
    <>
      <Helmet>
        <title>Accueil | Café sans-fil</title>
      </Helmet>
      <Container className="pt-9 pb-14 sm:py-14 space-y-6">
        <div className="flex items-center relative top-3">
            <h1 className="text-3xl sm:text-4xl text-opacity-90 font-secondary text-zinc-800">Cafés étudiants de l'UdeM</h1>
            <a href="https://www.umontreal.ca/" target="_blank" rel="noopener noreferrer">
                <img src="/udem_logo.png" alt="UdeM Logo" className="h-12 sm:h-16 w-auto ml-6 relative bottom-1 sm:bottom-3" />
            </a>
        </div>
        <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      </Container>
      <main>
        <Container>
          {(!isSearching && <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} />) || (
            <SearchResults searchQuery={searchQuery} storedCafes={storedCafes} />
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
