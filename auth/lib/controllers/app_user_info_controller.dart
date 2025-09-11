import 'package:auth/models/user.dart';
import 'package:auth/utils/app_response.dart';
import 'package:conduit_core/conduit_core.dart';

class AppUserInfoController extends ResourceController {
  final ManagedContext managedContext;

  AppUserInfoController(this.managedContext);

  @Operation.get()
  Future<Response> getAllUsers(
    //@Bind.header(HttpHeaders.authorizationHeader) String header,
  ) async {
    try {
      final qGetAllUsers = Query<User>(managedContext);
      final List<User> users = await qGetAllUsers.fetch();

      if (users.isEmpty) {
        return Response.notFound();
      }

      users.sort((a, b) => a.id!.compareTo(b.id!));

      // Удаляем из ответа лишние поля для каждого пользователя
      final List<Map<String, dynamic>> fetchUsers = users.map((user) {
        return {
          'id': user.id,
          'username': user.username,
          'surName': user.surName,
          'name': user.name,
          'patronymicName': user.patronymicName,
          'jobTitle': user.jobTitle,
          'userRole': user.userRole,
        };
      }).toList();


      return Response.ok(fetchUsers);
    } catch (error) {
      return AppResponse.serverError(error, message: "Ошибка при получении всех пользователей");
    }
  }



}