import Input from "@/components/Input";
import Avatar from "@/components/Avatar";
import { Link } from "react-router-dom";

const AccountParameters = ({ user, userFullName, userDetails, memberCafes, setUserDetails, handleSubmit }) => {
    return (
        <>
            <div className="border-b border-gray-900/10 pb-12">
              <h2 className="text-xl font-semibold leading-7 text-gray-900">Photo de profil</h2>
              <p className="mt-1 text-md leading-6 text-gray-600">
                Votre photo de profil est visible par les cafés où vous passez une commande.
              </p>
          
              <div className="mt-6">
                <Avatar name={userFullName} size="lg" image={user?.photo_url} key={user?.photo_url} />
              </div>
          
              <div className="sm:col-span-3 sm:w-1/2 mt-6">
                <label htmlFor="profile-picture" className="block text-md font-medium leading-6 text-gray-900">
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
                className="mt-6 rounded-md bg-emerald-600 px-3 py-2 text-md font-semibold text-white shadow-sm \
              hover:bg-emerald-500 \
              focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 \
              disabled:bg-gray-300 disabled:text-gray-500 disabled:shadow-none">
                Enregistrer
              </button>
            </div>
          
            <div className="border-b border-gray-900/10 pb-12">
              <h2 className="text-xl font-semibold leading-7 text-gray-900">Informations personnelles</h2>
          
              <p className="mt-1 text-md leading-6 text-gray-600">
                Vous ne pouvez pas modifier ces informations. Elles sont liées à votre compte de l'UdeM.
              </p>
          
              <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                <div className="sm:col-span-3">
                  <label htmlFor="first-name" className="block text-md font-medium leading-6 text-gray-900">
                    Prénom
                  </label>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">{user?.first_name}</p>
                  </div>
                </div>
          
                <div className="sm:col-span-3">
                  <label htmlFor="last-name" className="block text-md font-medium leading-6 text-gray-900">
                    Nom
                  </label>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">{user?.last_name}</p>
                  </div>
                </div>
          
                <div className="sm:col-span-3">
                  <label htmlFor="email" className="block text-md font-medium leading-6 text-gray-900">
                    Adresse courriel de l'UdeM
                  </label>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">{user?.email}</p>
                  </div>
                </div>
          
                <div className="sm:col-span-3">
                  <label htmlFor="email" className="block text-md font-medium leading-6 text-gray-900">
                    Matricule de l'UdeM
                  </label>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">{user?.matricule}</p>
                  </div>
                </div>
              </div>
            </div>
          
            <div className="border-b border-gray-900/10 pb-12">
              <h2 className="text-xl font-semibold leading-7 text-gray-900">Cafés</h2>
              {(memberCafes.length === 0 && (
                <p className="mt-1 text-md leading-6 text-gray-600">
                  Vous n'êtes bénévole dans aucun café. Contactez les cafés pour vous impliquer!
                </p>
              )) || (
                <p className="mt-1 text-md leading-6 text-gray-600">
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
        </>
    );
}

export default AccountParameters;