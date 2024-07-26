import { Helmet } from "react-helmet-async";
import { useAuth } from "@/hooks/useAuth";
import { useState } from "react";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import toast from "react-hot-toast";
import useApi from "@/hooks/useApi";
import { useEffect } from "react";
import AccountParameters from "@/components/Profile/AccountParameters";
import NutriProfile from "@/components/Profile/NutriProfile";
import OtherProfileAction from "@/components/Profile/OtherProfileAction";

const Profile = () => {
  const { user, setUser, onAccountDelete, verifyPassword } = useAuth();
  const userFullName = user ? user.first_name + " " + user.last_name : "";

  const [activeTab, setActiveTab] = useState(localStorage.getItem("activeTab") || 0);

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

  // const getMemberCafes = () => {
  //   const memberCafes = [];
  //   data?.map((cafe) => {
  //     cafe.staff.map((staff) => {
  //       if (staff.username === user.username) {
  //         memberCafes.push({ ...cafe, role: staff.role });
  //       }
  //     });
  //   });
  //   return memberCafes;
  // };
  const memberCafes = [];

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

  // const handleDeleteClick = () => {
  //   if (isConfirmingDelete) {
  //     onAccountDelete();
  //   } else {
  //     setIsConfirmingDelete(true);
  //   }
  // };

  const handleDeleteClick = () => {
    const deleteToast = toast.loading("Suppression en cours...");
      onAccountDelete();
    toast.success("Votre compte a été supprimé");
    toast.dismiss(deleteToast);
  };

  const handleTabChange = (index) => {
    localStorage.setItem("activeTab", index);
    setActiveTab(index);
  }

  useEffect(() => {
    if (isConfirmingDelete) {
      const timer = setTimeout(() => setIsConfirmingDelete(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [isConfirmingDelete]);

  useEffect(() => {
    if (activeTab) {
      setActiveTab(parseInt(activeTab));
    }
  }, []);

  return (
    <>
      <Helmet>
        <title>Profil | Café sans-fil</title>
      </Helmet>
      <h2 className="text-3xl h-5 px-5 py-5 font-bold mb-6">Mon profile</h2>
      <div className="w-full p-4">
        <div className="flex text-xl border-b border-gray-200 mb-4">
          <button 
          className={`py-2 px-4 ${activeTab === 0 ? 'border-b-2 border-blue-500': ''}`}
          onClick={() => handleTabChange(0)}
          >
            Informations Personnels
          </button>

          <button 
          className={`py-2 px-4 ${activeTab === 1 ? 'border-b-2 border-blue-500': ''}`}
          onClick={() => handleTabChange(1)}
          >
            Profile nutritif
          </button>

          <button 
          className={`py-2 px-4 ${activeTab === 2 ? 'border-b-2 border-blue-500': ''}`}
          onClick={() => handleTabChange(2)}
          >
            Paramètres de compte
          </button>

        </div>

        {activeTab === 0 && (
          <AccountParameters
            user={user}
            userFullName={userFullName}
            userDetails={userDetails}
            memberCafes={memberCafes}
            setUserDetails={setUserDetails}
            handleSubmit={handleSubmit}
          />
        )}

        {activeTab === 1 && (
          <NutriProfile
            user={user}
            userDetails={userDetails}
            setUserDetails={setUserDetails}
            handleSubmit={handleSubmit}
          />
        )}

        {activeTab === 2 && (
          <OtherProfileAction
            passwordDetails={passwordDetails}
            setPasswordDetails={setPasswordDetails}
            handleChangePassword={handleChangePassword}
            isSubmitting={isSubmitting}
            handleDeleteClick={handleDeleteClick}
            isConfirmingDelete={isConfirmingDelete}
          />
        )}

      </div>
    </>
  );
};

export default Profile;
