import { useState } from "react";
import ProductView from "@/components/Items/ProductView";
import { useCart } from "react-use-cart";
import toast from "react-hot-toast";
import { getCafeFromId } from "@/utils/getFromId";
import { formatPrice, getIdFromSelectedOptions } from "@/utils/cart";
import classNames from "classnames";
import { OUT_OF_STOCK_TEXT } from "@/utils/items";
import EditItemView from "@/components/Items/EditItemView";

const ItemCard = ({ item, cafeSlug, edit, onItemUpdate }) => {
  const [itemPreviewOpen, setItemPreviewOpen] = useState(false);
  const [itemEditOpen, setItemEditOpen] = useState(false);

  const [selectedOptions, setSelectedOptions] = useState({});
  const [itemFinalPrice, setItemFinalPrice] = useState(item.price);

  const { addItem } = useCart();
  const handleAddToCart = async (e, setIsAddingToCart) => {
    e.preventDefault();
    setIsAddingToCart(true);
    const cafe = await getCafeFromId(cafeSlug);
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
      {(!edit && (
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
      )) || (
        <EditItemView
          item={item}
          open={itemEditOpen}
          setOpen={setItemEditOpen}
          cafeSlug={cafeSlug}
          onItemUpdate={onItemUpdate}
        />
      )}
      <button
        key={item.item_id}
        className="group text-left focus:outline-2 focus:outline-offset-4 focus:outline-indigo-600 focus:rounded"
        onClick={() => (edit ? setItemEditOpen(true) : setItemPreviewOpen(true))}>
        <div className="aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-3xl bg-gray-200 xl:aspect-h-8 xl:aspect-w-7 relative hover:animate-scale">
          <img
            src={item.image_url || "https://placehold.co/300x300?text=Item"}
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "https://placehold.co/300x300?text=:/";
            }}
            className={classNames("h-full w-full object-cover object-center", {
              "group-hover:opacity-90 group-hover:scale-105 hover:transition-all duration-200": item.in_stock,
            })}
          />
          {!item.in_stock && (
            <div className="absolute inset-0 p-4 bg-gradient-to-t from-gray-500 to-transparent font-bold text-white flex items-end justify-center">
              {OUT_OF_STOCK_TEXT}
            </div>
          )}
        </div>
        <h3 className={classNames("mt-4 font-semibold tracking-tight text-gray-800", { "opacity-60": !item.in_stock })}>
          {item.name || "Sans nom"}
        </h3>
        <p className={classNames("mt-1 text-lg font-medium text-gray-900", { "opacity-60": !item.in_stock })}>
          {formatPrice(item.price)}
        </p>
      </button>
    </>
  );
};

export default ItemCard;
