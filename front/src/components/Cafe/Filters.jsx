import { Fragment, useState } from "react";
import { Dialog, Disclosure, Menu, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { ChevronDownIcon, FunnelIcon, MinusIcon, PlusIcon } from "@heroicons/react/20/solid";

const sortOptions = [
  { name: "Tous les pavillons", href: "#", current: true },
  { name: "3200, Jean-Brillant", href: "#", current: false },
  { name: "André-Aisenstadt", href: "#", current: false },
  { name: "Campus MIL", href: "#", current: false },
  { name: "Campus de Saint-Hyacinthe", href: "#", current: false },
  { name: "Cepsum", href: "#", current: false },
  { name: "Faculté de l'Aménagement", href: "#", current: false },
  { name: "Faculté de Musique", href: "#", current: false },
  { name: "Jean-Coutu", href: "#", current: false },
  { name: "Liliane-de-Stewart", href: "#", current: false },
  { name: "Lionel-Groulx", href: "#", current: false },
  { name: "Marie-Victorin", href: "#", current: false },
  { name: "Maximilien-Caron", href: "#", current: false },
  { name: "Roger-Gaudry", href: "#", current: false },
];

const filterTypes = [
  // {
  //   id: "facts",
  //   name: "Caractéristiques",
  //   options: [{ value: "open", label: "Ouvert", checked: false }],
  // },
  {
    id: "payement",
    name: "Mode de payement",
    options: [
      { value: "cash", label: "Comptant", checked: false },
      { value: "debit", label: "Débit", checked: false },
      { value: "credit", label: "Crédit", checked: false },
    ],
  },
  {
    id: "products",
    name: "Types de produits",
    options: [
      { value: "coffee", label: "Café", checked: false },
      { value: "tea", label: "Thé", checked: false },
      { value: "sandwich", label: "Sandwich", checked: false },
      { value: "salad", label: "Salade", checked: false },
      { value: "dessert", label: "Dessert", checked: false },
      { value: "snack", label: "Collation", checked: false },
    ],
  },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

const Filters = ({ filters, setFilters }) => {
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);

  return (
    <div className="bg-white">
      <div>
        {/* Mobile filter dialog */}
        <Transition.Root show={mobileFiltersOpen} as={Fragment}>
          <Dialog as="div" className="relative z-40" onClose={setMobileFiltersOpen}>
            <Transition.Child
              as={Fragment}
              enter="transition-opacity ease-linear duration-300"
              enterFrom="opacity-0"
              enterTo="opacity-100"
              leave="transition-opacity ease-linear duration-300"
              leaveFrom="opacity-100"
              leaveTo="opacity-0">
              <div className="fixed inset-0 bg-black bg-opacity-25" />
            </Transition.Child>

            <div className="fixed inset-0 z-40 flex">
              <Transition.Child
                as={Fragment}
                enter="transition ease-in-out duration-300 transform"
                enterFrom="translate-x-full"
                enterTo="translate-x-0"
                leave="transition ease-in-out duration-300 transform"
                leaveFrom="translate-x-0"
                leaveTo="translate-x-full">
                <Dialog.Panel className="relative ml-auto flex h-full w-full max-w-xs flex-col overflow-y-auto bg-white py-4 pb-12 shadow-xl">
                  <div className="flex items-center justify-between px-4">
                    <h2 className="text-lg font-medium text-gray-900">Filtres</h2>
                    <button
                      type="button"
                      className="-mr-2 flex h-10 w-10 items-center justify-center rounded-md bg-white p-2 text-gray-400"
                      onClick={() => setMobileFiltersOpen(false)}>
                      <span className="sr-only">Fermer le menu</span>
                      <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                    </button>
                  </div>

                  {/* Filters */}
                  <form className="mt-4 border-t border-gray-200">
                    {filterTypes.map((section) => (
                      <Disclosure as="div" key={section.id} className="border-t border-gray-200 px-4 py-6">
                        {({ open }) => (
                          <>
                            <h3 className="-mx-2 -my-3 flow-root">
                              <Disclosure.Button className="flex w-full items-center justify-between bg-white px-2 py-3 text-gray-400 hover:text-gray-500">
                                <span className="font-medium text-gray-900">{section.name}</span>
                                <span className="ml-6 flex items-center">
                                  {open ? (
                                    <MinusIcon className="h-5 w-5" aria-hidden="true" />
                                  ) : (
                                    <PlusIcon className="h-5 w-5" aria-hidden="true" />
                                  )}
                                </span>
                              </Disclosure.Button>
                            </h3>
                            <Disclosure.Panel className="pt-6">
                              <div className="space-y-6">
                                {section.options.map((option, optionIdx) => (
                                  <div key={option.value} className="flex items-center">
                                    <label
                                      className="relative inline-flex items-center cursor-pointer"
                                      htmlFor={`filter-mobile-${section.id}-${optionIdx}`}>
                                      <input
                                        className="sr-only peer"
                                        id={`filter-mobile-${section.id}-${optionIdx}`}
                                        name={`${section.id}[]`}
                                        defaultValue={option.value}
                                        type="checkbox"
                                        defaultChecked={option.checked}
                                      />
                                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-emerald-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
                                      <span className="ml-3 min-w-0 flex-1 text-sm font-medium text-gray-500">
                                        {option.label}
                                      </span>
                                    </label>
                                  </div>
                                ))}
                              </div>
                            </Disclosure.Panel>
                          </>
                        )}
                      </Disclosure>
                    ))}
                  </form>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </Dialog>
        </Transition.Root>

        <div>
          <div className="flex items-baseline justify-end border-b border-gray-200 pb-6">
            {/* <h1 className="text-3xl font-semibold tracking-tight text-gray-900 font-secondary">Cafés</h1> */}
            <div className="flex items-center select-none">
              <div className="flex items-center mr-8">
                <label className="relative inline-flex items-center cursor-pointer" htmlFor={`filter-mobile-open`}>
                  <input
                    className="sr-only peer"
                    id={`filter-mobile-open`}
                    name={`filter-mobile-open`}
                    value={filters.openOnly}
                    type="checkbox"
                    onChange={(e) => setFilters({ ...filters, openOnly: e.target.checked })}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-emerald-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
                  <span className="ml-3 min-w-0 flex-1 text-sm font-medium text-gray-700">Ouverts</span>
                </label>
              </div>

              <Menu as="div" className="relative inline-block text-left">
                <div>
                  <Menu.Button className="group inline-flex justify-center text-sm font-medium text-gray-700 hover:text-gray-900">
                    Pavillon
                    <ChevronDownIcon
                      className="-mr-1 ml-1 h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-gray-500"
                      aria-hidden="true"
                    />
                  </Menu.Button>
                </div>

                <Transition
                  as={Fragment}
                  enter="transition ease-out duration-100"
                  enterFrom="transform opacity-0 scale-95"
                  enterTo="transform opacity-100 scale-100"
                  leave="transition ease-in duration-75"
                  leaveFrom="transform opacity-100 scale-100"
                  leaveTo="transform opacity-0 scale-95">
                  <Menu.Items className="absolute right-0 z-10 mt-2 w-40 origin-top-right rounded-md bg-white shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none max-h-64 overflow-auto">
                    <div className="py-1">
                      {sortOptions.map((option) => (
                        <Menu.Item key={option.name}>
                          {({ active }) => (
                            <a
                              href={option.href}
                              className={classNames(
                                option.current ? "font-medium text-gray-900" : "text-gray-500",
                                active ? "bg-gray-100" : "",
                                "block px-4 py-2 text-sm"
                              )}>
                              {option.name}
                            </a>
                          )}
                        </Menu.Item>
                      ))}
                    </div>
                  </Menu.Items>
                </Transition>
              </Menu>

              <button
                type="button"
                className="-m-2 ml-4 p-2 text-gray-400 hover:text-gray-500 sm:ml-6 flex items-center gap-2"
                onClick={() => setMobileFiltersOpen(true)}>
                <span className="hidden sm:block text-sm font-medium text-gray-700">Filtres</span>
                <FunnelIcon className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Filters;
