export enum SocketResponseEventTypes {
  RoomCreated = "RoomCreated",
  RoomsFound = "RoomsFound",
}

export type Player = {
  readonly id: string;
  readonly username: string;
  readonly status: string;
  readonly start_game: string;
  readonly current_tokens: number;
};

export type Room = {
  readonly id: string;
  readonly room_name: string;
  readonly blind: number;
  readonly turn_player_index: number;
  readonly start_tokens: number;
  readonly players: ReadonlyArray<Player>;
};

export type RoomCreatedData = {
  readonly event_type: SocketResponseEventTypes.RoomCreated;
  readonly room: Room;
};

export type RoomsFoundData = {
  readonly event_type: SocketResponseEventTypes.RoomsFound;
  readonly rooms: ReadonlyArray<Room>;
};

export type SocketResponseEvent = {
  readonly data: RoomCreatedData | RoomsFoundData;
};
