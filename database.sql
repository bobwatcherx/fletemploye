PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tblemployee (
  emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name VARCHAR(255),
  first_name VARCHAR(255),
  tgl_masuk_kerja VARCHAR(255),
  tgl_keluar_kerja VARCHAR(255),
  cnic VARCHAR(255),
  gender VARCHAR(255),
  desig VARCHAR(255),
  high_edu VARCHAR(255),
  contact VARCHAR(255),
  email VARCHAR(255),
  salary INTEGER,
  address VARCHAR(255)
);
INSERT INTO tblemployee VALUES(18,'jangUPDATE','jongUPDATE','20-12-2019','14-02-2018','test cnincUPDATE','male','designUPDATE','smaUPDATE','223112222','UPDATE@gmail.com',22222,'paris');
INSERT INTO tblemployee VALUES(20,'Ujang Dadang','Ujang','20-09-2023','20-09-1887','cnic','male','design','sd','1232','dw@gmail.com',12312,'bekasi');
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  login_with TEXT NOT NULL,
  time_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users VALUES(1,'oop','123','manual','2023-02-28 04:53:09');
INSERT INTO users VALUES(2,'jajang','90000','manual','2023-02-28 04:12:30');
INSERT INTO users VALUES(3,'surip','123','manual','2023-02-28 03:35:08');
INSERT INTO users VALUES(4,'','','manual','2023-02-28 11:18:10.890962');
INSERT INTO users VALUES(5,'kio','123','manual','2023-02-28 04:23:54');
INSERT INTO users VALUES(6,'smile','123','manual','2023-02-28 04:57:30');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',6);
INSERT INTO sqlite_sequence VALUES('tblemployee',20);
COMMIT;
