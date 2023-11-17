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
      <Container className="py-10 space-y-6">
        <h1 className="text-xl md:text-2xl text-gray-900 font-secondary">Cafés étudiants de l'UdeM</h1>
        <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      </Container>
      <main>
        <Container>
          {(!isSearching && <CafeList setStoredCafes={setStoredCafes} />) || (
            <SearchResults searchQuery={searchQuery} storedCafes={storedCafes} />
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
