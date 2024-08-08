import { MainController } from "./contollers/mainController";

const server = new MainController();

server.listen();

server.getIndex("/api/v1/");
