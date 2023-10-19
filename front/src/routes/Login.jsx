import logo from "/logo.png";
import { Link } from "react-router-dom";
import { Helmet } from "react-helmet";
import Input from "../components/ui/Input";

const Login = () => {
  return (
    <>
      <Helmet>
        <title>Se connecter | Café sans-fil</title>
      </Helmet>
      <div className="flex min-h-[80vh] flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img className="mx-auto h-24 lg:h-32 w-auto" src={logo} alt="Café sans-fil logo" />
          <h2 className="mt-6 text-center text-xl lg:text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Connectez-vous à votre compte
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" action="#" method="POST">
            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                Adresse courriel de l'UdeM
              </label>
              <div className="mt-2">
                <Input id="email" name="email" type="email" autoComplete="email" required />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                  Mot de passe
                </label>
                <div className="text-sm">
                  <a href="#" className="font-semibold text-emerald-600 hover:text-emerald-500">
                    Mot de passe oublié?
                  </a>
                </div>
              </div>
              <div className="mt-2">
                <Input id="password" name="password" type="password" autoComplete="current-password" required />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
                Se connecter
              </button>
            </div>
          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Pas encore de compte?{" "}
            <Link to="/signup" className="font-semibold leading-6 text-emerald-600 hover:text-emerald-500">
              Créez le maintenant
            </Link>
          </p>
        </div>
      </div>
    </>
  );
};

export default Login;
