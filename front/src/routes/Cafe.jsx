import { useParams } from "react-router-dom";
import ItemCard from "../components/ItemCard";
import Container from "../components/ui/Container";
import { products } from "../components/Cart";

const Cafe = () => {
  const { id } = useParams();

  return (
    <div className="bg-white">
      <Container className="py-10">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{id}</h2>
        <p className="mt-2 text-lg leading-8 text-gray-600">Description de {id}</p>
        <div className="my-2 flex items-center gap-x-1.5">
          <div className="flex-none rounded-full bg-emerald-500/20 p-1">
            <div className="h-3 w-3 rounded-full bg-emerald-500" />
          </div>
          <p className="text-sm leading-5 text-gray-500">Ouvert</p>
        </div>
        <img
          className="mt-6 rounded-lg shadow-xl h-80 object-cover"
          src="https://i.pinimg.com/originals/8f/5f/d0/8f5fd07d1034e0d4941c4ad9d58ec055.jpg"
          alt=""
        />
      </Container>
      <Container className="py-10 border-t border-gray-200">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Menu</h2>
        <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
          {products.map((product) => (
            <ItemCard key={product.id} item={product} />
          ))}
        </div>
      </Container>
    </div>
  );
};

export default Cafe;