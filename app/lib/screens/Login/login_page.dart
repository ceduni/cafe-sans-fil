import 'package:flutter/material.dart';
import 'package:app/provider/auth_provider.dart';
import 'package:provider/provider.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  void _login() async {
    if (_emailController.text.isNotEmpty &&
        _passwordController.text.isNotEmpty) {
      final String email = _emailController.text.trim();
      final String password = _passwordController.text.trim();

      try {
        // Appel de la méthode de login qui stocke le token
        await Provider.of<AuthProvider>(context, listen: false)
            .login(email, password);
        Navigator.pushReplacementNamed(context, '/home');
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Login failed: ${e.toString()}')),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill in all fields.')),
      );
    }
  } //

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 138, 199, 249),
        body: SafeArea(
            child: Center(
                child: Column(
          children: [
            //logo app
            const SizedBox(height: 70),
            Image.asset('images/logo.png', width: 100, height: 100),
            const SizedBox(height: 70),

            //username textfield
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.emailAddress,
            ),

            const SizedBox(height: 16),
            //Password textfield
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),

            ElevatedButton(
              onPressed: _login,
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 36),
              ),
              child: const Text('Login'),
            ),
          ],
        ))));
  }
}
