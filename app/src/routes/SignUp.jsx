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
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    onSignUp(e, userData, setHasSubmitted);
  };

  return (
    <>
      <Helmet>
        <title>Créer un compte | Café sans-fil</title>
      </Helmet>
      <div className="flex min-h-[93vh] flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <Link to="/">
            <img className="mx-auto h-40 sm:h-44  w-auto hover:animate-scale" src={logo} alt="Café sans-fil logo" />
          </Link>
          <h2 className="mt-4 sm:mt-6 text-center text-xl lg:text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Créez votre compte
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" method="POST" onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
              <div>
                <label htmlFor="firstName" className="block text-sm font-medium leading-6 text-gray-900">
                  Prénom
                </label>
                <div className="mt-2.5">
                  <Input
                    type="text"
                    name="firstName"
                    id="firstName"
                    autoComplete="given-name"
                    value={userData.firstName}
                    onChange={handleChange}
                    required
                    minLength="2"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="lastName" className="block text-sm font-medium leading-6 text-gray-900">
                  Nom
                </label>
                <div className="mt-2.5">
                  <Input
                    type="text"
                    name="lastName"
                    id="lastName"
                    autoComplete="family-name"
                    value={userData.lastName}
                    onChange={handleChange}
                    required
                    minLength="2"
                  />
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                Adresse courriel de l'UdeM
              </label>
              <Input
                type="email"
                name="email"
                id="email"
                autoComplete="email"
                required
                value={userData.email}
                onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="matricule" className="block text-sm font-medium leading-6 text-gray-900">
                Matricule UdeM
              </label>
              <Input
                type="text"
                name="matricule"
                id="matricule"
                value={userData.matricule}
                onChange={handleChange}
                required
                minLength="6"
                pattern="[0-9]{6,8}"
              />
              <p className="text-sm text-gray-500">
                Doit contenir entre 6 et 8 chiffres. Affiché sur votre carte étudiante.
              </p>
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                Mot de passe
              </label>
              <Input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                value={userData.password}
                onChange={handleChange}
                required
                minLength="8"
              />
              <p className="text-sm text-gray-500">Minimum de 8 caractères.</p>
            </div>

            <div className="space-y-2">
              <label htmlFor="passwordConfirm" className="block text-sm font-medium leading-6 text-gray-900">
                Confirmez le mot de passe
              </label>
              <Input
                id="passwordConfirm"
                name="passwordConfirm"
                type="password"
                autoComplete="current-password"
                value={userData.passwordConfirm}
                onChange={handleChange}
                required
              />
              {userData.password !== userData.passwordConfirm && userData.passwordConfirm.length > 0 && (
                <p className="text-sm text-red-500">Les mots de passe ne correspondent pas.</p>
              )}
            </div>

            <button
              type="submit"
              className="flex w-full justify-center rounded-3xl bg-emerald-600 px-3 py-1.5 \
              text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 \
              focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 \
              disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={hasSubmitted}>
              Créer le compte
            </button>
          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Vous avez déjà un compte?{" "}
            <Link to="/login" className="font-semibold leading-6 text-sky-600 hover:text-sky-500">
              Connectez-vous
            </Link>
          </p>
        </div>
      </div>
    </>
  );
};

export default SignUp;
