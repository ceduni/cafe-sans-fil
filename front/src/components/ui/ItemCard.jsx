import { useState } from "react";
import ProductView from "../ProductView";

const ItemCard = ({ item }) => {
  const [itemPreviewOpen, setItemPreviewOpen] = useState(false);

  return (
    <>
      <ProductView product={item} open={itemPreviewOpen} setOpen={setItemPreviewOpen} />
      <button key={item.item_id} className="group text-left" onClick={() => setItemPreviewOpen(true)}>
        <div className="aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-lg bg-gray-200 xl:aspect-h-8 xl:aspect-w-7">
          <img
            src="https://placehold.co/300x300?text=Item"
            className="h-full w-full object-cover object-center group-hover:opacity-75"
          />
        </div>
        <h3 className="mt-4 text-sm text-gray-700">{item.name}</h3>
        <p className="mt-1 text-lg font-medium text-gray-900">${item.price}</p>
      </button>
    </>
  );
};

export default ItemCard;
