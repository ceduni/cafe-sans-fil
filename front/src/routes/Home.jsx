import Container from "../components/ui/Container";
import { Helmet } from "react-helmet";
import Card from "../components/ui/Card";
import Search from "../components/Search";
import cafeList from "../data/cafes.json";

const Home = () => {
  return (
    <>
      <Helmet>
        <title>Accueil | Café sans-fil</title>
      </Helmet>
      <Search />
      <main>
        <Container>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
            {cafeList["cafes"].map((cafe) => (
              <Card key={cafe.id}>
                <Card.Header>
                  <Card.Header.Title>{cafe.name}</Card.Header.Title>
                </Card.Header>
                <Card.Body>{cafe.description}</Card.Body>
                <Card.Footer>Visiter</Card.Footer>
              </Card>
            ))}
          </div>
        </Container>
      </main>
    </>
  );
};

export default Home;
