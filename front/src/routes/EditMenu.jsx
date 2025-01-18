import { useParams } from "react-router-dom";
import Container from "@/components/Layout/Container";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";
import { getCafeCategories, getItemByCategory } from "@/utils/items";
import ItemCard from "@/components/Items/ItemCard";
import Breadcrumbs from "@/components/Breadcrumbs";
import LoadingSpinner from "@/components/LoadingSpinner";
import AddItemCard from "@/components/Items/AddItemCard";
import MemberOnly from "@/helpers/MemberOnly";

const EditMenu = () => {
  const { id: cafeSlug } = useParams();
  const { data, isLoading, error, refetch } = useApi(`/cafes/${cafeSlug}`);

  const menuItems = data?.menu_items || [];
  const categories = getCafeCategories(menuItems);

  const onItemUpdate = () => refetch();

  return (
    <MemberOnly cafe={data} error={error}>
      <Helmet>{data && <title>Édition du menu de {data.name} | Café sans-fil</title>}</Helmet>
      <Container className="py-10">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
            {data?.name}
          </Breadcrumbs.Item>
          <Breadcrumbs.Item>Modifier le menu</Breadcrumbs.Item>
        </Breadcrumbs>

        <div className="pb-12">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Catégories de produits</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Ici apparaissent les catégories de produits qui apparaîtront sur la page de votre café.
            <br /> Elles sont générées automatiquement à partir des produits que vous avez ajoutés.
          </p>
        </div>

        <div className="mb-12 border-b pb-12 last:border-b-0 last:pb-0">
          <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-4 lg:grid-cols-5 lg:gap-x-8 items-start">
            <AddItemCard cafeSlug={cafeSlug} onItemUpdate={onItemUpdate} />
          </div>
        </div>

        {isLoading && menuItems.length === 0 && <LoadingSpinner />}

        {categories.map((category) => (
          <div key={category} className="mb-12 border-b pb-12 last:border-b-0 last:pb-0">
            <h3 className="font-medium">{category}</h3>
            <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-4 lg:grid-cols-5 lg:gap-x-8 items-start">
              {getItemByCategory(menuItems, category).map((product) => (
                <ItemCard key={product.slug} item={product} cafeSlug={cafeSlug} edit onItemUpdate={onItemUpdate} />
              ))}
            </div>
          </div>
        ))}
      </Container>
    </MemberOnly>
  );
};

export default EditMenu;
