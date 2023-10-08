import logo from "/logo.png";

const Home = () => {
  return (
    <>
      <section className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 font-secondary">Liste des cafés</h1>
        </div>
      </section>
      <main>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
          <div className="bg-white rounded-lg border-2">
            <div className="relative pb-5/6">
              <img className="absolute h-full w-full object-cover rounded-t-lg" src={logo} alt="Café 1" />
            </div>
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Café 1</h3>
              <p className="mt-2 max-w-2xl text-sm text-gray-500">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis aliquid atque, nulla? Quos cum ex
                quis soluta, a laboriosam. Dicta expedita corporis animi vero voluptate voluptatibus possimus, veniam
                magni quis!
              </p>
              <div className="mt-3">
                <a href="#" className="text-sm font-medium text-emerald-600 hover:text-emerald-500">
                  Voir plus
                </a>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg border-2">
            <div className="relative pb-5/6">
              <img className="absolute h-full w-full object-cover rounded-t-lg" src={logo} alt="Café 2" />
            </div>
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Café 2</h3>
              <p className="mt-2 max-w-2xl text-sm text-gray-500">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis aliquid atque, nulla? Quos cum ex
                quis soluta, a laboriosam. Dicta expedita corporis animi vero voluptate voluptatibus possimus, veniam
                magni quis!
              </p>
              <div className="mt-3">
                <a
                  href="#"
                  className="text-sm font-medium text-emerald-600 hover:text-emerald-500
                  ">
                  Voir plus
                </a>
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
};

export default Home;
