import {Containment} from "../../Models/types.ts";
import {ReactSVG} from "react-svg";
import {Fire} from "./img/fire.tsx";
import {Cross} from "./img/cross.tsx";
import {Ship} from "./img/ship.tsx";
import {Skull} from "./img/skull.tsx";
import {Box} from "@mui/material";

type FieldProps = {
    position: {x: number, y: number},
    containment: Containment
}
const bgImg = {
    "fire": <Fire/>,
    "cross": <Cross/>,
    "ship": <Ship/>,
    "skull": <Skull/>,
    "empty_shot": <ReactSVG src={""}/>
};

export const Cell = ({position, containment}: FieldProps) => {
    console.log(position.x, position.y, containment)
    return (
        <Box component={"div"} sx={{ border: "#111 solid 0.5px"}}>
            {bgImg[containment]}
        </Box>
    );
};