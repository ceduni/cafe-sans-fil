import { BuildingStorefrontIcon, ChartBarIcon, PencilIcon, UserIcon } from "@heroicons/react/24/outline";
import { Link, useParams } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { getUserRole, isAdmin } from "@/utils/admin";

const CafeMemberHeader = ({ cafe }) => {
  const { id: cafeSlug } = useParams();
  const { isLoggedIn, user } = useAuth();

  if (!isLoggedIn || !user || !cafe) {
    return null;
  }

  const role = getUserRole(cafe, user.username);

  if (!role) {
    return null;
  }

  const memberActions = [
    { name: "Commandes en cours", href: `/cafes/${cafeSlug}/orders`, icon: BuildingStorefrontIcon },
    { name: "Liste de staff", href: `/cafes/${cafeSlug}/staff`, icon: UserIcon },
    { name: "Modifier le menu", href: `/cafes/${cafeSlug}/edit/menu`, icon: PencilIcon },
  ];

  const adminActions = [
    { name: "Commandes en cours", href: `/cafes/${cafeSlug}/orders`, icon: BuildingStorefrontIcon },
    { name: "Gérer le staff", href: `/cafes/${cafeSlug}/staff`, icon: UserIcon },
    { name: "Modifier le menu", href: `/cafes/${cafeSlug}/edit/menu`, icon: PencilIcon },
    { name: "Modifier le café", href: `/cafes/${cafeSlug}/edit`, icon: PencilIcon },
    { name: "Rapports de ventes", href: `/cafes/${cafeSlug}/sales-report`, icon: ChartBarIcon },
    {name: "Modifier les annonces", href: `/cafes/${cafeSlug}/announcements`, icon: PencilIcon},
    {name: "Modifier les évenements", href: `/cafes/${cafeSlug}/events`, icon: PencilIcon},     
  ];

  let actions = isAdmin(cafe, user.username) ? adminActions : memberActions;

  return (
    <div className="mb-6 p-6 rounded-3xl bg-sky-100 border-sky-400 border-l-4">
      <div className="min-w-0 flex-1">
        <h2 className="text-xl font-bold">
          Vous êtes <span className="lowercase">{role}</span> dans ce café
        </h2>
      </div>
      <div className="mt-5 flex gap-3 flex-wrap">
        {actions.map((action) => (
          <span key={action.name}>
            <Link to={action.href} className="contents">
              <button
                type="button"
                className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                <action.icon className="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                {action.name}
              </button>
            </Link>
          </span>
        ))}
      </div>
    </div>
  );
};

export default CafeMemberHeader;
