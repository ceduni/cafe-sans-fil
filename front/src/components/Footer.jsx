import { QuestionMarkCircleIcon } from "@heroicons/react/24/solid";

const Footer = () => {
    return (
        <footer className="bg-white border-t border-gray-200 py-5">
            <div className="w-full max-w-screen-xl mx-auto p-5 md:py-8">
                <div className="flex gap-3 items-center mb-4 justify-center">
                    <img src="/logo_text.png" className="h-[2.6rem]" alt="Logo de café sans-fil" />
                </div>
                <div className="text-sm text-gray-500 text-center space-y-4">
                    <span className="font-semibold">Version {APP_VERSION}</span>
                    <div>
                        <p>
                            Ceduni &bull; Projet disponible sur{" "}
                            <a className="underline" href="https://github.com/ceduni/cafe-sans-fil" target="_blank">
                                GitHub
                            </a>
                        </p>
                    </div>
                    <a className="underline block" href="https://discord.com/channels/1143019940501274634/1199491803901075506" rel='noreferrer' target="_blank">
                        Signalez un problème ou faites une suggestion
                    </a>
                    {/* <a
                        href="mailto:louis.edouard.lafontant@umontreal.ca"
                        className="p-2 rounded-md bg-gray-100 hover:bg-gray-200 transition-all inline-flex items-center max-w-xs gap-4 sm:max-w-none">
                        <QuestionMarkCircleIcon className="h-5 w-5 text-gray-500" />
                        <span className="text-left">Vous êtes gérant d'un café? Contactez&nbsp;nous</span>
                    </a> */}
                    <p className="font-medium">&copy; 2024 Café sans-fil</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
