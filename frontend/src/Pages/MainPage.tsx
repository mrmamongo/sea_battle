import {Box, AppBar, Button, Toolbar, Typography, Container, CssBaseline} from "@mui/material";
import {Field} from "../Components/Field/Field.tsx";
import {Statistics} from "../Components/Statistics.tsx";
import {LoginModal} from "../Components/LoginModal.tsx";
import {useEffect, useState} from "react";
import {observer} from "mobx-react-lite";
import {useStore} from "../Models/Root.ts";

const MainPage = observer(() => {
    const {user, opponent} = useStore();

    const [loginModalOpen, setLoginModalOpen] = useState<boolean>(user.authenticated);
    const authenticate = (login: string) => {
        user.setLogin(login);
        setLoginModalOpen(false);
    }

    useEffect(() => {
        console.log(user);
    }, [user])

    return (
        <>
            <LoginModal open={loginModalOpen} handleSubmit={authenticate} handleCancel={() => setLoginModalOpen(false)}/>
            <Box sx={{ flexGrow: 1 }}>
                <CssBaseline/>
                <AppBar position="static">
                    <Toolbar sx={{ width: "40%", ml: "30%" }}>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Морской бой имени МВЯ
                        </Typography>
                        {opponent !== null && <Button color="error" variant={"contained"}>Новая игра</Button>}
                        <Button color="success" variant={"contained"} sx={{ ml: "5%"}} onClick={() => setLoginModalOpen(true)}>Сменить никнейм</Button>
                    </Toolbar>
                </AppBar>

                <Container sx={{ display: "flex", ml:"15vw", mt: "5vh", gap: "1vw", minWidth: "70vw"}}>
                    {
                        opponent !== null ?
                    <>
                        <Field owner={user} editable={false}/>
                        <Field owner={opponent} editable={true} clickHandler={(a, b) => console.log(a, b)}/>
                        <Statistics/>
                    </>
                        : <Button size={"large"} variant={"contained"} color={"error"} sx={{ ml: "25%"}}>Начните игру!</Button>
                    }
                </Container>


            </Box>
        </>
    )
})

export default MainPage;