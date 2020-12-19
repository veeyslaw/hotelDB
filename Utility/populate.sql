INSERT INTO GUEST (first_name, last_name, passport_number, email, phone_number) VALUES ('Iuliana', 'Berdianu', 'RO252342', 'iuliana.berdianu@gmail.com', '+40764974854');
INSERT INTO GUEST (first_name, last_name, passport_number, email, phone_number) VALUES ('Dumitru', 'Frunza', 'RO525355', 'dumitrufrunza@gmail.com', '+40744652474');
INSERT INTO GUEST (first_name, last_name, passport_number, email) VALUES ('Ion', 'Ceban', 'MDC52522', 'cebanion84@mail.ru');
INSERT INTO GUEST (first_name, last_name, passport_number, email, phone_number) VALUES ('Adrian', 'Smith', 'UK2432L52342', 'asmith@yahoo.com', '+443526284958');
INSERT INTO GUEST (first_name, last_name, passport_number, email) VALUES ('Alexandrin', 'Dogot', 'IT251NA321542', 'a1dogot@gmail.com');

INSERT INTO CITY (city_name) VALUES ('Iasi');
INSERT INTO CITY (city_name) VALUES ('Bucuresti');
INSERT INTO CITY (city_name) VALUES ('Cluj');
INSERT INTO CITY (city_name) VALUES ('Constanta');
INSERT INTO CITY (city_name) VALUES ('Sinaia');

INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Stefan cel Mare Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Iasi'), '+40789235342', 'Ana-Maria Iftime');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotelul se afla in centrul orasului, in apropierea Palas Mall-ului.', 4, 1, 1, 0, 1);

INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Universitatea Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Iasi'), '+40753489232', 'Adrian Bagiu');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotel pentru studenti si nu numai. Chiar vis-a-vis de Universitatea Alexandru Ioan Cuza.', 3, 1, 0, 0, 1);


INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('City Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Bucuresti'), '+40795348232', 'Zaharia Banana');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotel prietenos cu mediul.', 2, 0, 0, 0, 0);


INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Universitatea Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Constanta'), '+40753485432', 'Ana Rusu');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Vacanta pe malul marii.', 4, 1, 1, 1, 1);


INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Universitatea Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Sinaia'), '+40753499992');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotelul se afla pe varful muntelui. Toate apartementele au o priveliste minunata.', 5, 1, 1, 1, 1);