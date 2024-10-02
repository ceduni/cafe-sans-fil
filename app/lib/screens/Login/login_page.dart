import 'package:app/screens/Login/components/my_button.dart';
import 'package:app/screens/Login/components/my_textfield.dart';
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
      backgroundColor: Colors.grey.shade50,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            //logo app
            const SizedBox(height: 50),
            Image.asset('images/logo.png', width: 200, height: 200),
            const SizedBox(height: 50),
            //Email textField
            MyTextField(
              hintText: "email",
              obscureText: false,
              controller: _emailController,
            ),

            const SizedBox(height: 20),

            //PassWord textField
            MyTextField(
              hintText: "Password",
              obscureText: true,
              controller: _passwordController,
            ),

            const SizedBox(height: 35),

            //Login Button
            MyButton(
              text: "Login",
              onTap: _login,
            )
          ],
        ),
      ),
    );
  }
}
