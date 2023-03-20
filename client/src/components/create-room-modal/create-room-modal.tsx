import { useEffect } from "react";
import { getAccessToken } from "../../helpers/local-storage-helper";
import { useInput } from "../../hooks/use-input";
import { socket } from "../../socket";
import { SocketResponseEvent, SocketResponseEventTypes } from "../../types/socket-response-types";
import { FormControl } from "../form-control/form-control";
import { Modal } from "../modal/modal";
import "./create-room-modal.scss";

type CreateRoomModalProps = {
  readonly onHide: () => void;
};

export const CreateRoomModal = ({ onHide }: CreateRoomModalProps) => {
  const roomNameInput = useInput({ isRequired: true });
  const blindInput = useInput({ isRequired: true });
  const startTokensInput = useInput({ isRequired: true });

  const socketListener = (event: SocketResponseEvent) => {
    const data = JSON.parse(event.data);
    if (data.event_type !== SocketResponseEventTypes.RoomCreated) return;
    console.log(data);
  };

  useEffect(() => {
    socket.addEventListener("message", socketListener);
    return () => socket.removeEventListener("message", socketListener);
  }, []);

  const onCreateRoomClick = () => {
    if (!roomNameInput.isValid || !blindInput.isValid || !startTokensInput.isValid) return;

    const data = {
      jwt: getAccessToken(),
      event_type: "CreateRoom",
      room_info: {
        room_name: roomNameInput.value,
        blind: Number(blindInput.value),
        start_tokens: Number(startTokensInput.value),
      },
    };

    socket.send(JSON.stringify(data));
  };

  return (
    <Modal onHide={onHide}>
      <div className="create-room-modal">
        <FormControl
          value={roomNameInput.value}
          onChange={roomNameInput.onChange}
          name="room-name"
          type="text"
          label="Room name"
        />
        <div className="half-width-inputs-container">
          <FormControl
            marginTop="10px"
            value={blindInput.value}
            width="48%"
            onChange={blindInput.onChange}
            name="blind"
            type="number"
            label="Blind"
          />
          <FormControl
            marginTop="10px"
            value={startTokensInput.value}
            width="48%"
            onChange={startTokensInput.onChange}
            name="start-tokens"
            type="number"
            label="Start tokens"
          />
        </div>
        <button onClick={onCreateRoomClick}>Create Room</button>
      </div>
    </Modal>
  );
};
