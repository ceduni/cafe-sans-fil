import { Fragment, useState } from "react";
import { Dialog, Popover, Transition, Menu } from "@headlessui/react";
import { Bars3Icon, MagnifyingGlassIcon, ShoppingBagIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { Link, NavLink } from "react-router-dom";
import Cart from "./Cart";
import Container from "./ui/Container";
import Avatar from "./ui/Avatar";
import { useAuth } from "../hooks/useAuth";

const routes = {
  home: "/",
  login: "/login",
  signup: "/signup",
  profile: "/me",
};

const navigation = [{ name: "Accueil", href: routes.home }];

const avatarNavigation = [
  { name: "Mon profil", href: routes.profile },
  { name: "Mes commandes", href: "/me/orders" },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

const Navbar = () => {
  const { token, onLogout } = useAuth();
  const isLoggedIn = token !== null;

  const [open, setOpen] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  return (
    <>
      {/* Cart */}
      <Cart open={cartOpen} setOpen={setCartOpen} />

      {/* Navbar */}
      <div className="bg-white">
        {/* Mobile menu */}
        <Transition.Root show={open} as={Fragment}>
          <Dialog as="div" className="relative z-40 lg:hidden" onClose={setOpen}>
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
                enterFrom="-translate-x-full"
                enterTo="translate-x-0"
                leave="transition ease-in-out duration-300 transform"
                leaveFrom="translate-x-0"
                leaveTo="-translate-x-full">
                <Dialog.Panel className="relative flex w-full max-w-xs flex-col overflow-y-auto bg-white pb-12 shadow-xl">
                  <div className="flex px-4 pb-2 pt-5">
                    <button
                      type="button"
                      className="relative -m-2 inline-flex items-center justify-center rounded-md p-2 text-gray-400"
                      onClick={() => setOpen(false)}>
                      <span className="absolute -inset-0.5" />
                      <span className="sr-only">Close menu</span>
                      <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                    </button>
                  </div>

                  {/* Links */}
                  <div className="space-y-6 px-5 py-6">
                    {navigation.map((page) => (
                      <div key={page.name} className="flow-root">
                        <Link
                          to={page.href}
                          className="-m-2 p-2 block font-medium text-gray-900"
                          onClick={() => setOpen(false)}>
                          {page.name}
                        </Link>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-6 border-t border-gray-200 px-5 py-6">
                    <div className="flow-root">
                      <Link
                        to={routes.login}
                        className="-m-2 p-2 block font-medium text-gray-900"
                        onClick={() => setOpen(false)}>
                        Se connecter
                      </Link>
                    </div>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </Dialog>
        </Transition.Root>

        <header className="relative bg-white">
          <nav aria-label="Top">
            <div className="border-b border-gray-200">
              <Container>
                <div className="flex h-16 items-center">
                  <button
                    type="button"
                    className="relative rounded-md bg-white p-2 text-gray-400 lg:hidden"
                    onClick={() => setOpen(true)}>
                    <span className="absolute -inset-0.5" />
                    <span className="sr-only">Open menu</span>
                    <Bars3Icon className="h-6 w-6" aria-hidden="true" />
                  </button>

                  {/* Logo */}
                  <div className="ml-4 flex lg:ml-0">
                    <Link to={routes.home} className="text-xl font-bold text-gray-900 font-secondary">
                      café sans-fil
                    </Link>
                  </div>

                  {/* Flyout menus */}
                  <Popover.Group className="hidden lg:ml-8 lg:block lg:self-stretch">
                    <div className="flex h-full space-x-8">
                      {navigation.map((page) => (
                        <NavLink
                          key={page.name}
                          to={page.href}
                          // active: "border-emerald-500 text-gray-900"
                          // inactive: "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                          // always: "inline-flex items-center py-5 px-1 border-b-2 text-sm font-medium"
                          className={({ isActive }) =>
                            classNames(
                              isActive ? "text-gray-900" : "text-gray-500 hover:text-gray-700",
                              "inline-flex items-center py-5 px-1 text-sm font-medium"
                            )
                          }
                          end>
                          {page.name}
                        </NavLink>
                      ))}
                    </div>
                  </Popover.Group>

                  <div className="ml-auto flex items-center">
                    {isLoggedIn ? (
                      <Menu as="div" className="relative ml-3">
                        <div>
                          <Menu.Button>
                            <Avatar name="John Doe"></Avatar>
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
                                    className={classNames(
                                      active ? "bg-gray-100" : "",
                                      "block px-4 py-2 text-sm text-gray-700"
                                    )}>
                                    {item.name}
                                  </Link>
                                )}
                              </Menu.Item>
                            ))}
                            <Menu.Item>
                              {({ active }) => (
                                <a
                                  href="#"
                                  className={classNames(
                                    active ? "bg-gray-100" : "",
                                    "block px-4 py-2 text-sm text-gray-700"
                                  )}>
                                  Gestion cafés
                                </a>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  onClick={onLogout}
                                  className={classNames(
                                    active ? "bg-gray-100" : "",
                                    "block px-4 py-2 text-sm text-gray-700 w-full text-left"
                                  )}>
                                  Déconnexion
                                </button>
                              )}
                            </Menu.Item>
                          </Menu.Items>
                        </Transition>
                      </Menu>
                    ) : (
                      <div className="hidden lg:flex lg:flex-1 lg:items-center lg:justify-end lg:space-x-6">
                        <NavLink
                          to={routes.login}
                          className={({ isActive }) =>
                            classNames(
                              isActive ? "text-gray-900" : "text-gray-500 hover:text-gray-700",
                              "text-sm font-medium"
                            )
                          }>
                          Se connecter
                        </NavLink>
                      </div>
                    )}

                    {/* Search */}
                    {/* <div className="flex lg:ml-6">
                      <NavLink
                        to={routes.search}
                        className={({ isActive }) =>
                          classNames(isActive ? "text-gray-900" : "text-gray-500 hover:text-gray-700", "p-2")
                        }>
                        <span className="sr-only">Search</span>
                        <MagnifyingGlassIcon className="h-6 w-6" aria-hidden="true" />
                      </NavLink>
                    </div> */}

                    {/* Cart */}
                    <div className="ml-4 flow-root lg:ml-6">
                      <button onClick={() => setCartOpen(true)} className="group -m-2 flex items-center p-2">
                        <ShoppingBagIcon
                          className="h-6 w-6 flex-shrink-0 text-gray-400 group-hover:text-gray-500"
                          aria-hidden="true"
                        />
                        <span className="ml-2 text-sm font-medium text-gray-700 group-hover:text-gray-800">2</span>
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
