import 'package:conduit_core/conduit_core.dart';

class User extends ManagedObject<_User> implements _User {} //расширение от объекта ManagedObject: сопоставление с БД

class _User {
  @primaryKey
  int? id; // id пользователя

  @Column(unique: true, indexed: true) // логин учетной записи
  String? username;
  @Serialize(input: true, output: false) // получить можем, хранить в бд не будем
  String? password;

  String? surName; // фамилия
  String? name; // имя
  
  @Column(nullable: true)
  String? patronymicName; // отчество (необязательно)

  @Column(nullable: true)
  String? jobTitle; // должность (необязательно)

  int? userRole; // роль 1-админ, 2-обычный

  @Column(nullable: true)
  String? userStatus; //Статус (необязательно)
  ///
  ///Технические переменные
  ///

  @Column(nullable: true) // возможность быть нулевыми, чтобы получать инфу без данных переменных
  String? accessToken;
  @Column(nullable: true)
  String? refreshToken;
  @Column(omitByDefault: true)
  String? salt;
  @Column(omitByDefault: true)
  String? hashPassword;
}