import Input from "../components/ui/Input";
import { useState } from "react";
import { Helmet } from "react-helmet-async";
import logo from "/logo.png";

const ResetPassword = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("Cette fonctionnalité n'est pas encore disponible.");
  };

  return (
    <>
      <Helmet>
        <title>Réinitialiser le mot de passe | Café sans-fil</title>
      </Helmet>
      <div className="flex min-h-[80vh] flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img className="mx-auto h-24 lg:h-32 w-auto" src={logo} alt="Café sans-fil logo" />
          <h2 className="mt-6 text-center text-xl lg:text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Réinitialiser votre mot de passe
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" method="POST" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                Adresse courriel de l'UdeM
              </label>
              <div className="mt-2">
                <Input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  onChange={handleChange}
                  value={email}
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
                Envoyer le lien de réinitialisation
              </button>
            </div>
          </form>

          {error && <p className="mt-10 text-center text-sm text-red-500 font-semibold">{error}</p>}
        </div>
      </div>
    </>
  );
};

export default ResetPassword;
