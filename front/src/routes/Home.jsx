import Container from "@/components/Container";
import { Helmet } from "react-helmet-async";
import SearchBar from "@/components/Search/SearchBar";
import { useState } from "react";
import CafeList from "@/components/CafeList";
import SearchResults from "@/components/Search/SearchResults";

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
