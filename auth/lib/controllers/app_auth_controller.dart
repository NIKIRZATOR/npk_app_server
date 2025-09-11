import 'package:auth/models/user.dart';
import 'package:auth/utils/app_env.dart';
import 'package:auth/utils/app_response.dart';
import 'package:auth/utils/app_utils.dart';
import 'package:conduit_core/conduit_core.dart';
import 'package:jaguar_jwt/jaguar_jwt.dart';

class AppAuthController extends ResourceController {
  final ManagedContext managedContext;

  AppAuthController(this.managedContext);

  @Operation.post()
  Future<Response> singIn(@Bind.body() User user) async {
    if (user.username == null || user.password == null) {
      return AppResponse.badRequest(
          message: "Поля username и password должны быть заполнены!");
    }
    try {
      final qFindUser = Query<User>(managedContext)
        ..where((table) => table.username).equalTo(user.username)
        ..returningProperties(
            (table) => [table.id, table.salt, table.hashPassword]);
      final findUser = await qFindUser.fetchOne();
      if (findUser == null) {
        throw QueryException.input("Пользователь не найден", []);
      }

      final requestHasPassword =
          generatePasswordHash(user.password ?? "", findUser.salt ?? "");
      if (requestHasPassword == findUser.hashPassword) {
        await _updateTokens(findUser.id ?? -1, managedContext);
        final newUser =
            await managedContext.fetchObjectWithID<User>(findUser.id);
        return AppResponse.ok(
          body: newUser?.backing.contents,
          message: "Успешная авторизация!",
        );
      } else {
        throw QueryException.input("Неверный пароль", []);
      }
    } catch (error) {
      return AppResponse.serverError(error, message: "Ошибка авторизации");
    }
  }

  @Operation.put()
Future<Response> singUp(@Bind.body() User user) async {
  if (
      user.username == null || 
      user.password == null ||
      user.surName == null ||
      user.name == null ||
      user.userRole == null) {
    return AppResponse.badRequest(
        message: "Поля username, password, surName, name, userRole должны быть заполнены!");
  }

  final salt = generateRandomSalt();
  final hashPassword = generatePasswordHash(user.password ?? "", salt);

  try {
    // Получение последнего ID пользователя из базы данных
    final qLastUserId = Query<User>(managedContext)
      ..sortBy((table) => table.id, QuerySortOrder.descending)
      ..returningProperties((table) => [table.id])
      ..fetchLimit = 1;

    final lastUser = await qLastUserId.fetchOne();
    final newUserId = (lastUser?.id ?? 0) + 1; // Если база пуста, начнем с ID = 1

    await managedContext.transaction((transaction) async {
      final qCreateUser = Query<User>(transaction)
        ..values.id = newUserId // Устанавливаем автоматически сгенерированный ID
        ..values.username = user.username
        ..values.salt = salt
        ..values.hashPassword = hashPassword
        ..values.surName = user.surName
        ..values.name = user.name
        ..values.patronymicName = user.patronymicName
        ..values.jobTitle = user.jobTitle
        ..values.userRole = user.userRole;

      final createdUser = await qCreateUser.insert();

      await _updateTokens(createdUser.id!, transaction);
    });

    final userData = await managedContext.fetchObjectWithID<User>(newUserId);

    return AppResponse.ok(
      body: userData?.backing.contents,
      message: "Успешная регистрация",
    );
  } catch (error) {
    return AppResponse.serverError(error, message: "Ошибка регистрации");
  }
}

  @Operation.post("refresh")
  Future<Response> refreshToken(
      @Bind.path("refresh") String refreshToken) async {
    try {
      final id = AppUtils.getIdFromToken(refreshToken);
      final user = await managedContext.fetchObjectWithID<User>(id);
      if (user?.refreshToken != refreshToken) {
        return AppResponse.unauthorized(message: "Ошибка совпадения токенов. Токен не валидный");
      } else {
        await _updateTokens(id, managedContext);
        final user = await managedContext.fetchObjectWithID<User>(id);
        return AppResponse.ok(
          body: user?.backing.contents,
          message: "Успешное обновление токенов",
        );
      }
    } catch (error) {
      return AppResponse.serverError(error,
          message: "Ошибка обновления токенов");
    }
  }

  Map<String, dynamic> _getTokens(int id) {
    final key = AppEnv.secretKet;
    final accessClaimSet =
        JwtClaim(maxAge: Duration(hours: AppEnv.time), otherClaims: {"id": id});
    final refreshClaimSet = JwtClaim(otherClaims: {"id": id});
    final tokens = <String, dynamic>{};
    tokens["access"] = issueJwtHS256(accessClaimSet, key);
    tokens["refresh"] = issueJwtHS256(refreshClaimSet, key);
    return tokens;
  }

  Future<void> _updateTokens(int id, ManagedContext transaction) async {
    final Map<String, dynamic> tokens = _getTokens(id);
    final qUpdateTokens = Query<User>(transaction)
      ..where((user) => user.id).equalTo(id)
      ..values.accessToken = tokens["access"]
      ..values.refreshToken = tokens["refresh"];
    await qUpdateTokens.updateOne();
  }
}
