import { Fragment } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { useCart } from "react-use-cart";
import { TrashIcon } from "@heroicons/react/20/solid";
import Badge from "../Badge";
export const products = [
  {
    id: 1,
    name: "Café latte",
    href: "#",
    color: "Taille unique",
    price: "$2.00",
    quantity: 7,
    imageSrc:
      "https://media.carrefour.fr/medias/370b7c262e583c43bae0e4ac1276d223/p_1500x1500/05711953145483-h1n1-s02.jpg",
    imageAlt: "Café latte",
    sizes: [
      { name: "XXS", inStock: true },
      { name: "XS", inStock: true },
      { name: "S", inStock: true },
      { name: "M", inStock: true },
      { name: "L", inStock: true },
      { name: "XL", inStock: true },
      { name: "XXL", inStock: true },
      { name: "XXXL", inStock: false },
    ],
  },
  {
    id: 2,
    name: "Sandwich au thon",
    href: "#",
    color: "Taille unique",
    price: "$3.00",
    quantity: 1,
    imageSrc: "https://img.circulaire-en-ligne.ca/wp-content/uploads/Tuna-Mayo-Sub-Roll.jpg",
    imageAlt: "Sandwich au thon",
    sizes: [
      { name: "XXS", inStock: true },
      { name: "XS", inStock: true },
      { name: "S", inStock: true },
      { name: "M", inStock: true },
      { name: "L", inStock: true },
      { name: "XL", inStock: true },
      { name: "XXL", inStock: true },
      { name: "XXXL", inStock: false },
    ],
  },
];

const Cart = ({ open, setOpen }) => {
  const { isEmpty, totalItems, items, updateItemQuantity, removeItem, cartTotal, emptyCart } = useCart();

  // On vérifie si les items du panier sont de cafe.name différents
  // Si c'est le cas on affiche un message prévenant l'utilisateur
  const cafeNames = [...new Set(items.map((item) => item.cafe?.name))];
  const differentCafeNames = cafeNames.length > 1;

  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={setOpen}>
        <Transition.Child
          as={Fragment}
          enter="ease-in-out duration-500"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in-out duration-500"
          leaveFrom="opacity-100"
          leaveTo="opacity-0">
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-hidden">
          <div className="absolute inset-0 overflow-hidden">
            <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
              <Transition.Child
                as={Fragment}
                enter="transform transition ease-in-out duration-500 sm:duration-700"
                enterFrom="translate-x-full"
                enterTo="translate-x-0"
                leave="transform transition ease-in-out duration-500 sm:duration-700"
                leaveFrom="translate-x-0"
                leaveTo="translate-x-full">
                <Dialog.Panel className="pointer-events-auto w-screen max-w-md">
                  <div className="flex h-full flex-col overflow-y-scroll bg-white shadow-xl">
                    <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
                      <div className="flex items-start justify-between">
                        <Dialog.Title className="text-lg font-medium text-gray-900">Panier ({totalItems})</Dialog.Title>
                        <div className="ml-3 flex h-7 items-center">
                          <button
                            type="button"
                            className="relative -m-2 p-2 text-gray-400 hover:text-gray-500"
                            onClick={() => setOpen(false)}>
                            <span className="absolute -inset-0.5" />
                            <span className="sr-only">Close panel</span>
                            <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                          </button>
                        </div>
                      </div>

                      <div className="mt-8">
                        <div className="flow-root">
                          {isEmpty && (
                            <div className="flex justify-center items-center">
                              <p className="text-gray-500">Votre panier est vide</p>
                            </div>
                          )}
                          <ul role="list" className="-my-6 divide-y divide-gray-200">
                            {items.map((item) => (
                              <li key={item.id} className="flex py-6">
                                <div className="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">
                                  <img
                                    src={item.image_url || "https://placehold.co/300x300?text=Item"}
                                    alt={item.name}
                                    className="h-full w-full object-cover object-center"
                                  />
                                </div>

                                <div className="ml-4 flex flex-1 flex-col">
                                  <div>
                                    <div className="flex justify-between text-base font-medium text-gray-900">
                                      <h3>{item.name}</h3>
                                      <p className="ml-4">{item.price}&nbsp;$</p>
                                    </div>
                                    <p className="mt-1 text-sm text-gray-500">{item.cafe?.name}</p>
                                    {/* // TODO ajouter variantes */}
                                  </div>
                                  <div className="flex flex-1 justify-between text-sm items-end">
                                    <select
                                      className="text-gray-900 w-16 border border-gray-300 rounded-md shadow-sm focus:ring-emerald-500 focus:border-emerald-500"
                                      value={item.quantity}
                                      onChange={(e) => updateItemQuantity(item.id, parseInt(e.target.value, 10))}>
                                      {Array.from(Array(9).keys()).map((i) => (
                                        <option key={i} value={i + 1}>
                                          {i + 1}
                                        </option>
                                      ))}
                                    </select>

                                    <div className="flex">
                                      <button
                                        type="button"
                                        className="font-medium text-emerald-600 hover:text-emerald-500"
                                        onClick={() => removeItem(item.id)}>
                                        Supprimer
                                      </button>
                                    </div>
                                  </div>
                                </div>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div className="border-t border-gray-200 px-4 py-6 sm:px-6">
                      <div className="flex justify-between text-base font-medium text-gray-900">
                        <p>Total</p>
                        <p>{cartTotal.toFixed(2)} $</p>
                      </div>
                      <p className="mt-0.5 text-sm text-gray-500">Taxes incluses</p>

                      {differentCafeNames && (
                        <div className="mt-2 flex items-center justify-center w-full">
                          <Badge variant="warning" className="mt-4">
                            Vous avez des produits de plusieurs cafés dans votre panier. Vous devrez donc récupérer
                            plusieurs commandes.
                          </Badge>
                        </div>
                      )}

                      <div className="mt-6 flex justify-center text-center text-sm text-gray-500 gap-2 hover:text-gray-700">
                        <TrashIcon className="h-5 w-5" aria-hidden="true" />
                        <button className="disabled:cursor-not-allowed" onClick={() => emptyCart()} disabled={isEmpty}>
                          Vider le panier
                        </button>
                      </div>
                      <div className="mt-4">
                        <button
                          className="w-full rounded-md \
                          border border-transparent bg-emerald-600 px-6 py-3 \
                          text-base font-medium text-white shadow-sm hover:bg-emerald-700 \
                          disabled:bg-gray-300 disabled:cursor-not-allowed"
                          disabled={isEmpty}>
                          Valider la commande
                        </button>
                      </div>
                      <div className="mt-4 flex justify-center text-center text-sm text-gray-500">
                        <p>
                          ou{" "}
                          <button
                            type="button"
                            className="font-medium text-emerald-600 hover:text-emerald-500"
                            onClick={() => setOpen(false)}>
                            Continuer vos achats
                            <span aria-hidden="true"> &rarr;</span>
                          </button>
                        </p>
                      </div>
                    </div>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
};

export default Cart;
