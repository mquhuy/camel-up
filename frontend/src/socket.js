import SocketIO from "socket.io-client";

const options = {path: "/backend/socket.io"};
const socket = SocketIO("/message", options);

export default socket;
