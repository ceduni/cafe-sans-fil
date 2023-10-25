import { useParams } from "react-router-dom";
import ItemCard from "../components/ui/ItemCard";
import Container from "../components/ui/Container";
import { products } from "../components/Cart";
import { Link } from "react-router-dom";
import OpeningHours from "../components/ui/OpeningHours";
import CafeMemberHeader from "../components/ui/CafeMemberHeader";
import useApi from "../hooks/useApi";

const Cafe = () => {
  const { id } = useParams();
  const { data, isLoading, error } = useApi(`/cafes/${id}`);

  if (error) {
    console.error(error);
    return (
      <div className="flex flex-col items-center justify-center py-10">
        <p className="text-2xl font-semibold tracking-tight text-gray-900 sm:text-3xl">Une erreur est survenue...</p>
        <p className="mt-6 text-base leading-7 text-gray-600 text-center">
          <i>
            {error.status ? `${error.status} - ` : ""} {error.statusText || error.message}
          </i>
          <br />
          L'API est-elle bien lancée?
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white">
      <Container className="py-10">
        <CafeMemberHeader />
        <div className="mb-5 text-gray-500 font-semibold">
          <Link to="/" className="underline underline-offset-2 hover:no-underline">
            Liste des cafés
          </Link>
          <span className="px-3">&gt;</span>
          {(isLoading && <span className="animate-pulse">Chargement...</span>) || data?.name}
        </div>

        <img
          className="mb-6 rounded-lg shadow-xl object-cover w-full md:w-auto md:h-96"
          src="https://i.pinimg.com/originals/8f/5f/d0/8f5fd07d1034e0d4941c4ad9d58ec055.jpg"
          alt=""
        />

        {(isLoading && <div className="animate-pulse h-6 w-1/5 bg-gray-200 rounded-full mb-4" />) || (
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{data?.name}</h2>
        )}
        {(data?.is_open && (
          <div className="my-3 flex items-center gap-x-1.5">
            <div className="flex-none rounded-full bg-emerald-500/20 p-1">
              <div className="h-3 w-3 rounded-full bg-emerald-500" />
            </div>
            <p className="text-sm leading-5 text-gray-500 font-semibold">Ouvert</p>
          </div>
        )) || (
          <div className="my-3 flex items-center gap-x-1.5">
            <div className="flex-none rounded-full bg-red-500/20 p-1">
              <div className="h-3 w-3 rounded-full bg-red-500" />
            </div>
            <p className="text-sm leading-5 text-gray-500 font-semibold">Fermé</p>
          </div>
        )}
        <p className="mt-2 text-lg leading-8 text-gray-600 max-w-3xl">{data?.description || "Description du café"}</p>
        <OpeningHours openingHours={data?.opening_hours} />
      </Container>
      <Container className="py-10 border-t border-gray-200">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Menu</h2>
        <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:grid-cols-4 lg:gap-x-8">
          {data?.menu_items.map((product) => (
            <ItemCard key={product.item_id} item={product} />
          ))}
        </div>
      </Container>
    </div>
  );
};

export default Cafe;
