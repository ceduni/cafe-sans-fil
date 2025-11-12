import { useSyncExternalStore } from "react";
import { getStore } from "./../utils/Store";
import type { AppState } from "./../utils/Store";

export const Store = getStore();

/**
 * Hook to select a specific slice of the store state
 * @param selector - Function to select a piece of state
 * @returns The selected state
 */
export function useStore<T>(selector: (state: AppState) => T): T {
    return useSyncExternalStore(
        Store.subscribe.bind(Store),
        () => selector(Store.getState()),
        () => selector(Store.getState())
    );
}

/**
 * Hook to get the entire store state
 * @returns The complete store state
 */
export function useFullStore(): AppState {
    return useSyncExternalStore(
        Store.subscribe.bind(Store),
        () => Store.getState(),
        () => Store.getState()
    );
}
