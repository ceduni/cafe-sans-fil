import 'package:flutter/material.dart';
import 'package:app/services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();

  String? _token;

  String? get token => _token;

  Future<void> login(String email, String password) async {
    try {
      _token = await _authService.login(email, password);
      notifyListeners(); // Notify listeners that the login state has changed
    } catch (e) {
      throw Exception('Failed to login: ${e.toString()}');
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    _token = null; // Clear the token on logout
    notifyListeners(); // Notify listeners that the logout occurred
  }

  Future<bool> isLoggedIn() async {
    final token = await _authService.getToken();
    return token != null;
  }
}
