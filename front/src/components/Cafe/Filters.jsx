import { Fragment, useState } from "react";
import { Dialog, Disclosure, Menu, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { ChevronDownIcon, FunnelIcon, MinusIcon, PlusIcon } from "@heroicons/react/20/solid";
import classNames from "classnames";
import Switch from "@/components/CustomSwitch";
import { PAYMENT_METHODS } from "@/utils/cafe";

const filterTypes = [
  {
    id: "payement",
    name: "Mode de payement",
    options: [
      { value: "takesCash", label: PAYMENT_METHODS.CASH },
      { value: "takesCreditCard", label: PAYMENT_METHODS.CREDIT_CARD },
      { value: "takesDebitCard", label: PAYMENT_METHODS.DEBIT_CARD },
    ],
  },
];

const Filters = ({ filters, setFilters, cafes }) => {
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);

  const generatedSortOptions = cafes
    ? [
        { name: "Tous les pavillons" },
        ...cafes
          .map((cafe) => cafe.location.pavillon)
          .filter((value, index, self) => self.indexOf(value) === index) // On retire les doublons
          .sort() // On trie par ordre alphabétique
          .sort((a, b) => (a === filters.pavillon ? -1 : b === filters.pavillon ? 1 : 0)) // On met le pavillon sélectionné en premier
          .map((pavillon) => ({ name: pavillon })),
      ]
    : [];

  const getShortPavillonName = (pavillon) => {
    let shortPavillon = pavillon;
    // Si le nom commence par Pavillon, on le retire
    if (pavillon.startsWith("Pavillon ")) {
      shortPavillon = pavillon.slice(9);
      // Si maintenant ça commence par "de la", on le retire aussi
      if (shortPavillon.toLowerCase().startsWith("de la ")) {
        shortPavillon = shortPavillon.slice(6);
      }
    }
    return shortPavillon;
  };

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
                                {section.options.map((option) => (
                                  <div key={option.value} className="flex items-center">
                                    <Switch
                                      checked={filters[option.value]}
                                      onChange={(e) => setFilters({ ...filters, [option.value]: e })}
                                      label={option.label}
                                    />
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
            <div className="flex items-center select-none">
              <div className="flex items-center sm:mr-8 mr-4">
                <Switch
                  checked={filters.openOnly}
                  onChange={(e) => setFilters({ ...filters, openOnly: e })}
                  label="Ouvert"
                />
              </div>

              <Menu as="div" className="relative inline-block text-left">
                <div>
                  <Menu.Button className="group inline-flex items-center justify-center text-sm font-medium text-gray-700 hover:text-gray-900">
                    <span className="max-w-[8rem] sm:max-w-none truncate">
                      {getShortPavillonName(filters.pavillon)}
                    </span>
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
                      {generatedSortOptions.map((option) => (
                        <Menu.Item key={option.name}>
                          {({ active }) => (
                            <button
                              onClick={() => setFilters({ ...filters, pavillon: option.name })}
                              className={classNames({
                                "font-medium text-gray-900": filters.pavillon === option.name,
                                "text-gray-500": filters.pavillon !== option.name,
                                "bg-gray-100": active,
                                "block px-4 py-2 text-sm w-full text-left": true,
                              })}>
                              {option.name}
                            </button>
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
