import Container from "../components/ui/Container";
import { Helmet } from "react-helmet-async";
import SearchBar from "../components/SearchBar";
import { useState } from "react";
import CafeList from "../components/CafeList";
import SearchResults from "../components/SearchResults";

const Home = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const isSearching = searchQuery.length > 0;

  return (
    <>
      <Helmet>
        <title>Accueil | Café sans-fil</title>
      </Helmet>
      <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <main>
        <Container>{(!isSearching && <CafeList />) || <SearchResults searchQuery={searchQuery} />}</Container>
      </main>
    </>
  );
};

export default Home;
