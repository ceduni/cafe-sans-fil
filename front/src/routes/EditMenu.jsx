import { useParams } from "react-router-dom";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";
import { Link } from "react-router-dom";
import { getCafeCategories, getItemByCategory } from "@/utils/items";
import AdminOnly from "@/helpers/AdminOnly";
import ItemCard from "@/components/items/ItemCard";

const EditMenu = () => {
  const { id: cafeSlug } = useParams();
  const [data, isLoading, error] = useApi(`/cafes/${cafeSlug}`);

  const menuItems = data?.menu_items;
  const categories = getCafeCategories(menuItems);

  return (
    <AdminOnly cafe={data} error={error}>
      <Helmet>{data && <title>Édition du menu de {data.name} | Café sans-fil</title>}</Helmet>
      <Container className="py-10">
        <div className="mb-6 text-gray-500 font-semibold">
          <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
            {(isLoading && <span className="animate-pulse">Chargement...</span>) || data?.name}
          </Link>
          <span className="px-3">&gt;</span>
          <span className="text-gray-600 font-bold">Modifier le menu</span>
        </div>

        <div className="pb-12 border-b mb-12">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Catégories de produits</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Ici apparaissent les catégories de produits qui apparaîtront sur la page de votre café.
          </p>
        </div>

        {categories.map((category) => (
          <div key={category} className="mb-12 border-b pb-12 last:border-b-0 last:pb-0">
            <h3 className="font-medium">{category}</h3>
            <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-4 lg:grid-cols-5 lg:gap-x-8 items-start">
              {getItemByCategory(menuItems, category).map((product) => (
                <ItemCard key={product.item_id} item={product} cafeId={cafeSlug} edit />
              ))}
            </div>
          </div>
        ))}
      </Container>
    </AdminOnly>
  );
};

export default EditMenu;
