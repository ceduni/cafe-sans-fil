import Container from "./Container";

// TODO: remoce if not used

const TitleBanner = ({ title }) => {
  return (
    <section className="bg-white shadow">
      <Container>
        <div className="py-6">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 font-secondary">{title}</h1>
        </div>
      </Container>
    </section>
  );
};

export default TitleBanner;
