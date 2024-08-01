import { useState } from "react";
import ProductView from "@/components/Items/ProductView";
import { useCart } from "react-use-cart";
import toast from "react-hot-toast";
import { getCafeFromId } from "@/utils/getFromId";
import { formatPrice, getIdFromSelectedOptions } from "@/utils/cart";
import classNames from "classnames";
import { OUT_OF_STOCK_TEXT } from "@/utils/items";
import EditItemView from "@/components/Items/EditItemView";

const ItemCard = ({ item, cafeSlug, edit, onItemUpdate, showDescription }) => {
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

  {/* <div className="flex items-center  bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-300 "> */}
  <div className="flex items-center   transition-shadow duration-300 ">
          <div className="flex-shrink-0 relative">
            <img
              src={item.image_url || "https://placehold.co/300x300?text=Item"}
              alt={item.name}
              className={classNames(
                "h-14 w-14 object-cover rounded-full transition-transform duration-500",
                { "opacity-50": !item.in_stock },
                { "group-hover:opacity-75": item.in_stock },
                {"scale-50": !showDescription}, // diminue la taille quand la description n'est pas montrée
                {"scale-200": showDescription}, // augmente la taille quand la description est montrée
              )}
            />
            {!item.in_stock && (
                <div className={classNames(
              "absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center font-bold text-white rounded-full transition-transform duration-500",
              {"scale-50": !showDescription}, 
              {"scale-200": showDescription}, )}>
            {OUT_OF_STOCK_TEXT}
          </div>
            )}
          </div>
          <div className=" ml-2 flex-grow">
            {/* <h3 className="text-lg font-semibold text-gray-800">{item.name || "Sans nom"}</h3> */}
            <h3 className={`text-xs mr-2 font-semibold transition-all duration-500 ${!item.in_stock ? 'line-through text-gray-400' : 'text-gray-900'} ${showDescription ? 'scale-text-125' : ''}`}>
              {item.name || "Sans nom"} </h3>
            {showDescription && <p className="text-sm text-gray-600">{item.description}</p>}
          </div>
          <div className="flex-shrink-0">
            {/* <p className="text-lg font-medium text-gray-900">{formatPrice(item.price)}</p> */}
            <p className={`text-sm font-medium ${!item.in_stock ? 'text-gray-400' : 'text-gray-900'}`}>
    {formatPrice(item.price)}
  </p>
          </div>
        </div>
      </button>
    </>
  );
};

export default ItemCard;