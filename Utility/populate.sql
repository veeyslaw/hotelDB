-- GUESTS
INSERT INTO GUEST (first_name, last_name, passport_number, email, phone_number) VALUES ('Iuliana', 'Berdianu', 'RO252342', 'iuliana.berdianu@gmail.com', '+40764974854');
INSERT INTO GUEST (first_name, last_name, passport_number, email, phone_number) VALUES ('Dumitru', 'Frunza', 'RO525355', 'dumitrufrunza@gmail.com', '+40744652474');
INSERT INTO GUEST (first_name, last_name, passport_number, email) VALUES ('Ion', 'Ceban', 'MDC52522', 'cebanion84@mail.ru');
INSERT INTO GUEST (first_name, last_name, passport_number, email, phone_number) VALUES ('Adrian', 'Smith', 'UK2432L52342', 'asmith@yahoo.com', '+443526284958');
INSERT INTO GUEST (first_name, last_name, passport_number, email) VALUES ('Alexandrin', 'Dogot', 'IT251NA321542', 'a1dogot@gmail.com');

-- CITIES
INSERT INTO CITY (city_name) VALUES ('Iasi');
INSERT INTO CITY (city_name) VALUES ('Bucuresti');
INSERT INTO CITY (city_name) VALUES ('Cluj');
INSERT INTO CITY (city_name) VALUES ('Constanta');
INSERT INTO CITY (city_name) VALUES ('Sinaia');

-- HOTELS AND DESCRIPTIONS
INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Stefan cel Mare Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Iasi'), '+40789235342', 'Ana-Maria Iftime');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotelul se afla in centrul orasului, in apropierea Palas Mall-ului.', 4, 1, 1, 0, 1);

INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Universitatea Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Iasi'), '+40753489232', 'Adrian Bagiu');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotel pentru studenti vis-a-vis de Universitatea Alexandru Ioan Cuza.', 3, 1, 0, 0, 1);


INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('City Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Bucuresti'), '+40795348232', 'Zaharia Banana');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotel prietenos cu mediul.', 2, 0, 0, 0, 0);


INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Constanta Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Constanta'), '+40753485432', 'Ana Rusu');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Vacanta pe malul marii.', 4, 1, 1, 1, 1);


INSERT INTO HOTEL (hotel_name, city_id, contact_number)
VALUES ('Peak Hotel', (SELECT city_id FROM CITY WHERE city_name = 'Sinaia'), '+40753499992');
INSERT INTO HOTEL_DESCRIPTION (hotel_id, text_desc, rating, restaurant, free_meals, pool, free_internet)
VALUES (HOTEL_HOTEL_ID_SEQ.CURRVAL, 'Hotelul se afla pe varful muntelui. Toate apartementele au o priveliste minunata.', 5, 1, 1, 1, 1);

-- APARTMENTS AND DESCRIPTIONS
-- stefan
INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 1, 3, 6, 300);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 1, 1, 1, 1, 1);

INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 2, 2, 2, 200);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 2, 1, 1, 1, 0);

INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 10, 2, 3, 150);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 10, 1, 0, 1, 1);

-- univer
INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Universitatea Hotel'), 1, 1, 2, 75);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Universitatea Hotel'), 1, 1, 0, 0, 0);

INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Universitatea Hotel'), 2, 1, 2, 50);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Universitatea Hotel'), 2, 0, 0, 0, 0);

-- city
INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'City Hotel'), 10, 2, 3, 125);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'City Hotel'), 10, 0, 0, 0, 0);

INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'City Hotel'), 20, 1, 3, 100);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'City Hotel'), 20, 0, 0, 0, 1);

-- constan
INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Constanta Hotel'), 100, 2, 4, 200);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Constanta Hotel'), 100, 1, 1, 0, 1);

-- peak
INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 1, 1, 2, 150);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 1, 1, 1, 1, 1);

INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 2, 2, 4, 225);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 2, 1, 1, 1, 1);

INSERT INTO APARTMENT (hotel_id, apart_number, room_count, apart_capacity, price_per_night_euro)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 3, 4, 8, 375);
INSERT INTO APARTMENT_DESCRIPTION (hotel_id, apart_number, air_conditioner, minibar, tv, double_bed)
VALUES ((SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 3, 1, 1, 1, 0);

-- BOOKINGS
INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO252342'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 2,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 1 FROM DUAL), (SELECT SYSDATE + 7 FROM DUAL), 3, 1);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO252342'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Constanta Hotel'), 100,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 13 FROM DUAL), (SELECT SYSDATE + 20 FROM DUAL), 1, 3);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO252342'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'City Hotel'), 20,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 8 FROM DUAL), (SELECT SYSDATE + 12 FROM DUAL), 2, 0);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO525355'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Universitatea Hotel'), 2,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 16 FROM DUAL), (SELECT SYSDATE + 30 FROM DUAL), 2, 0);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO525355'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 2,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 10 FROM DUAL), (SELECT SYSDATE + 15 FROM DUAL), 2, 2);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO525355'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Constanta Hotel'), 100,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 6 FROM DUAL), (SELECT SYSDATE + 10 FROM DUAL), 2, 2);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'RO525355'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Universitatea Hotel'), 1,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 1 FROM DUAL), (SELECT SYSDATE + 5 FROM DUAL), 2, 0);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'MDC52522'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Peak Hotel'), 3,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE FROM DUAL), (SELECT SYSDATE + 2 FROM DUAL), 7, 0);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'UK2432L52342'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Stefan cel Mare Hotel'), 10,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE + 4 FROM DUAL), (SELECT SYSDATE + 15 FROM DUAL), 3, 0);

INSERT INTO BOOKING (guest_id, hotel_id, apart_number, book_date, check_in, check_out, adults_count, children_count)
VALUES ((SELECT guest_id FROM GUEST WHERE passport_number = 'IT251NA321542'), (SELECT hotel_id FROM HOTEL WHERE hotel_name = 'Constanta Hotel'), 100,
    (SELECT SYSDATE FROM DUAL),(SELECT SYSDATE FROM DUAL), (SELECT SYSDATE + 6 FROM DUAL), 4, 0);
