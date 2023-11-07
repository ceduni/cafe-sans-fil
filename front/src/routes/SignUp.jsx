import Input from "@/components/Input";
import { useAuth } from "@/hooks/useAuth";
import logo from "/logo.png";
import { Helmet } from "react-helmet-async";
import { Link } from "react-router-dom";
import { useState } from "react";

const SignUp = () => {
  const { onSignUp } = useAuth();
  const [userData, setUserData] = useState({
    email: "",
    firstName: "",
    lastName: "",
    password: "",
    passwordConfirm: "",
    matricule: "",
  });

  return (
    <>
      <Helmet>
        <title>Créer un compte | Café sans-fil</title>
      </Helmet>
      <div className="flex min-h-[80vh] flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img className="mx-auto h-24 lg:h-32 w-auto" src={logo} alt="Café sans-fil logo" />
          <h2 className="mt-6 text-center text-xl lg:text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Créez votre compte
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" action="#" method="POST" onSubmit={(e) => onSignUp(e, userData)}>
            <div className="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
              <div>
                <label htmlFor="prenom" className="block text-sm font-medium leading-6 text-gray-900">
                  Prénom
                </label>
                <div className="mt-2.5">
                  <Input
                    type="text"
                    name="prenom"
                    id="prenom"
                    autoComplete="given-name"
                    required
                    value={userData.firstName}
                    onChange={(e) => setUserData({ ...userData, firstName: e.target.value })}
                  />
                </div>
              </div>
              <div>
                <label htmlFor="nom" className="block text-sm font-medium leading-6 text-gray-900">
                  Nom
                </label>
                <div className="mt-2.5">
                  <Input
                    type="text"
                    name="nom"
                    id="nom"
                    autoComplete="family-name"
                    required
                    value={userData.lastName}
                    onChange={(e) => setUserData({ ...userData, lastName: e.target.value })}
                  />
                </div>
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                Adresse courriel de l'UdeM
              </label>
              <div className="mt-2">
                <Input
                  type="email"
                  name="email"
                  id="email"
                  autoComplete="email"
                  required
                  value={userData.email}
                  onChange={(e) => setUserData({ ...userData, email: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label htmlFor="matricule" className="block text-sm font-medium leading-6 text-gray-900">
                Matricule UdeM
              </label>
              <div className="mt-2">
                <Input
                  type="text"
                  name="matricule"
                  id="matricule"
                  required
                  value={userData.matricule}
                  onChange={(e) => setUserData({ ...userData, matricule: e.target.value })}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                  Mot de passe
                </label>
              </div>
              <div className="mt-2">
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={userData.password}
                  onChange={(e) => setUserData({ ...userData, password: e.target.value })}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password-confirm" className="block text-sm font-medium leading-6 text-gray-900">
                  Confirmez le mot de passe
                </label>
              </div>
              <div className="mt-2">
                <Input
                  id="password-confirm"
                  name="password-confirm"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={userData.passwordConfirm}
                  onChange={(e) => setUserData({ ...userData, passwordConfirm: e.target.value })}
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
                Créer le compte
              </button>
            </div>
          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Vous avez déjà un compte?{" "}
            <Link to="/login" className="font-semibold leading-6 text-emerald-600 hover:text-emerald-500">
              Connectez-vous
            </Link>
          </p>
        </div>
      </div>
    </>
  );
};

export default SignUp;
