import i18next from 'i18next'

const trad = (key, def) => i18next.t(key, { defaultValue: def });

const upper = (string, index = 0) => {
    return string.charAt(index).toUpperCase() + string.slice(1);
};

const lower = (string, index = 0) => {
    return string.charAt(index).toLowerCase() + string.slice(1);
};

export const displayCafeLocation = (location) => {
    if (!location || !location.pavillon) {
        return "";
    }

    return `${upper(location.pavillon)}, ${lower(location.local)}`;
};

export const shouldDisplayInfo = (object) => {
    if (!object) {
        return false;
    }

    const now = new Date();
    const defaultStartTime = new Date("1900-01-01T00:00:00.000Z");
    const defaultEndTime = new Date("9999-12-31T23:59:59.999Z");

    const start = object.start ? new Date(object.start) : defaultStartTime;
    const end = object.end ? new Date(object.end) : defaultEndTime;

    return object.value && now >= start && now <= end;
};



export const PAYMENT_METHODS = {
    CASH: trad("payment_method.cash", "Argent comptant"),
    CREDIT_CARD: trad("payment_method.credit", "Carte de crédit"),
    DEBIT_CARD: trad("payment_method.debit", "Carte de débit"),
};
