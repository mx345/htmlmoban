CREATE  TABLE  user_information(
  uid  int UNSIGNED AUTO_INCREMENT,
  dnmae VARCHAR(20) NOT NULL ,
  real_name VARCHAR(20) NOT NULL ,
  sex char(2) default 'male' check (sex in ('male','female')) NOT NULL ,
  Birth_Date VARCHAR(12),
  phone char(11) NOT NULL ,
  email VARCHAR(320)
)ENGINE =InnDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8