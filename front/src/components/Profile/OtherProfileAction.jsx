import Input from "@/components/Input";
import DeleteConfirmation from "@/components/Profile/DeleteConfirmation";
import { useState } from "react";

const OtherProfileAction = ({ passwordDetails, setPasswordDetails, handleChangePassword, isSubmitting, handleDeleteClick, isConfirmingDelete }) => {

    const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);
    const handleDeleteConfirmation = () => {
        setShowDeleteConfirmation(!showDeleteConfirmation);
    }

    return (
        <>
            <div className="space-y-12">
                <form onSubmit={handleChangePassword}>
                    <div className="pb-12">
                        <h2 className="text-xl font-semibold leading-7 text-gray-900">Mot de passe</h2>
                        <p className="mt-1 text-md leading-6 text-gray-600">
                            Créer un nouveau mot de passe pour votre compte de 8 caractères minimum.
                        </p>

                        <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                            <div className="sm:col-span-3">
                                <label htmlFor="current-password" className="block text-md font-medium leading-6 text-gray-900">
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
                                <label htmlFor="new-password" className="block text-md font-medium leading-6 text-gray-900">
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
                                <label htmlFor="confirm-password" className="block text-md font-medium leading-6 text-gray-900">
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
                <h2 className="text-xl font-semibold leading-7 text-gray-900">Actions supplémentaires</h2>
                <p className="mt-1 text-md leading-6 text-gray-600">Ces actions sont irréversibles.</p>

                {/* <button
                onClick={handleDeleteClick}
                className={`mt-10 w-64 rounded-md px-3 py-2 text-md font-semibold shadow-sm ${
                isConfirmingDelete ? "bg-red-600 hover:bg-red-500 text-white" : "bg-red-600 hover:bg-red-500 text-white"
                } focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600`}>
                {isConfirmingDelete ? "Confirmez la suppression" : "Supprimer votre compte"}
                </button> */}
                
                <button
                onClick={handleDeleteConfirmation}
                className={`mt-10 w-64 rounded-md px-3 py-2 text-md font-semibold shadow-sm bg-red-600 hover:bg-red-500 text-white`}
                >
                    Supprimer votre compte
                </button>
            </div>

            {showDeleteConfirmation && (
                <DeleteConfirmation
                isModalOpen={showDeleteConfirmation}
                setIsModalOpen={setShowDeleteConfirmation}
                handleDeleteClick={handleDeleteClick}
                />
            )}

        </>
    );
};

export default OtherProfileAction;