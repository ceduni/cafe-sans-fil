import { PlusIcon } from "@heroicons/react/24/solid";
import EditItemView from "@/components/Items/EditItemView";
import { useState } from "react";

const AddItemCard = ({ cafeSlug, onItemUpdate }) => {
  const [itemEditOpen, setItemEditOpen] = useState(false);

  const item = {
    category: "",
    description: "",
    image_url: "",
    in_stock: true,
    name: "",
    options: [],
    price: 1,
    tags: [],
  };

  return (
    <>
      <EditItemView
        item={item}
        open={itemEditOpen}
        setOpen={setItemEditOpen}
        cafeSlug={cafeSlug}
        onItemUpdate={onItemUpdate}
      />
      <button
        className="group text-left focus:oiutline-2 focus:outline-offset-4 focus:outline-indigo-600 focus:rounded"
        onClick={() => setItemEditOpen(true)}>
        <div className="aspect-h-1 aspect-w-1 xl:aspect-h-8 xl:aspect-w-7 w-full rounded-3xl bg-gray-200 flex justify-center items-center">
          <PlusIcon className="text-gray-400 group-hover:text-gray-500 group-hover:scale-105 hover:transition-all duration-200" />
        </div>
        <h3 className="mt-4 font-medium tracking-tight text-gray-800">Ajouter un produit</h3>
      </button>
    </>
  );
};

export default AddItemCard;
