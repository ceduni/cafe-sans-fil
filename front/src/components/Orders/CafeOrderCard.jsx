import { Fragment, useState, useEffect } from "react";
import { CheckIcon, ChevronDownIcon } from "@heroicons/react/20/solid";
import { Menu, Transition } from "@headlessui/react";
import { BellAlertIcon, ClockIcon, InformationCircleIcon, NoSymbolIcon } from "@heroicons/react/24/outline";
import { getBadgeVariant } from "@/utils/orders";
import { formatDate } from "@/utils/dates";
import classNames from "classnames";
import { displayOptions, formatPrice } from "@/utils/cart";
import { CurrencyDollarIcon } from "@heroicons/react/24/solid";
import { getUserFromUsername } from "@/utils/getFromId";
import Avatar from "@/components/Avatar";
import useCountdown from "@/hooks/useCountdown";
import Badge from "@/components/Badge";

const CafeOrderCard = ({ order, setOrderReady, setOrderCanceled }) => {
  const [orderUser, setOrderUser] = useState(null);

  useEffect(() => {
    getUserFromUsername(order.user_username).then((user) => {
      setOrderUser(user);
    });
  }, []);

  const minutes = useCountdown(order.created_at);

  return (
    <div className="py-10 border-b border-gray-200 last:border-b-0">
      <div className="lg:flex lg:items-center lg:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Commande #{order.order_number}
          </h2>
          {(orderUser && (
            <div className="my-6 flex gap-3">
              <Avatar name={`${orderUser.first_name} ${orderUser.last_name}`} size="md" image={orderUser.photo_url} />
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {orderUser.first_name} {orderUser.last_name}
                </h3>
                <p className="text-sm text-gray-500">{orderUser.matricule}</p>
              </div>
            </div>
          )) || (
            <div className="my-6 flex gap-3">
              <div className="w-12 h-12 rounded-full bg-gray-200 animate-pulse"></div>
              <div>
                <div className="w-32 h-4 mb-2 rounded-full bg-gray-200 animate-pulse"></div>
                <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
              </div>
            </div>
          )}
          <div className="mt-1 flex flex-col sm:mt-0 sm:flex-row sm:flex-wrap sm:space-x-6">
            <div className="mt-2 flex items-center text-sm text-gray-500 font-bold">
              <CurrencyDollarIcon className="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
              {formatPrice(order.total_price)}
            </div>
            <div className="mt-2 flex items-center text-sm text-gray-500">
              <InformationCircleIcon className="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
              <Badge variant={getBadgeVariant(order.status)}>{order.status}</Badge>
            </div>
            <div className="mt-2 flex items-center text-sm text-gray-500">
              <ClockIcon className="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
              {formatDate(order.created_at)}
            </div>
            <div className="mt-2 flex items-center text-sm text-gray-500">
              <BellAlertIcon
                className={classNames("mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400", {
                  "text-red-500": minutes < 0,
                })}
                aria-hidden="true"
              />
              {(minutes < 0 && <span className="text-red-500 font-semibold">La commande va expirer</span>) || (
                <span>Expire dans {minutes} minutes</span>
              )}
            </div>
          </div>
        </div>
        <div className="mt-5 flex lg:ml-4 lg:mt-0">
          <span className="hidden sm:block">
            <button
              type="button"
              onClick={() => setOrderCanceled(order.order_id)}
              className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <NoSymbolIcon className="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true" />
              Annuler la commande
            </button>
          </span>

          <span className="sm:ml-3">
            <button
              type="button"
              onClick={() => setOrderReady(order.order_id)}
              className="inline-flex items-center rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
              <CheckIcon className="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
              Prête
            </button>
          </span>

          {/* Dropdown */}
          <Menu as="div" className="relative ml-3 sm:hidden">
            <Menu.Button className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400">
              Plus
              <ChevronDownIcon className="-mr-1 ml-1.5 h-5 w-5 text-gray-400" aria-hidden="true" />
            </Menu.Button>

            <Transition
              as={Fragment}
              enter="transition ease-out duration-200"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95">
              <Menu.Items className="absolute right-0 z-10 -mr-1 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <Menu.Item>
                  {({ active }) => (
                    <button
                      type="button"
                      onClick={() => setOrderCanceled(order.order_id)}
                      className={classNames({
                        "bg-gray-100": active,
                        "block px-4 py-2 text-sm text-gray-700 w-full": true,
                      })}>
                      Annuler la commande
                    </button>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
      <div className="mt-5">
        {order.items.map((item, index) => (
          <div className="flex flex-col sm:flex-row sm:space-x-6" key={index}>
            <div className="mt-2 flex items-center text-sm text-gray-500">
              <span className="mr-1.5">{item.quantity}</span>
              <span>
                {item.item_name} {displayOptions(item.options)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CafeOrderCard;
