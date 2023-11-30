import logo from "/logo.png";
import { Link } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import Input from "@/components/Input";
import { useAuth } from "@/hooks/useAuth";
import { useState } from "react";
import { EyeIcon, EyeSlashIcon } from "@heroicons/react/24/solid";

const Login = () => {
  const { onLogin } = useAuth();
  const [credentials, setCredentials] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  return (
    <>
      <Helmet>
        <title>Se connecter | Café sans-fil</title>
      </Helmet>
      <div className="flex min-h-[93vh] flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <Link to="/">
            <img className="mx-auto h-36 lg:h-48 w-auto" src={logo} alt="Café sans-fil logo" />
          </Link>
          <h2 className="mt-6 text-center text-xl lg:text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Connectez-vous à votre compte
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" method="POST" onSubmit={(e) => onLogin(e, credentials, setCredentials)}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                Adresse courriel de l'UdeM
              </label>
              <div className="mt-2">
                <Input
                  id="email"
                  name="email"
                  type="text"
                  autoComplete="email"
                  required
                  value={credentials.email}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                  Mot de passe
                </label>
                <div className="text-sm">
                  <Link to="/reset" className="font-semibold text-sky-600 hover:text-sky-500">
                    Mot de passe oublié?
                  </Link>
                </div>
              </div>
              <div className="mt-2 w-full flex items-center gap-1">
                <Input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  required
                  value={credentials.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="inline-flex items-center rounded-md bg-white px-3 py-2 \
                  text-gray-400 hover:text-gray-500 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400">
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5" aria-hidden="true" />
                  ) : (
                    <EyeIcon className="h-5 w-5" aria-hidden="true" />
                  )}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="flex w-full justify-center rounded-3xl bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
              Se connecter
            </button>
          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Pas encore de compte?{" "}
            <Link to="/signup" className="font-semibold leading-6 text-sky-600 hover:text-sky-500">
              Créez le maintenant
            </Link>
          </p>
        </div>
      </div>
    </>
  );
};

export default Login;
