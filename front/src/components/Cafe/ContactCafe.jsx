import Instagram from "@/assets/icons/logo-instagram.svg";
import Facebook from "@/assets/icons/logo-facebook.svg";
import Twitter from "@/assets/icons/logo-twitter.svg";
import { ComputerDesktopIcon, EnvelopeIcon, LinkIcon, PhoneIcon } from "@heroicons/react/24/solid";

const icon = (platform) => {
  switch (platform) {
    case "Facebook":
      return <img src={Facebook} alt="Facebook logo" className="h-6 w-6" />;
    case "Instagram":
      return <img src={Instagram} alt="Instagram logo" className="h-6 w-6" />;
    case "Twitter":
      return <img src={Twitter} alt="Twitter logo" className="h-6 w-6" />;
    default:
      return <LinkIcon className="h-6 w-6" />;
  }
};

const ContactCafe = ({ contact, socialMedia }) => {
  return (
    <div>
      <div className="mt-4 flex flex-col">
        {contact?.phone_number && (
          <div className="flex items-center gap-x-4 p-6 border-b border-gray-200 last:border-b-0">
            <PhoneIcon className="h-6 w-6" />
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
              <EnvelopeIcon className="h-6 w-6" />
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
              <ComputerDesktopIcon className="h-6 w-6" />
              <p className="text-gray-600">{contact?.website}</p>
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
              {icon(s.platform_name)}
              <p className="text-gray-600">{s.platform_name || s.link}</p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

const SocialIcons = ({ socialMedia }) => {
  return (
    <div className="flex items-center gap-x-4 py-3">
      {socialMedia?.map((s, index) => (
        <a href={s.link} key={index} target="_blank" rel="noreferrer" className="opacity-60 hover:opacity-100">
          {icon(s.platform_name)}
        </a>
      ))}
    </div>
  );
};

export { ContactCafe, SocialIcons };
