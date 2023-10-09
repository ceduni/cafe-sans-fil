import Container from "../components/ui/Container";
import TitleBanner from "../components/ui/TitleBanner";
import logo from "/logo.png";
import { Helmet } from "react-helmet";
import Card from "../components/ui/Card";

const Home = () => {
  return (
    <>
      <Helmet>
        <title>Accueil | Café sans fil</title>
      </Helmet>
      <TitleBanner title="Liste des cafés" />
      <main>
        <Container>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-10">
            {Array.from(Array(4).keys()).map((i) => (
              <Card key={i}>
                <Card.Header>
                  <Card.Header.Title>Card Title</Card.Header.Title>
                </Card.Header>
                <Card.Body>This is the body</Card.Body>
                <Card.Footer>This is the footer</Card.Footer>
              </Card>
            ))}
          </div>
        </Container>
      </main>
    </>
  );
};

export default Home;
