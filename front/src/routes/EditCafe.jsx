import { useParams } from "react-router-dom";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import EmptyState from "@/components/EmptyState";
import { Helmet } from "react-helmet-async";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import Input from "@/components/Input";
import { useEffect, useState } from "react";
import Switch from "@/components/CustomSwitch";
import { Link } from "react-router-dom";
import { CheckIcon } from "@heroicons/react/24/solid";
import { isAdmin } from "@/utils/admin";
import { useAuth } from "@/hooks/useAuth";
import ErrorState from "@/components/ErrorState";

const EditCafe = () => {
  const { id: cafeSlug } = useParams();
  const [data, isLoading, error, setData] = useApi(`/cafes/${cafeSlug}`);
  const { user: loggedInUser } = useAuth();

  if (error) {
    if (error.status === 404) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  const [cafeData, setCafeData] = useState(data);

  useEffect(() => {
    setCafeData(data);
  }, [data]);

  if (data && !isAdmin(data, loggedInUser?.username)) {
    return (
      <ErrorState
        title="Accès refusé"
        message="Vous n'avez pas accès à cette page"
        linkText={`Retour à ${data.name}`}
        linkTo={`/cafes/${cafeSlug}`}
      />
    );
  }

  const updateCafe = async (payload) => {
    const toastId = toast.loading("Mise à jour du café...");
    authenticatedRequest
      .put(`/cafes/${data?.slug}`, payload)
      .then((response) => {
        toast.success("Café mis à jour !");
        setData(response.data);
        if (response.data.slug !== data.slug) {
          window.history.pushState({}, "", `/cafes/${response.data.slug}/edit`);
        }
      })
      .catch((error) => {
        toast.error("Erreur lors de la mise à jour du café");
      })
      .finally(() => {
        toast.dismiss(toastId);
      });
  };

  const newChanges = JSON.stringify(cafeData) !== JSON.stringify(data);

  return (
    <>
      <Helmet>{data && <title>Édition {data.name} | Café sans-fil</title>}</Helmet>
      <Container className="py-10">
        <div className="mb-6 text-gray-500 font-semibold">
          <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
            {(isLoading && <span className="animate-pulse">Chargement...</span>) || data?.name}
          </Link>
          <span className="px-3">&gt;</span>
          <span>Modifier</span>
        </div>

        <div className="border-b border-gray-900/10 pb-12">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Informations générales</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Ces informations sont affichées sur la page du café et dans la liste des cafés.
          </p>

          <div className="space-y-2 mt-6">
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
              Nom du café
            </label>
            <Input
              id="name"
              type="text"
              value={cafeData?.name || ""}
              onChange={(e) => setCafeData({ ...cafeData, name: e.target.value })}
            />
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              id="description"
              rows="3"
              className="block w-full shadow-sm sm:text-sm focus:ring-sky-500 focus:border-sky-500 border-gray-300 rounded-md"
              value={cafeData?.description || ""}
              onChange={(e) => setCafeData({ ...cafeData, description: e.target.value })}
            />
          </div>

          <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div className="sm:col-span-3">
              <label htmlFor="pavillon" className="block text-sm font-medium leading-6 text-gray-900">
                Lieu
              </label>
              <div className="mt-2">
                <Input
                  type="text"
                  name="pavillon"
                  id="pavillon"
                  value={cafeData?.location.pavillon || ""}
                  onChange={(e) =>
                    setCafeData({ ...cafeData, location: { ...cafeData.location, pavillon: e.target.value } })
                  }
                />
              </div>
            </div>

            <div className="sm:col-span-3">
              <label htmlFor="local" className="block text-sm font-medium leading-6 text-gray-900">
                Local
              </label>
              <div className="mt-2">
                <Input
                  type="text"
                  name="local"
                  id="local"
                  value={cafeData?.location.local || ""}
                  onChange={(e) =>
                    setCafeData({ ...cafeData, location: { ...cafeData.location, local: e.target.value } })
                  }
                />
              </div>
            </div>
          </div>
        </div>

        <div className="pb-12 mt-6">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Ouverture</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600 mb-3">
            {cafeData?.status_message !== data?.status_message || cafeData?.is_open !== data?.is_open
              ? "Prévisualisation du futur statut"
              : "Statut affiché actuellement"}
          </p>

          <OpenIndicator
            isOpen={cafeData?.is_open}
            openingHours={cafeData?.opening_hours}
            statusMessage={cafeData?.status_message}
          />

          <div className="mt-3">
            <div className="flex items-center">
              <Switch
                checked={!cafeData?.is_open}
                onChange={(e) => {
                  setCafeData({ ...cafeData, is_open: !e, status_message: null });
                }}
                label="Forcer la fermeture"
              />
            </div>
          </div>

          {!cafeData?.is_open && (
            <div className="mt-6">
              <label htmlFor="status-message" className="block text-sm font-medium text-gray-700">
                Raison de fermeture exceptionnelle (optionnel)
              </label>
              <div className="mt-2">
                <Input
                  type="text"
                  name="status-message"
                  id="status-message"
                  placeholder="Exemple: Fermé pour examens"
                  value={cafeData?.status_message || ""}
                  onChange={(e) => setCafeData({ ...cafeData, status_message: e.target.value })}
                />
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 flex items-center justify-end gap-x-4 text-sm font-semibold">
          <Link to={`/cafes/${cafeSlug}`}>
            <button type="button" className="leading-6 text-gray-900 px-3 py-2">
              Annuler
            </button>
          </Link>
          <button
            className="flex items-center gap-2 \
            rounded-md bg-emerald-600 px-3 py-2 text-white shadow-sm hover:bg-emerald-500 \
            focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 \
            disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-emerald-600"
            onClick={() => updateCafe(cafeData)}
            disabled={!newChanges}>
            <CheckIcon className="w-5 h-5" />
            <span>Enregistrer</span>
          </button>
        </div>
      </Container>

      {newChanges && (
        <div className="fixed bottom-0 start-0 z-50 flex justify-between w-full p-4 border-t border-gray-200 bg-sky-50">
          <div className="flex items-center mx-auto gap-4">
            <p className="flex items-center text-sm font-semibold text-gray-600">
              <span>Vous avez des changements non enregistrés. </span>
            </p>
            <button
              className="flex items-center gap-2 bg-emerald-600 rounded-md px-3 py-2"
              onClick={() => updateCafe(cafeData)}>
              <CheckIcon className="text-white w-5 h-5" />
              <span className="text-sm font-semibold text-white">Enregistrer</span>
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default EditCafe;