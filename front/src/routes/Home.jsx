import Container from "../components/ui/Container";
import { Helmet } from "react-helmet-async";
import SearchBar from "../components/SearchBar";
import { useState } from "react";
import CafeList from "../components/CafeList";

const Home = () => {
  const [isSearching, setIsSearching] = useState(false);

  return (
    <>
      <Helmet>
        <title>Accueil | Café sans-fil</title>
      </Helmet>
      <SearchBar isSearching={isSearching} setIsSearching={setIsSearching} />
      <main>
        <Container>
          {!isSearching && (
            <>
              <CafeList />
            </>
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
