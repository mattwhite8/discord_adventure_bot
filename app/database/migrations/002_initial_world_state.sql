-- Sample Rooms
INSERT INTO Rooms (name, description, short_description) VALUES
('Entrance Hall', 'A grand hall with marble floors and towering pillars.', 'A vast marble hall.'),
('Library', 'Shelves of ancient books line the walls.', 'A quiet library.'),
('Armory', 'Racks of gleaming weapons and armor.', 'A well-stocked armory.');

-- Sample RoomConnections
INSERT INTO RoomConnections (from_room_id, to_room_id, direction) VALUES
(1, 2, 'north'),
(2, 1, 'south'),
(1, 3, 'east'),
(3, 1, 'west');
