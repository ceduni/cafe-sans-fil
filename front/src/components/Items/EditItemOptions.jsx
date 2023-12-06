import { formatPrice } from "@/utils/cart";
import { PlusIcon, TrashIcon } from "@heroicons/react/24/solid";
import { useState, useEffect } from "react";
import Input from "@/components/Input";

const EditItemOptions = ({ productData, setProductData }) => {
  const [options, setOptions] = useState(productData.options || []);

  const handleOptionChange = (index, key, value) => {
    setOptions(options.map((option, i) => (i === index ? { ...option, [key]: value } : option)));
  };

  const addOption = () => {
    setOptions([...options, { type: "", value: "", fee: 0 }]);
  };

  const removeOption = (index) => {
    setOptions(options.filter((_, i) => i !== index));
  };

  useEffect(() => {
    if (!options.type || !options.value) return;
    setProductData({ ...productData, options: options });
  }, [options]);

  return (
    <div className="mt-6">
      <p className="text-sm font-medium text-gray-700">Options du produit</p>
      <p className="text-sm text-gray-500 mt-1">
        Les options sont des variantes d'un produit pouvant avoir un surcoût. Un café peut avoir comme type "taille" et
        comme valeurs "grand" et "moyen".{" "}
      </p>
      <p className="text-sm text-gray-500 mt-1 font-medium">
        Les options seront groupées par type. Attention à entrer le même type pour les options liées.
      </p>
      {options.map((option, index) => (
        <div key={index} className="mt-6">
          <div className="mt-6 grid grid-cols-6 gap-x-6 gap-y-4 sm:grid-cols-12">
            <div className="sm:col-span-4 space-y-2 col-span-3">
              <label htmlFor="type" className="block text-sm font-medium text-gray-700">
                Type
              </label>
              <Input
                type="text"
                id="type"
                value={option.type}
                onChange={(e) => handleOptionChange(index, "type", e.target.value.toLowerCase())}
                required
              />
            </div>
            <div className="sm:col-span-4 space-y-2 col-span-3">
              <label htmlFor="value" className="block text-sm font-medium text-gray-700">
                Valeur
              </label>
              <Input
                type="text"
                id="value"
                value={option.value}
                onChange={(e) => handleOptionChange(index, "value", e.target.value.toLowerCase())}
                required
              />
            </div>
            <div className="sm:col-span-2 space-y-2 col-span-3">
              <label htmlFor="fee" className="block text-sm font-medium text-gray-700 mb-2">
                Frais en +
              </label>
              <Input
                type="number"
                value={option.fee}
                onChange={(e) => handleOptionChange(index, "fee", e.target.value)}
                step="0.01"
                min="0"
                max="1000"
              />
            </div>

            <div className="sm:col-span-2 flex items-end sm:justify-end col-span-3">
              <button
                type="button"
                onClick={() => removeOption(index)}
                className="text-red-500 p-2 rounded-md hover:bg-gray-200 inline-flex gap-2 items-center focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                <TrashIcon className="w-5 h-5" />
                <span className="sm:hidden">Supprimer</span>
              </button>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-4">
            {productData.name}{" "}
            {option.type && option.value && (
              <>
                avec <span className="capitalize">{option.type}</span>{" "}
                <span className="capitalize">{option.value}</span>
              </>
            )}{" "}
            coûtera{" "}
            {option.fee > 0 ? (
              <>{formatPrice(parseFloat(option.fee) + parseFloat(productData.price))} au total</>
            ) : (
              "le même prix"
            )}
          </p>
        </div>
      ))}

      <button type="button" className="mt-6 text-sm font-medium text-gray-700 hover:text-gray-500" onClick={addOption}>
        <PlusIcon className="w-5 h-5 inline-block mr-2 -mt-1" />
        Ajouter un type de variante
      </button>
    </div>
  );
};

export default EditItemOptions;
