import { makeAutoObservable } from 'mobx';
import { UserStore } from './User.store.ts';
import { SeaBattleStore } from './SeaBattle.store.ts';
import {io, Socket} from "socket.io-client";

export class GameStore {
    opponentNickname = '';
    currentTurn = '';
    userBattlefield = new SeaBattleStore();
    opponentBattlefield = new SeaBattleStore();

    socket: Socket
    constructor(userStore: UserStore) {
        makeAutoObservable(this);
        this.currentTurn = userStore.nickname;
        this.socket = io("ws://localhost:3000");
    }

    setOpponentNickname(nickname: string) {
        this.opponentNickname = nickname;
    }

    setCurrentTurn(nickname: string) {
        this.currentTurn = nickname;
    }

    setUserBattlefield(battlefield: SeaBattleStore) {
        this.userBattlefield = battlefield;
    }

    setOpponentBattlefield(battlefield: SeaBattleStore) {
        this.opponentBattlefield = battlefield;
    }

    disconnect() {
        this.socket.disconnect();
    }
}
