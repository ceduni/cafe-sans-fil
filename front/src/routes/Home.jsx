import Container from "../components/ui/Container";
import { Helmet } from "react-helmet-async";
import Card from "../components/ui/Card";
import Search from "../components/Search";
import cafeList from "../data/cafes.json";
import { useState } from "react";
import Filters from "../components/ui/FIlters";

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
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
                {cafeList["cafes"].map((cafe) => (
                  <Card key={cafe.name} link={`/cafes/${cafe.name}`}>
                    <Card.Header>
                      <Card.Header.Title>{cafe.name}</Card.Header.Title>
                      <Card.Header.Subtitle>{cafe.location}</Card.Header.Subtitle>
                    </Card.Header>
                    <Card.Body>{cafe.description}</Card.Body>
                  </Card>
                ))}
              </div>
            </>
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
