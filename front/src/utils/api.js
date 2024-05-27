import { Cafe, CafeMenu, CafeMenuItem, Order, User } from "@/models";
import { Event } from "@/models/event";

const buildUrl = (url) => import.meta.env.VITE_API_ENDPOINT + "/api" + url;

async function fetchData(url, setLoading = null) {
    if (setLoading) {
        setLoading(true);
    }

    try {
        const response = await fetch(buildUrl(url));

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        const responseData = await response.json();

        return responseData;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // Propagate the error to the caller
    } finally {
        if (setLoading) {
            setLoading(false);
        }
    }
}

function resolveQuery(query) {
    // TODO: Future development (small query language)
    // Example: OrderAPI.get(`user:${this.id}`)
}

export async function isAPIAvailable() {
    const result = await fetchData(`/health`);
    return result.status === "available";
}

export const CafeAPI = {
    /**
     * Fetches a specific cafe by ID.
     * @param {string} id - The ID of the cafe to fetch.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Cafe[]>} - A promise that resolves with an array of Cafe objects.
     */
    get: async function (id, setLoading = null, cancel = false) {
        const result = await fetchData(`/cafes/${id}`, setLoading);
        return result.map(cafeData => new Cafe(cafeData));
    },
    /**
     * Fetches all cafes.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Cafe[]>} - A promise that resolves with an array of Cafe objects.
     */
    getAll: async function (setLoading = null, cancel = false) {
        const result = await fetchData(`/cafes`, setLoading);
        return result.map(cafeData => new Cafe(cafeData));
    },
    /**
     * Fetches all cafes.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Cafe[]>} - A promise that resolves with an array of Cafe objects.
     */
    getMenu: async function (id, setLoading = null, cancel = false) {
        const result = await fetchData(`/cafes/${id}/menu`, setLoading);
        return result.map(cafeData => new CafeMenu(cafeData));
    },
    /**
     * Fetches all cafes.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Cafe[]>} - A promise that resolves with an array of Cafe objects.
     */
    getMenuItem: async function (id, item, setLoading = null, cancel = false) {
        const result = await fetchData(`/cafes/${id}/menu/${item}`, setLoading);
        return result.map(cafeData => new CafeMenuItem(cafeData));
    },
    /**
     * Fetches all cafe matching a query.
     * @param {string} query - The query used to filter the cafe.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Cafe[]>} - A promise that resolves with an array of Cafe objects.
     */
    search: async function (query, setLoading = null, cancel = false) {
        const result = await fetchData(`/search/${query}`, setLoading);
        return result.map(cafeData => new Cafe(cafeData));
    },
}

export const UserAPI = {
    /**
     * Fetches a specific user by ID.
     * @param {string} id - The ID of the user to fetch.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<User[]>} - A promise that resolves with an array of User objects.
     */
    get: async function (id, setLoading = null, cancel = false) {
        const result = await fetchData(`/users/${id}`, setLoading).then();
        return result.map(userData => new User(userData));
    },
    /**
     * Fetches all users.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<User[]>} - A promise that resolves with an array of User objects.
     */
    getAll: async function (setLoading = null, cancel = false) {
        const result = await fetchData(`/users`, setLoading);
        return result.map(userData => new User(userData));
    },
}

export const OrderAPI = {
    /**
     * Fetches a specific order by ID.
     * @param {string} id - The ID of the order to fetch.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Order[]>} - A promise that resolves with an array of Order objects.
     */
    get: async function (id, setLoading = null, cancel = false) {
        const result = await fetchData(`/orders/${id}`, setLoading).then();
        return result.map(orderData => new Order(orderData));
    },
    /**
     * Fetches all orders.
     * @param {string} userId - Optional. The ID of the user to fetch the orders for.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Order[]>} - A promise that resolves with an array of Order objects.
     */
    getAll: async function (userId = null, setLoading = null, cancel = false) {
        if (userId) {
            const result = await fetchData(`/users/${userId}`, setLoading);
            return result.map(orderData => new Order(orderData));
        } else {
            const result = await fetchData(`/orders`, setLoading);
            return result.map(orderData => new Order(orderData));
        }
    }
}

export const EventAPI = {
    /**
     * Fetches a specific event by ID.
     * @param {string} id - The ID of the event to fetch.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Order[]>} - A promise that resolves with an array of Event objects.
     */
    get: async function (id, setLoading = null, cancel = false) {
        const result = await fetchData(`/events/${id}`, setLoading).then();
        return result.map(eventData => new Event(eventData));
    },
    /**
     * Fetches all events.
     * @param {Function} setLoading - Optional. A function to set loading state.
     * @param {boolean} cancel - Optional. Flag to cancel the request.
     * @returns {Promise<Cafe[]>} - A promise that resolves with an array of Event objects.
     */
    getAll: async function (setLoading = null, cancel = false) {
        const result = await fetchData(`/events`, setLoading);
        return result.map(eventData => new Event(eventData));
    },
}
