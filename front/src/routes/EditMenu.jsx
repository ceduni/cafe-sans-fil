import { useParams } from "react-router-dom";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import EmptyState from "@/components/EmptyState";
import { Helmet } from "react-helmet-async";
import { Link } from "react-router-dom";
import { isAdmin } from "@/utils/admin";
import { useAuth } from "@/hooks/useAuth";
import ErrorState from "@/components/ErrorState";

const EditMenu = () => {
  const { id: cafeSlug } = useParams();
  const [data, isLoading, error] = useApi(`/cafes/${cafeSlug}`);
  const { user: loggedInUser } = useAuth();

  if (error) {
    if (error.status === 404) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  if (data && !isAdmin(data, loggedInUser?.username)) {
    return (
      <ErrorState
        title="Accès refusé"
        message="Vous n'avez pas accès à cette page"
        linkText={`Retour à ${data.name}`}
        linkTo={`/cafes/${cafeSlug}`}
      />
    );
  }

  // On récupère les catégories de produits proposées par le café, sans doublons
  const categories = [...new Set(data?.menu_items.map((product) => product.category))];
  const getItemByCategory = (category) => {
    return data?.menu_items.filter((product) => product.category === category);
  };

  return (
    <>
      <Helmet>{data && <title>Édition du menu de {data.name} | Café sans-fil</title>}</Helmet>
      <Container className="py-10">
        <div className="mb-6 text-gray-500 font-semibold">
          <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
            {(isLoading && <span className="animate-pulse">Chargement...</span>) || data?.name}
          </Link>
          <span className="px-3">&gt;</span>
          <span className="text-gray-600 font-bold">Modifier le menu</span>
        </div>

        <div className="pb-12">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Catégories de produits</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Ici apparaissent les catégories de produits qui apparaîtront sur la page de votre café.
          </p>
        </div>

        {categories.map((category) => (
          <div key={category} className="mb-12">
            <h3 className="text-lg font-semibold">{category}</h3>
            <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:grid-cols-4 lg:gap-x-8 items-start">
              {getItemByCategory(category).map((product) => (
                <p key={product.item_id} className="text-gray-900">
                  {product.name}
                </p>
              ))}
            </div>
          </div>
        ))}
      </Container>
    </>
  );
};

export default EditMenu;
