import { FormEventHandler, useEffect, useState } from "react";
import { getAccessToken } from "../../helpers/local-storage-helper";
import { useInput } from "../../hooks/use-input";
import { socket } from "../../socket";
import { Room, SocketResponseEvent, SocketResponseEventTypes } from "../../types/socket-response-types";
import { FormControl } from "../form-control/form-control";
import { Modal } from "../modal/modal";
import "./join-room-modal.scss";

type JoinRoomModalProps = {
  readonly onHide: () => void;
};

export const JoinRoomModal = ({ onHide }: JoinRoomModalProps) => {
  const searchRoomInput = useInput();
  const [foundRooms, setFoundRooms] = useState<ReadonlyArray<Room>>([]);

  const socketListener = (event: SocketResponseEvent) => {
    const data = JSON.parse(event.data);
    if (data.event_type !== SocketResponseEventTypes.RoomsFound) return;
    setFoundRooms(data.rooms);
  };

  useEffect(() => {
    socket.addEventListener("message", socketListener);
    return () => socket.removeEventListener("message", socketListener);
  }, []);

  const onSubmit: FormEventHandler = (e) => {
    e.preventDefault();

    const data = {
      jwt: getAccessToken(),
      event_type: "FindRoom",
      room_info: {
        room_name: searchRoomInput.value,
      },
    };

    socket.send(JSON.stringify(data));
  };

  return (
    <Modal onHide={onHide}>
      <div className="join-room-modal">
        <form onSubmit={onSubmit}>
          <FormControl onChange={searchRoomInput.onChange} value={searchRoomInput.value} name="search-room" />
          <button type="submit">Search</button>
        </form>
        {foundRooms.length !== 0 && (
          <ul>
            {foundRooms.map((room, i) => (
              <li key={i}>
                <h5>{room.room_name}</h5>
                <button>Join</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </Modal>
  );
};
