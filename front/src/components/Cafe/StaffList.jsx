import Avatar from "@/components/Avatar";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import React, { useEffect, useState } from 'react';
import { useParams, Link } from "react-router-dom";
import { getUserFromUsername } from "@/utils/getFromId";

const StaffList = () => {
  const { id } = useParams();
  const cafeSlug = id;
  const [data, isLoading, error] = useApi(`/cafes/${cafeSlug}`);
  const [staffDetails, setStaffDetails] = useState([]);

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

  if (error) {
    if (error.status === 422) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  return (
    <Container className="py-10">
      <div className="mb-5 text-gray-500 font-semibold">
        <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
          {(isLoading && <span className="animate-pulse">Chargement...</span>) || data?.name}
        </Link>
        <span className="px-3">&gt;</span>
        <span>Staff</span>
      </div>

      <ul role="list" className="divide-y divide-gray-100">
        {staffDetails.map((user) => (
          <li key={user.username} className="flex justify-between gap-x-6 py-5">
            <div className="flex min-w-0 gap-x-4">
              <Avatar name={user.username} image={user.photo_url} key={user.user_id} />
              <div className="min-w-0 flex-auto">
                <p className="text-sm font-semibold leading-6 text-gray-900">{`${user.first_name} ${user.last_name}`}</p>
                <p className="mt-1 truncate text-xs leading-5 text-gray-500">{user.email}</p>
              </div>
            </div>
            <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
              <p className="text-sm leading-6 text-gray-900">{user.role}</p>
            </div>
          </li>
        ))}
      </ul>
    </Container>
  );
};

export default StaffList;
