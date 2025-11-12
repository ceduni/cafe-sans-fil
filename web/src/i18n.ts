import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import enTranslation from './locales/en.json';
import frTranslation from './locales/fr.json';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: enTranslation },
    fr: { translation: frTranslation },
  },
  lng: 'fr', // Default language
  fallbackLng: 'fr', // Fallback language
  interpolation: {
    escapeValue: false, // React already escapes by default
  },
});

export default i18n;
