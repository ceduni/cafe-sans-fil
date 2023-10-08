import logo from "/logo.png";

const Home = () => {
  return (
    <>
      <div>
        <img src={logo} className="h-36 p-4" alt="Café sans fil logo" />
      </div>
      <h1 className="text-3xl font-bold underline">Café sans fil</h1>
    </>
  );
};

export default Home;
