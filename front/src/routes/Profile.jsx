// import { Helmet } from "react-helmet-async";
import Container from "@/components/Layout/Container";
import Input from "@/components/Widgets/Input";
import Avatar from "@/components/Avatar";
import { useAuth } from "@/hooks/useAuth";
import { useState } from "react";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import toast from "react-hot-toast";
import useApi from "@/hooks/useApi";
import { Link } from "react-router-dom";
import { useEffect } from "react";
import useTitle from "@/hooks/useTitle";

const Profile = () => {
  const { user, setUser, onAccountDelete, verifyPassword } = useAuth();
  const userFullName = user ? user.first_name + " " + user.last_name : "";

  const [userDetails, setUserDetails] = useState({
    photo_url: user?.photo_url,
  });

  const handleSubmit = async (e) => {
    const response = await authenticatedRequest.put(`/users/${user.username}`, userDetails);
    if (response.status === 200) {
      toast.success("Votre profil a été mis à jour");
      setUser({
        ...user,
        photo_url: response.data.photo_url,
      });
    } else {
      toast.error("Une erreur est survenue");
    }
  };

  const { data } = useApi(`/cafes`);

  const getMemberCafes = () => {
    const memberCafes = [];
    data?.item?.map((cafe) => {
      cafe.staff.map((staff) => {
        if (staff.username === user.username) {
          memberCafes.push({ ...cafe, role: staff.role });
        }
      });
    });
    return memberCafes;
  };
  const memberCafes = getMemberCafes();

  // Change password
  const [passwordDetails, setPasswordDetails] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    if (passwordDetails.newPassword !== passwordDetails.confirmPassword) {
      toast.error("Les mots de passe ne correspondent pas");
      setIsSubmitting(false);
      return;
    }

    const isCurrentPasswordCorrect = await verifyPassword(passwordDetails.currentPassword);
    if (!isCurrentPasswordCorrect) {
      toast.error("Le mot de passe actuel est incorrect");
      setIsSubmitting(false);
      return;
    }

    const response = await authenticatedRequest.put(`/users/${user.username}`, {
      password: passwordDetails.newPassword,
    });

    if (response.status === 200) {
      toast.success("Votre mot de passe a été mis à jour");
    } else {
      toast.error("Une erreur est survenue lors de la mise à jour du mot de passe");
    }
    setIsSubmitting(false);
  };

  // Delete account
  const [isConfirmingDelete, setIsConfirmingDelete] = useState(false);

  const handleDeleteClick = () => {
    if (isConfirmingDelete) {
      onAccountDelete();
    } else {
      setIsConfirmingDelete(true);
    }
  };

  useEffect(() => {
    if (isConfirmingDelete) {
      const timer = setTimeout(() => setIsConfirmingDelete(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [isConfirmingDelete]);

  useTitle("Profil | Café sans-fil");

  return (
    <>
      <Container className="py-10">
        <div className="space-y-12">
          <div className="border-b border-gray-900/10 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Photo de profil</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600">
              Votre photo de profil est visible par les cafés où vous passez une commande.
            </p>

            <div className="mt-6">
              <Avatar name={userFullName} size="lg" image={user?.photo_url} key={user?.photo_url} />
            </div>

            <div className="sm:col-span-3 sm:w-1/2 mt-6">
              <label htmlFor="profile-picture" className="block text-sm font-medium leading-6 text-gray-900">
                URL de la photo de profil
              </label>
              <div className="mt-2">
                <Input
                  id="profile-picture"
                  name="profile-picture"
                  type="text"
                  value={userDetails.photo_url || ""}
                  onChange={(e) => setUserDetails({ ...userDetails, photo_url: e.target.value })}
                />
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={userDetails.photo_url === user?.photo_url}
              className="mt-6 rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white shadow-sm \
            hover:bg-emerald-500 \
            focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 \
            disabled:bg-gray-300 disabled:text-gray-500 disabled:shadow-none">
              Enregistrer
            </button>
          </div>
          <div className="border-b border-gray-900/10 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Informations personnelles</h2>

            <p className="mt-1 text-sm leading-6 text-gray-600">
              Vous ne pouvez pas modifier ces informations. Elles sont liées à votre compte de l'UdeM.
            </p>

            <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
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

          <div className="border-b border-gray-900/10 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Cafés</h2>
            {(memberCafes.length === 0 && (
              <p className="mt-1 text-sm leading-6 text-gray-600">
                Vous n'êtes bénévole dans aucun café. Contactez les cafés pour vous impliquer!
              </p>
            )) || (
              <p className="mt-1 text-sm leading-6 text-gray-600">
                Ici s'affichent les cafés où vous êtes bénévole ou administrateur.
              </p>
            )}

            {memberCafes.map((cafe) => (
              <div className="mt-6" key={cafe.slug}>
                <Link to={`/cafes/${cafe.slug}`} className="contents">
                  <div className="flex items-center gap-3 w-fit">
                    <img
                      className="h-10 w-10 rounded-full object-cover"
                      src={cafe.image_url}
                      alt={`Photo du café ${cafe.name}`}
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = "https://placehold.co/700x400?text=:/";
                      }}
                    />
                    <div className="text-sm leading-5">
                      <p className="font-medium text-gray-900">{cafe.name}</p>
                      <p className="text-gray-500">{cafe.role}</p>
                    </div>
                  </div>
                </Link>
              </div>
            ))}
          </div>

          <form onSubmit={handleChangePassword}>
            <div className="pb-12">
              <h2 className="text-base font-semibold leading-7 text-gray-900">Mot de passe</h2>
              <p className="mt-1 text-sm leading-6 text-gray-600">
                Créer un nouveau mot de passe pour votre compte de 8 caractères minimum.
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
                      value={passwordDetails.currentPassword}
                      onChange={(e) => setPasswordDetails({ ...passwordDetails, currentPassword: e.target.value })}
                    />
                  </div>
                </div>

                <div className="sm:col-span-3">
                  <label htmlFor="new-password" className="block text-sm font-medium leading-6 text-gray-900">
                    Nouveau mot de passe
                  </label>
                  <div className="mt-2">
                    <Input
                      id="new-password"
                      name="new-password"
                      type="password"
                      autoComplete="new-password"
                      value={passwordDetails.newPassword}
                      onChange={(e) => setPasswordDetails({ ...passwordDetails, newPassword: e.target.value })}
                    />
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
                      value={passwordDetails.confirmPassword}
                      onChange={(e) => setPasswordDetails({ ...passwordDetails, confirmPassword: e.target.value })}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-end gap-x-6">
              <button
                type="submit"
                disabled={
                  isSubmitting ||
                  !passwordDetails.currentPassword ||
                  !passwordDetails.newPassword ||
                  !passwordDetails.confirmPassword ||
                  passwordDetails.newPassword.length < 8
                }
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
            onClick={handleDeleteClick}
            className={`mt-10 w-52 rounded-md px-3 py-2 text-sm font-semibold shadow-sm ${
              isConfirmingDelete ? "bg-red-600 hover:bg-red-500 text-white" : "bg-red-600 hover:bg-red-500 text-white"
            } focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600`}>
            {isConfirmingDelete ? "Confirmez la suppression" : "Supprimer votre compte"}
          </button>
        </div>
      </Container>
    </>
  );
};

export default Profile;
