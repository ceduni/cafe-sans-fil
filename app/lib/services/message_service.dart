import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:app/services/auth_service.dart';

class MessageService {
  final AuthService _authService = AuthService();

  // Get User Stream
  Stream<List<Map<String, dynamic>>> getUsersStream() async* {
    const String apiUrl = 'https://cafesansfil-api-r0kj.onrender.com/api/users';

    //while (true) {
    try {
      final token = await _authService.getToken();
      final response = await http.get(
        Uri.parse(apiUrl),
        headers: {
          'Authorization': 'Bearer $token', // Add the authorization header
          'Content-Type':
              'application/json' // Optionally specify the content type
        },
      );

      // Check if the request was successful (status code 200)
      if (response.statusCode == 200) {
        // Decode the JSON response
        List<dynamic> usersJson = json.decode(response.body);
        // Convert the JSON to a List of Maps
        List<Map<String, dynamic>> users =
            List<Map<String, dynamic>>.from(usersJson);

        // Yield the users list
        yield users;
      } else {
        // Optionally handle different status codes
        throw Exception('Failed to load users: ${response.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
      // Handle any connection errors or exceptions accordingly
    }

    // Delay before the next API call
    //  await Future.delayed(Duration(seconds: 30)); // Adjust the delay as needed
    //}
  }
}
