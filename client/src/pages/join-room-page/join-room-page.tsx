import { useState } from "react";
import { CreateRoomModal } from "../../components/create-room-modal/create-room-modal";
import { JoinRoomModal } from "../../components/join-room-modal/join-room-modal";
import { MenuCard } from "../../components/menu-card/menu-card";
import "./join-room-page.scss";

export const JoinRoomPage = () => {
  const [isCreateRoomModalVisible, setIsCreateRoomModalVisible] = useState<boolean>(false);
  const [isJoinRoomModalVisible, setIsJoinRoomModalVisible] = useState<boolean>(false);

  const hideCreateRoomModal = () => setIsCreateRoomModalVisible(false);
  const hideJoinRoomModal = () => setIsJoinRoomModalVisible(false);
  const showCreateRoomModal = () => setIsCreateRoomModalVisible(true);
  const showJoinRoomModal = () => setIsJoinRoomModalVisible(true);

  return (
    <div className="join-room-page">
      <MenuCard title="Start game">
        <button onClick={showCreateRoomModal}>Create room</button>
        <button onClick={showJoinRoomModal}>Join room</button>
      </MenuCard>
      {isCreateRoomModalVisible && <CreateRoomModal onHide={hideCreateRoomModal} />}
      {isJoinRoomModalVisible && <JoinRoomModal onHide={hideJoinRoomModal} />}
    </div>
  );
};
