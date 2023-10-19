import { BuildingStorefrontIcon, PencilIcon, UserIcon } from "@heroicons/react/24/outline";

const CafeMemberHeader = () => {
  const IS_ADMIN = true;

  const actions = [
    { name: "Commandes en cours", href: "#", icon: BuildingStorefrontIcon },
    { name: "Modifier le menu", href: "#", icon: PencilIcon },
  ];

  const adminActions = [
    { name: "Gérer le staff", href: "#", icon: UserIcon },
    { name: "Modifier le café", href: "#", icon: PencilIcon },
  ];

  if (IS_ADMIN) {
    actions.push(...adminActions);
  }

  return (
    <div className="mb-10 p-6 rounded-lg bg-emerald-100">
      <div className="min-w-0 flex-1">
        <h2 className="text-xl font-bold">Vous êtes bénévole dans ce café</h2>
      </div>
      <div className="mt-5 flex gap-3 flex-wrap">
        {actions.map((action) => (
          <span key={action.name}>
            <button
              type="button"
              className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <action.icon className="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true" />
              {action.name}
            </button>
          </span>
        ))}
      </div>
    </div>
  );
};

export default CafeMemberHeader;
