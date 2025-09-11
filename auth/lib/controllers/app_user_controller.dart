import 'dart:io';

import 'package:auth/models/user.dart';
import 'package:auth/utils/app_const.dart';
import 'package:auth/utils/app_response.dart';
import 'package:auth/utils/app_utils.dart';
import 'package:conduit_core/conduit_core.dart';

class AppUserController extends ResourceController {
  final ManagedContext managedContext;

  AppUserController(this.managedContext);

  @Operation.get()
  Future<Response> getUserProfile(
      @Bind.header(HttpHeaders.authorizationHeader) String header) async {
    try {
      final id = AppUtils.getIdFromHeader(header);
      final user = await managedContext.fetchObjectWithID<User>(id);
      //убираем из выводимого ответа токены
      user?.removePropertiesFromBackingMap(
          [AppConst.accessToken, AppConst.refreshToken]);
      return AppResponse.ok(
          message: "Профиль успешно получен", body: user?.backing.contents);
    } catch (error) {
      return AppResponse.serverError(error,
          message: "Ошибка получения профиля");
    }
  }

  @Operation.post()
  Future<Response> updateUserProfile(
    @Bind.header(HttpHeaders.authorizationHeader) String header,
    @Bind.body() User user,
  ) async {
    try {
      final id = AppUtils.getIdFromHeader(header);
      final fetchedUser = await managedContext.fetchObjectWithID<User>(id);
      final qUpdateUserJobTitle = Query<User>(managedContext)
        ..where((x) => x.id).equalTo(id)
        ..values.jobTitle = user.jobTitle ?? fetchedUser?.jobTitle
        ..values.userStatus = user.userStatus ?? fetchedUser?.userStatus;
      final updateUser = await qUpdateUserJobTitle.updateOne();
      updateUser?.removePropertiesFromBackingMap(
          [AppConst.accessToken, AppConst.refreshToken]);

      return AppResponse.ok(
          message: "Данные профиля успешно обновлены",
          body: updateUser?.backing.contents);
    } catch (error) {
      return AppResponse.serverError(error,
          message: "Ошибка обновление профиля (должность)");
    }
  }

  @Operation.put()
  Future<Response> updateUserPassword(
    @Bind.header(HttpHeaders.authorizationHeader) String header,
    @Bind.query("oldPassword") String oldPassword,
    @Bind.query("newPassword") String newPassword,
  ) async {
    try {
      final id = AppUtils.getIdFromHeader(header);
      final qFindUser = Query<User>(managedContext)
        ..where((table) => table.id).equalTo(id)
        ..returningProperties((table) => [table.salt, table.hashPassword]);
      final findUser = await qFindUser.fetchOne();
      final salt = findUser?.salt ?? "";
      final oldPasswordHash = generatePasswordHash(oldPassword, salt);
      if (oldPasswordHash != findUser?.hashPassword) {
        return AppResponse.badRequest(message: "Пароль неверный");
      }
      final newPasswordHash = generatePasswordHash(newPassword, salt);
      final qUpdateUserPassword = Query<User>(managedContext)
        ..where((x) => x.id).equalTo(id)
        ..values.hashPassword = newPasswordHash;
      await qUpdateUserPassword.updateOne();

      return AppResponse.ok(message: "Пароль успешно обновлен");
    } catch (error) {
      return AppResponse.serverError(error, message: "Ошибка обновления пароля");
    }
  }
}
