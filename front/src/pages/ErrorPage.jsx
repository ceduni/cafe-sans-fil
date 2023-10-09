import { useRouteError } from "react-router-dom";
import { Link } from "react-router-dom";
import { Helmet } from "react-helmet";

const ErrorPage = () => {
  const error = useRouteError();
  console.error(error);

  return (
    <>
      <Helmet>
        <title>Erreur | Café sans fil</title>
      </Helmet>
      <main className="grid min-h-full place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8 h-screen">
        <div className="text-center">
          <p className="text-base font-semibold text-emerald-600">{error.status}</p>
          <h1 className="mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl">Oops!</h1>
          <p className="mt-6 text-base leading-7 text-gray-600">
            Une erreur est survenue. <i>{error.statusText || error.message}</i>
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link
              to="/"
              className="rounded-md bg-emerald-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
              Retour à l'accueil
            </Link>
            <a href="#" className="text-sm font-semibold text-gray-900">
              Nous contacter <span aria-hidden="true">&rarr;</span>
            </a>
          </div>
        </div>
      </main>
    </>
  );
};

export default ErrorPage;
