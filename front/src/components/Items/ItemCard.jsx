import { useState } from "react";
import ProductView from "@/components/Items/ProductView";
import Badge from "@/components/Badge";
import { useCart } from "react-use-cart";
import toast from "react-hot-toast";
import { getCafeFromId } from "@/helpers/getFromId";

const ItemCard = ({ item, cafeId }) => {
  const [itemPreviewOpen, setItemPreviewOpen] = useState(false);

  // On update le prix pour qu'il soit affiché avec 2 décimales
  item = {
    ...item,
    price: item.price.toFixed(2),
  };

  const { addItem } = useCart();
  const handleAddToCart = async (e, setIsAddingToCart) => {
    e.preventDefault();
    setIsAddingToCart(true);
    const cafe = await getCafeFromId(cafeId);
    addItem({
      ...item,
      id: item.item_id, // Il est obligatoire de passer un id unique à chaque item
      cafe: cafe, // On ajout l'info du café pour pouvoir l'afficher dans le panier
    });
    setItemPreviewOpen(false);
    toast.success(`${item.name} a été ajouté au panier`);
    setIsAddingToCart(false);
  };

  return (
    <>
      <ProductView item={item} open={itemPreviewOpen} setOpen={setItemPreviewOpen} onSubmit={handleAddToCart} />
      <button key={item.item_id} className="group text-left" onClick={() => setItemPreviewOpen(true)}>
        <div className="aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-lg bg-gray-200 xl:aspect-h-8 xl:aspect-w-7">
          <img
            src="https://placehold.co/300x300?text=Item"
            className="h-full w-full object-cover object-center group-hover:opacity-75"
          />
        </div>
        <h3 className="mt-4 text-gray-800">{item.name}</h3>
        <p className="mt-1 text-lg font-medium text-gray-900">${item.price}</p>
        {!item.is_available && (
          <div className="my-1">
            <Badge variant="danger">Indisponible</Badge>
          </div>
        )}
      </button>
    </>
  );
};

export default ItemCard;
