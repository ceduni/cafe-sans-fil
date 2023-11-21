import { useState } from "react";
import ProductView from "@/components/Items/ProductView";
import Badge from "@/components/Badge";
import { useCart } from "react-use-cart";
import toast from "react-hot-toast";
import { getCafeFromId } from "@/utils/getFromId";
import { formatPrice, getIdFromSelectedOptions } from "@/utils/cart";
import classNames from "classnames";
import { OUT_OF_STOCK_TEXT } from "@/utils/items";

const ItemCard = ({ item, cafeId }) => {
  const [itemPreviewOpen, setItemPreviewOpen] = useState(false);

  const [selectedOptions, setSelectedOptions] = useState({});
  const [itemFinalPrice, setItemFinalPrice] = useState(item.price);

  // On update le prix pour qu'il soit affiché avec 2 décimales
  item = {
    ...item,
    price: formatPrice(item.price),
  };

  const { addItem } = useCart();
  const handleAddToCart = async (e, setIsAddingToCart) => {
    e.preventDefault();
    setIsAddingToCart(true);
    const cafe = await getCafeFromId(cafeId);
    addItem({
      ...item,
      // Il est obligatoire de passer un id unique à chaque item
      id: item.item_id + getIdFromSelectedOptions(selectedOptions),
      cafe: cafe, // On ajout l'info du café pour pouvoir l'afficher dans le panier
      price: itemFinalPrice,
      selectedOptions: selectedOptions,
    });
    setItemPreviewOpen(false);
    toast.success(`${item.name} a été ajouté au panier`);
    setIsAddingToCart(false);
  };

  return (
    <>
      <ProductView
        item={item}
        open={itemPreviewOpen}
        setOpen={setItemPreviewOpen}
        onSubmit={handleAddToCart}
        selectedOptions={selectedOptions}
        setSelectedOptions={setSelectedOptions}
        itemFinalPrice={itemFinalPrice}
        setItemFinalPrice={setItemFinalPrice}
      />
      <button key={item.item_id} className="group text-left" onClick={() => setItemPreviewOpen(true)}>
        <div className="aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-lg bg-gray-200 xl:aspect-h-8 xl:aspect-w-7">
          <img
            src={item.image_url || "https://placehold.co/300x300?text=Item"}
            className={classNames("h-full w-full object-cover object-center", {
              "group-hover:opacity-60 hover:transition-all duration-300": item.in_stock,
              "opacity-50": !item.in_stock,
            })}
          />
        </div>
        <h3 className="mt-4 text-gray-800">{item.name}</h3>
        <p className="mt-1 text-lg font-medium text-gray-900">${item.price}</p>
        {!item.in_stock && (
          <div className="my-1">
            <Badge variant="danger">{OUT_OF_STOCK_TEXT}</Badge>
          </div>
        )}
      </button>
    </>
  );
};

export default ItemCard;
