import { Fragment, useEffect, useState } from "react";
import { Dialog, RadioGroup, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import Badge from "../Badge";
import { DEFAULT_OPTION_NAME, arrayToOptionsByType, formatPrice } from "@/utils/cart";
import classNames from "classnames";
import { IN_STOCK_TEXT, OUT_OF_STOCK_TEXT } from "@/utils/items";

const ProductView = ({
  item,
  open,
  setOpen,
  onSubmit,
  selectedOptions,
  setSelectedOptions,
  itemFinalPrice,
  setItemFinalPrice,
}) => {
  const [isAddingToCart, setIsAddingToCart] = useState(false);

  const optionsByType = arrayToOptionsByType(item.options);

  useEffect(() => {
    // On sélectionne "Régulier" par défaut pour chaque type d'option
    const defaultOptions = {};
    Object.keys(optionsByType).forEach((type) => {
      defaultOptions[type] = {
        value: DEFAULT_OPTION_NAME,
        fee: "0",
      };
    });
    setSelectedOptions(defaultOptions);
  }, [open]);

  useEffect(() => {
    // On update le prix de l'item en fonction des options sélectionnées
    let finalPrice = item.price;
    Object.keys(selectedOptions).forEach((type) => {
      finalPrice = parseFloat(finalPrice) + parseFloat(selectedOptions[type].fee);
    });
    setItemFinalPrice(formatPrice(finalPrice));
  }, [selectedOptions]);

  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={setOpen}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0">
          <div className="fixed inset-0 hidden bg-gray-500 bg-opacity-75 transition-opacity md:block" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 w-screen overflow-y-auto bg-black/50">
          <div className="flex min-h-full items-stretch justify-center text-center md:items-center md:px-2 lg:px-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 md:translate-y-0 md:scale-95"
              enterTo="opacity-100 translate-y-0 md:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 md:scale-100"
              leaveTo="opacity-0 translate-y-4 md:translate-y-0 md:scale-95">
              <Dialog.Panel className="flex w-full transform text-left text-base transition md:my-8 md:max-w-2xl md:px-4 lg:max-w-4xl">
                <div className="relative flex w-full items-center overflow-hidden bg-white px-4 pb-8 pt-14 shadow-2xl sm:px-6 sm:pt-8 md:p-6 lg:p-8 rounded-lg">
                  <button
                    type="button"
                    className="absolute right-4 top-4 text-gray-400 hover:text-gray-500 sm:right-6 sm:top-8 md:right-6 md:top-6 lg:right-8 lg:top-8"
                    onClick={() => setOpen(false)}>
                    <span className="sr-only">Close</span>
                    <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                  </button>

                  <div className="grid w-full grid-cols-1 items-start gap-x-6 gap-y-8 sm:grid-cols-12 lg:gap-x-8">
                    <div className="aspect-h-3 aspect-w-2 overflow-hidden rounded-lg bg-gray-100 sm:col-span-4 lg:col-span-5">
                      <img
                        src={item.image_url || "https://placehold.co/300x300?text=Item"}
                        className="object-cover object-center"
                      />
                    </div>
                    <div className="sm:col-span-8 lg:col-span-7">
                      <h2 className="text-2xl font-bold text-gray-900 sm:pr-12">{item.name}</h2>

                      <section className="mt-2">
                        <p className="text-gray-600 mb-3">{item.description}</p>

                        {item.in_stock ? (
                          <Badge variant="success">{IN_STOCK_TEXT}</Badge>
                        ) : (
                          <Badge variant="danger">{OUT_OF_STOCK_TEXT}</Badge>
                        )}

                        <p className="mt-4 text-2xl text-gray-900">{item.price}&nbsp;$</p>
                      </section>

                      {/* Options (affichées seulement si l'item en a et qu'il est en stock) */}
                      {item.options.length > 0 && (
                        <section className="mt-5 select-none">
                          {/* On affiche chaque type d'option (ex: sirop, taille, etc.) */}
                          {Object.keys(optionsByType).map((type) => (
                            <div key={type} className="mt-5">
                              <h4 className="text-sm font-medium text-gray-900 capitalize mb-4">{type}</h4>
                              {/* On affiche chaque option pour le type en cours */}
                              <RadioGroup
                                value={selectedOptions[type]}
                                onChange={(value) =>
                                  setSelectedOptions({
                                    ...selectedOptions,
                                    [type]: {
                                      value: value,
                                      fee: optionsByType[type].find((option) => option.value === value).fee,
                                    },
                                  })
                                }>
                                <div className="grid grid-cols-4 gap-4">
                                  {/* On affiche les options pour le type en cours */}
                                  {optionsByType[type].map((option) => (
                                    <RadioGroup.Option
                                      key={option.value}
                                      value={option.value}
                                      className={classNames({
                                        "border-emerald-600 bg-emerald-50":
                                          selectedOptions[type]?.value === option.value,
                                        "hover:bg-gray-50": selectedOptions[type]?.value !== option.value,
                                        "cursor-pointer shadow-sm group relative flex items-center justify-center rounded-md border py-3 px-4 focus:outline-none sm:flex-1": true,
                                      })}>
                                      <RadioGroup.Label as="div" className="flex flex-col items-start">
                                        <span className="text-gray-900 text-sm font-medium capitalize">
                                          {option.value}
                                        </span>
                                        {/* On affiche le prix de l'option si celui-ci est supérieur à 0 */}
                                        {parseFloat(option.fee) > 0 && (
                                          <span className="text-gray-500 text-xs">
                                            +{formatPrice(option.fee)}&nbsp;$
                                          </span>
                                        )}
                                      </RadioGroup.Label>
                                    </RadioGroup.Option>
                                  ))}
                                </div>
                              </RadioGroup>
                            </div>
                          ))}
                        </section>
                      )}

                      <form onSubmit={(e) => onSubmit(e, setIsAddingToCart)}>
                        <button
                          type="submit"
                          className="mt-6 flex w-full items-center justify-center rounded-md \
                            border border-transparent bg-emerald-600 px-8 py-3 \
                            text-base font-medium text-white \
                            hover:bg-emerald-700 \
                            focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 \
                            disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-emerald-600"
                          disabled={!item.in_stock || isAddingToCart}>
                          {isAddingToCart
                            ? "Ajout en cours..."
                            : item.in_stock
                            ? `Ajouter au panier (${itemFinalPrice} $)`
                            : OUT_OF_STOCK_TEXT}
                        </button>
                      </form>
                    </div>
                  </div>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
};

export default ProductView;
