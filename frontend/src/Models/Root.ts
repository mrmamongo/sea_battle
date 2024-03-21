import { createContext } from "react";
import { useContext } from 'react';
import {UserStore} from "./User.store.ts";
import {GameStore} from "./Game.store.ts";

export class RootStore {
    userStore = new UserStore();
    gameStore = new GameStore();
}

export const rootStore = new RootStore();
export const StoreContext = createContext<RootStore | null>(null);

export const useStore = () => {
    const store = useContext(StoreContext);

    if (store === null) {
        throw new Error('Store cannot be null, please add a context provider');
    }

    return store;
};
