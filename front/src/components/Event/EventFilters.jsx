import { Fragment, useState } from "react";
import { useTranslation } from "react-i18next";
import { Dialog, Disclosure, Menu, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { ChevronDownIcon, FunnelIcon, MinusIcon, PlusIcon } from "@heroicons/react/20/solid";
import Switch from "@/components/Widgets/CustomSwitch";

import "react-date-range/dist/styles.css";
import "react-date-range/dist/theme/default.css";
import { DateRangePicker } from "react-date-range";

const filterTypes = [
    {
        id: "date-range",
        name: "Date",
    },
];

const EventFilters = ({ filters, setFilters, events }) => {
    const { t } = useTranslation();
    
    const [filtersOpen, setFiltersOpen] = useState(false);
    
    const selectionRange = {
        startDate: new Date(),
        endDate: new Date(),
        key: 'selection',
    }

    return (
        <>
            <Transition.Root show={filtersOpen} as={Fragment}>
            <Dialog as="div" onClose={setFiltersOpen}>
            <Transition.Child 
                as={Fragment}
                enter=""
                enterFrom=""
                enterTo=""
                leave=""
                leaveFrom=""
                leaveTo="">
                <div />
            </Transition.Child>
            <div className="fixed inset-0 bg-black bg-opacity-25">
            <Transition.Child
                as={Fragment}
                enter=""
                enterFrom=""
                enterTo=""
                leave=""
                leaveFrom=""
                leaveTo="">
                <Dialog.Panel >
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

                <form>
                    <Disclosure as="div" >
                        {({ open }) => (
                            <>
                                <h3>
                                    <Disclosure.Button>
                                        <span >Choix de date</span>
                                        <span className="ml-6 flex items-center">
                                            {open ? (
                                                <MinusIcon className="h-5 w-5" aria-hidden="true" />
                                            ) : (
                                                <PlusIcon className="h-5 w-5" aria-hidden="true" />
                                            )}
                                        </span> 
                                    </Disclosure.Button>
                                </h3>
                                <Disclosure.Panel>
                                    <div>
                                        <div>
                                            <DateRangePicker
                                                ranges={[selectionRange]}
                                                onChange={this.handleSelect}>
                                            </DateRangePicker>
                                        </div>
                                    </div>
                                </Disclosure.Panel>
                            </>
                        )}
                    </Disclosure>
                </form>
            </Dialog.Panel>
            </Transition.Child>
            </div>
            </Dialog>
            </Transition.Root>
        </>
    );
};
