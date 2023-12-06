import { formatPrice } from "@/utils/cart";
import Modal from "@/components/Modal";
import { useEffect, useState } from "react";
import { CheckIcon, TrashIcon } from "@heroicons/react/24/solid";
import Input from "@/components/Input";
import Switch from "@/components/CustomSwitch";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import classNames from "classnames";
import EditItemOptions from "@/components/Items/EditItemOptions";

const EditItemView = ({ open, setOpen, item, cafeSlug, onItemUpdate }) => {
  const [productData, setProductData] = useState({
    category: item.category,
    description: item.description,
    image_url: item.image_url,
    in_stock: item.in_stock,
    name: item.name,
    options: item.options,
    price: item.price,
    tags: item.tags,
  });

  const isNewItem = item.item_id === undefined;

  useEffect(() => {
    // On réinitialise les données du produit à chaque ouverture du modal
    if (open) {
      setProductData({
        category: item.category,
        description: item.description,
        image_url: item.image_url,
        in_stock: item.in_stock,
        name: item.name,
        options: item.options,
        price: item.price,
        tags: item.tags,
      });
      !isNewItem && console.log(`Editing item ${item.slug}`);
    }
  }, [open]);

  const updateItem = (newItem) => {
    const toastId = toast.loading("Mise à jour du produit...");
    authenticatedRequest
      .put(`/cafes/${cafeSlug}/menu/${item.slug}`, newItem)
      .then(() => {
        onItemUpdate(); // Refetch the data
        toast.success("Produit mis à jour");
        setOpen(false);
      })
      .catch((error) => {
        switch (error.response?.status) {
          case 409:
            if (error.response.data?.detail.includes("name")) {
              toast.error("Le nom du produit doit être unique dans le menu de votre café.");
            } else {
              toast.error("Les options du produit doivent être uniques.");
            }
            break;
          default:
            toast.error("Erreur lors de la mise à jour du produit");
            break;
        }
      })
      .finally(() => {
        toast.dismiss(toastId);
      });
  };

  const deleteItem = () => {
    if (confirm(`La suppression de ${item.name} est irréversible. Continuer ?`)) {
      const toastId = toast.loading("Suppression du produit...");
      authenticatedRequest
        .delete(`/cafes/${cafeSlug}/menu/${item.slug}`)
        .then(() => {
          onItemUpdate(); // Refetch the data
          toast.success("Produit supprimé");
          setOpen(false);
        })
        .catch(() => {
          toast.error("Erreur lors de la suppression du produit");
        })
        .finally(() => {
          toast.dismiss(toastId);
        });
    }
  };

  const addItem = (newItem) => {
    const toastId = toast.loading("Ajout du produit...");
    authenticatedRequest
      .post(`/cafes/${cafeSlug}/menu`, newItem)
      .then(() => {
        onItemUpdate(); // Refetch the data
        toast.success("Produit ajouté");
        setOpen(false);
      })
      .catch(() => {
        toast.error("Erreur lors de l'ajout du produit");
      })
      .finally(() => {
        toast.dismiss(toastId);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isNewItem) {
      addItem(productData);
    } else {
      updateItem(productData);
    }
  };

  return (
    <Modal open={open} setOpen={setOpen}>
      <form className="w-full" onSubmit={handleSubmit}>
        <h2 className="text-lg font-medium text-gray-900 leading-6">
          {isNewItem ? "Ajouter un produit" : "Modifier le produit"}
        </h2>
        <div>
          <div className="space-y-2 mt-6">
            <label htmlFor="itemName" className="block text-sm font-medium text-gray-700">
              Nom
            </label>
            <Input
              type="text"
              id="itemName"
              value={productData.name}
              onChange={(e) => setProductData({ ...productData, name: e.target.value })}
              required
            />
            <p className="mt-2 text-sm text-gray-500">Le nom du produit doit être unique dans le menu de votre café.</p>
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor="price" className="block text-sm font-medium text-gray-700">
              Prix
            </label>
            <Input
              type="number"
              step="0.01"
              min="0"
              max="1000"
              id="price"
              value={productData.price}
              className="peer"
              onChange={(e) => setProductData({ ...productData, price: e.target.value })}
              required
            />
            <p className="mt-2 text-sm text-gray-500 peer-invalid:invisible">
              Apparaîtra: {formatPrice(productData.price)}
            </p>
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              id="description"
              value={productData.description}
              onChange={(e) => setProductData({ ...productData, description: e.target.value })}
              className="block w-full rounded-md shadow-sm sm:text-sm \
              focus:ring-2 focus:ring-inset focus:ring-sky-600 focus:ring-opacity-75 \
              ring-1 ring-inset ring-gray-300 border-0 \
              focus:invalid:border-red-600 focus:invalid:ring-red-600 focus:invalid:ring-opacity-70"
              required
            />
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor="category" className="block text-sm font-medium text-gray-700">
              Catégorie
            </label>
            <Input
              type="text"
              id="category"
              value={productData.category}
              onChange={(e) => setProductData({ ...productData, category: e.target.value })}
              required
            />
            <p className="mt-2 text-sm text-gray-500">
              Il faut que le nom de la catégorie soit exactement identique à celui de la catégorie cible.
            </p>
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor="image_url" className="block text-sm font-medium text-gray-700">
              URL de l'image
            </label>
            <Input
              type="url"
              id="image_url"
              value={productData.image_url}
              onChange={(e) => setProductData({ ...productData, image_url: e.target.value })}
              required
            />
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor="in_stock" className="block text-sm font-medium text-gray-700">
              En stock
            </label>
            <Switch checked={productData.in_stock} onChange={(e) => setProductData({ ...productData, in_stock: e })} />
          </div>
        </div>

        <EditItemOptions productData={productData} setProductData={setProductData} />

        <div
          className={classNames("flex items-center mt-12 text-sm font-semibold", {
            "justify-between": !isNewItem,
            "justify-end": isNewItem,
          })}>
          {!isNewItem && (
            <button
              type="button"
              className="inline-flex items-center justify-center gap-2 px-3 py-2 bg-white text-red-500 rounded-md hover:bg-red-50 \
            focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              onClick={() => deleteItem()}>
              <TrashIcon className="w-5 h-5" />
              <span className="hidden sm:block">Supprimer le produit</span>
            </button>
          )}

          <div className="flex space-x-4">
            <button
              type="button"
              className="px-3 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 \
            focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              onClick={() => setOpen(false)}>
              Annuler
            </button>
            <button
              type="submit"
              className="inline-flex items-center justify-center gap-2 px-3 py-2 text-white bg-emerald-600 rounded-md shadow-sm hover:bg-emerald-500 \
            focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
              <CheckIcon className="w-5 h-5" />
              Enregistrer
            </button>
          </div>
        </div>
      </form>
    </Modal>
  );
};

export default EditItemView;
