import { ComputerDesktopIcon, EnvelopeIcon, PhoneIcon } from "@heroicons/react/24/solid";
import { getPlatformIcon, getPlatformName, iconClassNames } from "@/utils/socials";

const displayWebsite = (website) => {
  if (!website) return null;
  try {
    const url = new URL(website);
    return url.hostname;
  } catch (e) {
    return website;
  }
};

const ContactCafe = ({ contact, socialMedia }) => {
  return (
    <div>
      <div className="mt-4 flex flex-col">
        {contact?.phone_number && (
          <div className="flex items-center gap-x-4 p-6 border-b border-gray-200 last:border-b-0">
            <PhoneIcon className={iconClassNames} />
            <p className="text-gray-600">{contact?.phone_number}</p>
          </div>
        )}
        {contact?.email && (
          <a
            href={`mailto:${contact?.email}`}
            target="_blank"
            rel="noreferrer"
            className="border-b border-gray-200 hover:bg-gray-50 last:border-b-0">
            <div className="flex items-center gap-x-4 p-6">
              <EnvelopeIcon className={iconClassNames} />
              <p className="text-gray-600">{contact?.email}</p>
            </div>
          </a>
        )}
        {contact?.website && (
          <a
            href={contact?.website}
            target="_blank"
            rel="noreferrer"
            className="border-b border-gray-200 hover:bg-gray-50 last:border-b-0">
            <div className="flex items-center gap-x-4 p-6">
              <ComputerDesktopIcon className={iconClassNames} />
              <p className="text-gray-600">{displayWebsite(contact.website)}</p>
            </div>
          </a>
        )}
        {socialMedia?.map((s, index) => (
          <a
            href={s.link}
            key={index}
            target="_blank"
            rel="noreferrer"
            className="border-b border-gray-200 hover:bg-gray-50 last:border-b-0">
            <div className="flex items-center gap-x-4 p-6">
              {getPlatformIcon(s)}
              <p className="text-gray-600">{getPlatformName(s)}</p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default ContactCafe;
