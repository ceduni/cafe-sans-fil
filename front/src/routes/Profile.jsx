import { Helmet } from "react-helmet-async";
import Container from "@/components/Container";
import Input from "@/components/Input";
import { useAuth } from "@/hooks/useAuth";
import { useEffect, useState } from "react";
import Avatar from "@/components/Avatar";

const Profile = () => {
  const { getCurrentUser } = useAuth();
  const [user, setUser] = useState(null);
  const userFullName = user ? user.first_name + " " + user.last_name : "";

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getCurrentUser();
        setUser(user);
      } catch (error) {
        console.log(error);
      }
    };
    fetchUser();
  }, []);

  return (
    <>
      <Helmet>
        <title>Profil | Café sans-fil</title>
      </Helmet>
      <Container className="py-10">
        <div className="space-y-12">
          <div className="border-b border-gray-900/10 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Informations personnelles</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600">
              Vous ne pouvez pas modifier ces informations. Elles sont liées à votre compte de l'UdeM.
            </p>

            <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div className="sm:col-span-3">
                <label htmlFor="photo" className="block text-sm font-medium leading-6 text-gray-900">
                  Photo de profil
                </label>
                <div className="mt-2">
                  <Avatar name={userFullName} size="lg" />
                </div>
              </div>
            </div>
            <div className="mt-16 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div className="sm:col-span-3">
                <label htmlFor="first-name" className="block text-sm font-medium leading-6 text-gray-900">
                  Prénom
                </label>
                <div className="mt-2">
                  <p className="text-sm text-gray-500">{user?.first_name}</p>
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="last-name" className="block text-sm font-medium leading-6 text-gray-900">
                  Nom
                </label>
                <div className="mt-2">
                  <p className="text-sm text-gray-500">{user?.last_name}</p>
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                  Adresse courriel de l'UdeM
                </label>
                <div className="mt-2">
                  <p className="text-sm text-gray-500">{user?.email}</p>
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                  Matricule de l'UdeM
                </label>
                <div className="mt-2">
                  <p className="text-sm text-gray-500">{user?.matricule}</p>
                </div>
              </div>
            </div>
          </div>

          <form>
            <div className="pb-12">
              <h2 className="text-base font-semibold leading-7 text-gray-900">Mot de passe</h2>
              <p className="mt-1 text-sm leading-6 text-gray-600">
                Pour des raisons de sécurité, veuillez choisir un mot de passe unique et complexe.
              </p>

              <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                <div className="sm:col-span-3">
                  <label htmlFor="current-password" className="block text-sm font-medium leading-6 text-gray-900">
                    Mot de passe actuel
                  </label>
                  <div className="mt-2">
                    <Input
                      id="current-password"
                      name="current-password"
                      type="password"
                      autoComplete="current-password"
                      disabled
                    />
                  </div>
                </div>

                <div className="sm:col-span-3">
                  <label htmlFor="new-password" className="block text-sm font-medium leading-6 text-gray-900">
                    Nouveau mot de passe
                  </label>
                  <div className="mt-2">
                    <Input id="new-password" name="new-password" type="password" autoComplete="new-password" disabled />
                  </div>
                </div>

                <div className="sm:col-span-3">
                  <label htmlFor="confirm-password" className="block text-sm font-medium leading-6 text-gray-900">
                    Confirmer le nouveau mot de passe
                  </label>
                  <div className="mt-2">
                    <Input
                      id="confirm-password"
                      name="confirm-password"
                      type="password"
                      autoComplete="confirm-password"
                      disabled
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-end gap-x-6">
              <button
                disabled
                type="submit"
                className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white shadow-sm \
                hover:bg-emerald-500 \
                focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 \
                disabled:bg-gray-300 disabled:text-gray-500 disabled:shadow-none">
                Enregistrer
              </button>
            </div>
          </form>
        </div>

        <div className="border-t border-gray-900/10 py-12 mt-6">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Actions supplémentaires</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">Ces actions sont irréversibles.</p>

          <button
            disabled
            className="mt-10 rounded-md bg-red-800 px-3 py-2 text-sm font-semibold text-white shadow-sm \
          hover:bg-red-700 \
          focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600 \
          disabled:bg-gray-300 disabled:text-gray-500 disabled:shadow-none">
            Supprimer votre compte
          </button>
        </div>
      </Container>
    </>
  );
};

export default Profile;
