import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:app/modeles/user_model.dart';
import 'package:app/config.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

class AuthService {
  final storage = const FlutterSecureStorage();

  Future<String?> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('${Config.baseUrl}/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      String token = data['authToken']; // Accede au 'authToken'
      await storeToken(token);
      return token;
    } else {
      throw Exception('Failed to login: ${response.body}');
    }
/*
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      User user = User.fromJson(data['user']);
      await storage.write(key: 'token', value: data['authToken']);
      return user;
    } else {
      throw Exception('Failed to login');
    }*/
  }

  Future<void> logout() async {
    final token = await getToken();
    if (token != null) {
      final response = await http.post(
        Uri.parse('${Config.baseUrl}/auth/logout'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token'
        },
      );
      if (response.statusCode == 200) {
        await storage.delete(key: 'token'); // Suppression du token
      } else {
        throw Exception('Failed to logout: ${response.body}');
      }
    }
  }

  Future<void> storeToken(String token) async {
    await storage.write(key: 'token', value: token);
  }

  Future<String?> getToken() async {
    return await storage.read(key: 'token');
  }

  bool isTokenExpired(String token) {
    return JwtDecoder.isExpired(token);
  }

  User? getUserFromToken(String token) {
    Map<String, dynamic> decodedToken = JwtDecoder.decode(token);
    return User.fromJson(decodedToken);
  }
}

// le code est inspiré de https://medium.com/@hpatilabhi10/understanding-jwt-tokens-in-flutter-0dfd0f495715
