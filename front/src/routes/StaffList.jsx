import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import React, { useEffect, useState } from "react";
import Input from "@/components/Input";
import { getUserFromUsername } from "@/utils/getFromId";
import { CheckIcon } from "@heroicons/react/24/solid";
import { ROLES, isAdmin } from "@/utils/admin";
import { useAuth } from "@/hooks/useAuth";
import toast from "react-hot-toast";
import { useParams, Link } from "react-router-dom";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { Helmet } from "react-helmet-async";
import EmptyState from "@/components/EmptyState";
import Breadcrumbs from "@/components/Breadcrumbs";
import Avatar from "@/components/Avatar";
import classNames from "classnames";

const StaffList = () => {
  const { id: cafeSlug } = useParams();
  const { data, isLoading, error } = useApi(`/cafes/${cafeSlug}`);
  const [staffDetails, setStaffDetails] = useState([]);

  const { user: loggedInUser } = useAuth();
  const isLoggedUserAdmin = isAdmin(data, loggedInUser?.username);

  useEffect(() => {
    const fetchStaffDetails = async () => {
      const fetchedStaffDetails = await Promise.all(
        data?.staff.map(async (person) => {
          const userData = await getUserFromUsername(person.username);
          return userData ? { ...person, ...userData } : person;
        }) || []
      );
      setStaffDetails(fetchedStaffDetails);
    };

    if (data?.staff) {
      fetchStaffDetails();
    }
  }, [data?.staff]);

  const [hasChanges, setHasChanges] = useState(false);
  const [updatedRoles, setUpdatedRoles] = useState({});
  const [newStaff, setNewStaff] = useState("");

  if (error) {
    if (error.status === 404) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  const handleRoleChange = (username, newRole) => {
    const newUpdatedRoles = { ...updatedRoles, [username]: newRole };

    const anyChange = Object.keys(newUpdatedRoles).some(
      (key) => newUpdatedRoles[key] !== data?.staff.find((staff) => staff.username === key)?.role
    );

    setUpdatedRoles(newUpdatedRoles);
    setHasChanges(anyChange);
  };

  const handleConfirmChanges = async () => {
    let success = true;
    for (const [username, role] of Object.entries(updatedRoles)) {
      try {
        if (role !== "remove") {
          await authenticatedRequest.put(`/cafes/${cafeSlug}/staff/${username}`, { role });
        } else {
          await authenticatedRequest.delete(`/cafes/${cafeSlug}/staff/${username}`);
          setStaffDetails(staffDetails.filter((user) => user.username !== username));
        }
      } catch (error) {
        success = false;
        toast.error(`Erreur: ${error.message || "Erreur inconnue"}`);
      }
    }
    if (success) {
      toast.success("Modifications enregistrées avec succès");
      window.location.reload();
    } else {
      toast.error("Des erreurs sont survenues lors de l'enregistrement");
    }
    setUpdatedRoles({});
    setHasChanges(false);
  };

  const handleAddStaff = async () => {
    if (!newStaff.trim()) return;

    try {
      const response = await authenticatedRequest.post(`cafes/${cafeSlug}/staff`, {
        username: newStaff,
        role: "Bénévole",
      });
      setStaffDetails([...staffDetails, response.data]);
      setNewStaff("");
      toast.success("Staff ajouté avec succès");
      window.location.reload();
    } catch (error) {
      if (error.response && error.response.status === 404) {
        toast.error("Compte non trouvé");
      } else if (error.response && error.response.status === 409) {
        toast.error("Compte déjà membre du staff");
      } else {
        toast.error("Erreur lors de l'ajout d'un staff");
      }
    }
  };

  return (
    <>
      <Helmet>{data && <title>Staff de {data.name} | Café sans-fil</title>}</Helmet>

      <Container className="py-10">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
            {data?.name}
          </Breadcrumbs.Item>
          <Breadcrumbs.Item>Staff</Breadcrumbs.Item>
        </Breadcrumbs>

        <div className={classNames("pb-12 w-full", { "border-b border-gray-900/10": isLoggedUserAdmin })}>
          <h2 className="text-base font-semibold leading-7 text-gray-900">Liste de staff</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            {`${isLoggedUserAdmin ? "Gérer" : "Consulter"}`} les membres du personnel actuels de votre café.
          </p>

          <ul role="list" className="divide-y divide-gray-100 mt-6">
            {staffDetails.length === 0 &&
              Array.from({ length: 5 }).map((_, i) => (
                <li key={i} className="px-2 rounded-2xl flex flex-col sm:flex-row justify-between gap-x-6 gap-y-4 py-5">
                  <div className="flex min-w-0 gap-x-4">
                    <div className="animate-pulse bg-gray-200 rounded-full h-12 w-12" />
                    <div className="min-w-0 flex-auto">
                      <div className="animate-pulse bg-gray-200 rounded-full h-4 w-24" />
                      <div className="animate-pulse bg-gray-200 rounded-full h-3 w-36 mt-3" />
                      <div className="animate-pulse bg-gray-200 rounded-full h-3 w-24 mt-3" />
                    </div>
                  </div>
                  <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
                    <div className="animate-pulse bg-gray-200 rounded-full h-4 w-24" />
                  </div>
                </li>
              ))}

            {staffDetails.map((user) => (
              <li
                key={user.username}
                className={`px-2 rounded-2xl flex flex-col sm:flex-row justify-between gap-x-6 gap-y-4 py-5  ${
                  updatedRoles[user.username] === "remove"
                    ? "bg-red-100 "
                    : updatedRoles[user.username] && updatedRoles[user.username] !== user.role
                      ? "bg-sky-50"
                      : ""
                  }`}>
                <div className="flex min-w-0 gap-x-4">
                  <Avatar
                    name={`${user.first_name} ${user.last_name}`}
                    size="md"
                    image={user?.photo_url}
                    key={user?.user_id}
                  />
                  <div className="min-w-0 flex-auto">
                    <p className="text-sm font-semibold leading-6 text-gray-900">{`${user.first_name} ${user.last_name}`}</p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">{user.email}</p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-400">{`${user.username}`}</p>
                  </div>
                </div>
                <div className="flex flex-col relative left-16 sm:left-0 ">
                  {isLoggedUserAdmin ? (
                    <select
                      id="role"
                      name="role"
                      defaultValue={user.role}
                      className={
                        "w-32 sm:w-full py-2 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 text-sm border-gray-300"
                      }
                      onChange={(e) => handleRoleChange(user.username, e.target.value)}>
                      <option
                        value={ROLES.ADMIN}
                        disabled={user.role === ROLES.ADMIN && loggedInUser.username !== user.username}>
                        {ROLES.ADMIN}
                      </option>
                      <option
                        value={ROLES.MEMBER}
                        disabled={user.role === ROLES.ADMIN && loggedInUser.username !== user.username}>
                        {ROLES.MEMBER}
                      </option>
                      <option
                        value="remove"
                        disabled={user.role === ROLES.ADMIN && loggedInUser.username !== user.username}>
                        Supprimer
                      </option>
                    </select>
                  ) : (
                    <p className="text-sm leading-6 text-gray-900">{user.role}</p>
                  )}
                </div>
              </li>
            ))}
          </ul>

          {isLoggedUserAdmin && (
            <div className="mt-3 flex items-center justify-end gap-x-4 text-sm font-semibold sm:justify-end relative sm:right-24">
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
                onClick={handleConfirmChanges}
                disabled={!hasChanges}>
                <CheckIcon className="w-5 h-5" />
                <span>Enregistrer</span>
              </button>
            </div>
          )}
        </div>

        {isLoggedUserAdmin && (
          <div className="pb-12 mt-6">
            <h2 className="text-base font-semibold leading-7 text-gray-900">Ajouter un staff</h2>
            <p className="mt-1 text-sm leading-6 text-gray-600">Intégrez un nouveau membre.</p>

            <div className="space-y-2 mt-6 sm:w-1/2">
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Username ou matricule du nouveau staff
              </label>
              <Input id="new staff" type="text" onChange={(e) => setNewStaff(e.target.value)} />
            </div>

            <button
              className="mt-6 rounded-md bg-emerald-600 px-5 py-2 text-sm font-semibold text-white shadow-sm \
        hover:bg-emerald-500 \
        focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 \
        disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-emerald-600"
              onClick={() => handleAddStaff()}
              disabled={!newStaff.trim()}>
              <span>Enregistrer</span>
            </button>
          </div>
        )}
      </Container>
    </>
  );
};

export default StaffList;
