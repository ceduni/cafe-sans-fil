import { useParams } from "react-router-dom";
import ItemCard from "../components/ui/ItemCard";
import Container from "../components/ui/Container";
import { products } from "../components/Cart";
import { Link } from "react-router-dom";
import OpeningHours from "../components/ui/OpeningHours";
import CafeMemberHeader from "../components/ui/CafeMemberHeader";
import useApi from "../hooks/useApi";
import OpenIndicator from "../components/ui/OpenIndicator";
import EmptyState from "../components/ui/EmptyState";
import InfoBox from "../components/ui/InfoBox";
import { Helmet } from "react-helmet-async";
import PaymentMethods from "../components/ui/PaymentMethods";
import ContactCafe from "../components/ui/ContactCafe";

const Cafe = () => {
  const { id } = useParams();
  const { data, isLoading, error } = useApi(`/cafes/${id}`);

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  return (
    <>
      <Helmet>{data?.name && <title>{data.name} | Café sans-fil</title>}</Helmet>
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
          className="mb-6 rounded-lg shadow-xl object-cover h-52 md:h-96"
          src="https://placehold.co/800x400?text=Photo+du+café"
          alt=""
        />

        {(isLoading && <div className="animate-pulse h-10 w-1/5 bg-gray-200 rounded-full" />) || (
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{data?.name}</h2>
        )}
        <OpenIndicator isOpen={data?.is_open} />
        <p className="mt-2 text-lg leading-8 text-gray-600 max-w-3xl">
          {data?.description || (
            <>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5"></div>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
            </>
          )}
        </p>
        {!isLoading && (
          <>
            <PaymentMethods arrayOfMethods={data?.payment_methods} />
            <InfoBox
              title="Notre valeur ajoutée"
              message={`${data?.additional_info_cafe[0].key}: ${data?.additional_info_cafe[0].value}`}
            />
          </>
        )}
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
      <Container className="py-10 border-t border-gray-200">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Nous contacter</h2>
        <ContactCafe contact={data?.contact} socialMedia={data?.social_media} />
      </Container>
    </>
  );
};

export default Cafe;
