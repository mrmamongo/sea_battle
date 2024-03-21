import { makeAutoObservable } from "mobx";
import {CellState, CellUpdate} from "./types.ts";

export class SeaBattleStore {
    grid: CellState[][] = Array(10)
        .fill(null)
        .map(() => Array(10).fill(CellState.cross));

    constructor() {
        makeAutoObservable(this);
    }

    handleCellUpdate = ({ x, y, state }: CellUpdate) => {
        this.grid[x][y] = state;
    };

    tryHit(x: number, y: number): void {
        if (this.grid[x][y] === CellState.cross) {
            this.socket.emit("try-hit", { x, y, state: this.grid[x][y] });
        }
    }

    disconnect(): void {
        this.socket.disconnect();
    }
}
