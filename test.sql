SAVEPOINT empty_tables;
ROLLBACK TO SAVEPOINT empty_tables;

INSERT INTO CITY (city_name) VALUES ('Iasi');
INSERT INTO HOTEL (hotel_name, city_id, contact_number, manager_name)
VALUES ('Iasi Hotel', SELECT city_id FROM CITY WHERE city_name = 'Iasi', '0789235342', 'Ana-Maria');

SELECT APART_APART_ID_SEQ.CURRVAL FROM DUAL;
SELECT APART_APART_ID_SEQ.NEXTVAL FROM DUAL;