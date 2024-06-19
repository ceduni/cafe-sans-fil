import { useParams } from "react-router-dom";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import { Helmet } from "react-helmet-async";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import Input from "@/components/Input";
import { useEffect, useRef, useState } from "react";
import Switch from "@/components/CustomSwitch";
import { Link, useNavigate } from "react-router-dom";
import { CheckIcon } from "@heroicons/react/24/solid";
import { useIsVisible } from "@/hooks/useIsVisible";
import AdminOnly from "@/helpers/AdminOnly";
import Breadcrumbs from "@/components/Breadcrumbs";
import EditAdditionalInfo from "@/components/Cafe/EditAdditionalInfo";
import EditPaymentMethods from "@/components/Cafe/EditPaymentMehods";
import EditOpeningHours from "@/components/Cafe/EditOpeningHours";
import EditSocials from "@/components/Cafe/EditSocials";

const EditCafe = () => {
  const { id: cafeSlug } = useParams();
  const { data, isLoading, error, refetch } = useApi(`/cafes/${cafeSlug}`);

  // On utilise un état local pour sauegarder les changements et l'état précédent
  const [cafeData, setCafeData] = useState(null);
  useEffect(() => {
    setCafeData(JSON.parse(JSON.stringify(data)));
  }, [data]);
  const newChanges = JSON.stringify(cafeData) !== JSON.stringify(data);

  const navigate = useNavigate();

  const saveButtonRef = useRef();
  const isSaveButtonVisible = useIsVisible(saveButtonRef);

  const updateCafe = async (payload) => {
    const toastId = toast.loading("Mise à jour du café...");
    authenticatedRequest
      .put(`/cafes/${cafeSlug}`, payload)
      .then((response) => {
        toast.success("Café mis à jour");
        if (response.data.slug !== data.slug) {
          // Redirection vers la nouvelle page
          navigate(`/cafes/${response.data.slug}/edit`, { replace: true });
        }
        refetch();
      })
      .catch((error) => {
        switch (error.response?.status) {
          case 409:
            if (error.response.data?.detail.includes("name")) {
              toast.error("Le nom du café doit être unique.");
            } else if (error.response.data?.detail.includes("time")) {
              toast.error("Les heures d'ouverture ne peuvent pas se chevaucher.");
            } else if (error.response.data?.detail.includes("already exists")) {
              toast.error("Vous devez choisir un autre nom pour ce café.");
            } else {
              toast.error("Conflit lors de la mise à jour du café");
            }
            break;
          default:
            toast.error("Erreur lors de la mise à jour du café");
        }
      })
      .finally(() => {
        toast.dismiss(toastId);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    updateCafe(cafeData);
  };

  return (
    <AdminOnly cafe={data} error={error}>
      <Helmet>{data && <title>Édition {data.name} | Café sans-fil</title>}</Helmet>
      <Container className="py-10">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
            {data?.name}
          </Breadcrumbs.Item>
          <Breadcrumbs.Item>Modifier</Breadcrumbs.Item>
        </Breadcrumbs>

        <form onSubmit={handleSubmit}>
          <div className="border-b border-gray-900/10 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Informations générales</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600">
              Ces informations sont affichées sur la page du café et dans la liste des cafés.
            </p>

            <div className="space-y-2 mt-6">
              <label htmlFor="cafeName" className="block text-sm font-medium text-gray-700">
                Nom du café
              </label>
              <Input
                id="cafeName"
                type="text"
                value={cafeData?.name || ""}
                onChange={(e) => setCafeData({ ...cafeData, name: e.target.value })}
                required
              />
              {cafeData?.name !== data?.name && (
                <p className="text-sm text-red-500">
                  Cela changera l'URL du café et vous serez redirigé vers la nouvelle page.
                </p>
              )}
            </div>

            <div className="space-y-2 mt-6">
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                id="description"
                rows="3"
                value={cafeData?.description || ""}
                onChange={(e) => setCafeData({ ...cafeData, description: e.target.value })}
                className="block w-full rounded-md shadow-sm sm:text-sm \
                focus:ring-2 focus:ring-inset focus:ring-sky-600 focus:ring-opacity-75 \
                ring-1 ring-inset ring-gray-300 border-0 \
                focus:invalid:border-red-600 focus:invalid:ring-red-600 focus:invalid:ring-opacity-70"
                required
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
                    placeholder="Pavillon Claire-McNicoll"
                    required
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
                    placeholder="local 1234"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="space-y-2 mt-6">
              <label htmlFor="image_url" className="block text-sm font-medium text-gray-700">
                Image de bannière
              </label>
              <Input
                type="url"
                name="image_url"
                id="image_url"
                value={cafeData?.image_url || ""}
                onChange={(e) => setCafeData({ ...cafeData, image_url: e.target.value })}
                placeholder="https://example.com/image.jpg"
                required
              />
            </div>
          </div>

          <div className="border-b border-gray-900/10 pb-12 mt-6">
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
                  Raison de fermeture <span className="text-xs text-gray-500">(optionnel)</span>
                </label>
                <div className="mt-2">
                  <Input
                    type="text"
                    name="status-message"
                    id="status-message"
                    placeholder="Fermé pour examens"
                    value={cafeData?.status_message || ""}
                    onChange={(e) => setCafeData({ ...cafeData, status_message: e.target.value })}
                  />
                </div>
              </div>
            )}

            <EditOpeningHours cafeData={cafeData} setCafeData={setCafeData} />
          </div>

          <div className="border-b border-gray-900/10 pb-12 mt-6">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Messages additionnels</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600 mb-3">
              Vous pouvez ajouter des messages additionnels courts qui seront affichés sur la page du café et dans la
              liste des cafés. Il peut s'agir de messages temporaires ou permanents.
            </p>
            <EditAdditionalInfo cafeData={cafeData} setCafeData={setCafeData} />
          </div>

          <div className="border-b border-gray-900/10 pb-12 mt-6">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Methodes de paiement</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600 mb-3">
              Vous pouvez définir quelles méthodes de paiement sont acceptées dans ce café. Cela sera affiché sur la
              page du café.
            </p>
            <EditPaymentMethods cafeData={cafeData} setCafeData={setCafeData} />
          </div>

          <div className="border-b border-gray-900/10 mt-6 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Informations de contact</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600">Ces informations sont affichées sur la page du café</p>

            <div className="space-y-2 mt-6">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Adresse courriel <span className="text-xs text-gray-500">(optionnel)</span>
              </label>
              <Input
                type="email"
                name="email"
                id="email"
                value={cafeData?.contact.email || ""}
                onChange={(e) => setCafeData({ ...cafeData, contact: { ...cafeData.contact, email: e.target.value } })}
              />
            </div>

            <div className="space-y-2 mt-6">
              <label htmlFor="website" className="block text-sm font-medium text-gray-700">
                Site web <span className="text-xs text-gray-500">(optionnel)</span>
              </label>
              <Input
                type="url"
                name="website"
                id="website"
                value={cafeData?.contact.website || ""}
                onChange={(e) =>
                  setCafeData({ ...cafeData, contact: { ...cafeData.contact, website: e.target.value } })
                }
              />
            </div>

            <div className="space-y-2 mt-6">
              <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700">
                Numéro de téléphone <span className="text-xs text-gray-500">(optionnel)</span>
              </label>
              <Input
                type="text"
                name="phone_number"
                id="phone_number"
                value={cafeData?.contact.phone_number || ""}
                onChange={(e) =>
                  setCafeData({ ...cafeData, contact: { ...cafeData.contact, phone_number: e.target.value } })
                }
              />
            </div>
          </div>

          <div className="mt-6 pb-12">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Réseaux sociaux</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600">Ces informations sont affichées sur la page du café</p>

            <EditSocials cafeData={cafeData} setCafeData={setCafeData} />
          </div>

          <div className="mt-6 flex items-center justify-end gap-x-4 text-sm font-semibold">
            <Link to={`/cafes/${cafeSlug}`} className="leading-6 text-gray-900 px-3 py-2">
              Annuler
            </Link>
            <button
              className="flex items-center gap-2 \
            rounded-md bg-emerald-600 px-3 py-2 text-white shadow-sm hover:bg-emerald-500 \
            focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 \
            disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-emerald-600"
              type="submit"
              disabled={!newChanges}
              ref={saveButtonRef}>
              <CheckIcon className="w-5 h-5" />
              <span>Enregistrer</span>
            </button>
          </div>

          {newChanges && !isSaveButtonVisible && (
            <div className="fixed bottom-0 start-0 z-50 flex justify-between w-full p-4 border-t border-gray-200 bg-sky-50">
              <div className="flex items-center mx-auto gap-4">
                <p className="flex items-center text-sm font-semibold text-gray-600">
                  <span>Vous avez des changements non enregistrés. </span>
                </p>
                <button className="flex items-center gap-2 bg-emerald-600 rounded-md px-3 py-2" type="submit">
                  <CheckIcon className="text-white w-5 h-5" />
                  <span className="text-sm font-semibold text-white">Enregistrer</span>
                </button>
              </div>
            </div>
          )}
        </form>
      </Container>
    </AdminOnly>
  );
};

export default EditCafe;
