import 'package:app/side_bar.dart';
import 'package:flutter/material.dart';

class Horaire extends StatelessWidget {
  const Horaire({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: const Text('Horaire'),
      ),
    );
  }
}
