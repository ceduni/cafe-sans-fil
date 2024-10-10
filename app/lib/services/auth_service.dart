import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:app/modeles/user_model.dart';
//import 'package:app/config.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

class AuthService {
  final storage = const FlutterSecureStorage();

  Future<String?> login(String email, String password) async {
    final response = await http.post(
        Uri.parse('https://cafesansfil-api-r0kj.onrender.com/api/auth/login'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'grant_type': 'password',
          'username': email,
          'password': password,
          'scope': '',
          'client_id': 'string', // Mettez votre Client ID ici
          'client_secret': 'string' // Mettez votre Client Secret ici
        });

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      //print(data); // Ajoutez ceci pour déboguer
      if (data['access_token'] != null) {
        String accessToken = data['access_token'];
        String refreshToken = data['refresh_token'];
        await storeToken(accessToken, refreshToken);
        return accessToken;
      } else {
        throw Exception('Auth Token not found in response: ${response.body}');
      }
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
      await storage.delete(key: 'token'); // Suppression du token
      await storage.delete(key: 'refresh_token');
    }
  }

  Future<String?> refreshAccessToken() async {
    final refreshToken = await storage.read(key: 'refresh_token');
    if (refreshToken == null) {
      throw Exception("No refresh token available");
    }
    final response = await http.post(
        Uri.parse('https://cafesansfil-api-r0kj.onrender.com/api/auth/refresh'),
        headers: {
          'Content-Type': 'application/json'
        },
        body: {
          'refresh_token': refreshToken,
          'client_id': 'string', // Your Client ID
          'client_secret': 'string' // Your Client Secret
        });

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      String newAccessToken = data['access_token'];
      // Optionally update refresh token if provided
      if (data['refresh_token'] != null) {
        await storeToken(newAccessToken, data['refresh_token']);
      } else {
        await storeToken(
            newAccessToken, refreshToken); // Keep the same refresh token
      }
      return newAccessToken;
    } else {
      throw Exception('Failed to refresh token: ${response.body}');
    }
  }

  Future<void> storeToken(String accessToken, String refreshToken) async {
    await storage.write(key: 'token', value: accessToken);
    await storage.write(key: 'refresh_token', value: refreshToken);
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
