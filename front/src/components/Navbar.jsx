import { Fragment, useState } from "react";
import { Dialog, Transition, Menu } from "@headlessui/react";
import { Bars3Icon, ShoppingBagIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { Link, NavLink } from "react-router-dom";
import Cart from "@/components/Orders/Cart";
import Container from "@/components/Container";
import Avatar from "@/components/Avatar";
import { useAuth } from "@/hooks/useAuth";
import { useCart } from "react-use-cart";
import classNames from "classnames";

const routes = {
  home: "/",
  login: "/login",
  signup: "/signup",
  profile: "/me",
  orders: "/me/orders",
};

const avatarNavigation = [
  { name: "Mon profil", href: routes.profile },
  { name: "Mes commandes", href: routes.orders },
];

const Navbar = () => {
  const { isLoggedIn, onLogout, user } = useAuth();
  const userFullName = user ? user.first_name + " " + user.last_name : "";

  const [open, setOpen] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  const { totalItems } = useCart();

  return (
    <>
      {/* Cart */}
      <Cart open={cartOpen} setOpen={setCartOpen} />

      {/* Navbar */}
      <div className="bg-white sticky top-0 z-30">
        <header className="relative bg-white">
          <nav aria-label="Top">
            <div className="border-b border-gray-200">
              <Container>
                <div className="flex h-16 items-center">
                  {/* Logo */}
                  <div className="flex">
                    <Link to={routes.home} className="flex items-center gap-2 md:gap-4">
                      <img className="h-9 w-auto ml-2" src="/logo_text.png" alt="Café sans-fil" />
                      <span className="text-xl font-bold text-gray-900 font-secondary mt-2">
                        <span className="text-xs font-sans font-bold text-gray-500">preview</span>
                      </span>
                    </Link>
                  </div>

                  <div className="ml-auto flex items-center">
                    {isLoggedIn ? (
                      <Menu as="div" className="relative ml-3">
                        <div className="flex items-center justify-center">
                          <Menu.Button>
                            <Avatar name={userFullName} image={user?.photo_url} key={user?.photo_url} />
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
                          <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                            {avatarNavigation.map((item) => (
                              <Menu.Item key={item.name}>
                                {({ active }) => (
                                  <Link
                                    to={item.href}
                                    className={classNames({
                                      "bg-gray-100": active,
                                      "block px-4 py-2 text-sm text-gray-700": true,
                                    })}>
                                    {item.name}
                                  </Link>
                                )}
                              </Menu.Item>
                            ))}
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  onClick={onLogout}
                                  className={classNames({
                                    "bg-gray-100": active,
                                    "block px-4 py-2 text-sm text-gray-700 w-full text-left": true,
                                  })}>
                                  Déconnexion
                                </button>
                              )}
                            </Menu.Item>
                          </Menu.Items>
                        </Transition>
                      </Menu>
                    ) : (
                      <div className="flex flex-1 items-center justify-end space-x-6">
                        <NavLink
                          to={routes.login}
                          className={({ isActive }) =>
                            classNames({
                              "text-gray-900": isActive,
                              "text-gray-500 hover:text-gray-700": !isActive,
                              "text-sm font-medium": true,
                            })
                          }>
                          Se connecter
                        </NavLink>
                      </div>
                    )}

                    {/* Cart */}
                    <div className="ml-4 flow-root lg:ml-6">
                      <button onClick={() => setCartOpen(true)} className="group -m-2 flex items-center p-2">
                        <ShoppingBagIcon
                          className="h-6 w-6 flex-shrink-0 text-gray-400 group-hover:text-gray-500"
                          aria-hidden="true"
                        />
                        <span className="ml-2 text-sm font-medium text-gray-700 group-hover:text-gray-800">
                          {totalItems}
                        </span>
                        <span className="sr-only">items in cart, view bag</span>
                      </button>
                    </div>
                  </div>
                </div>
              </Container>
            </div>
          </nav>
        </header>
      </div>
    </>
  );
};

export default Navbar;
