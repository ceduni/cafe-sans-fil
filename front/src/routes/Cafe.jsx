import { useParams } from "react-router-dom";
import ItemCard from "../components/ui/ItemCard";
import Container from "../components/ui/Container";
import { products } from "../components/Cart";
import { Link } from "react-router-dom";
import OpeningHours from "../components/ui/OpeningHours";
import CafeMemberHeader from "../components/ui/CafeMemberHeader";

const Cafe = () => {
  const { id } = useParams();

  return (
    <div className="bg-white">
      <Container className="py-10">
        <CafeMemberHeader />
        <div className="mb-5 text-gray-500 font-semibold">
          <Link to="/" className="underline underline-offset-2 hover:no-underline">
            Liste des cafés
          </Link>
          <span className="px-3">&gt;</span>
          {id}
        </div>

        <img
          className="mb-6 rounded-lg shadow-xl object-cover w-full md:w-auto md:h-96"
          src="https://i.pinimg.com/originals/8f/5f/d0/8f5fd07d1034e0d4941c4ad9d58ec055.jpg"
          alt=""
        />

        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{id}</h2>
        <div className="my-3 flex items-center gap-x-1.5">
          <div className="flex-none rounded-full bg-emerald-500/20 p-1">
            <div className="h-3 w-3 rounded-full bg-emerald-500" />
          </div>
          <p className="text-sm leading-5 text-gray-500 font-semibold">Ouvert</p>
        </div>
        <p className="mt-2 text-lg leading-8 text-gray-600 max-w-3xl">
          Sandwichs maisons préparés sur place. Succulents bagels au saumon fumé. De namebreux choix végé. Carte de
          fidélité disponible. Baby-foot. Ouvert l'été.
        </p>
        <OpeningHours />
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
