import Container from "../components/ui/Container";
import { Helmet } from "react-helmet-async";
import Search from "../components/Search";
import cafeList from "../data/cafes.json";
import { useState } from "react";
import Filters from "../components/ui/FIlters";
import CafeList from "../components/CafeList";

const Home = () => {
  const [isSearching, setIsSearching] = useState(false);

  return (
    <>
      <Helmet>
        <title>Accueil | Café sans-fil</title>
      </Helmet>
      <Search isSearching={isSearching} setIsSearching={setIsSearching} />
      <main>
        <Container>
          {!isSearching && (
            <>
              <Filters />
              <CafeList />
            </>
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
