import 'package:flutter/material.dart';
import 'package:app/services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();

  String? _token;

  String? get token => _token;
  Future<void> login(String email, String password) async {
    try {
      await _authService.login(email, password);
      notifyListeners();
    } catch (e) {
      throw Exception('Failed to login: ${e.toString()}');
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    notifyListeners();
  }

  Future<bool> isLoggedIn() async {
    final token = await _authService.getToken();
    return token != null;
  }
}
